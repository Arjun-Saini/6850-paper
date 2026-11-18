# CS 6850 Track A: handoff to run 2

Written Tue Nov 17, 2026, late evening ET, by run 1 (Claude Code on the Mac Studio, repo `~/Documents/6850-paper`, branch `aryavardhan/track-a`). Run 2 is planned for after the results freeze (Fri Nov 20). Read this whole file first. The original planning handoff it replaces is in git history (`git show 4f9d223:final/track_a/HANDOFF.md`).

## Where things stand (end of run 1)

All Phase 1 theory is done except the evidence part of A4, which waits on Arjun's B2. Everything is pushed to `origin/aryavardhan/track-a` and lives only under `final/track_a/`. `final/track_a/README.md` maps each task to its script, result JSON and write-up. 36 tests pass: 17 Track A and 19 exploratory. `code/run_all.py` regenerates every result byte for byte in about 7 minutes.

| Task | Tracker status | What exists | What's left |
|---|---|---|---|
| A3 Lemma A, n=4, k=2 | Done | `code/lemma_a_n4k2.py`, `notes/lemma_a_n4k2.md`. Window p₋(s) < p < 2/3, with p₋(s) = 2/(4s + √(2s(5s−3))); it opens at s > (3−√3)/2 | Cross-check vs B1's `cov()` when it lands |
| A6 Claim 3, any refinement | Done | `code/claim3_refinement.py`, `code/partition_coverage.py`, `notes/claim3_refinement.md`. Proof by the identity φs(1−q^b₁)(1−q^b₂) ≥ 0. Fails for non-nested splits (21 of 43 pairs) | Nothing |
| A4 Theorem B | **Blocked** (on B2) | `code/theorem_b_base_case.py`, `notes/theorem_b.md`. Proof is complete (Lemmas 1–2 + theorem + corollary). Base case reproduced from code. The condition is **sufficient, not necessary** (m=1, x=1 vs co-located) | Evidence section from B2's 109-setting output, then Done |
| A5 Lemma A, general | Done | `code/lemma_a_general.py`, `notes/lemma_a_general.md`. c=2 proved for all (n, k) with an s-free cutoff p̂(n, k); other c: s→0 / s→1 limits + numerics. Monotonicity of the edge in s is numerical only | Cross-check vs B1 grid data |
| A7 Large-n limit | Done | `code/large_n.py`, `notes/large_n.md`. Formal limit: every intermediate c is strictly worse than spread (Markov), and than co-location when m=1. Finite n up to 160 keeps the ordering; convergence is slow | The swap of limits is not proved; say so in §6 |
| A2 Citations | In progress | `refs_track_a.bib` (draft location), `notes/citations.md`. All four plan.md [VERIFY] refs verified; two summaries reworded. Added Kuo & Zuo 2003 (verified) and Bai–Yun–Chung 1991 | **Bai et al. content is unverified**: its abstract couldn't be fetched (see notes). Then mark A2 Done |
| A1 Roadmap | Done | Submitted Nov 16 as `final/roadmap.tex` stands | Nothing |
| W2 Paper §2, §4–6 | To do | Write-ups in `notes/` are the source material | Waits on the paper layout (below) and F1 |

## Decisions the user made in run 1

- **Paper layout (open question 1):** Arjun had **not** agreed yet, so Track A writes nothing into `final/paper/`. `refs_track_a.bib` sits in `final/track_a/` until then. Ask the user at the start of run 2 whether Arjun has answered.
- **A2:** start now, before the freeze (Nov 17).
- **Tracker:** keep the Track A rows current yourself. Tick a Handoffs box only after the user confirms the item was actually communicated.
- **Arjun message:** the user sent it on Nov 17. It contained the A3 window formula and file path, the "sufficient, not necessary" heads-up for B2, the plan.md correction (F_spread(r_P) = 0.6975 and F_coloc(r_P) = 0.6910, not 0.696 / 0.690), asks for B2 by Nov 18–19 and the location of `cov()`, and the paper-layout proposal. The Handoffs row "Closed-form window edges (A3)" is ticked.

## Waiting on others

| From | What | Unblocks |
|---|---|---|
| Arjun | B2 109-setting output | A4 → Done; Handoffs row "109-setting results (B2)" |
| Arjun | B1 `cov()` + grid data, and the path where `cov()` lives | Cross-checks for A3/A5; Handoffs rows "cov() function…" and "Grid data…" |
| Arjun | Answer on the `final/paper/` layout | W2 |
| User | Bai, Yun & Chung (1991) abstract from IEEE Xplore (doi 10.1109/24.75334) | A2 → Done |

## Start-of-run checklist for run 2

