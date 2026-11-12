# Branch notes (`aryavardhan/geography-kcore`)

What this branch adds on top of `main` (9f0e410), in the paper's current numbering.
`README.md` covers the code, experiments and how to reproduce them.

## Paper (`paper.tex`, 5 pages + references)

- **Three focus papers:** EGL (2022), CNST (2021), and DGM (2006, k-cores). None is linked from the course page.
- **Section 4** adds one check of our own code: k-core pruning on simulated 100,000-vertex ER graphs (E6) vanishes within
  about 0.01 of DGM's thresholds.
- **Section 5** poses Q1–Q3 and positions the work against the closest prior work: Papachristou–Rahimian–Azadegan
  (arXiv v4, 2026; percolation, but 1-of-n sourcing and correlation instead of regions); Ang–Iancu–Swinney (2017; shared
  tier-2 suppliers make tier-1 disruptions coincide); Bimpikis–Fearing–Tahbaz-Salehi (2018; with S-shaped production,
  upstream dual sourcing can hurt the manufacturer, the same kind of mechanism as Example 1).
- **Section 6 (model):** k-of-n sourcing plus regional shocks with c supplier clusters.
  - Claim 1: collapse is abrupt iff km ≥ 2.
  - Claim 2: φ*_spread = 1 − x_crit/x and φ*_co = 1 − (1 − φ*_spread)^{1/m}; the extremes tie when m = 1.
  - Claim 3: with k = 1, splitting clusters never hurts (Jensen).
  - Example 1: with n = 4, k = 2, m = 1, x = 0.9, two pairs give φ* = 0.171 versus 0.195 for both extremes;
    a grid scan finds such reversals in 72 of 288 settings with k ≥ 2 and none with k = 1.
- **Section 7 (simulations):** E1 validation, E2 bimodality (Q1), E3/E5 thresholds (Q2), E4 hub regions (Q3).
  E3/E5 bisect each network's tipping point on 2,000 regions; all 20 bootstrap intervals contain the 20-layer theory.
- **Section 8:** final-project plans (endogenous supplier count and geography; OECD input–output test on the 2011 Thailand floods).

## Rules for edits

- Every number in the paper must appear in `results/summary.txt` (regenerate with `code/make_figures.py`).
- Figures are drawn at their printed size (`FIG_W` in `make_figures.py` = the `\includegraphics` width), so keep the two in sync.
- Check the page count after every edit: references must start on page 6.
