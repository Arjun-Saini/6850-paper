# Citations for §2 Related work (A2)

Checked Nov 17, 2026. BibTeX is in `final/track_a/refs_track_a.bib`; it moves to `final/paper/` once the layout is agreed. Bibliographic details (authors, title, journal, volume, issue, pages, year) come from each DOI's Crossref record, or from the CiNii catalog for the book. What each paper claims comes from its abstract, read on the page linked.

**Result.** All four [VERIFY] references in plan.md §6 exist as cited, and their abstracts support using them. Two of plan.md's one-line summaries need rewording, because the abstracts don't say what plan.md says (see the Wagner and Ibragimov et al. rows). Two reliability references were added: Kuo & Zuo is verified. For Bai, Yun & Chung, the details are verified but the content claim is not (see the Bai et al. row).

## The [VERIFY] list from plan.md §6

| Key | Reference | What the abstract supports | Status |
|---|---|---|---|
| `aot2015` | Acemoglu, Ozdaglar, Tahbaz-Salehi, *AER* 105(2):564–608, 2015 ([doi](https://doi.org/10.1257/aer.20130456)) | A phase transition: denser interconnection makes the system more stable while shocks are small, and more fragile beyond a point. Abstract read in its Crossref record. | Verified. plan.md's summary is accurate. |
| `battiston2012` | Battiston, Delli Gatti, Gallegati, Greenwald, Stiglitz, *JEDC* 36(8):1121–1141, 2012 ([IDEAS](https://ideas.repec.org/a/eee/dyncon/v36y2012i8p1121-1141.html)) | A financial network can be most resilient at intermediate risk diversification, not at maximal diversification, when a financial accelerator is present. | Verified. Closest in spirit to our non-monotonicity in c. |
| `wagner2010` | Wagner, *J. Financial Intermediation* 19(3):373–386, 2010 ([IDEAS](https://ideas.repec.org/a/eee/jfinin/v19y2010i3p373-386.html)) | Diversification lowers each institution's own probability of failure but makes systemic crises more likely. When crises carry extra costs, full diversification is not optimal. | Verified. Reword: plan.md's "makes failures coincide" is the mechanism, not the abstract's wording. Say "makes systemic crises more likely". |
| `ijw2011` | Ibragimov, Jaffee, Walden, *J. Financial Economics* 99(2):333–348, 2011 ([IDEAS](https://ideas.repec.org/a/eee/jfinec/v99y2011i2p333-348.html)) | Diversification that is optimal for each intermediary can be suboptimal for society. The externality depends on the distribution of risks, and the paper gives exact conditions under which restricting risk-sharing is better. | Verified, but optional per plan.md. Reword: "heavy tails" is not in the abstract. Say "depending on the distribution of risks". |

## Reliability: k-out-of-n systems and common-cause failure

| Key | Reference | Use | Status |
|---|---|---|---|
| `kuozuo2003` | Kuo & Zuo, *Optimal Reliability Modeling: Principles and Applications*, Wiley, Hoboken, 2003, ISBN 047139761X ([CiNii record](https://ci.nii.ac.jp/ncid/BA60879982)) | The standard reference for the k-out-of-n model: "an input is covered if k of n suppliers work" is a k-out-of-n:G system. | Details verified. Bookseller listings put the k-out-of-n model in chapters 7–8, but the catalog shows no table of contents. Cite the book without chapter numbers unless someone checks a copy. |
| `byc1991` | Bai, Yun, Chung, *IEEE Trans. Reliability* 40(1):56–59, 1991 ([doi](https://doi.org/10.1109/24.75334)) | Redundancy in a k-out-of-n system with common-cause failures. Reportedly, the number of redundant units that minimizes the mean cost rate is finite and unique. | Details verified (Crossref). **Content [VERIFY]:** the IEEE and KAIST pages could not be fetched, and Semantic Scholar has no abstract. The content claim comes only from a search-result summary. Check the abstract on IEEE Xplore (Cornell access) before using it for anything beyond "k-out-of-n systems with common-cause failures". |

A fallback if Bai et al. can't be checked is Chae & Clark, "System reliability in the presence of common-cause failures," *IEEE Trans. Reliability* 35(1):32–35, 1986 ([doi](https://doi.org/10.1109/TR.1986.4335336)). Its details are verified on Crossref; its content is not.

## Positioning sentence for §2 (draft)

Diversification that helps each unit but can hurt the system is known in financial networks. There, resilience can peak at intermediate diversification (Battiston et al. 2012), dense links help against small shocks but spread large ones (Acemoglu, Ozdaglar and Tahbaz-Salehi 2015), and diversification makes systemic crises more likely even as individual failures fall (Wagner 2010). In reliability engineering, the k-of-n coverage rule is a k-out-of-n system (Kuo and Zuo 2003), and common-cause failures are the reliability analogue of regional shocks.

Our contribution is the supply-network geography version, with an explicit single-firm window (Lemma A) and the reduction to the network's tipping point (Theorem B).

## Not re-checked here

The references already in the exploratory paper were not part of A2, since plan.md does not flag them: EGL 2022, CNST 2021, DGM 2006, Ang–Iancu–Swinney 2017, Bimpikis–Fearing–Tahbaz-Salehi 2018, Papachristou–Rahimian–Azadegan, Centola–Macy, Granovetter, Easley–Kleinberg, KKT 2003 and Kleinberg 2007. They should get the same Crossref check before the final pass (W6).