1. `cd ~/Documents/6850-paper && git status && git fetch origin`. The local branch tracks `origin/aryavardhan/track-a` (fixed in run 1; it used to track `final-project-roadmap`, so a bare `git push` was risky).
2. See what Arjun pushed: `git for-each-ref --sort=-committerdate refs/remotes --format='%(refname:short) %(committerdate:iso) %(authorname)'`, then `git log --oneline ec6f1ca..origin/final-project-roadmap`. If `final-project-roadmap` moved, merge it into `aryavardhan/track-a` (merge, never rebase). Read Arjun's feature branches only with `git show`.
3. `python3 -m pytest final/track_a/tests exploratory/tests -q`. The venv is `~/.venvs/cs6850` (numpy 2.5, scipy 1.18, sympy 1.14, pytest 9.2).
4. Tracker: check for a Claude Docs connector (`claude mcp list`; in run 1 it showed "claude.ai Claude Docs … ✔ Connected"). Load the docs skill and the `topic.sheets` guide, then read the Track A tab:
   - Sheet doc id `1c3f8e42-23af-440c-aa53-151375605d28` (link https://claude.ai/artifact/4VKMpnrcEuiiasLQKBq8CF); workbook node `e38670b0-b22c`, engine `workbook`.
   - Track A rows: A2 = row 4, A3 = 5, A1 = 6, A6 = 7, A4 = 8, A5 = 9, A7 = 10, W2 = 11. Status is column D (To do / In progress / Blocked / Done), Notes is column H.
   - Handoffs: Done checkbox in column F. Row 2 = B1 cov() → A, row 3 = A3 edges → B (ticked), row 4 = B2 → A, row 5 = B1 grid → A, row 6 = freeze, row 7 = framing sentence (A → B, Nov 21), row 8 = swap sections.
   - Every `applyEdits` needs the current `revision` as `base`. Run 1 ended at revision 19; read first, because Arjun may have edited since.
5. Ask the user the open questions: has Arjun answered on the layout, and does the user have the Bai et al. abstract.

## Task plan for run 2 (in order)

1. **Bring in Arjun's work.**
   - If B2 has landed: add an "Evidence" section to `notes/theorem_b.md` from B2's output. Count the settings where the pairs tipping point (1 − φ\*_P, x·r_P) lies in the single-firm window (pairs strictly below both extremes there) and compare with where the network reversal occurred. Because the condition is only sufficient, expect reversals outside the window; report how many and how far from the edge. Cite B2's file and do not rerun the 109 settings. Then set A4 to Done and tick Handoffs row 4.
   - If B1 has landed: add a test importing Arjun's `cov()` that checks it against `lemma_a_n4k2` and `lemma_a_general`, then tick Handoffs rows 2 and 5. If his `cov()` disagrees with `model.F`, report it to the user and don't fix his code.
2. **A2 wrap-up.** Once the Bai et al. abstract is checked, update `notes/citations.md` and mark A2 Done. If it can't be checked, use Chae & Clark (1986) or drop the common-cause citation.
3. **Handoff, Nov 21: a one-sentence framing for the slides** (Handoffs row 7). Draft for the user to approve or edit:
   > When firms need more than one supplier to keep running, splitting suppliers across two regions can make a supply network more fragile than either keeping them together or spreading them out, and the network's own cascades push it into exactly the conditions where this happens.
4. **P1 slides (Track B owns, Track A edits).** Check every Track A number on the slides against `results/*.json`.
5. **W2 (due Dec 4), once the layout is agreed.** Turn the notes into `final/paper/sections/`:
   - sec2_related.tex ← notes/citations.md
   - sec4_lemma_a.tex ← notes/lemma_a_n4k2.md + notes/lemma_a_general.md + notes/claim3_refinement.md (Claim 3′ as a remark)
   - sec5_theorem_b.tex ← notes/theorem_b.md
   - sec6_large_n.tex ← notes/large_n.md

   Move `refs_track_a.bib` to `final/paper/refs_track_a.bib`. Keep plan.md's guardrails: don't headline the m=1 tie; say the reversal matters near the tipping point; every number comes from `results/`.
6. **Merge at the end** (Git plan below), only with the user's yes.

## Run 1 notes that save time

- **Runtime:** `claim3_refinement.py` takes about 6 minutes; everything else takes seconds. The tests take about 10 s.
- **Crossref** (`api.crossref.org/works/<doi>` and `?query.bibliographic=`) gave reliable metadata, and abstracts for AER. IDEAS/RePEc pages gave the Elsevier abstracts. IEEE Xplore, wiley.com, KAIST dspace and the TAMU catalog all failed to fetch.
- **Never put the user's email address** in a request to an outside service (a Crossref "mailto" header was rightly blocked).
- **Notes on notation:** s = 1 − φ throughout; p = x·r is the effective supplier reliability; "window" means pairs strictly below both extremes.
- **Old plan.md values:** some of its numbers are slightly off (see the Arjun message above). Always quote from `results/`.

## Limits carried over
Only push to `aryavardhan/track-a`. Never push to `final-project-roadmap`, `main` or Arjun's branches, never force-push or rewrite shared history. Don't open a PR, merge, or message anyone without Kris's yes. Tracker edits: only the Status (and Notes if useful) of Track A rows, and the Done box of Handoffs rows that Track A delivered or received. Don't edit Track B or Shared rows, owners, dates or the Read me tab. Every number in the paper must come from code in the repo. Check every [VERIFY] item. Anything outside Lemma A, Theorem B, the large-n limit and R1–R6 goes into a future-work sentence.

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
