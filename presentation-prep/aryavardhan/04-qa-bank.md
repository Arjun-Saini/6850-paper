# Q&A bank

> **TL;DR:** Likely staff questions, grouped by the handout's three topics plus math, simulations, weaknesses, course links, "explain it yourself"
> and curveballs. **★ = most likely.** Lead with the **Short** answer (one or two sentences, in your own words); use **If pushed** only when they dig.
> The staff won't ask for exact numbers, so answer with the *idea*.

How to drill: cover the answers, say yours out loud, then compare. On the study page, the Flashcards tab uses this file (with a "★ only" filter).

---

## A. Our questions and prior work

### QA1. What question does your paper ask, in one sentence? ★
**Short:** When do supply networks collapse suddenly, and how do two protections, having several suppliers per input and spreading them across regions, move that breaking point?
**If pushed:** Concretely: Q1, does needing k ≥ 2 working suppliers create a cliff even with one input? Q2, is it safer to spread suppliers or keep them together, and does that depend on k? Q3, when a region is hit, does its number of firms or its share of supply matter more?

### QA2. Why did you pick these three papers? ★
**Short:** EGL gives the theory of sudden collapse, CNST gives the best evidence of how a *regional* shock spreads through real supply links, and DGM explains abrupt collapse in k-cores, which is the same math as our model.
**If pushed:** None of the three is linked from the course page. EGL is the model we extend, CNST motivates the regional shock and our calibration (about five suppliers per firm), and DGM tells us what to expect when a node needs k neighbors.

### QA3. What is EGL's "precipice"?
**Short:** When firms need several inputs, reliability doesn't decline gradually as relationships weaken; it jumps from a healthy level to zero at a critical relationship strength.
**If pushed:** Reliability is the largest fixed point of R_x(r) = (1 − (1 − xr)^n)^m. For m ≥ 2 that curve is S-shaped, so as x falls the high crossing disappears at a tangency. They also show that firms investing in their own relationships end up just above that point, and a planner never would.

### QA4. What does CNST find, and how do they know it's causal?
**Short:** Firms linked to the 2011 disaster area, as suppliers or customers, grew several points more slowly, and the effect faded with network distance. A placebo network with randomly rewired links shows no effect.
**If pushed:** Difference-in-differences on roughly three-quarters of a million Japanese firms, comparing firms 1–4 links from the disaster area with firms 5+ links away. Their calibrated model says network links roughly doubled the GDP hit.

### QA5. What's a k-core, and why is DGM relevant to supply chains?
**Short:** It's what remains after repeatedly deleting nodes with fewer than k neighbors. For k ≥ 3 it vanishes with a jump under random damage, and our equation with one input has the same form as DGM's equation (binomial instead of Poisson).
**If pushed:** Our k corresponds to their K = k + 1 core: a core vertex needs k neighbors besides the one it was reached from, as our firm needs k suppliers below it. So DGM predicted our cliff for k ≥ 2.

### QA6. Hasn't someone already studied geographic diversification in supply networks? ★
**Short:** Yes, partly. Papachristou et al. study supply cascades with percolation and correlated failures, but one supplier suffices and regions are just a correlation parameter. Ang–Iancu–Swinney and Bimpikis–Fearing–Tahbaz-Salehi study three-tier chains.
**If pushed:** Bimpikis et al. show dual sourcing can backfire with S-shaped production. We get a similar backfire from the k-of-n rule alone, in a full cascading network with explicit regions. To our knowledge, regional pairs being worst network-wide is new, and so is the closed form for spread versus co-located.

### QA7. What's missing from the prior literature that you add?
**Short:** Two things: firms needing more than one working supplier per input, and disasters that knock out whole regions so that co-located suppliers fail together.
**If pushed:** EGL and DGM assume independent failures; CNST's model has no backup suppliers. Real firms dual-source because of capacity or policy, and real disasters are regional.

---

## B. What we did

