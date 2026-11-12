"""Study figures for the presentation prep, computed from code/model.py (the paper's model).

Run: python3 make_prep_figures.py   -> writes SVGs to ../figures/
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "code"))
from model import F, S, largest_fixed_point, phi_star  # noqa: E402

OUT = os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)

# Validated categorical slots 1-3 (dataviz reference palette, light mode); slot 3 needs direct labels.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID_C, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID_C, "grid.linewidth": 0.8, "figure.facecolor": SURF,
    "axes.facecolor": SURF, "svg.fonttype": "path", "svg.hashsalt": "prep",
})
META = {"Date": None}


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), metadata=META)
    plt.close(fig)
    print("wrote", name)


# 1. The cliff: reliability r* against relationship strength x, no shock, n = 4.
xs = np.linspace(0.15, 1.0, 341)
fig, ax = plt.subplots(figsize=(6.4, 4.1))
for (m, k, col, ls, txt, _) in [
    (1, 1, BLUE, "-", "m=1, k=1: smooth (branching process)", 0.30),
    (2, 1, ORANGE, "--", "m=2, k=1: EGL's cliff", 0.52),
    (1, 2, AQUA, "-.", "m=1, k=2: our new cliff", 0.725),
]:
    ys = [largest_fixed_point(x, m, 4, k) for x in xs]
    ax.plot(xs, ys, color=col, lw=2, ls=ls, label=txt)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=9)
ax.set(xlabel="relationship strength x", ylabel="reliability r*", ylim=(-0.03, 1.05),
       title="Needing two of anything turns a slope into a cliff (n = 4, no shock)")
ax.title.set_fontsize(10)
save(fig, "cliff.svg")

# 2. Fixed point picture: F(r) against the diagonal, m=1, n=4, k=2, spread, x=0.9.
P = dict(x=0.9, m=1, n=4, k=2, c=4)
ps = phi_star(P["x"], P["m"], P["n"], P["k"], P["c"])
rs = np.linspace(0, 1, 401)
fig, ax = plt.subplots(figsize=(6.0, 4.4))
ax.plot(rs, rs, color=INK2, lw=1.2, ls=":")
ax.plot([], [], color=INK2, lw=1.2, ls=":", label="diagonal F(r) = r")
for phi, col, ls, txt in [(0.10, BLUE, "-", "φ = 0.10: crosses high, r* large"),
                          (ps, ORANGE, "--", f"φ = φ* ≈ {ps:.3f}: just touches"),
                          (0.28, AQUA, "-.", "φ = 0.28: no crossing, r* = 0")]:
    ys = F(rs, P["x"], P["m"], P["n"], P["k"], P["c"], phi)
    ax.plot(rs, ys, color=col, lw=2, ls=ls, label=txt)
    r_star = largest_fixed_point(P["x"], P["m"], P["n"], P["k"], P["c"], phi)
    if r_star > 0:
        ax.plot([r_star], [r_star], "o", ms=8, color=col, mec=SURF, mew=2)
ax.legend(loc="upper left", frameon=False, fontsize=8.5)
ax.set(xlabel="r = chance a supplier works", ylabel="F(r) = chance a firm works", xlim=(0, 1.02), ylim=(0, 1.02),
       title="Reliability is the largest crossing with the diagonal")
ax.title.set_fontsize(10)
save(fig, "fixed_point.svg")

# 3. Pairs are worst: r* against shock size phi, m=1, n=4, k=2, x=0.9.
phis = np.linspace(0, 0.26, 261)
fig, ax = plt.subplots(figsize=(6.4, 3.6))
for c, col, ls, txt in [(1, BLUE, "-", "co-located (c=1)"), (2, ORANGE, "--", "two pairs (c=2)"),
                        (4, AQUA, "-.", "spread (c=4)")]:
    ys = [largest_fixed_point(0.9, 1, 4, 2, c, p) for p in phis]
    pst = phi_star(0.9, 1, 4, 2, c)
    ax.plot(phis, ys, color=col, lw=2, ls=ls, label=f"{txt}: φ* = {pst:.3f}")
ax.legend(loc="lower left", frameon=False, fontsize=9)
ax.set(xlabel="shock size φ (chance a region is hit)", ylabel="reliability r*", ylim=(-0.03, 1.05),
       title="Example 1: with k = 2, two pairs break first (n = 4, m = 1, x = 0.9)")
ax.title.set_fontsize(10)
save(fig, "pairs.svg")

# 4. Why: the coverage gap between pairs and co-located is s*phi*[2p^2 - S_2(4,p)].
p = np.linspace(0, 1, 401)
br = 2 * p ** 2 - S(2, 4, p)
r_pairs = largest_fixed_point(0.9, 1, 4, 2, 2, phi_star(0.9, 1, 4, 2, 2) - 1e-4)
p_thr = 0.9 * r_pairs
fig, ax = plt.subplots(figsize=(6.0, 3.4))
ax.axhline(0, color=INK2, lw=1)
ax.plot(p, br, color=BLUE, lw=2)
ax.fill_between(p, br, 0, where=br < 0, color=ORANGE, alpha=0.18, lw=0)
ax.axvline(2 / 3, color=INK2, lw=1, ls=":")
ax.annotate("p = 2/3: sign change", (2 / 3, 0.55), xytext=(-118, 0), textcoords="offset points", fontsize=9)
ax.plot([p_thr], [2 * p_thr ** 2 - float(S(2, 4, p_thr))], "o", ms=8, color=ORANGE, mec=SURF, mew=2)
ax.annotate(f"near the pairs tipping point\np = x·r* ≈ {p_thr:.2f}: pairs worse", (p_thr, 2 * p_thr ** 2 - float(S(2, 4, p_thr))),
            xytext=(-200, 40), textcoords="offset points", fontsize=9, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.annotate("pairs better\n(above 0)", (0.80, 0.03), fontsize=9, color=INK2)
ax.annotate("pairs worse\n(shaded)", (0.30, -0.12), fontsize=9, color=INK2)
ax.set(xlabel="p = chance a surviving supplier is usable", ylabel="2p² − S₂(4, p)",
       title="Pairs minus co-located coverage = sφ · [2p² − S₂(4, p)]")
ax.title.set_fontsize(10)
save(fig, "pairs_bracket.svg")

# 5. Two inputs: co-location hurts (Claim 2b), m=2, n=4, k=1, x=0.9.
phis = np.linspace(0, 0.5, 251)
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for c, col, ls, txt in [(1, BLUE, "-", "co-located (c=1)"), (4, AQUA, "-.", "spread (c=4)")]:
    ys = [largest_fixed_point(0.9, 2, 4, 1, c, q) for q in phis]
    pst = phi_star(0.9, 2, 4, 1, c)
    ax.plot(phis, ys, color=col, lw=2, ls=ls, label=f"{txt}: φ* = {pst:.3f}")
ax.legend(loc="lower left", frameon=False, fontsize=9, bbox_to_anchor=(0.0, 0.04))
ax.set(xlabel="shock size φ", ylabel="reliability r*", ylim=(-0.03, 1.05),
       title="With two inputs, co-locating suppliers breaks earlier (k = 1, n = 4, x = 0.9)")
ax.title.set_fontsize(10)
save(fig, "two_inputs.svg")
