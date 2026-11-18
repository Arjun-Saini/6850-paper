# CS 6850 Track A: handoff to the Mac Studio session

Written Tue Nov 17, 2026 (evening ET) by the cloud session that did the planning.

## Status
- Done: read the repo, plan.md and the tracker; drafted the task plan and Git plan below.
- Not started: every Track A task. No branch has been created and no files in the repo were changed.
- Why it moved: the cloud session could clone the repo but could not push (the Claude GitHub App is not installed on Arjun-Saini/6850-paper). On Nov 17 Kris chose to run the work in Claude Code on his Mac Studio, which pushes with his own GitHub access. Kris is a collaborator with write access.
- A1 is done: Kris says the roadmap was submitted on Nov 16, exactly as `final/roadmap.tex` stands on `final-project-roadmap`. So A2 (citations) no longer blocks anything for the freeze and runs after it.
- Tracker: the Claude Sheet "CS 6850 Final Project Tracker", https://claude.ai/artifact/4VKMpnrcEuiiasLQKBq8CF (tabs Read me, Track A, Track B, Shared, Handoffs). Kris wants this session to keep the Track A rows current. Check at the start whether a Claude Docs tool is available (`/mcp`). If it is, read the tracker with it. If not, tell Kris which row to change each time instead.

## First steps on the Mac Studio
1. The local clone is `~/Documents/6850-paper`. Work only there. This file should be at `final/track_a/HANDOFF.md` on branch `aryavardhan/track-a` (Kris's setup steps put it there).
2. `git fetch origin` and check whether Arjun pushed anything after Nov 12 (B1 `cov()`, grid data, B2). Update the plan below if so.
3. Check the Python environment: `python3 -c "import numpy, scipy, sympy, pytest"`, then `python3 -m pytest exploratory/tests`.
4. Check tracker access (see Status), then start with A3.
5. First commit: this HANDOFF.md plus `final/track_a/requirements.txt`. Push with `git push -u origin aryavardhan/track-a`.

## Open questions for Kris
1. The shared-file layout under "Shared files to agree with Arjun" needs Arjun's agreement before Track A writes into `final/paper/`.

## Limits carried over
Only push to `aryavardhan/track-a`. Never push to `final-project-roadmap`, `main` or Arjun's branches, never force-push or rewrite shared history. Don't open a PR, merge, or message anyone without Kris's yes. Tracker edits: only the Status (and Notes if useful) of Track A rows, and the Done box of Handoffs rows that Track A delivered or received. Don't edit Track B or Shared rows, owners, dates or the Read me tab. Every number in the paper must come from code in the repo. Check every [VERIFY] item. Anything outside Lemma A, Theorem B, the large-n limit and R1–R6 goes into a future-work sentence.

---

## What the repo shows right now

- Branches on GitHub: `main`, `final-project-roadmap` (Arjun, Nov 12), `aryavardhan/presentation-prep` (Nov 4).
- Arjun has pushed nothing since Nov 12, so B1 (`cov()` and grid data) and B2 (109-setting results) are not in the repo yet.
- `final/` holds `plan.md`, `roadmap.tex` and `roadmap.pdf`. This roadmap is the version that was submitted.
- There is no paper source for the final yet (no `final/paper/`).
- `exploratory/code/model.py` already has `F(r, x, m, n, k, c, phi)`. With m = 1, p = x·r and s = 1 − φ, `F` is exactly the single-firm coverage C_c(s, p) from plan.md §4. So Track A can cross-check its closed forms against existing code tonight, without waiting for B1. B1 is still needed to match Arjun's official grid counts.
- `model.F` only handles equal clusters (it asserts c divides n). Track A's Claim 3 work needs unequal clusters, so Track A will add its own small coverage function for arbitrary cluster sizes in its own folder rather than changing `model.py`.

## Task plan (in order)

Dates: today is Tue Nov 17. Results freeze (F1) is Fri Nov 20.

0. **Setup (tonight).** Branch, install numpy, scipy, sympy and pytest, run the existing tests.

1. **A3. Lemma A, n = 4, k = 2 (overdue).** Depends on nothing; B1 is only a cross-check, and `model.F` covers that now.
   - Upper edge vs co-location: pairs − co-located = s(1 − s)·[2p² − S₂(4, p)], so the edge is s-free and sits at the root of 2p² = S₂(4, p), which is p = 2/3 (S₂(4, 2/3) = 72/81 = 2·(2/3)²).
   - Lower edge vs spread: solve pairs = spread, i.e. s²S₂(4, p) + 2s(1 − s)p² = S₂(4, sp), symbolically in (s, p). Also find the smallest s at which a window opens (plan.md says none at s = 0.6).
   - Produces: `lemma_a_n4k2.py` (sympy), `results/lemma_a_n4k2.json`, `notes/lemma_a_n4k2.md`, and a test checking the closed forms against `model.F`.
   - Hands off: closed-form window edges to Track B for the key figure (Handoffs row "Closed-form window edges (A3)", unblocks B3).

2. **A6. Claim 3 for any refinement (due today).** Depends on nothing.
   - Likely short proof (to be checked): with k = 1, a cluster of size b fails with probability φ + s·qᵇ (q = 1 − p). Splitting b = b₁ + b₂ changes the failure probability by φs(1 − q^b₁)(1 − q^b₂) ≥ 0, so any split, unequal ones included, can only help. Pointwise larger F gives a larger fixed point, so φ* can only go up.
   - Produces: proof write-up, `partition_coverage.py` for arbitrary cluster sizes, and a numerical check.

3. **A4. Theorem B proof (due Nov 18).** Proof is not blocked; the evidence part waits on B2.
   - Fixed-point comparison: if F_B(r_A*) ≥ r_A*, then F_B has a fixed point in [r_A*, 1]. Then strictness and continuity in φ to get φ*_pairs < φ*_X, and the m-input case via F = coverage^m.
   - Base-case check script reproducing φ* = 0.1946 / 0.1705 / 0.1946 and r_P ≈ 0.678 from code, not from plan.md.
   - Produces: proof write-up and `theorem_b_base_case.py`.
   - The 109-setting test (explaining 72/109) is Arjun's B2. Track A will not redo it; the write-up will cite B2's output once it lands.

4. **A5. Lemma A for general (n, k, c) (due Nov 20, riskiest).** Depends on A3; B1 grid data only for cross-checking counts.
   - Likely clean result for c = 2 and any (n, k): C₂ − C₁ = s(1 − s)·[2S_k(n/2, p) − S_k(n, p)], so the cutoff vs co-location is an s-free root p̂(n, k) of 2S_k(n/2, p) = S_k(n, p). This generalizes 2/3, and with k = 1 there is no root, matching Claim 3.
   - Other c and the edge vs spread: prove what is tractable and characterize the rest numerically. A general closed form may not exist [VERIFY].
   - Fallback if it runs long: freeze with the c = 2 theorem plus a numerical characterization for the rest.

5. **A7. Large-n limit (due Nov 20).** Depends on A5.
   - Coverage tends to Pr[Bin(c, s) ≥ ⌈k/(b·p)⌉]; closed-form tipping points and whether the reversal persists as redundancy grows.
   - Proposed cut line: if A5 is not done by Thu Nov 19 night, A7 becomes a short numerical remark or a future-work sentence. plan.md already marks it optional.

6. **A2. Citations (overdue).** Verify the [VERIFY] references and find 1–2 k-of-n / common-cause-failure reliability references.
   - A1 is already submitted, so A2 only feeds §2 Related work and runs after the freeze.

7. **A1. Roadmap.** Done: submitted Nov 16 as it stands in the repo. Mark the tracker row Done if it still says To do.

8. **Handoff Nov 21:** one-sentence framing of the question for the slides (unblocks P1).

9. **W2. Paper §2, §4, §5, §6 (due Dec 4).** After the freeze.

## Git plan

**Branch.** `aryavardhan/track-a`, cut from `origin/final-project-roadmap`, matching the existing `aryavardhan/...` naming. Pushes go only to this branch. Never to `final-project-roadmap`, `main` or any Arjun branch; no force-push; no rebase of anything already pushed.

**Commits.** Authored as `Aryavardhan Singh` with the GitHub noreply address already used in the repo's history. Not signed with any sandbox key. Small commits, one per piece (e.g. "A3: closed-form upper edge of the n=4, k=2 window").

**Files Track A owns (new folder, nothing else touched):**

```
final/track_a/
  README.md            what each script makes; how to rerun
  requirements.txt     numpy, scipy, sympy, pytest
  code/                lemma_a_n4k2.py, partition_coverage.py, claim3_refinement.py,
                       theorem_b_base_case.py, lemma_a_general.py, large_n.py, run_all.py
  results/             JSON written by the scripts (every Track A number comes from here)
  notes/               proof write-ups in Markdown
  tests/               pytest checks against exploratory/code/model.py (and Arjun's cov() once it lands)
final/paper/sections/  sec2_related.tex, sec4_lemma_a.tex, sec5_theorem_b.tex, sec6_large_n.tex
final/paper/refs_track_a.bib
```

**Arjun's code is read-only.** Track A imports from `exploratory/code/` (as the repo README says final-project code should) and, once B1 lands, from wherever Arjun puts `cov()`. Track A never edits those files. If Track A finds a bug in Arjun's code, it reports it to Kris instead of fixing it.

**Bringing in Arjun's work.** `git fetch origin` at the start of every working session and before each push. Merge `origin/final-project-roadmap` into `aryavardhan/track-a` (merge, not rebase) whenever it moves. Arjun's own feature branches are read only (`git show origin/<branch>:<path>`) and are not merged into Track A, so the two lines of work stay separate until the end.

**Merge at the end.** After the freeze, with Kris's yes: merge `final-project-roadmap` into `aryavardhan/track-a` once more, run all tests, then open a PR into `final-project-roadmap`. Because the folders don't overlap, the merge should be conflict-free whichever of you merges first.

**Shared files to agree with Arjun (Track A won't touch these without that):**
1. Paper source. Proposal: one `final/paper/main.tex` that `\input`s each section file and lists `\bibliography{refs_track_a,refs_track_b}`. One person owns `main.tex`; each track owns only its own section and bib files.
2. `final/roadmap.tex`. Submitted as is; Track A won't edit it.
3. `final/plan.md`. Track A won't edit it; Track A status lives in `final/track_a/README.md` and the tracker.
4. Root `README.md`. Track A won't edit it (its extra dependency, sympy, goes in `final/track_a/requirements.txt`).
5. Where `cov()` lives. Track A tests will import it from wherever Arjun puts it; it would help to know the path.

