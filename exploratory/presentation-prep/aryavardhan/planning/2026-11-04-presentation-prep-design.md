# Design: presentation prep material (Aryavardhan's folder)

Author: Aryavardhan Singh. Date: 2026-11-04. Status: design approved in chat; spec for review.
Branch: `aryavardhan/presentation-prep` from `main` at `2360e7f` (the submitted paper).

## 1. Purpose and success criteria

The CS/INFO 6850 one-on-one presentation is a 20-minute conversation with one staff member, with no slides,
notes or devices. It covers three topics, each with both the math and the simulations:
(1) the questions we explored and what prior work did; (2) what we did beyond it; (3) what we found.
Staff grade whether we can accurately describe the questions, what we did and the conclusions, in our own words.
They do not ask about exact numbers.

The prep material therefore aims at **explainable understanding**, not memorization. Only the opening summary is
spoken to staff; everything else is for Aryavardhan and Arjun.

Success criteria:
1. The opening summary is about 2 minutes (~280–320 words) for one speaker. It covers all three handout topics with
   math and simulation in each, and it matches the submitted paper.
2. Every factual statement and number agrees with the submitted `paper.tex`/`results/` or with the cited source papers.
3. Each paper explainer has a TL;DR, an ELI5 and at least one visual.
4. The model explorer reproduces `code/model.py`'s φ* to 3 decimals on a test grid (k=1–3, m=1–3, n=4/6, all c | n).
5. The study page renders without console errors at desktop and phone widths, and works offline apart from CDN libraries.
6. Files are added only under `presentation-prep/aryavardhan/`, plus the placeholder `presentation-prep/arjun/.gitkeep`.

## 2. Files (all in `presentation-prep/aryavardhan/`)

| File | Content |
|---|---|
| `README.md` | Index, suggested study order, link to the published study page |
| `01-opening-summary.md` | ~2-minute spoken summary; a 5-step outline to memorize; a 30-second fallback; delivery tips; "hooks" that invite good follow-up questions |
| `02-our-work-explained.md` | TL;DR + ELI5 of the model, Claims 1–3, Example 1, experiments E1–E6. Mermaid diagrams: (a) research story; (b) one firm's survival check; (c) the fixed point and the cliff; (d) the pairs case tree; (e) the code-to-paper pipeline |
| `03-papers/egl.md`, `cnst.md`, `dgm.md` | Full explainers: TL;DR, ELI5, what they did, key result, visual, how we used or differ from it, weaknesses we named, likely questions |
| `03-papers/prior-work.md` | Shorter explainers: Papachristou–Rahimian–Azadegan, Ang–Iancu–Swinney, Bimpikis–Fearing–Tahbaz-Salehi |
| `03-papers/course-references.md` | One card each: Granovetter 1978, Centola–Macy 2007, Kempe–Kleinberg–Tardos 2003, Kleinberg 2007, Easley–Kleinberg §14.6, §19.2, §21.8 |
| `04-qa-bank.md` | ~50 questions grouped by the three topics, math, simulations, weaknesses, course links, "explain without the paper" and curveballs; each with a short answer and an "if pushed" answer; the most likely ones flagged |
| `05-cheatsheet.md` | Notation and terms, and the qualitative takeaways |
| `study-guide.html` | Interactive page: tabs Opening, Our work, Papers, Flashcards, Model explorer. It renders the Markdown files above, which are inlined at build time, so the two cannot drift apart |
| `tools/build_study_guide.py` | Inlines the Markdown into the HTML template |
| `tools/check_explorer.mjs` | Compares the explorer's math with values exported from `code/model.py` |

### Model explorer (inside the study page)
- **Inputs:** k, m, n, c (divisors of n), x, φ, and presets: EGL cliff (m=2, k=1), new one-input cliff (m=1, k=2), pairs result (n=4, k=2, m=1, x=0.9).
- **Plot 1:** F(r) against the diagonal at the current φ, with the largest fixed point r* marked; shows the tangency and the jump.
- **Plot 2:** r*(φ) for c=1, c=pairs (when n is even) and c=n, with each φ* marked.
- **Math:** coverage for c equal clusters of b=n/c suppliers, where j surviving clusters leave jb candidates:
  Σ_j C(c,j) s^j φ^(c−j) S_k(jb, xr); then F(r) = coverage^m; r* by iteration from r=1; φ* by bisection on r*>0.
  This is the paper's equation (2).

## 3. Verification
- Recompute the trap-scan denominator ("72 of the 109 settings") from `code/model.py`.
- Check the explorer against `model.py` (criterion 4).
- Open the study page in headless Chromium at 1280 px and 390 px wide; take screenshots and check the console.
- An independent reviewer that has not seen this conversation checks all files against `paper.tex`, `results/` and the cited
  papers. Its findings are fixed before delivery.

## 4. Delivery
- Commits are created through GitHub's API as realAryavardhanSingh (shown as Verified). Push the branch only, with no PR.
- Publish `study-guide.html` as a private artifact and add its link to `README.md`.

## Non-goals
No slides or pitch deck. No changes to the paper, code or results. Nothing in `presentation-prep/arjun/` beyond the placeholder.
