# Opening summary (spoken, ~2 minutes, one speaker)

> **TL;DR:** Three papers, two things we add, one equation, four results (three proved claims and one worked example), three simulation tests.
> Say it like you're explaining it to a friend. Learn it as the five steps below, not word for word.

The handout asks the opening to cover three things, each with the math and the simulations:
**(1)** our questions and what prior work did, **(2)** what we did beyond it, and **(3)** what we found.
The marginal tags **[1] [2] [3]** show where each one is covered.

---

## The 2-minute opening

**[1]** Our paper asks when supply networks collapse *suddenly*, and how two protections firms use, buying each input from several suppliers and spreading them across regions, change that breaking point.

We built on three papers. Elliott, Golub and Leduc model supply chains as deep random trees: when firms need several inputs, output falls off a cliff once relationships get too weak. Carvalho and coauthors measure how the 2011 Japan earthquake spread through supplier–customer links, and see smooth, fading spillovers. Dorogovtsev, Goltsev and Mendes show that k-cores of random graphs vanish abruptly once k is three or more, for the same mathematical reason; our own pruning code matches their thresholds in simulation. What's missing is a firm that needs more than one working supplier per input, and a model where a regional disaster takes out co-located backup suppliers together. So we asked: does needing two suppliers cause a cliff by itself? Is spreading suppliers out safer than keeping them together? And does a hit region's firm count matter more, or its supply?

**[2]** We extended EGL so an input counts as covered only if at least *k* of its suppliers are usable, and a disaster shuts every firm in a region, with suppliers grouped into regional clusters. Reliability is still the largest fixed point of one equation, so we could prove results, and we simulated layered 420,000-firm networks to test them.

**[3]** We proved three results and found one example. Collapse is sudden whenever suppliers needed times inputs is at least two. With one input, spread and co-located suppliers break at the same shock. When one supplier is enough, spreading never hurts. But when firms need two, two regional pairs can be the *worst* option, because a firm that loses one pair is left barely sourced. In the simulations, thresholds matched the theory, two-supplier networks split sharply into survivors and collapses, and hitting one supply-heavy region did far more damage than many random ones.

*(≈ 320 words, about 2 minutes at a relaxed pace.)*

---

## Five steps to memorize (since notes aren't allowed)

Memory hook: **3 – 2 – 1 – 4 – 3**

| # | Step | Say this in one breath |
|---|---|---|
| 1 | **3 papers** | EGL = cliff in theory; CNST = smooth spread in the Japan data; DGM = k-cores (k ≥ 3) vanish abruptly. |
| 2 | **2 things we add to EGL** | needing *k* working suppliers per input; regional disasters that hit co-located suppliers together → Q1, Q2, Q3. |
| 3 | **1 equation** | reliability is the largest fixed point of r = F(r), so we can *prove* things. |
| 4 | **4 results** (3 proved + 1 example) | cliff iff k·m ≥ 2 · spread = co-located with one input · k = 1: spreading never hurts · *example*: k = 2, pairs can be worst. |
| 5 | **3 simulation tests** | thresholds match theory · k = 2 splits into survive/collapse · supply share beats firm count. |

## 30-second fallback (if the staff member wants to jump straight to questions)

> We extended Elliott, Golub and Leduc's supply-network model so that firms need *k* working suppliers per input and disasters hit whole regions. We prove that needing two of anything makes collapse sudden and that spreading suppliers never hurts when one is enough, and we show, surprisingly, that when firms need two, splitting them into two regional pairs can be the worst arrangement. Large simulations match the theory, and they show that a region's share of supply matters much more than how many firms it holds.

## Hooks we *want* them to pick up

Each one leads to a question we can answer well.

- **"…the same mathematical reason as k-cores."** Leads to DGM, and how our k maps to their K = k + 1 core. See `03-papers/dgm.md`.
- **"…left barely sourced."** Leads to the explanation of why pairs are worst (the 2/3 crossover). See `02-our-work-explained.md` § Example 1.
- **"…CNST see smooth spillovers."** Leads to why that is *consistent* with a cliff: their model can't produce one, their sample needs sales every year, and a network far from its tipping point also looks smooth.
- **"…supply share beats firm count."** Leads to the hub-regions experiment and what it means for measuring exposure.

## Delivery tips (no notes, no devices)

- **Talk to the person, not at them.** It's a conversation, so pause after step 2 or step 4 if they look ready to ask something.
- **Use your hands for the cliff:** with one input, a slope for k = 1 and a sudden drop for k = 2. It's memorable and it's accurate.
- **Use words, not numbers.** The staff won't ask for exact values. Say "about five times smaller" or "pairs break first", not "0.171".
- **If you blank, go back to the equation:** "everything comes from one fixed-point equation r = F(r)". Every result follows from it.
- **Own the AI question:** we used Claude for editing, code and numerical checks, and we can explain every result ourselves. That is what this conversation is for.
