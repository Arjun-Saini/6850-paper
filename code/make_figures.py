"""Build the paper's figures and numeric summaries from ../results/*.json.

Usage: python3 make_figures.py      (after run_experiments.py)
Writes ../figures/fig_*.pdf and ../results/summary.txt
"""
import collections
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

for _f in font_manager.findSystemFonts():
    if "texgyretermes" in _f.lower():
        font_manager.fontManager.addfont(_f)

from model import finite_depth, jump_at_threshold, phi_star, phi_star_closed_form, refinement_violations, rho, x_crit

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
FIG = os.path.join(HERE, "..", "figures")
os.makedirs(FIG, exist_ok=True)

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, MUTED, GRID = "#1f1f1d", "#6b6a63", "#e1e0d9"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["TeX Gyre Termes", "DejaVu Serif"],
    "mathtext.fontset": "stix", "pdf.fonttype": 42, "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "legend.fontsize": 6.8, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.4,
    "legend.frameon": False,
})
load = lambda f: json.load(open(os.path.join(RES, f)))
out = []


def group_mean(runs, keyf, valf):
    g = collections.defaultdict(list)
    for r in runs:
        g[keyf(r)].append(valf(r))
    return {k: (np.mean(v), np.std(v), len(v)) for k, v in g.items()}


# ---------------------------------------------------------------- Figure 1: validation (E1)
e1 = load("e1.json")
fig, ax = plt.subplots(1, 3, figsize=(6.8, 2.05), gridspec_kw=dict(width_ratios=[1.15, 1, 1]))
xs = np.linspace(0.2, 1.0, 400)
for (m, k), col, mk in [((1, 1), BLUE, "o"), ((1, 2), ORANGE, "s"), ((2, 1), AQUA, "^"), ((2, 2), YELLOW, "D")]:
    ax[0].plot(xs, [rho(x, m, 4, k) for x in xs], color=col, lw=1.3)
    gm = group_mean([r for r in e1 if r["_exp"] == "E1x" and r["m"] == m and r["k"] == k],
                    lambda r: r["x"], lambda r: r["rho_sim"])
    kx = sorted(gm)
    ax[0].plot(kx, [gm[x][0] for x in kx], mk, color=col, ms=3.4, mec="white", mew=0.5,
               label=f"$m={m},\\ k={k}$")
ax[0].set(xlabel="relationship strength $x$", ylabel=r"reliability $\rho$", xlim=(0.2, 1.0),
          ylim=(-0.03, 1.03), title=r"(a) No shock ($\phi=0$, $n=4$)")
ax[0].legend(loc="upper left", handletextpad=0.2, borderaxespad=0.2)

for j, (k, pmax) in enumerate([(1, 0.5), (2, 0.12)], start=1):
    p = np.linspace(0, pmax, 500)
    for c, col, mk in [(4, BLUE, "o"), (2, AQUA, "^"), (1, ORANGE, "s")]:
        ax[j].plot(p, [rho(0.9, 2, 4, k, c, q) for q in p], color=col, lw=1.3)
        ax[j].plot(p, [(1 - q) * finite_depth(0.9, 2, 4, k, c, q, 20) for q in p], ":", color=col, lw=0.9)
        gm = group_mean([r for r in e1 if r["_exp"] == "E1phi" and r["k"] == k and r["c"] == c],
                        lambda r: r["phi"], lambda r: r["rho_sim"])
        kp = sorted(gm)
        ax[j].plot(kp, [gm[q][0] for q in kp], mk, color=col, ms=3.0, mec="white", mew=0.4,
                   label=f"$c={c}$")
    ax[j].set(xlabel=r"share of regions hit $\phi$", ylim=(-0.03, 1.03), xlim=(0, pmax),
              title=f"({'bc'[j-1]}) Regional shock, $k={k}$")
    ax[j].legend(loc="lower left", handletextpad=0.2, borderaxespad=0.2)
