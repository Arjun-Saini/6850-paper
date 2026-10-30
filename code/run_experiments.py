"""Run all simulation experiments for the exploratory paper and save raw results to ../results.

  E1  Validation: Monte Carlo vs mean-field theory (sweeps over x and over phi).        [H1]
  E2  Bimodality: distribution of outcomes across replications near the threshold.     [H2]
  E3  Collapse thresholds phi* vs supplier geography c, simulation vs theory.          [Claims 2-3]
  E4  Realism: heavy-tailed supplier popularity, and hub regions hit by random vs
      targeted shocks.                                                                  [H4]
  E5  Pairs reversal and closed form: phi* vs cluster count c on finite networks.      [Claim 2, Example 1]
      E3 and E5 bisect each network's tipping point (number of hit regions) on G = 2000 regions.
  E6  DGM (2006) reproduction: k-core sizes of damaged Erdos-Renyi graphs vs theory.     [DGM]

Usage:  python3 run_experiments.py [--quick] [E1 ... E6]
        (no names = the original E1-E4; quick = fewer replications, for a smoke run)
Full run takes ~20-30 minutes on 2 cores.
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

from kcore import core_numbers, er_edges, kcore_sizes
from model import F, dgm_er_Qc, finite_depth, phi_star, rho, x_crit
from simulate import simulate

QUICK = "--quick" in sys.argv
REPS = 6 if QUICK else 20
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(OUT, exist_ok=True)
BASE = dict(depth=20, N=20000, G=200)
# threshold experiments (E3, E5): 10x more regions so the shock moves in steps of 0.0005
FINE = dict(depth=20, N=20000, G=2000, balanced=True)
NETS = 10 if QUICK else 40


def run_one(job):
    """Worker: one simulation. Returns the job dict augmented with the outcome."""
    kw = {k: v for k, v in job.items() if not k.startswith("_")}
    val, phi_hat, _ = simulate(**kw, return_layers=True)
    out = dict(job)
    out.update(rho_sim=float(val), phi_hat=float(phi_hat))
    if "region_weights" in out:
        out["region_weights"] = None          # don't dump big arrays into json
    if "hit" in out:
        out["hit"] = None
    return out


def pmap(jobs):
    with Pool(os.cpu_count()) as pool:
        return pool.map(run_one, jobs, chunksize=1)


def theory_at(x, m, n, k, c, phi_s, phi_own, depth=20):
    """Finite-depth and infinite-depth theory at a given realized shock."""
    fin = (1 - phi_own) * finite_depth(x, m, n, k, c, phi_s, depth)
    inf = rho(x, m, n, k, c, phi_s, phi_own)
    return fin, inf


def save(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, indent=1)


# ---------------------------------------------------------------------------------------
def e1():
    jobs = []
    # (a) reliability vs relationship strength, no shock (n = 4, spread suppliers)
    for (m, k) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        for x in np.round(np.arange(0.20, 1.0001, 0.04), 3):
            for s in range(REPS // 2):          # phi = 0: little run-to-run noise
                jobs.append(dict(_exp="E1x", m=m, n=4, k=k, x=float(x), phi=0.0, c=4, seed=s, **BASE))
    # (b) reliability vs regional shock (m = 2, n = 4, x = 0.9)
    for k in (1, 2):
        grid = np.arange(0.0, 0.501, 0.025) if k == 1 else np.arange(0.0, 0.1201, 0.006)
        for c in (1, 2, 4):
            for phi in np.round(grid, 4):
                for s in range(REPS):
                    jobs.append(dict(_exp="E1phi", m=2, n=4, k=k, x=0.9, phi=float(phi), c=c,
                                     seed=1000 + s, **BASE))
    res = pmap(jobs)
    for r in res:
        r["theory_fin"], r["theory_inf"] = theory_at(r["x"], r["m"], r["n"], r["k"], r["c"],
                                                     r["phi_hat"], r["phi_hat"])
        r["theory_nominal"] = rho(r["x"], r["m"], r["n"], r["k"], r["c"], r["phi"])
    save("e1.json", res)
    return res


def e2():
    """m = 1 (simple production): k = 1 has a continuous transition, k = 2 a precipice (P2).
    Run many replications at each configuration's theoretical phi*; the randomness in which
    regions get hit spreads the realized shock around the threshold."""
    jobs, meta = [], {}
    nrep = 60 if QUICK else 300
    for k in (1, 2):
        ps = phi_star(0.9, 1, 4, k, 4)
        meta[k] = ps
        for s in range(nrep):
            jobs.append(dict(_exp="E2", m=1, n=4, k=k, x=0.9, phi=float(ps), c=4, seed=5000 + s, **BASE))
    res = pmap(jobs)
    save("e2.json", dict(phi_star=meta, runs=res))
    return res


def depth20_threshold(x, m, n, k, c, depth=20):
    """Largest phi with finite-depth theory reliability (1 - phi) F^D(1) >= 0.1 (E3's collapse criterion)."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if (1 - mid) * finite_depth(x, m, n, k, c, mid, depth) >= 0.1:
            lo = mid
        else:
            hi = mid
    return lo


def nested_hit(seed, h, G):
    """The first h regions of a seed-specific random order: hit sets grow with h."""
    hit = np.zeros(G, dtype=bool)
    hit[np.random.default_rng([seed, 1]).permutation(G)[:h]] = True
    return hit


def collapses(job, h):
    """Does this job's network end with reliability below 0.1 when exactly h regions are hit?"""
    kw = {key: v for key, v in job.items() if not key.startswith("_")}
    return simulate(**kw, phi=h / kw["G"], hit=nested_hit(job["seed"], h, kw["G"])) < 0.1


def critical_hits(job):
    """Worker: the smallest number of hit regions that collapses one network, by bisection.

    With a fixed seed the network (supplier picks, relationship coin flips) is the same for every h,
    and hit sets are nested, so collapse is monotone in h and bisection finds the exact tipping point."""
    G, guess = job["G"], job["_guess"]
    sims = 0

    def test(h):
        nonlocal sims
        sims += 1
        return collapses(job, h)

    lo, hi = max(0, int(0.7 * guess)), min(G, int(np.ceil(1.3 * guess)) + 1)
    while lo > 0 and test(lo):                 # widen until lo survives ...
        lo, hi = lo // 2, lo
    while hi < G and not test(hi):             # ... and hi collapses (all G regions hit always does)
        lo, hi = hi, min(G, 2 * hi)
    if lo == 0 and test(0):
        hi = 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if test(mid):
            hi = mid
        else:
            lo = mid
    out = {key: v for key, v in job.items() if key != "balanced"}
    out.update(h_crit=hi, n_sims=sims)
    return out


def threshold_summary(nets, G):
    """Median tipping point over networks (= the shock at which half of them collapse), with a
    bootstrap 95% CI over networks widened by half a grid step (each tipping point is known to +-0.5/G)."""
    v = np.array([(r["h_crit"] - 0.5) / G for r in nets])
    rng = np.random.default_rng(0)
    boots = np.median(v[rng.integers(len(v), size=(2000, len(v)))], axis=1)
    half = 0.5 / G
    return float(np.median(v)), float(np.percentile(boots, 2.5) - half), float(np.percentile(boots, 97.5) + half)


def threshold_experiment(name, configs, seed0):
    """phi* on finite networks for each (m, n, k, c): bisect the tipping point of NETS networks each."""
    jobs, theo = [], {}
    for (m, n, k, c) in configs:
        d20 = depth20_threshold(0.9, m, n, k, c)
        theo[(m, n, k, c)] = (phi_star(0.9, m, n, k, c), d20)
        for s in range(NETS):
            jobs.append(dict(_exp=name, _guess=d20 * FINE["G"], m=m, n=n, k=k, x=0.9, c=c,
                             seed=seed0 + s, **FINE))
    with Pool(os.cpu_count()) as pool:
        nets = pool.map(critical_hits, jobs, chunksize=1)
    summary = []
    for (m, n, k, c), (deep, d20) in theo.items():
        rr = [r for r in nets if (r["m"], r["n"], r["k"], r["c"]) == (m, n, k, c)]
        est, lo, hi = threshold_summary(rr, FINE["G"])
        summary.append(dict(m=m, n=n, k=k, c=c, phi_star_theory=deep, phi_star_depth20=d20, phi_star_sim=est,
                            ci_lo=lo, ci_hi=hi, n_networks=len(rr), n_sims=sum(r["n_sims"] for r in rr)))
    save(f"{name.lower()}.json", dict(summary=summary, networks=nets))
    return summary


def e3():
    return threshold_experiment("E3", [(2, 4, k, c) for k in (1, 2) for c in (1, 2, 4)], 9000)


def e4():
    nrep = 6 if QUICK else 20
    G = BASE["G"]
    # (a) heavy-tailed supplier popularity, phi sweep, k in {1, 2}, c = 4
    jobs = []
    for alpha in (None, 2.0, 1.25):
        for k in (1, 2):
            grid = [0.0, 0.03, 0.05, 0.07, 0.09] if k == 2 else [0.0, 0.1, 0.2, 0.3, 0.4]
            for phi in grid:
                for s in range(nrep):
                    jobs.append(dict(_exp="E4a", m=2, n=4, k=k, x=0.9, phi=phi, c=4, alpha=alpha,
                                     seed=20000 + s, **BASE))
    # (b) hub regions: supply weights ~ Pareto(1.25); hit the h largest-supply regions
    #     (targeted) or h random regions. Firms are spread evenly, so h/G of firms are hit.
    wrng = np.random.default_rng(42)
    w = wrng.pareto(1.25, size=G) + 1.0
    w = w / w.sum()
    rank = np.argsort(-w)
    for k in (1, 2):
        for h in (1, 2, 3, 4, 6, 8, 10, 14, 20):
            for mode in ("targeted", "random"):
                for s in range(nrep):
                    hit = np.zeros(G, dtype=bool)
                    if mode == "targeted":
                        hit[rank[:h]] = True
                    else:
                        hit[np.random.default_rng(30000 + 97 * h + s).choice(G, h, replace=False)] = True
                    jobs.append(dict(_exp="E4b", _mode=mode, _h=h, _supply_share=float(w[hit].sum()),
                                     m=2, n=4, k=k, x=0.9, c=4, region_weights=w, hit=hit,
                                     seed=40000 + s, **BASE))
    res = pmap(jobs)
    for r in res:
        if r["_exp"] == "E4a":
            r["theory_inf"] = rho(r["x"], 2, 4, r["k"], 4, r["phi_hat"])
        else:
            r["theory_inf"] = rho(r["x"], 2, 4, r["k"], 4, r["_supply_share"], r["phi_hat"])
            r["theory_fin"] = (1 - r["phi_hat"]) * finite_depth(r["x"], 2, 4, r["k"], 4, r["_supply_share"], 20)
    save("e4.json", dict(weights=w.tolist(), runs=res))
    return res


def e5():
    """Theorem 2 and Proposition 4 on finite networks: phi* for every cluster count c | n."""
    configs = [(1, 4, 2), (1, 6, 3), (2, 6, 3), (3, 4, 2)]
    return threshold_experiment("E5", [(m, n, k, c) for (m, n, k) in configs
                                       for c in range(1, n + 1) if n % c == 0], 60000)


def e6():
    """DGM (2006): giant k-core sizes of an Erdos-Renyi graph (N = 100,000, mean degree 10) after random
    vertex removal, against the analytic thresholds Q_c(k)."""
    N, z, ks = 100_000, 10, range(2, 8)
    qc = {k: dgm_er_Qc(k, z) for k in ks}
    grid = {0.0, 0.2, 0.4, 0.6, 0.8}
    for k in ks:
        for d in (-0.01, 0.01):
            grid.add(float(np.clip(round(qc[k] + d, 3), 0.0, 0.95)))
    runs = []
    for rep in range(2):
        rng = np.random.default_rng(70000 + rep)
        edges = er_edges(N, z, rng)
        u = rng.random(N)                       # common random numbers across Q
        for Q in sorted(grid):
            sizes = kcore_sizes(core_numbers(N, edges, u >= Q), ks)
            runs.append(dict(Q=Q, rep=rep, sizes={str(k): v for k, v in sizes.items()}))
    save("e6.json", dict(theory={str(k): v for k, v in qc.items()}, runs=runs))
    return runs


EXPERIMENTS = ["E1", "E2", "E3", "E4", "E5", "E6"]


def selected_experiments(argv):
    """Experiment names from the command line; no names means the original E1-E4."""
    names = [a.upper() for a in argv if not a.startswith("--")]
    for nm in names:
        if nm not in EXPERIMENTS:
            raise ValueError(f"unknown experiment {nm}; choose from {EXPERIMENTS}")
    return names or ["E1", "E2", "E3", "E4"]


if __name__ == "__main__":
    fns = dict(E1=e1, E2=e2, E3=e3, E4=e4, E5=e5, E6=e6)
    for name in selected_experiments(sys.argv[1:]):
        t = time.time()
        fns[name]()
        print(f"{name} done in {time.time() - t:.0f}s", flush=True)
    # also store the analytic tables
    tab1 = [dict(m=m, n=n, k=k, x_crit=x_crit(m, n, k))
            for (m, n, k) in [(1, 4, 1), (1, 4, 2), (2, 4, 1), (2, 4, 2), (2, 4, 3),
                              (3, 4, 1), (3, 4, 2), (2, 6, 2), (2, 8, 2)]]
    save("table1_theory.json", tab1)
    print("all done")
