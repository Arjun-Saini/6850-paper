# Track B: computation

Single-firm coverage, the 109-setting test of Theorem B, and the key figure. The model is imported from `exploratory/code/model.py`, which Track B does not edit. Every Track B number comes from a script here and is saved in `results/`.

`cov(c, s, p, k, n)` lives in `final/track_b/code/coverage.py`.

| Task | Script | Output | Runtime |
|---|---|---|---|
| B1 `cov()` + §4 grid counts and n = 4, k = 2 window | `code/coverage.py`, `code/b1_grid.py` | `results/b1_grid.json` | seconds |
| B2 Theorem B on the 109 settings | `code/b2_settings.py` | `results/b2_settings.json` | ~10–15 min |
| B3 key figure: window in (s, p) + network paths | `code/b3_key_figure.py` | `figures/fig_key_window.pdf`, `results/b3_paths.json` | < 1 min |

Run from the repo root:

```
python3 final/track_b/code/b1_grid.py
python3 final/track_b/code/b2_settings.py
python3 final/track_b/code/b3_key_figure.py
python3 -m pytest final/track_b/tests                 # fast checks (~10 s)
RUN_SLOW=1 python3 -m pytest final/track_b/tests      # adds the full B2 scan (asserts 109 / 72)
```

## Definitions

- **Window** (single firm): some c with 1 < c < n, c | n, has C_c(s, p) < min(C_1, C_n). For n = 4, k = 2 this is Track A's p₋(s) < p < 2/3.
- **Reversal** (network): some refinement c | c2 has φ\*_c > φ\*_c2 + 1e-4, as in `model.refinement_violations`, so the 72 is the paper's 72.
- **Theorem B hypothesis** for a pair (c, c2): at c2's tipping point (s₂, p₂) = (1 − φ\*_c2, x·r\*_c2), C_c(s₂, p₂) > C_c2(s₂, p₂) + 1e-9. It must imply a reversal. `b2_settings.json` lists any pair that breaks this (should be none) and every reversal the hypothesis does not explain.

## Notes

- Track A's "reversal without the hypothesis" example (n = 4, k = 2, m = 1, x = 1, pairs vs co-located) is a boundary case. The pairs tipping point is exactly (s, p) = (3/4, 2/3): there C₂ = p with slope 1, and C₁ = C₂. So it sits on the window's edge, not outside it. `tests/test_track_b.py::test_pairs_x1_exact_tangency` checks this.
- The Nov 11 informal check did not record its grid spacing, so B1's counts may differ slightly from plan.md's 754 / 283 / 606 / 83 / 543 / 222 / 616.
