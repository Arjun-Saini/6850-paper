# Presentation prep (Aryavardhan)

Prep for the CS/INFO 6850 one-on-one presentation of our exploratory paper,
*Redundancy and Geography in Supply-Network Cascades* (submitted version: `main` at `2360e7f`).

**Format reminder:** 20 minutes, one staff member, no slides, notes or devices. We open with a short summary covering
(1) our questions and prior work, (2) what we did beyond it, and (3) what we found, each with the **math** and the **simulations**.
Staff grade whether we can explain the questions, methods and conclusions accurately in our own words. They don't ask for exact numbers.

**Interactive study page:** *(link added after publishing)*. It has the same content as these files, plus flashcards and a model explorer.
The same page is saved here as `study-guide.html`.

## Suggested study order

| # | File | What it's for | Time |
|---|---|---|---|
| 1 | [`01-opening-summary.md`](01-opening-summary.md) | **The only thing we say to staff unprompted.** A 2-minute opening, a 5-step outline to memorize, a 30-second fallback. | 15 min, then rehearse out loud |
| 2 | [`02-our-work-explained.md`](02-our-work-explained.md) | Our model, Claims 1–3, Example 1 and the simulations: TL;DR, ELI5, proof ideas, flow diagrams, plots | 40 min |
| 3 | [`03-papers/`](03-papers/) | Every paper we used: TL;DR + ELI5 + visual + how we used it | 40 min |
| 4 | [`04-qa-bank.md`](04-qa-bank.md) | ~50 likely questions with short and "if pushed" answers (★ = most likely) | drill out loud |
| 5 | [`05-cheatsheet.md`](05-cheatsheet.md) | Notation, vocabulary, ten takeaways | last look before going in |

## How to practise

1. Read 02 and the three focus-paper explainers once.
2. Say the opening out loud three times, *from the 5-step outline*, not the script.
3. Drill the ★ flashcards on the study page until you can answer each in two sentences.
4. Play with the model explorer: move k from 1 to 2 and watch the cliff appear, then load the "pairs" preset.
5. Swap roles with Arjun: one asks questions from the Q&A bank, the other answers without looking.

## Folder contents

- `figures/`: plots generated from `code/model.py` by `tools/make_prep_figures.py`
- `tools/`: explorer math (`explorer_math.js`) and its check against the Python model, the figure script, and the study-page builder
- `planning/`: the design spec and plan for this folder