fig.tight_layout(pad=0.3, w_pad=0.8)
fig.savefig(os.path.join(FIG, "fig_validation.pdf"))

err_fin = np.array([abs(r["rho_sim"] - r["theory_fin"]) for r in e1])
err_inf = np.array([abs(r["rho_sim"] - r["theory_inf"]) for r in e1])
out.append(f"E1: runs={len(e1)}  MAE vs depth-20 theory at realized phi = {err_fin.mean():.4f} "
           f"(95th pct {np.percentile(err_fin, 95):.4f}, max {err_fin.max():.3f}); "
           f"MAE vs infinite-depth theory = {err_inf.mean():.4f}")
far = [abs(r["rho_sim"] - r["theory_fin"]) for r in e1 if abs(r["theory_fin"] - r["theory_inf"]) < 0.01]
out.append(f"E1: runs away from threshold (fin~inf within .01): n={len(far)}, MAE={np.mean(far):.4f}")

# ---------------------------------------------------------------- Figure 2: E2 + E4b
e2 = load("e2.json")
e4 = load("e4.json")
fig, ax = plt.subplots(1, 3, figsize=(6.9, 2.1), gridspec_kw=dict(width_ratios=[1, 1.15, 0.95]))
bins = np.linspace(0, 1, 21)
vals, labs = [], []
for k in (1, 2):
    v = np.array([r["rho_sim"] for r in e2["runs"] if r["k"] == k])
    ps = e2["phi_star"][str(k)]
    vals.append(v); labs.append(f"$k={k}$ at $\\phi^*={ps:.3f}$")
    out.append(f"E2 k={k}: phi*={ps:.4f} runs={len(v)} mean={v.mean():.3f} "
               f"frac<0.1={np.mean(v < 0.1):.3f} frac>0.4={np.mean(v > 0.4):.3f} "
               f"median of survivors(>0.1)={np.median(v[v > 0.1]) if np.any(v > 0.1) else float('nan'):.3f} "
               f"max={v.max():.3f}")
ax[0].hist(vals, bins=bins, color=[BLUE, ORANGE], label=labs, rwidth=0.9)
ax[0].set(xlabel=r"reliability $\rho$ of one replication", ylabel="replications",
          title=r"(a) Outcomes at threshold ($m=1$, $n=4$, $x=0.9$)")
ax[0].legend(loc="upper center")

b = [r for r in e4["runs"] if r["_exp"] == "E4b"]
q = np.linspace(0, 0.5, 500)
for k, ls in [(1, "-"), (2, "--")]:
    ax[1].plot(q, [rho(0.9, 2, 4, k, 4, v, 0.0) for v in q], ls, color=MUTED, lw=1.1,
               label=f"theory, $k={k}$")
for mode, col, mk in [("random", BLUE, "o"), ("targeted", ORANGE, "s")]:
    for k in (1, 2):
        rr = [r for r in b if r["k"] == k and r["_mode"] == mode]
        ax[1].plot([r["_supply_share"] for r in rr], [r["rho_sim"] / (1 - r["phi_hat"]) for r in rr],
                   mk, color=col, ms=3.0 if k == 1 else 3.6, mfc=col if k == 1 else "none", mew=0.7,
                   alpha=0.8, label=f"{mode}, $k={k}$")
for k in (1, 2):
    for mode in ("random", "targeted"):
        gm = group_mean([r for r in b if r["k"] == k and r["_mode"] == mode],
                        lambda r: r["_h"], lambda r: r["rho_sim"])
        sh = group_mean([r for r in b if r["k"] == k and r["_mode"] == mode],
                        lambda r: r["_h"], lambda r: r["_supply_share"])
        for h in sorted(gm):
            out.append(f"E4b k={k} {mode:8s} h={h:2d} firms_hit={h/2:.1f}% supply_share={sh[h][0]:.3f} "
                       f"rho_sim={gm[h][0]:.3f}+-{gm[h][1]:.3f}")
