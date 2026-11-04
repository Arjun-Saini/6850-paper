# Presentation Prep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the study set for the CS 6850 one-on-one presentation in `presentation-prep/aryavardhan/`. It contains the spoken opening summary, an explainer of our work, explainers for each paper we used, a Q&A bank and a cheatsheet, plus an interactive study page with flashcards and a model explorer.

**Architecture:** The Markdown files are the single source of content. `tools/build_study_guide.py` inlines them, together with `tools/explorer.js`, into `study-guide.html`, which renders the Markdown (marked) and diagrams (mermaid) in the browser. The explorer's math is a small pure-JS module that is checked against `code/model.py` through an exported reference file.

**Tech Stack:** Markdown + Mermaid; one HTML page with marked 12.0.2 and mermaid 10.9.1 from cdnjs/jsdelivr; plain JS, with plots drawn in inline SVG (no plotting library); Python 3 (build and reference export); Node 22 (math check); Playwright/Chromium (render check).

**Spec:** `presentation-prep/aryavardhan/planning/2026-11-04-presentation-prep-design.md`

## Global Constraints
- Write only under `presentation-prep/aryavardhan/`, plus the placeholder `presentation-prep/arjun/.gitkeep`. Do not touch the paper, code or results.
- Content must match the submitted paper (`main` at `2360e7f`): use its names (Claims 1–3, Example 1, Q1–Q3, E1–E6) and its numbers.
- Opening summary: one speaker, ~2 minutes (280–320 words), covering all three handout topics with math and simulation in each.
- Every paper explainer has a TL;DR, an ELI5 and at least one visual (a Mermaid diagram or an SVG figure).
- Explorer φ* matches `code/model.py` `phi_star` within 1e-3 on the test grid.
- No exact-number memorization drills. Q&A answers lead with the qualitative takeaway.

## Review Focus
1. **The explorer on n with no pairs split (n odd, or c not dividing n):** offer only divisors of n for c, and hide the "pairs" curve when n is odd. Test `clusterOptions(5)` → `[1,5]`.
2. **An explorer setting that is collapsed at φ=0 (x < x_crit):** φ* shows 0 and the plot shows r* = 0, with no NaN. Test `phiStar({x:0.3,m:2,n:4,k:2,c:4})` → `0`.
3. **k > n:** coverage is 0 everywhere. Test `coverage(0.5,0,{x:.9,m:1,n:2,k:3,c:2})` → `0`, and φ* = 0.
4. **Mermaid syntax errors break a whole tab silently:** the render check fails if any `.mermaid` node contains an error SVG ("Syntax error").
5. **Phone width:** no horizontal page scroll at 390 px. The render check asserts `scrollWidth <= clientWidth`.

---

### Task 1: Explorer math, checked against the Python model

**Files:**
- Create: `presentation-prep/aryavardhan/tools/explorer_math.js` (ES module, no DOM)
- Create: `presentation-prep/aryavardhan/tools/export_reference.py`
- Create: `presentation-prep/aryavardhan/tools/check_explorer.mjs`
- Generated: `presentation-prep/aryavardhan/tools/explorer_reference.json`

**Interfaces:**
- Produces: `binomTail(k, N, p) -> number`, `coverage(r, phi, P) -> number`, `F(r, phi, P) -> number`, `rStar(phi, P) -> number`, `phiStar(P) -> number`, `clusterOptions(n) -> number[]`, where `P = {x, m, n, k, c}`. These functions are inlined by Task 5.

