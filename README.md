# CS/INFO 6850 Exploratory Paper: k-of-n Multisourcing under Regional Shocks

## Layout
- `paper.tex` / `paper.pdf`: the paper (5 pages of content plus a references page).
- `figures/`: figures included by the paper (built by `code/make_figures.py`).
- `results/`: raw simulation output (`e1.json` … `e4.json`), `summary.txt` (every number quoted in the paper), and `run_log.txt`.
- `code/model.py`: mean-field theory. It solves the recursion (eq. 2 in the paper) for its largest fixed point and computes `x_crit`, `phi_star`, and finite-depth reliability. Running `python3 model.py` reproduces the analytic numbers (x_crit table, phi* table, Property 2 check).
- `code/simulate.py`: Monte Carlo on finite layered networks (vectorized NumPy). Supports k-of-n sourcing, c supplier clusters, regional shocks, heavy-tailed supplier popularity (`alpha`), hub regions (`region_weights`), and targeted shocks (`hit`). Running `python3 simulate.py` does a quick smoke test against the theory.
- `code/run_experiments.py`: runs experiments E1–E4 (about 25 min on 2 cores; `--quick` takes about 5 min with fewer replications).
- `code/make_figures.py`: builds the figures and `results/summary.txt` from the JSON results.

## Reproduce
```bash
pip install numpy scipy matplotlib
cd code
python3 model.py              # analytic tables
python3 run_experiments.py    # all simulations -> ../results/*.json
python3 make_figures.py       # figures + ../results/summary.txt
cd .. && pdflatex paper.tex && pdflatex paper.tex
```
All runs are seeded, so results reproduce exactly on the same NumPy version (2.x was used).

## Experiments
| ID | Hypothesis | What it does |
|----|-----------|---------------|
| E1 | H1: simulations match eq. (2) | sweeps x (phi = 0) and phi (x = 0.9) for k in {1,2}, c in {1,2,4}; compares each run to theory at its realized share of hit regions |
| E2 | H2: k >= 2 gives bimodal outcomes | 300 runs each of m = 1, k in {1,2} at the theoretical phi* |
| E3 | H3: phi* increases with c | estimates phi* from 270 runs per (k, c) and bootstraps a 95% CI |
| E4 | H4: realism | (a) Pareto supplier popularity; (b) Pareto supply weights across regions, hit by targeted vs random shocks |

Default network: depth 20 (21 layers), N = 20,000 firms per layer, G = 200 regions, m = 2, n = 4, x = 0.9.
