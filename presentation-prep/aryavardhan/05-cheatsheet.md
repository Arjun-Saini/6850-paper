# Cheatsheet

> **TL;DR:** The symbols, the vocabulary, and the ten takeaways. If you can explain every row here in your own words, you're ready.

## Notation

| Symbol | Meaning | Plain words |
|---|---|---|
| m | essential inputs per firm | how many different things a firm must buy |
| n | potential suppliers per input | how many places it can buy each thing from |
| **k** | suppliers needed per input | how many of those must actually come through (EGL: k = 1) |
| x | relationship strength | chance a given supplier deal works |
| φ | regional shock size | chance any given region is hit by a disaster |
| s = 1 − φ | survival | chance a region is *not* hit |
| **c** | number of supplier clusters per input | c = n spread · c = 2 pairs (n = 4) · c = 1 co-located |
| b = n/c | cluster size | suppliers that share one region |
| p = x·r | usable chance | a surviving supplier works *and* its deal works |
| S_k(N, p) | binomial tail | chance at least k of N independent suppliers are usable |
| r, F(r) | reliability, recursion | r = chance a firm works (own region OK); r = F(r) is eq. (2) |
| **r\*** | deep-network reliability | the **largest** solution of r = F(r) |
| ρ = s·r\* | share of all firms working | includes firms whose own region was hit |
| **x_crit** | critical strength | weakest x where r\* > 0 with no shock |
| **φ\*** | tolerable shock | biggest φ where r\* > 0 |
| K = k + 1 | DGM core index | our k-of-n rule ↔ DGM's (k+1)-core |

## Vocabulary

| Term | Meaning |
|---|---|
| **Precipice / cliff** | reliability jumps from a healthy value straight to 0 (a discontinuous, "first-order" transition). |
| **Tipping point** | the x or φ where the jump happens (x_crit, φ\*). |
| **Fixed point** | where F(r) = r; reliability is the largest one. A tangency is where the high one disappears. |
| **Branching process** | the k = m = 1 case: like a family tree that survives if each firm has > 1 working supplier on average. Smooth transition. |
| **k-core** | what's left after repeatedly deleting vertices with fewer than k neighbors (DGM). |
| **Corona** | core vertices with *exactly* k core neighbors; one more loss and they drop out (DGM 2006 describes them; the name is from the same authors' follow-up). Our "barely sourced" firms are the analogue. |
| **Complex contagion** | Centola–Macy: adoption needs several contacts, not one. Our m ≥ 2 or k ≥ 2 failure rule is the reverse. |
| **Threshold model** | Granovetter / Easley–Kleinberg §19.2: act when enough neighbors act. Our firms *fail* when too few suppliers remain. |
| **Spread / pairs / co-located** | all suppliers in different regions / two regions with two suppliers each / all in one region. |
| **Supply-weighted shock** | the share of *supplier clusters* hit, not the share of firms. This is what predicts collapse with hub regions. |
| **Difference-in-differences** | CNST's method: compare how firms linked to the disaster area changed versus similar firms that weren't linked. |

## Ten takeaways (say them in words, no numbers needed)

1. Needing **two of anything** (inputs or suppliers per input) turns gradual decline into a **cliff** (Claim 1).
2. The new case is **one input, two required suppliers**: EGL needed several inputs for a cliff, and we don't.
3. Spreading suppliers out is mathematically **the same as weakening every relationship** (Claim 2a).
4. With **one input**, spread and co-located suppliers break at **the same shock** (Claim 2b).
5. With **several inputs**, co-location breaks earlier, because each input can be wiped out separately.
6. If **one supplier is enough**, splitting regions further **never hurts** (Claim 3, Jensen).
7. If firms need **two**, **two regional pairs can be the worst** arrangement: losing one pair leaves firms barely sourced (Example 1).
8. Partial diversification can **backfire**, so "split across two regions" is not automatically safe advice.
9. Simulations on 420,000-firm networks **match the theory**; k = 2 networks **split** into survivors and collapses.
10. What matters about a hit region is its **share of supply, not its number of firms**, so exposure should be measured by suppliers per input.
