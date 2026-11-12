"""Monte Carlo simulation of the k-of-n multisourcing model on finite layered supply networks.

Each of `depth`+1 layers holds N firms spread uniformly over G regions. A firm at layer d
draws, for each of its m inputs, c supplier clusters: each cluster sits in one uniformly
random region and contains b = n / c DISTINCT suppliers from layer d-1 firms in that region.
Each relationship is operational with probability x. A firm works iff its own region is not
hit and, for every input, at least k suppliers are both operational and functional.
Layer-0 firms need no inputs. Each region is hit independently with probability phi, and the
same set of hit regions applies to every layer (a single disaster).

Optional realism knob: `alpha` gives suppliers heavy-tailed popularity. Each firm gets a
fitness w ~ Pareto(alpha) and is chosen as a supplier with probability proportional to w
within its region, so a few hub suppliers serve many customers (CNST report in/out-degree
Pareto tails with shape ~1.25-1.3). alpha=None is uniform supplier choice.
"""
import numpy as np


def _draw_distinct(rng, starts, counts, cum_w, order, regions, b):
    """For each firm (row) pick b distinct suppliers from its chosen region.

    cum_w is the within-region cumulative fitness (None means uniform choice)."""
    N = len(regions)
    picks = np.empty((N, b), dtype=np.int64)
    todo = np.arange(N)
    while len(todo):
        g = regions[todo]
        if cum_w is None:
            off = (rng.random((len(todo), b)) * counts[g][:, None]).astype(np.int64)
        else:
            # inverse-CDF sampling inside the region's slice of cum_w
            lo = np.where(starts[g] > 0, cum_w[starts[g] - 1], 0.0)
            hi = cum_w[starts[g] + counts[g] - 1]
            u = lo[:, None] + rng.random((len(todo), b)) * (hi - lo)[:, None]
            off = np.searchsorted(cum_w, u, side="right") - starts[g][:, None]
            off = np.clip(off, 0, counts[g][:, None] - 1)
        picks[todo] = order[starts[g][:, None] + off]
        if b == 1:
            break
        s = np.sort(picks[todo], axis=1)
        dup = (s[:, 1:] == s[:, :-1]).any(axis=1)
        todo = todo[dup]                       # redraw only rows with a repeated supplier
    return picks


def simulate(m=2, n=4, k=1, x=0.9, phi=0.0, c=None, depth=20, N=20000, G=200,
             alpha=None, region_weights=None, hit=None, seed=0, return_layers=False, balanced=False):
    """Return the fraction of functional firms in the deepest layer (aggregate reliability).

    region_weights: optional length-G supply weights; a supplier cluster is placed in region g
      with probability proportional to region_weights[g] (hub regions host more supply
      relationships). Firms themselves stay uniformly spread over regions.
    hit: optional boolean length-G array fixing which regions are hit (overrides phi), used for
      targeted shocks.
    balanced: put exactly N / G firms in every region (still in random order) instead of drawing
      each firm's region independently; needed when N / G is small (many regions)."""
    c = n if c is None else c
    assert n % c == 0
    b = n // c
    rng = np.random.default_rng(seed)
    hit = (rng.random(G) < phi) if hit is None else np.asarray(hit, dtype=bool)
    pw = None if region_weights is None else np.asarray(region_weights, float) / np.sum(region_weights)

    assert not balanced or N % G == 0, "balanced placement needs G to divide N"

    def new_layer():
        reg = rng.permutation(np.repeat(np.arange(G), N // G)) if balanced else rng.integers(G, size=N)
        fit = None if alpha is None else rng.pareto(alpha, size=N) + 1.0
        return reg, fit

    region, fit = new_layer()
    alive = ~hit[region]                       # depth-0 firms need no sourcing
    layers = [alive.mean()]
    for _ in range(depth):
        order = np.argsort(region, kind="stable")
        counts = np.bincount(region, minlength=G)
        starts = np.concatenate(([0], np.cumsum(counts)[:-1]))
        cum_w = None if fit is None else np.cumsum(fit[order])
        assert counts.min() >= b, "region too small for distinct suppliers; raise N/G"
        ok = np.ones(N, dtype=bool)
        for _ in range(m):                     # each essential input
            cnt = np.zeros(N, dtype=np.int64)
            for _ in range(c):                 # each supplier cluster
                g = rng.integers(G, size=N) if pw is None else rng.choice(G, size=N, p=pw)
                picks = _draw_distinct(rng, starts, counts, cum_w, order, g, b)
                cnt += (alive[picks] & (rng.random((N, b)) < x)).sum(axis=1)
            ok &= cnt >= k
        region, fit = new_layer()
        alive = ok & ~hit[region]
        layers.append(alive.mean())
    if return_layers:
        return alive.mean(), hit.mean(), np.array(layers)
    return alive.mean()


if __name__ == "__main__":
    # smoke test against the mean-field fixed point (cf. draft Section 6)
    from model import rho
    for kw in [dict(k=1, phi=0.0, c=4), dict(k=2, phi=0.05, c=4),
               dict(k=2, phi=0.05, c=1), dict(k=1, phi=0.20, c=1)]:
        sims = [simulate(**kw, seed=s) for s in range(10)]
        print(kw, f"sim={np.mean(sims):.3f}+-{np.std(sims):.3f}",
              f"theory={rho(0.9, 2, 4, kw['k'], kw['c'], kw['phi']):.3f}")
