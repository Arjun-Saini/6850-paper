"""B3: the key figure. The single-firm reversal window in the (s, p) plane, with each geography's network path.

Base case n = 4, k = 2, m = 1, x = 0.9. Shaded: (s, p) where pairs give a single firm strictly less coverage than
both co-location and full spreading, computed from cov() on a grid. Lines: Track A's closed-form edges
p_minus(s) and p = 2/3 (A3), which should trace the shading's boundary. Paths: as the regional shock phi rises
from 0 to the geography's tipping point phi*_c, the network sits at (s, p) = (1 - phi, x r*_c(phi)). The dot ends
each path at its tipping point; the pairs path should end inside the window (Theorem B's condition).

Usage:  python3 b3_key_figure.py   (writes ../figures/fig_key_window.pdf and ../results/b3_paths.json; under a minute)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from coverage import S_OPEN_N4K2, interior_worst, lemma_a_window_n4k2  # noqa: E402
from model import largest_fixed_point, phi_star  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "figures", "fig_key_window.pdf")
RES = os.path.join(HERE, "..", "results", "b3_paths.json")

BASE = dict(x=0.9, m=1, n=4, k=2)
GEOS = [(4, "spread (c = 4)"), (2, "pairs (c = 2)"), (1, "co-located (c = 1)")]
S_LIM, P_LIM = (0.5, 1.0), (0.3, 1.0)

# styling matches exploratory/code/make_figures.py
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID, SHADE = "#1f1f1d", "#6b6a63", "#e1e0d9", "#f3d9cc"
COLORS = {4: BLUE, 2: ORANGE, 1: AQUA}
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["STIXGeneral"], "mathtext.fontset": "stix", "pdf.fonttype": 42,
    "font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 1.4, "legend.frameon": False,
})


def network_path(c, n_phi=80, x=0.9, m=1, n=4, k=2):
    """(s, p) = (1 - phi, x r*_c(phi)) for phi from 0 up to the tipping point phi*_c (included as the last point)."""
    ps = phi_star(x, m, n, k, c, tol=1e-9)
    phis = np.append(np.linspace(0.0, ps, n_phi, endpoint=False), ps)
    r = np.array([largest_fixed_point(x, m, n, k, c, f) for f in phis])
    return dict(c=c, phi_star=ps, phi=phis.tolist(), s=(1.0 - phis).tolist(), p=(x * r).tolist())


def build(fig_path=FIG, res_path=RES, n_phi=80, n_grid=400):
    paths = [network_path(c, n_phi, **BASE) for c, _ in GEOS]

    s = np.linspace(*S_LIM, n_grid)
    p = np.linspace(*P_LIM, n_grid)
    S_, P_ = np.meshgrid(s, p)
    window = interior_worst(S_, P_, k=BASE["k"], n=BASE["n"])

    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    ax.contourf(S_, P_, window.astype(float), levels=[0.5, 1.5], colors=[SHADE])
    ss = np.linspace(S_OPEN_N4K2 + 1e-9, S_LIM[1], 300)
    ax.plot(ss, [lemma_a_window_n4k2(v)[0] for v in ss], color=MUTED, lw=0.8, ls="--")
    ax.axhline(2 / 3, color=MUTED, lw=0.8, ls="--")
    ax.text(0.515, 0.672, "p = 2/3", color=MUTED, fontsize=7, va="bottom")
    ax.text(0.93, 0.50, "pairs\nworst", color=ORANGE, fontsize=7, ha="center", va="center")
    for (c, label), path in zip(GEOS, paths):
        ax.plot(path["s"], path["p"], color=COLORS[c], label=label)
        ax.plot(path["s"][-1], path["p"][-1], "o", color=COLORS[c], ms=3.5)
    ax.set_xlim(*S_LIM)
    ax.set_ylim(*P_LIM)
    ax.set_xlabel("region survival  s = 1 − φ")
    ax.set_ylabel("supplier reliability  p = x·r*")
    ax.legend(loc="lower left")
    fig.tight_layout()

    for path in (fig_path, res_path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(fig_path, metadata={"CreationDate": None})
    plt.close(fig)

    tips = []
    for (c, label), path in zip(GEOS, paths):
        s_t, p_t = path["s"][-1], path["p"][-1]
        tips.append(dict(c=c, label=label, phi_star=path["phi_star"], s=s_t, p=p_t,
                         in_window=bool(interior_worst(s_t, p_t, k=BASE["k"], n=BASE["n"]))))
    with open(res_path, "w") as f:
        json.dump(dict(setting=BASE, tipping_points=tips, paths=paths), f, indent=1)
    return tips


if __name__ == "__main__":
    for t in build():
        print(f"{t['label']}: phi*={t['phi_star']:.4f}  tip (s, p)=({t['s']:.4f}, {t['p']:.4f})  in window={t['in_window']}")
