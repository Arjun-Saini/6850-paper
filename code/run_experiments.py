"""Run all simulation experiments for the exploratory paper and save raw results to ../results.

  E1  Validation: Monte Carlo vs mean-field theory (sweeps over x and over phi).        [H1]
  E2  Bimodality: distribution of outcomes across replications near the threshold.     [H2]
  E3  Collapse thresholds phi* vs supplier geography c, simulation vs theory.          [Thm 3-4]
  E4  Realism: heavy-tailed supplier popularity, and hub regions hit by random vs
      targeted shocks.                                                                  [H4]
  E5  Diversification trap and closed form: phi* vs cluster count c on finite networks. [Thm 3, Prop 5]
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


def threshold_from_runs(phis, collapsed):
    """Split point on realized phi minimizing misclassification of collapsed / survived."""
    o = np.argsort(phis)
    p, y = np.asarray(phis)[o], np.asarray(collapsed)[o].astype(int)
    best, best_err = None, 1e9
    for i in range(len(p) + 1):
        err = y[:i].sum() + (1 - y[i:]).sum()   # left should survive, right should collapse
        if err < best_err:
            best_err = err
            lo = p[i - 1] if i > 0 else p[0]
            hi = p[i] if i < len(p) else p[-1]
            best = 0.5 * (lo + hi)
    return best, best_err / len(p)


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


def summarize_thresholds(rr, rng_seed=0):
    """E3-style threshold estimate from runs: split point on realized phi plus a 500-draw bootstrap CI."""
    ph = np.array([r["phi_hat"] for r in rr])
    col = np.array([r["rho_sim"] < 0.1 for r in rr])
    est, err = threshold_from_runs(ph, col)
    rng = np.random.default_rng(rng_seed)
    boots = []
    for _ in range(500):
        idx = rng.integers(len(ph), size=len(ph))
        boots.append(threshold_from_runs(ph[idx], col[idx])[0])
    return est, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), err


def e3():
    jobs = []
    nrep = 10 if QUICK else 30
    theo = {}
    for k in (1, 2):
        for c in (1, 2, 4):
            ps = phi_star(0.9, 2, 4, k, c)
            theo[f"{k},{c}"] = ps
            for phi in np.linspace(0.6 * ps, 1.4 * ps, 9):
                for s in range(nrep):
                    jobs.append(dict(_exp="E3", m=2, n=4, k=k, x=0.9, phi=float(phi), c=c,
                                     seed=9000 + s, **BASE))
    res = pmap(jobs)
    summary = []
    for k in (1, 2):
        for c in (1, 2, 4):
            rr = [r for r in res if r["k"] == k and r["c"] == c]
            ph = np.array([r["phi_hat"] for r in rr])
            col = np.array([r["rho_sim"] < 0.1 for r in rr])
            est, err = threshold_from_runs(ph, col)
            # bootstrap CI over replications
            rng = np.random.default_rng(0)
            boots = []
            for _ in range(500):
                idx = rng.integers(len(ph), size=len(ph))
                boots.append(threshold_from_runs(ph[idx], col[idx])[0])
            # finite-depth theory threshold with the same "rho < 0.1" collapse criterion
            lo = depth20_threshold(0.9, 2, 4, k, c)
            summary.append(dict(k=k, c=c, phi_star_theory=theo[f"{k},{c}"], phi_star_depth20=lo,
                                phi_star_sim=est, ci_lo=float(np.percentile(boots, 2.5)),
                                ci_hi=float(np.percentile(boots, 97.5)), misclass=err, n_runs=len(rr)))
    save("e3.json", dict(summary=summary, runs=res))
    return summary


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
    """Theorem 3 and Proposition 5 on finite networks: phi* for every cluster count c | n."""
    configs = [(1, 4, 2), (1, 6, 3), (2, 6, 3), (3, 4, 2)]
    nrep = 10 if QUICK else 30
    jobs, theo = [], {}
    for (m, n, k) in configs:
        for c in [c for c in range(1, n + 1) if n % c == 0]:
            d20 = depth20_threshold(0.9, m, n, k, c)
            theo[(m, n, k, c)] = (phi_star(0.9, m, n, k, c), d20)
            for phi in np.linspace(0.6, 1.4, 9) * d20:
                for s in range(nrep):
                    jobs.append(dict(_exp="E5", m=m, n=n, k=k, x=0.9, phi=float(phi), c=c,
                                     seed=60000 + s, **BASE))
    res = pmap(jobs)
    summary = []
    for (m, n, k, c), (deep, d20) in theo.items():
        rr = [r for r in res if (r["m"], r["n"], r["k"], r["c"]) == (m, n, k, c)]
        est, lo, hi, err = summarize_thresholds(rr)
        summary.append(dict(m=m, n=n, k=k, c=c, phi_star_theory=deep, phi_star_depth20=d20, phi_star_sim=est,
                            ci_lo=lo, ci_hi=hi, misclass=err, n_runs=len(rr)))
    save("e5.json", dict(summary=summary, runs=res))
    return summary


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
