"""Run all simulation experiments for the exploratory paper and save raw results to ../results.

  E1  Validation: Monte Carlo vs mean-field theory (sweeps over x and over phi).        [H1]
  E2  Bimodality: distribution of outcomes across replications near the threshold.     [H2]
  E3  Collapse thresholds phi* vs supplier geography c, simulation vs theory.          [H3]
  E4  Realism: heavy-tailed supplier popularity, and hub regions hit by random vs
      targeted shocks.                                                                  [H4]

Usage:  python3 run_experiments.py [--quick]      (quick = fewer replications, for a smoke run)
Full run takes ~20-30 minutes on 2 cores.
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

from model import F, finite_depth, phi_star, rho, x_crit
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
            lo, hi = 0.0, 1.0
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                if (1 - mid) * finite_depth(0.9, 2, 4, k, c, mid, 20) >= 0.1:
                    lo = mid
                else:
                    hi = mid
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


if __name__ == "__main__":
    for name, fn in [("E1", e1), ("E2", e2), ("E3", e3), ("E4", e4)]:
        t = time.time()
        fn()
        print(f"{name} done in {time.time() - t:.0f}s", flush=True)
    # also store the analytic tables
    tab1 = [dict(m=m, n=n, k=k, x_crit=x_crit(m, n, k))
            for (m, n, k) in [(1, 4, 1), (1, 4, 2), (2, 4, 1), (2, 4, 2), (2, 4, 3),
                              (3, 4, 1), (3, 4, 2), (2, 6, 2), (2, 8, 2)]]
    save("table1_theory.json", tab1)
    print("all done")
