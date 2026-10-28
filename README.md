# CS/INFO 6850 Exploratory Paper: k-of-n Multisourcing under Regional Shocks (a Directed k-Core)

## Layout
- `paper.tex` / `paper.pdf`: the paper (5 pages of content plus a references page).
- `figures/`: figures included by the paper (built by `code/make_figures.py`).
- `results/`: raw simulation output (`e1.json` … `e4.json`), `summary.txt` (every number quoted in the paper), and `run_log.txt`.
- `code/model.py`: mean-field theory, plus the geography theorems (`phi_star_closed_form`, `refinement_violations`) and DGM's Erdős–Rényi k-core equations (`dgm_er_core_size`, `dgm_er_Qc`). It solves the recursion (eq. 2 in the paper) for its largest fixed point and computes `x_crit`, `phi_star`, and finite-depth reliability. Running `python3 model.py` reproduces the analytic numbers (x_crit table, phi* table, Proposition 2 and Theorem 3 checks, trap scan).
- `code/simulate.py`: Monte Carlo on finite layered networks (vectorized NumPy). Supports k-of-n sourcing, c supplier clusters, regional shocks, heavy-tailed supplier popularity (`alpha`), hub regions (`region_weights`), and targeted shocks (`hit`). Running `python3 simulate.py` does a quick smoke test against the theory.
- `code/kcore.py`: k-core peeling (Batagelj–Zaversnik) and an Erdős–Rényi generator, used by E6.
- `code/run_experiments.py`: runs experiments by name, e.g. `python3 run_experiments.py E5 E6`; with no names it runs E1–E4 (about 25 min on 2 cores; `--quick` takes about 5 min with fewer replications).
- `tests/`: `python3 -m pytest tests` checks each theorem against the numerical recursion, the k-core code, and the experiment CLI.
- `NOTES.md`: what the `geography-kcore` branch changed and why.
- `code/make_figures.py`: builds the figures and `results/summary.txt` from the JSON results.

## Reproduce
```bash
pip install numpy scipy matplotlib pytest
cd code
python3 model.py              # analytic tables
python3 run_experiments.py    # E1-E4 -> ../results/*.json
python3 run_experiments.py E5 E6   # new experiments (~6 min)
python3 make_figures.py       # figures + ../results/summary.txt
cd .. && pdflatex paper.tex && pdflatex paper.tex
```
All runs are seeded, so results reproduce exactly on the same NumPy version (2.x was used).

## Experiments
| ID | Hypothesis | What it does |
|----|-----------|---------------|
| E1 | H1: simulations match eq. (2) | sweeps x (phi = 0) and phi (x = 0.9) for k in {1,2}, c in {1,2,4}; compares each run to theory at its realized share of hit regions |
| E2 | H2: k >= 2 gives bimodal outcomes | 300 runs each of m = 1, k in {1,2} at the theoretical phi* |
| E3 | H3: does phi* increase with c? (yes for k = 1, Theorem 4; not always for k >= 2, Proposition 5) | estimates phi* from 270 runs per (k, c) and bootstraps a 95% CI |
| E4 | H4: realism | (a) Pareto supplier popularity; (b) Pareto supply weights across regions, hit by targeted vs random shocks |
| E5 | Theorem 3, Proposition 5 | phi* for every cluster count c of (m,n,k) in {(1,4,2),(1,6,3),(2,6,3),(3,4,2)}: the closed form and the diversification trap on finite networks |
| E6 | DGM reproduction | k-core sizes of Erdős–Rényi graphs (N = 100,000, mean degree 10) after random vertex removal, against DGM's thresholds |

Default network: depth 20 (21 layers), N = 20,000 firms per layer, G = 200 regions, m = 2, n = 4, x = 0.9.