- [ ] **Step 1:** Write `export_reference.py`. It imports `code/model.py` and, for k ∈ {1,2,3}, m ∈ {1,2,3}, n ∈ {4,6}, every c | n and x ∈ {0.6, 0.8, 0.9, 1.0}, writes `{x,m,n,k,c,phi_star, r_star_at:{"0.05":…, "0.15":…}}` using `phi_star` and `largest_fixed_point`. Also add the three Review Focus cases.
- [ ] **Step 2:** Write `check_explorer.mjs`. It loads the JSON and asserts |phiStar − phi_star| ≤ 1e-3 and |rStar − r_star| ≤ 1e-3, plus the Review Focus assertions (`clusterOptions(5)` deep-equals `[1,5]`; `phiStar({x:0.3,m:2,n:4,k:2,c:4}) === 0`; `coverage(0.5,0,{x:.9,m:1,n:2,k:3,c:2}) === 0`). It prints `OK <count>` or the failures and exits 1.
- [ ] **Step 3:** Run `python3 tools/export_reference.py && node tools/check_explorer.mjs`. Expected: fails (module missing).
- [ ] **Step 4:** Implement `explorer_math.js`. Coverage with b = n/c: Σ_{j=0..c} C(c,j) s^j φ^{c−j} S_k(j·b, x·r). `F = coverage^m`. `rStar`: iterate r ← F(r) from r=1 for up to 2000 steps, stopping when the change is < 1e-12, and return 0 if r < 1e-9. `phiStar`: 0 if rStar(0)=0; otherwise bisect φ on [0,1] for 40 steps on rStar>0.
- [ ] **Step 5:** Run the check. Expected: `OK <n>` with no failures.
- [ ] **Step 6:** Commit: `Add model-explorer math checked against code/model.py`.

### Task 2: Core docs (opening summary, our work, cheatsheet)

**Files:** Create `README.md` (index; the artifact link is filled in during Task 7), `01-opening-summary.md`, `02-our-work-explained.md`, `05-cheatsheet.md`.

- [ ] **Step 1:** `01-opening-summary.md` has these sections: "The 2-minute opening" (280–320 words, first person plural, spoken style), "5 steps to memorize", "30-second fallback", "Hooks we want them to pick up" (3–4), and "Delivery tips (no notes allowed)".
- [ ] **Step 2:** `02-our-work-explained.md` has one section per item, each with a TL;DR, an ELI5, "what we actually showed" and "how we checked it". The items are the model, Claim 1, Claim 2, Claim 3, Example 1, E1–E6 and "what's new vs. prior work". It includes the Mermaid diagrams (a)–(e) from the spec.
- [ ] **Step 3:** `05-cheatsheet.md` contains a notation table (k, n, m, x, s, φ, c, b, p, r, r\*, ρ, x_crit, φ\*, S_k, K = k+1 core), a terms table (precipice, tipping point, k-core, corona, complex contagion, branching process, co-located/spread/pairs) and 8–10 one-line takeaways.
- [ ] **Step 4:** Verify. Run `wc -w` on the opening section (expected 280–320). Grep every number in the three files and confirm each appears in `paper.tex` or `results/summary.txt`, listing any that don't.
- [ ] **Step 5:** Commit: `Add opening summary, our-work explainer and cheatsheet`.

### Task 3: Paper explainers

**Files:** Create `03-papers/egl.md`, `cnst.md`, `dgm.md`, `prior-work.md`, `course-references.md`.