ax[1].set(xlabel="supply-weighted share of clusters hit $\\phi_s$", ylabel="reliability outside hit regions",
          ylim=(-0.03, 1.03), xlim=(0, 0.5), title="(b) Hub regions: random vs targeted shocks")
ax[1].legend(loc="center", bbox_to_anchor=(0.42, 0.45), ncol=1, handletextpad=0.2, fontsize=6.3)
# (c) the diversification trap (E5): phi* against cluster count c
e5 = load("e5.json")
cs_all = [1, 2, 3, 4, 6]
pos = {c: i for i, c in enumerate(cs_all)}
for (m, n, k), col, mk in [((1, 4, 2), BLUE, "o"), ((1, 6, 3), ORANGE, "s"), ((2, 6, 3), AQUA, "^"),
                           ((3, 4, 2), YELLOW, "D")]:
    rows = sorted([s for s in e5["summary"] if (s["m"], s["n"], s["k"]) == (m, n, k)], key=lambda s: s["c"])
    xs_ = [pos[s["c"]] for s in rows]
    ax[2].plot(xs_, [s["phi_star_depth20"] for s in rows], "-", color=col, lw=1.1)
    ax[2].errorbar(xs_, [s["phi_star_sim"] for s in rows],
                   yerr=[[s["phi_star_sim"] - s["ci_lo"] for s in rows], [s["ci_hi"] - s["phi_star_sim"] for s in rows]],
                   fmt=mk, color=col, ms=3.2, mec="white", mew=0.4, elinewidth=0.8, capsize=1.5,
                   label=f"$m={m},n={n},k={k}$")
ax[2].set_xticks(range(len(cs_all)), [str(c) for c in cs_all])
ax[2].set(xlabel="supplier clusters $c$ (1 = co-located)", ylabel=r"collapse threshold $\phi^*$",
          title="(c) The diversification trap", ylim=(0, 0.31))
ax[2].legend(loc="upper center", ncol=2, handletextpad=0.1, columnspacing=0.6, borderaxespad=0.1, fontsize=5.6)
fig.tight_layout(pad=0.3, w_pad=0.9)
fig.savefig(os.path.join(FIG, "fig_bimodal_hubs.pdf"))
e4b_err = np.array([abs(r["rho_sim"] - r["theory_fin"]) for r in b])
out.append(f"E4b: MAE vs depth-20 theory using supply-weighted shock = {e4b_err.mean():.4f}")

# ---------------------------------------------------------------- E3 and E4a summaries
e3 = load("e3.json")
for s in e3["summary"]:
    out.append("E3 k={k} c={c}: theory_inf={phi_star_theory:.3f} theory_D20={phi_star_depth20:.3f} "
               "sim={phi_star_sim:.3f} [{ci_lo:.3f},{ci_hi:.3f}] misclass={misclass:.3f} n={n_runs}".format(**s))
a = [r for r in e4["runs"] if r["_exp"] == "E4a"]
gm = group_mean(a, lambda r: (str(r["alpha"]), r["k"], r["phi"]), lambda r: r["rho_sim"])
for key in sorted(gm):
    out.append(f"E4a alpha={key[0]:5s} k={key[1]} phi={key[2]:.2f}: rho={gm[key][0]:.3f}+-{gm[key][1]:.3f}")
for k in (1, 2):
    for alpha in ("2.0", "1.25"):
        d = [abs(gm[(alpha, k, p)][0] - gm[("None", k, p)][0]) for (al, kk, p) in gm if al == alpha and kk == k]
        out.append(f"E4a k={k} alpha={alpha}: max |mean diff vs uniform| = {max(d):.3f}")

# ---------------------------------------------------------------- E5, E6, theorem checks
for s in e5["summary"]:
    out.append("E5 m={m} n={n} k={k} c={c}: theory_inf={phi_star_theory:.4f} theory_D20={phi_star_depth20:.4f} "
               "sim={phi_star_sim:.4f} [{ci_lo:.4f},{ci_hi:.4f}] misclass={misclass:.3f} n={n_runs}".format(**s))
