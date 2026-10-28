# Change notes for Arjun (branch `aryavardhan/geography-kcore`)

This branch builds on your `main` (9f0e410). Your E1–E4 code and results are untouched (`results/e1–e4.json` are
byte-identical, and the E1–E4 lines of `summary.txt` are unchanged). Your text was edited in place where needed to make room
for a third paper and the new results while staying at 5 pages. Design: `docs/specs/`; plan: `docs/plans/`.

## The headline change: the geography conjecture is false for k ≥ 2

Your Section 5 conjectured that φ* increases with c. That is true for k = 1 (now **Theorem 4**, with a proof) but
**false for k ≥ 2**: with n = 4, k = 2, m = 1, x = 0.9, φ* = 0.1946 co-located, **0.1705** with two regional pairs, and
0.1946 fully spread. Simulation confirms this on finite networks (E5; the c = 2 interval lies strictly below both extremes).
In a 360-case scan, splitting clusters lowers φ* in 72 cases, all with k ≥ 2 (`results/trap_scan.json`).
Your Table 1 numbers are exactly explained by the new closed form (**Theorem 3**):
φ*_co = 1 − (1 − φ*_spread)^{1/m}, so 0.425 → 0.242 and 0.077 → 0.039.

## Paper changes (section by section)

| Location in `paper.tex` | What changed | Why |
|---|---|---|
| Title | Subtitle now "A Directed k-Core View of Multisourcing under Correlated Regional Shocks" | Reflects DGM and the new framing |
| Abstract | Rewritten: three papers; Theorems 1, 3, 4 and the trap; "co-locating lowers the threshold in every case tested" removed | That claim is false for k ≥ 2 |
| §1 Introduction | Condensed; adds DGM and why it was added; roadmap for 8 sections | Third focus paper |
| §2 EGL | Technical content kept, slightly condensed; course connections and weaknesses merged into one paragraph; adds Easley–Kleinberg §21.8 | Space |
| §3 CNST | Condensed by about 40% (two paragraphs) | Space |
| §4 DGM (new) | Technical content; course connections, weaknesses, and directions | Third focus paper |
| §5 Synthesis | Three-paper version | Third focus paper |
| §6 Model | Setup kept (condensed); adds the directed k-core correspondence (K = k + 1). Property 1 → **Theorem 1** (now "abrupt iff km ≥ 2", both directions, with proof). Property 2 → **Proposition 2** (unchanged). Property 3 → folded into **Theorem 3** (closed form). Conjecture → **Theorem 4** (k = 1, proved) plus **Proposition 5** (the trap, k ≥ 2). Worked example kept (shortened) | New results; conjecture refuted |
| §7 Experiments | Setup and validation condensed (your numbers kept); bimodality kept; **Table 1 merged**: your E3 rows plus three E5 rows for m = 1 and a closed-form column; new paragraph on the geography results; realism paragraph keeps your hub result (and the 5% random-collapse sentence), compresses E4a to one sentence, adds the E6 DGM reproduction | New experiments |
| Figure 2 | New panel (c), the diversification trap (E5) | New result |
| §8 Discussion + Conclusion | Merged into one section; adds the CNST-style test of the trap and next steps | Space, new results |
| References | Adds Dhaene et al. (2002) and Shaked & Shanthikumar (2007) for the convex-order proof; drops Buldyrev et al. (2010) (its sentence was cut) | Proof citations |
| AI acknowledgment | Adds "check the proofs numerically" | Accuracy |

Numbering: the paper uses one counter (Theorem 1, Proposition 2, Theorem 3, Theorem 4, Proposition 5). The spec calls
these Theorem 1, —, Theorem 2, Theorem 3, Proposition 4.

## Code and results changes

- `code/model.py`: adds `phi_star_closed_form`, `refinement_violations`, `dgm_er_core_size`, `dgm_er_Qc`; `__main__` prints the
  Theorem 3 check and the trap scan.
- `code/kcore.py` (new): k-core peeling (Batagelj–Zaversnik) and an Erdős–Rényi generator; no networkx needed.
- `code/run_experiments.py`: adds E5 and E6; the command line now accepts experiment names (`python3 run_experiments.py E5 E6`);
  with no names it still runs E1–E4. E3's depth-20 bisection is factored into `depth20_threshold` (same logic).
- `code/make_figures.py`: Figure 2(c); new `summary.txt` lines (E5, E6, THM2 checks, trap scan, TABLE1/TABLE2, E4b random
  collapse share). The 360-case scan is cached in `results/trap_scan.json` (about 8 minutes to compute; delete the file to recompute).
- `tests/` (new): `python3 -m pytest tests` checks every theorem against the numerical recursion, the k-core code against
  a hand-checked graph and DGM's ER theory, and the experiment CLI.
- New results: `results/e5.json` (3,780 runs), `results/e6.json`, `results/trap_scan.json`.

## Reproduce the new results

```bash
pip install numpy scipy matplotlib pytest
python3 -m pytest tests                    # ~2 min
cd code
python3 run_experiments.py E5 E6           # ~6 min on 2 cores
python3 make_figures.py                    # first run ~8 min (trap scan), then fast
cd .. && pdflatex paper.tex && pdflatex paper.tex
```

## Things to look at

1. Section 6's policy sentence: "a buyer that needs two working suppliers per input can be worse off splitting its suppliers
   between two regions than keeping them together". It is a model result; tone it down if you think it overreaches.
2. CNST was cut the hardest. If you would rather cut DGM's weaknesses paragraph, there is room to restore about 4 lines.
3. Page 5 has roughly a quarter page free for anything you want to add back.