- [ ] **Step 1:** Fetch and read each source before writing about it: EGL (AER 2022 / arXiv 1909.10598), CNST (QJE 2021), DGM (PRL 2006 / cond-mat/0509102), PRA arXiv 2303.12660v4, AIS (Mgmt Sci 2017) and BFT (Ops Res 2018). For the course references, use known content plus a quick source check.
- [ ] **Step 2:** For each focus paper, write the sections TL;DR, ELI5, "What they did" (model, data, method), "Key result", one visual (Mermaid), "How we used it / how we differ", "Weaknesses we named" (quoting the submitted paper's points) and "Questions staff might ask" (3–4).
- [ ] **Step 3:** `prior-work.md` has the same sections, shortened, for each of the three papers, plus a comparison table (PRA / AIS / BFT / ours) with rows for sourcing rule, geography, network, result.
- [ ] **Step 4:** `course-references.md` has one card per reference: TL;DR, ELI5, and "where it shows up in our paper".
- [ ] **Step 5:** Commit: `Add explainers for the papers we used`.

### Task 4: Q&A bank

**Files:** Create `04-qa-bank.md`.

- [ ] **Step 1:** Write about 50 questions grouped under the headings A (questions and prior work), B (what we did), C (what we found), D (math), E (simulations), F (weaknesses and next steps), G (course connections), H ("explain it yourself") and I (curveballs). Each question uses the fixed format `### Q<id>. <question>` followed by `**Short:**`, `**If pushed:**` and optionally `★` for the most likely ones. Task 5 parses this format for flashcards.
- [ ] **Step 2:** Verify: `grep -c '^### Q' 04-qa-bank.md` gives a count between 45 and 60, and every question has both a Short and an If-pushed line.
- [ ] **Step 3:** Commit: `Add Q&A bank`.

### Task 5: Interactive study page

**Files:**
- Create: `tools/study_guide_template.html`, `tools/explorer.js` (DOM and SVG plots, uses `explorer_math.js` functions), `tools/build_study_guide.py`, `tools/render_check.py`
- Generated: `study-guide.html`

**Interfaces:**
- Consumes: Task 1 functions; Task 4's question format; the Markdown from Tasks 2–3.

- [ ] **Step 1:** Write `render_check.py` (Playwright). It loads `study-guide.html` at 1280×900 and 390×844, clicks every tab, and asserts: no console errors; every `.mermaid` node has rendered an SVG with no "Syntax error"; the Flashcards tab has as many cards as `^### Q` occurrences; the explorer's pairs preset shows a pairs φ* between 0.165 and 0.177 that is below both extremes; `scrollWidth <= clientWidth` at 390 px. It saves screenshots to the scratchpad.
- [ ] **Step 2:** Run it. Expected: fails (no page yet).
- [ ] **Step 3:** Build the page: the template, `explorer.js`, and `build_study_guide.py`. The build script strips `export` from the math module, embeds the Markdown files as `<script type="text/markdown" id=…>` blocks, and writes `study-guide.html`.
  - **Tabs:** Opening, Our work, Papers (sub-tabs per file), Flashcards (front = question, back = Short + If pushed; shuffle; "starred only" filter), Explorer, Cheatsheet.
  - **Theming:** color tokens on `:root` with a dark-mode override, and an explicit body background.
- [ ] **Step 4:** Run `python3 tools/build_study_guide.py && python3 tools/render_check.py`. Expected: all assertions pass. Look at the screenshots.
- [ ] **Step 5:** Commit: `Add interactive study guide with flashcards and model explorer`.

### Task 6: Verification and independent review

- [ ] **Step 1:** Recompute the trap-scan denominator. Using `model.py`, count the k≥2 settings in the scan grid where some c has φ\* > 0, and check that the count is 109 and the reversals are 72. If it differs, note it in `04-qa-bank.md` as a known discrepancy in the submitted paper, without changing the paper.
- [ ] **Step 2:** Dispatch a fresh reviewer, read-only. It checks every file against `paper.tex`, `results/` and the cited papers for errors, contradictions with the submitted paper, misattributions and unclear ELI5s, and checks that the opening covers all three handout topics.
- [ ] **Step 3:** Fix the findings, then rebuild and rerun Tasks 1, 4 and 5's checks.
- [ ] **Step 4:** Commit: `Address review of presentation prep`.

### Task 7: Delivery

- [ ] **Step 1:** Publish `study-guide.html` as a private artifact (icon "book"), put its link in `README.md`, rebuild and republish.
- [ ] **Step 2:** Create the branch `aryavardhan/presentation-prep` on GitHub from `2360e7f` and recreate the local commits through GraphQL `createCommitOnBranch` (Verified, authored by realAryavardhanSingh). After each commit, assert that the remote tree SHA equals the local one.
- [ ] **Step 3:** Confirm that `main` is unchanged and that the branch exists with the expected file list.