### QB1. Describe your model in plain words. ★
**Short:** EGL's layered supply tree, where each firm needs m inputs and has n possible suppliers per input. We add that an input is only covered if at least k suppliers come through, and that disasters hit whole regions, where a firm's suppliers sit in c regional clusters.
**If pushed:** A supplier is usable if it works and the relationship works (probability x). Each region is hit with probability φ. Reliability r is the chance a firm works given that its own region survived, and it satisfies r = F(r) = (coverage)^m, where coverage depends on the geography.

### QB2. What does k mean, and why would a firm need more than one supplier?
**Short:** k is how many suppliers for an input must come through. Firms need more than one because of capacity limits (one supplier can't cover all demand) or deliberate dual-sourcing policies.
**If pushed:** EGL is the special case k = 1. Raising k is a different kind of fragility from raising m: you need more of the *same* input, not more inputs.

### QB3. How do you model a regional disaster, and what is c?
**Short:** Each region is hit independently with probability φ, which shuts every firm in it. A firm's n suppliers for an input form c clusters that each share a region: c = n is spread, c = 1 is co-located, and with n = 4, c = 2 is two pairs.
**If pushed:** Different clusters are (almost always) in different regions, so cluster survivals are independent.

### QB4. Why keep the tree structure?
**Short:** Because it gives one clean fixed-point equation we can prove things about, the same reason EGL and DGM use it.
**If pushed:** Random sparse graphs look locally tree-like, so the tree approximation is the standard mean-field analysis. Cycles are a known limitation, and we list them as future work.

### QB5. What is reliability r\*, and why the *largest* fixed point?
**Short:** It's the chance a firm in a deep network works (given its own region is fine). It's the largest solution of r = F(r), because starting from working suppliers at the bottom (r = 1) and applying F layer by layer converges to the largest solution.
**If pushed:** F is increasing, so iterating from 1 gives a decreasing sequence that stops at the first crossing it meets, which is the largest one. Zero is always a solution, so a positive one is what we care about.

### QB6. Why both math and simulations?
**Short:** The math is about infinitely deep trees. The simulations check that the same thresholds and behaviors show up in finite networks with real randomness, and they let us test things the math doesn't cover, like hub regions.
**If pushed:** We compare each run with 20 steps of the equation at the share of regions actually hit, and the two agree closely.

### QB7. How did you use AI, and what did you do yourselves?
**Short:** We used Claude to help edit drafts, write and test the simulation code, check proofs numerically, and format the paper. We chose the questions, reviewed the analysis, reran the code and checked every number. *(Make this true and specific for you.)*
**If pushed:** Be ready to explain any result from scratch. That's the point of this conversation.

---

## C. What we found

### QC1. What are your main findings? ★
**Short:** Needing two of anything makes collapse sudden; with one input, spread and co-located suppliers break at the same shock; with one required supplier, spreading never hurts; but with two required, two regional pairs can be the worst arrangement. Simulations confirm all of it.
**If pushed:** And for Q3: a region's share of supply matters much more than how many firms it holds.

### QC2. What's the most surprising result? ★
**Short:** That splitting suppliers across *two* regions can be worse than both putting them all in one region and spreading them all out, when firms need two suppliers.
**If pushed:** A firm that loses one pair is left with exactly two suppliers and needs both. Near the tipping point each works only about 60% of the time, so that "barely sourced" state is worse than the all-or-nothing outcome of co-location.

### QC3. So is spreading suppliers out always better?
**Short:** Fully spreading is never worse than co-locating (they tie with one input, and spreading wins with more). Partial spreading is the risky one: with k = 1 any finer split helps, but with k ≥ 2 an intermediate split like two pairs can be worst.
**If pushed:** In our grid search the reversal showed up in about two-thirds of the k ≥ 2 settings where some geography survives a shock, and never with k = 1. It's common, but it doesn't hold everywhere.

### QC4. Does a region's number of firms or its share of supply matter more?
**Short:** Supply share, by far. One region holding a big share of supply relationships but very few firms can collapse a k = 2 network on its own, while hitting many random regions rarely does.
**If pushed:** The theory matches once the shock is measured as the share of *supplier clusters* hit, not the share of firms. Heavy-tailed supplier popularity on its own barely matters, because a popular supplier is no more likely to fail.

### QC5. What's the practical takeaway?
**Short:** Simple "diversify across two regions" advice can backfire when firms need several suppliers per input. Exposure should be measured per input, by the share of suppliers in a region, not by distance to the disaster.
**If pushed:** It also says *where* cliffs should show up in data: firms left with fewer than k suppliers for some input.

### QC6. How robust is the pairs result?
**Short:** It's a numerical result of the model, solved precisely, and an exact formula explains it: the coverage difference sφ[2p² − S₂(4,p)] turns negative below p = 2/3, and at the pairs tipping point p is about 0.6. The simulations separate the thresholds clearly. But it isn't universal: it depends on n, k, m and x.
**If pushed:** For example, with two inputs, n = 4 and k = 2, the ordering is monotone (co-located < pairs < spread). We'd like a clean rule for when pairs are worst; that's an open question.

### QC7. How do you reconcile CNST's smooth evidence with your cliffs?
**Short:** They're compatible. CNST's model has smooth substitution and no shutdowns, so it can't produce a jump; their sample requires sales every year, which excludes exits; and a network far from its tipping point absorbs shocks smoothly anyway.
**If pushed:** Our model predicts where to look for a jump: per-input supplier exposure crossing the point where fewer than k survive.

---

## D. Math

### QD1. Sketch the proof that collapse is abrupt when k·m ≥ 2 (Claim 1). ★
**Short:** By a union bound, F(r) ≤ K·r^(km) ≤ K·r². So for small r, F(r) < r: there is no small positive fixed point. Reliability is either 0 or at least 1/K, and since it moves monotonically, it has to jump.
**If pushed:** K = C(n,k)^m. The union bound adds up the chance over every group of k suppliers that all of them are usable.

### QD2. Why does k = m = 1 fade smoothly instead?
**Short:** Near zero F(r) ≈ n·s·x·r, which is a branching process with mean n·s·x. Its survival probability grows continuously from 0 once the mean passes 1.
**If pushed:** That's E–K §21.8. The same as DGM's 2-core (ordinary percolation) behaving continuously.

### QD3. Why do spread and co-located suppliers break at the same shock with one input? ★
**Short:** Both cases reduce to the same equation u = a·G(u). Only the constant in front differs: a = s for spread and a = s^m for co-located. With one input those are equal.
**If pushed:** Spread: r = G(s·r); set u = s·r to get u = s·G(u). Co-located: r = s^m·G(r). A positive solution exists exactly when a is at least a cutoff a\* that depends only on G. Reliability differs, but the breaking point doesn't.

### QD4. Why does co-location hurt with several inputs?
**Short:** With co-located suppliers, each input has its own chance of being wiped out by its region, and the firm needs all m inputs, so it gets hit m times over.
**If pushed:** Formally φ\*_co = 1 − (1 − φ\*_spread)^(1/m), which is smaller. For two inputs the tolerable shock roughly halves.

### QD5. Why does spreading never hurt when k = 1 (Claim 3)?
**Short:** With k = 1 an input fails only if no supplier is usable, and splitting a cluster in two turns one big all-or-nothing bet into two smaller ones. By Jensen's inequality, that lowers the failure probability.
**If pushed:** A cluster of b gives nothing with probability φ + s·q^b, with q = 1 − x·r. Halving it gives (φ + s·q^(b/2))², and convexity of y² gives (φ + s·t)² ≤ φ + s·t². So F goes up, and so does its largest fixed point.

### QD6. Explain intuitively why pairs are worst. ★
**Short:** A paired firm often loses one pair and is left with exactly two suppliers, both of which must work. Near the tipping point suppliers are flaky, so that is a bad state. A co-located firm is either untouched with four suppliers or wiped out.
**If pushed:** The coverage gap is s·φ·[2p² − S₂(4,p)], with p = x·r. The bracket is negative when p < 2/3, and at the pairs tipping point p is only about 0.6.

### QD7. Where does the 2/3 come from?
**Short:** It's where 2p² equals S₂(4,p), the chance that at least 2 of 4 are usable. Below it, needing both of two is worse than needing two of four in an all-or-nothing region.
**If pushed:** S₂(4,p) = 1 − (1−p)⁴ − 4p(1−p)³. Setting it equal to 2p² and solving gives p = 2/3 (besides p = 0).

### QD8. What exactly is the connection to DGM's equation?
**Short:** With one input and spread suppliers, writing u = s·r gives u = s·S_k(n, x·u), the same form as DGM's u = p·P[Poisson(z·u) ≥ K − 1] with K = k + 1.
**If pushed:** Both say: a node survives if enough of the branches below it survive. Binomial instead of Poisson, and directed instead of undirected.

### QD9. What's the coverage formula for two pairs?
**Short:** s²·S_k(4, xr) + 2sφ·S_k(2, xr): both pairs survive (four candidates), or exactly one does (two candidates).
**If pushed:** In general, with c clusters of size b: the sum over j surviving clusters of C(c,j)·s^j·φ^(c−j)·S_k(j·b, x·r).

### QD10. Why is there a jump rather than a steep slope?
**Short:** Because the solution we're tracking, the high crossing of F with the diagonal, stops existing at a tangency. After that the only solution left is 0.
**If pushed:** Just above the threshold reliability is clearly positive (for example, about 0.74 for the one-input, two-supplier case at x_crit), and just below it's zero.

---

## E. Simulations

### QE1. What did you simulate, and why? ★
**Short:** Finite layered networks, with a bottom layer plus 20 layers of 20,000 firms each, spread over regions. Each firm draws random suppliers according to its cluster pattern; we hit regions and let failures cascade upward. The goal was to check that the deep-tree theory holds in finite random networks and to test hub regions.
**If pushed:** We compare each run with 20 steps of the equation at the share of regions actually hit in that run.

### QE2. Why compare with "20-layer theory" and not the infinite-depth result?
**Short:** A finite network has less depth for failures to build up, so its thresholds sit a bit higher. Twenty steps of the equation is the right comparison for a 20-layer network, and the simulations match it.
**If pushed:** The infinite-depth values are still the ones the claims are about; the gap between the two is a depth effect, not an error.

### QE2b. In Table 1, co-located and spread don't tie at 20 layers with one input. Doesn't that contradict Claim 2?
**Short:** No. Claim 2(b) is an infinite-depth statement, and there the two thresholds are identical. At 20 layers the two recursions differ slightly, and the simulations match each 20-layer value.
**If pushed:** Finite depth gives failures less room to build up, so both 20-layer thresholds sit a bit above the infinite-depth one; the small gap between them is a depth effect that shrinks as the network gets deeper.

### QE3. What does the bimodality experiment show? ★
**Short:** At the predicted threshold, k = 1 networks all fade to low reliability, while k = 2 networks split into two groups: collapsed or healthy, with little in between. That's what a cliff looks like in finite networks.
**If pushed:** Which group a run lands in tracks how many regions happened to be hit in that run, just above or below the 20-layer threshold.

### QE4. How did you measure tolerable shocks precisely?
**Short:** Using many small regions, we hit an exact number of them and found each network's tipping point by bisection. In a fixed network, hitting more regions can only hurt, so the tipping point is well defined.
**If pushed:** 2,000 regions of 10 firms, 40 networks per setting, median tipping point with a bootstrap interval. All 20 settings' intervals contain the 20-layer theory.

### QE5. What did the hub-region experiment show?
**Short:** A region that holds a large share of supply relationships but few firms can collapse a k = 2 network by itself, while hitting many random regions rarely does. What matters is supply share, not firm count.
**If pushed:** The theory fits once φ is measured as the share of supplier clusters hit (supply-weighted). Making some suppliers far more popular than others barely changed reliability.

### QE6. Why did you reproduce DGM's k-core thresholds?
**Short:** As a check on our tooling: our own pruning code on simulated 100,000-vertex random graphs finds every k-core vanishing close to DGM's predicted thresholds.
**If pushed:** It also shows the striking contrast: the 7-core disappears after removing only about 1.25% of vertices, while the giant component survives until about 90%. (It checks our pruning code; the network simulator is checked separately, against the 20-layer theory.)

### QE7. How do you know your code is right?
**Short:** Three ways: the simulations match an independent theory computation; our separate k-core pruning code matches the thresholds from DGM's equations; and an automated test suite checks every claim against the numerical recursion.
**If pushed:** We also made the results reproducible: fixed random seeds, and regenerating the figures gives identical files.

### QE8. What is a "supply-weighted" shock?
**Short:** The share of supplier clusters whose region was hit, rather than the share of firms hit. With hub regions those two can be very different.
**If pushed:** It's the quantity that enters the equation, because firms care about losing suppliers, not about how many firms live in the region.

---

## F. Weaknesses and next steps

### QF1. What's the biggest weakness of your model? ★
**Short:** Geography and sourcing are fixed: firms don't choose k, n or how to split suppliers across regions. And it's a tree, with no cycles.
**If pushed:** We also assume region hits are independent and all firms share the same k. The next steps target the first point directly.

### QF2. What would change with cycles or real network structure?
**Short:** Cycles create feedback and correlation between suppliers' failures that the tree ignores, so thresholds would likely shift. Whether the pairs reversal survives is open.
**If pushed:** DGM's analysis has the same mean-field limitation. Simulating on real or clustered networks would be the test.

### QF3. What's your final-project direction? ★
**Short:** Let firms choose how many suppliers and regions to use, at a cost, compute the equilibrium, and compare it with a planner's choice.
**If pushed:** In EGL, equilibrium bunches near the cliff even though a planner never would. We expect firms to under-diversify, and with k = 2 sometimes to choose pairs, the worst split.

### QF4. How would you test this with data?
**Short:** Use public OECD inter-country input–output tables, treating countries as regions, around the 2011 Thailand floods, and check whether industries' losses jump once their input share from the hit region passes some level, instead of growing in proportion.
**If pushed:** Per-input supplier exposure and firm exit would need firm-level data like CNST's, which is proprietary.

### QF5. Is k realistic? How would you measure it?
**Short:** It stands for capacity limits or dual-sourcing rules: if no single supplier can cover your volume, you need several. You'd estimate it from supplier shares or capacity per input.
**If pushed:** In practice k would differ by firm and input; a heterogeneous-k version is a natural extension.

### QF6. Why assume regions are hit independently?
**Short:** It's the simplest model of correlated failure: everything inside a region fails together, regions are independent. It isolates the effect of how suppliers are grouped.
**If pushed:** In the extreme where two regions are always hit together, they act as one cluster (lower c). Partial correlation between regions is outside our model.

---

## G. Course connections

### QG1. How does this connect to the course? ★
**Short:** It's a cascade on a network with a threshold rule (a firm fails when too few suppliers remain), analyzed like branching processes and random-graph k-cores, and it shows the course's simple-versus-complex contagion distinction.
**If pushed:** The k = m = 1 case is a branching process; needing several things is like a complex contagion; DGM's k-cores use the configuration model; protecting firms on a budget is like reverse influence maximization.

### QG2. How is your failure rule related to threshold models?
**Short:** It's Granovetter's / Easley–Kleinberg's threshold rule run in reverse: instead of adopting when enough neighbors adopt, a firm fails when fewer than k of its suppliers for some input remain.

**If pushed:** And with m ≥ 2 it behaves like a complex contagion (Centola–Macy): several things must go right at once.

### QG3. Where do branching processes come in?
**Short:** In the k = m = 1 case, each firm's survival depends on at least one of its suppliers surviving, which is exactly a branching process with mean n·s·x. That's why that case is smooth.
**If pushed:** With k or m ≥ 2 the process is no longer "linear" near zero, which is what breaks continuity.

### QG4. Where does influence maximization come in?
**Short:** As an open question: if you can protect a few firms, which ones minimize collapse? That's a reverse of choosing seeds to maximize spread (Kempe–Kleinberg–Tardos).
**If pushed:** Our AND-type failure structure may break the submodularity that makes greedy work there, so it's a genuinely different problem.

---

## H. "Explain it yourself" (checks that you understand without the paper)

### QH1. Explain the cliff to someone with no math background. ★
**Short:** Each firm needs its suppliers, which need theirs, and so on. If you need just one thing from one supplier and things go wrong a bit more often, output gets a bit worse. But if you need two things (two inputs, or two suppliers), small problems compound, and past a point the chain can't sustain itself: it goes from mostly working to not working at all.

**If pushed:** Use your hands: with one input, a gentle slope for k = 1, a drop-off for k = 2.

### QH2. Describe the fixed-point picture without drawing it.
**Short:** Plot "chance a firm works" against "chance its suppliers work". Reliability is where that S-shaped curve crosses the diagonal. A shock lowers the curve; when it only just touches the diagonal, one more push and the crossing is gone, so reliability falls to zero.
**If pushed:** That touching point is the tangency at x_crit or φ\*.

### QH3. Walk me through one firm's survival check.
**Short:** Is my region hit? If not, for each input: which of my supplier clusters' regions survived? Of the surviving suppliers, how many work and have a working relationship? If at least k, that input is covered. I work if all inputs are covered.
**If pushed:** In the equation that's coverage^m, with coverage a mix of binomial tails weighted by how many clusters survive.

### QH4. What happens when you change k from 1 to 2, and why?
**Short:** The tolerable shock shrinks a lot, and the transition goes from smooth to a cliff even with one input, because one lucky supplier is no longer enough. You now need two.
**If pushed:** In our two-input base case, the tolerable shock is more than five times smaller with k = 2.

---

## I. Curveballs

### QI1. Couldn't firms just hold inventory?
**Short:** Inventory isn't in the model. It would act as a buffer, roughly like stronger relationships, delaying collapse during short disruptions, but it doesn't remove the threshold structure.
**If pushed:** It would be a natural extension: time-varying shocks with buffers. Ang–Iancu–Swinney treat inventory as a direct mitigation tool.

### QI2. Why n = 4 and x = 0.9?
**Short:** n = 4 is close to the roughly five suppliers per firm in CNST's data, and x = 0.9 keeps the network above its critical strength in every case, so collapse comes from the regional shock and not from weak relationships.
**If pushed:** We also show n = 6, k = 3, where a similar reversal appears.

### QI3. Is the pairs result just a numerical artifact?
**Short:** No. There's an exact formula for the coverage difference and a clean reason for its sign (the 2/3 crossover). Simulations with tight intervals separate the pairs threshold from both extremes.
**If pushed:** The grid scan also shows it is common for k ≥ 2 and absent for k = 1, exactly as Claim 3 says.

### QI4. What result would prove you wrong?
**Short:** If real industries' losses grew smoothly with exposure even when per-input supplier exposure crossed the point where fewer than k survive, the threshold mechanism wouldn't be what drives real collapses.
**If pushed:** That's the point of the Thailand-floods test.

### QI5. What did you learn that you didn't expect?
**Short:** That "more diversified" isn't monotonically safer. Going from one region to two can hurt when firms need two suppliers, even though going all the way to four is fine. *(Say it in your own words.)*

**If pushed:** And that a regional shock on spread suppliers is mathematically just a weaker relationship strength, which made the closed form possible.

### QI6. If you had another month, what would you do first?
**Short:** The endogenous-geography game, to see whether firms actually choose the fragile pairs arrangement in equilibrium.
**If pushed:** Then a rule in (n, k, m, x) for exactly when pairs are worst, and a simulation on networks with cycles.
