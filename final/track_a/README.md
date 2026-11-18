# Track A: theory

Lemma A, Claim 3 for any refinement, Theorem B and the large-n limit. Every Track A number comes from a script here and is saved in `results/`. The coverage and fixed-point code is imported from `exploratory/code/model.py`, which Track A never edits.

Setup and rerun (from the repo root):

```
pip install -r final/track_a/requirements.txt
python3 final/track_a/code/run_all.py        # regenerates results/ (about 7 minutes)
python3 -m pytest final/track_a/tests
```

| Task | Script | Result | Write-up |
|---|---|---|---|
| A3 Lemma A, n = 4, k = 2 | `code/lemma_a_n4k2.py` | `results/lemma_a_n4k2.json` | `notes/lemma_a_n4k2.md` |
| A6 Claim 3 for any refinement | `code/claim3_refinement.py` (uses `code/partition_coverage.py`) | `results/claim3_refinement.json` | `notes/claim3_refinement.md` |
| A4 Theorem B | `code/theorem_b_base_case.py` | `results/theorem_b_base_case.json` | `notes/theorem_b.md` |
| A5 Lemma A, general (n, k, c) | `code/lemma_a_general.py` | `results/lemma_a_general.json` | `notes/lemma_a_general.md` |
| A7 Large-n limit | `code/large_n.py` | `results/large_n.json` | `notes/large_n.md` |

## Status (Nov 17, end of run 1; next steps in HANDOFF.md)

- **A3 (done):** the window is p₋(s) < p < 2/3 with p₋(s) = 2/(4s + √(2s(5s−3))), and it opens at s > (3−√3)/2.
- **A6 (done):** Claim 3 holds for any refinement, unequal splits included. It does not hold for non-nested geographies with more clusters.
- **A4 (proof and base case done):** the evidence across the 109 settings waits on Track B's B2. The condition is sufficient, not necessary.
- **A5 (done):**
    - c = 2: proved for all (n, k), with an s-free cutoff p̂(n, k).
    - Other c: edge limits plus a numerical characterization.
    - Still to do: cross-check against B1's grid once it lands.
- **A7 (done):** formal limit. Every intermediate c is strictly worse than spread, and for m = 1 than co-location too. The swap of limits is not proved.
- **A2 (citations, in progress):** all plan.md [VERIFY] references are verified, and k-out-of-n references were added (`refs_track_a.bib`, `notes/citations.md`). The Bai et al. (1991) abstract still needs checking.
- **W2 (paper sections):** waits on agreeing the `final/paper/` layout with Arjun.