for (m, n, k) in [(2, 4, 1), (2, 4, 2), (3, 4, 2), (1, 4, 2)]:
    cf = phi_star_closed_form(0.9, m, n, k)
    out.append(f"THM2 check m={m} n={n} k={k} x=0.9: closed form spread={cf['spread']:.4f} colocated={cf['colocated']:.4f}; "
               f"numeric spread={phi_star(0.9, m, n, k, n):.4f} colocated={phi_star(0.9, m, n, k, 1):.4f}")
scan_path = os.path.join(RES, "trap_scan.json")      # slow (~8 min): computed once, then cached
if not os.path.exists(scan_path):
    scan = [dict(n=n, k=k, m=m, x=x, violations=[list(v) for v in refinement_violations(x, m, n, k)])
            for n in (2, 4, 6, 8) for k in range(1, n + 1) for m in (1, 2, 3)
            for x in (0.6, 0.7, 0.8, 0.9, 0.95, 1.0)]
    json.dump(scan, open(scan_path, "w"), indent=1)
scan = load("trap_scan.json")
cases = len(scan)
viol = sum(1 for r in scan if r["violations"])
viol_k1 = sum(1 for r in scan if r["violations"] and r["k"] == 1)
out.append(f"TRAP scan: cases={cases} violations={viol} (k=1: {viol_k1})")
for (x, m, n, k) in [(0.9, 1, 4, 2), (0.9, 1, 6, 3), (0.95, 2, 6, 3), (0.9, 2, 6, 3)]:
    cs = [c for c in range(1, n + 1) if n % c == 0]
    out.append(f"PHISTAR deep x={x} m={m} n={n} k={k}: " + " ".join(f"c={c}:{phi_star(x, m, n, k, c):.4f}" for c in cs))
for (m, n, k) in [(1, 4, 1), (1, 4, 2), (2, 4, 1), (2, 4, 2), (2, 8, 2)]:
    out.append(f"TABLE1 m={m} n={n} k={k}: x_crit={x_crit(m, n, k):.3f} jump={jump_at_threshold(m, n, k):.3f}")
out.append(f"TABLE2 m=2 n=4 k=2 c=4 x=0.9: rho(phi=0.05)={rho(0.9, 2, 4, 2, 4, 0.05):.3f} phi*={phi_star(0.9, 2, 4, 2, 4):.4f}")
rnd = [r for r in b if r["k"] == 2 and r["_mode"] == "random" and r["_h"] <= 10]
out.append(f"E4b k=2 random h<=10: runs={len(rnd)} collapsed(rho<0.1)={np.mean([r['rho_sim'] < 0.1 for r in rnd]):.3f}")
e6 = load("e6.json")
from model import dgm_er_core_size
e6_err = []
for k, qc in e6["theory"].items():
    rows = collections.defaultdict(list)
    for r in e6["runs"]:
        rows[r["Q"]].append(r["sizes"][k])
        if abs(r["Q"] - qc) > 0.02:
            e6_err.append(abs(r["sizes"][k] - dgm_er_core_size(int(k), 1 - r["Q"], 10)))
    lb = max(q for q in rows if q < qc)
    fa = min((q for q in rows if q > qc), default=float("nan"))
    out.append(f"E6 k={k}: Qc_theory={qc:.4f} last_Q_below={lb:.3f} size={np.mean(rows[lb]):.3f} "
               f"first_Q_above={fa:.3f} size={np.mean(rows[fa]) if fa in rows else float('nan'):.3f}")
out.append(f"E6: MAE vs DGM theory away from thresholds (|Q-Qc|>0.02) = {np.mean(e6_err):.4f} (n={len(e6_err)}, "
           f"max {np.max(e6_err):.4f})")

open(os.path.join(RES, "summary.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
