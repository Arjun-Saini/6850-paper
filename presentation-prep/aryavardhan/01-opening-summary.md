# Opening summary (spoken, ~2 minutes, one speaker)

> **TL;DR:** Three papers, two protections, one equation, four results, three simulation tests.
> Say it like you're explaining it to a friend. Learn it as the five steps below, not word for word.

The handout asks the opening to cover three things, each with the math and the simulations:
**(1)** our questions and what prior work did, **(2)** what we did beyond it, and **(3)** what we found.
The marginal tags **[1] [2] [3]** show where each one is covered.

---

## The 2-minute opening

**[1]** Our paper asks when supply networks collapse *suddenly*, and how two protections firms use, buying each input from several suppliers and spreading them across regions, change that breaking point.

We built on three papers. Elliott, Golub and Leduc model supply chains as deep random trees. When firms need several inputs, output doesn't fade gradually; it falls off a cliff once supplier relationships get too weak. Carvalho and coauthors measure how the 2011 Japan earthquake spread through real supplier links and see smooth, fading spillovers. Dorogovtsev, Goltsev and Mendes show that k-cores of random graphs vanish abruptly, for the same mathematical reason. What none of them has is a firm that needs more than one working supplier per input, or a disaster that knocks out a whole region at once. So we asked three questions. Does needing two suppliers cause a cliff by itself? Is it safer to spread suppliers out or keep them together? And when a region is hit, does its number of firms matter more, or its supply?

**[2]** We extended the EGL model so that an input counts as covered only if at least *k* of its suppliers work, and a disaster shuts down every firm in a region. Reliability is still the largest fixed point of a single equation, so we could prove results.

**[3]** The math gives four results. Collapse is sudden whenever the number of suppliers needed times the number of inputs is at least two. With one input, spread and co-located suppliers break at the same shock. When one supplier is enough, spreading never hurts. But when firms need two, splitting suppliers into two regional pairs can be the *worst* option, because a firm that loses one pair is left barely sourced. In simulations of 420,000-firm networks, the thresholds matched the theory, the two-supplier networks split sharply into survivors and collapses, and hitting one supply-heavy region did far more damage than hitting many random ones.

*(≈ 315 words, about 2 minutes at a relaxed pace.)*

---

## Five steps to memorize (since notes aren't allowed)

Memory hook: **3 – 2 – 1 – 4 – 3**

| # | Step | Say this in one breath |
|---|---|---|
| 1 | **3 papers** | EGL = cliff in theory; CNST = smooth spread in the Japan data; DGM = k-cores vanish abruptly. |
| 2 | **2 protections we add** | needing *k* working suppliers per input; regional disasters that hit co-located suppliers together → Q1, Q2, Q3. |
| 3 | **1 equation** | reliability is the largest fixed point of r = F(r), so we can *prove* things. |
| 4 | **4 results** | cliff iff k·m ≥ 2 · spread = co-located with one input · k = 1: spreading never hurts · k = 2: pairs can be worst. |
| 5 | **3 simulation tests** | thresholds match theory · k = 2 splits into survive/collapse · supply share beats firm count. |

## 30-second fallback (if the staff member wants to jump straight to questions)

> We extended Elliott, Golub and Leduc's supply-network model so that firms need *k* working suppliers per input and disasters hit whole regions. We prove that needing two of anything makes collapse sudden, that spreading suppliers never hurts when one is enough, and, surprisingly, that when firms need two, splitting them into two regional pairs can be the worst arrangement. Large simulations match the theory, and they show that a region's share of supply matters much more than how many firms it holds.

## Hooks we *want* them to pick up

Each one leads to a question we can answer well.

- **"…the same mathematical reason as k-cores."** Leads to DGM, and how our k maps to their K = k + 1 core. See `03-papers/dgm.md`.
- **"…left barely sourced."** Leads to the explanation of why pairs are worst (the 2/3 crossover). See `02-our-work-explained.md` § Example 1.
- **"…CNST see smooth spillovers."** Leads to why that is *consistent* with a cliff: their model can't produce one, their sample needs sales every year, and a network far from its tipping point also looks smooth.
- **"…supply share beats firm count."** Leads to the hub-regions experiment and what it means for measuring exposure.

## Delivery tips (no notes, no devices)

- **Talk to the person, not at them.** It's a conversation, so pause after step 2 or step 4 if they look ready to ask something.
- **Use your hands for the cliff:** a slope for k = 1 and a sudden drop for k = 2. It's memorable and it's accurate.
- **Use words, not numbers.** The staff won't ask for exact values. Say "about five times smaller" or "pairs break first", not "0.171".
- **If you blank, go back to the equation:** "everything comes from one fixed-point equation r = F(r)". Every result follows from it.
- **Own the AI question:** we used Claude for editing, code and numerical checks, and we can explain every result ourselves. That is what this conversation is for.
