"""Checks for the prep docs. Run from anywhere: python3 check_docs.py [--no-mermaid]

1. The spoken opening is 280-320 words.
2. Every multi-digit number in the docs appears in paper.tex or results/summary.txt (or is a known derived value).
3. Every ```mermaid block renders with mmdc (skip with --no-mermaid).
4. Q&A bank format: 45-60 questions, each with **Short:** and **If pushed:** (skipped if the file doesn't exist yet).
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(PREP, "..", ".."))
DERIVED = {"420,000": "21 layers x 20,000 firms (paper Sec. 7 setup)",
           "110": "trap-scan recheck: k>=2 settings with some phi* > 0 (Task 6)", "0.001": "tolerance used in that recheck"}
DOCS = sorted(glob.glob(os.path.join(PREP, "*.md")) + glob.glob(os.path.join(PREP, "03-papers", "*.md")))
# Paper explainers quote the source papers' own numbers; those are checked against the sources, not our paper.
OUR_DOCS = [d for d in DOCS if "03-papers" not in d and not d.endswith("README.md")]
fails = []

# 1. opening length
t = open(os.path.join(PREP, "01-opening-summary.md")).read()
m = re.search(r"## The 2-minute opening\n(.*?)\n\*\(≈", t, re.S)
words = len(re.sub(r"\*\*\[[123]\]\*\*|^---$", "", m.group(1), flags=re.M).split()) if m else 0
if not 280 <= words <= 320:
    fails.append(f"opening is {words} words (want 280-320)")

# 2. numbers
src = open(os.path.join(REPO, "paper.tex")).read() + open(os.path.join(REPO, "results", "summary.txt")).read()
for path in OUR_DOCS:
    body = open(path).read()
    for num in sorted(set(re.findall(r"(?<![\w.])\d[\d,]*\.?\d*%?", body))):
        core = num.rstrip("%").rstrip(".")
        if len(core) < 2 or core in DERIVED:
            continue
        if core not in src and core.replace(",", "{,}") not in src:
            fails.append(f"{os.path.relpath(path, PREP)}: number {num} not in paper.tex/summary.txt")

# 3. mermaid
n_blocks = 0
if "--no-mermaid" not in sys.argv:
    for path in DOCS:
        for i, block in enumerate(re.findall(r"```mermaid\n(.*?)```", open(path).read(), re.S)):
            n_blocks += 1
            d = tempfile.mkdtemp()
            open(os.path.join(d, "in.mmd"), "w").write(block)
            r = subprocess.run(["mmdc", "-i", os.path.join(d, "in.mmd"), "-o", os.path.join(d, "o.svg"), "-q"],
                               capture_output=True, text=True)
            if r.returncode:
                fails.append(f"{os.path.relpath(path, PREP)}: mermaid block {i} fails: {(r.stderr or r.stdout)[-200:]}")

# 4. Q&A format
qa = os.path.join(PREP, "04-qa-bank.md")
n_q = 0
if os.path.exists(qa):
    parts = re.split(r"^### Q", open(qa).read(), flags=re.M)[1:]
    n_q = len(parts)
    if not 45 <= n_q <= 60:
        fails.append(f"Q&A has {n_q} questions (want 45-60)")
    for p in parts:
        if "**Short:**" not in p or "**If pushed:**" not in p:
            fails.append("Q&A item missing Short/If pushed: Q" + p.split("\n")[0][:60])

if fails:
    print(f"FAIL {len(fails)}")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print(f"OK opening={words} words, docs={len(DOCS)}, mermaid={n_blocks}, questions={n_q}")
