"""Regenerate every Track A result in ../results (about 7 minutes; claim3_refinement.py is most of it).

Usage:  python3 run_all.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["lemma_a_n4k2.py", "claim3_refinement.py", "theorem_b_base_case.py", "lemma_a_general.py", "large_n.py"]

for script in SCRIPTS:
    print(f"== {script}", flush=True)
    subprocess.run([sys.executable, os.path.join(HERE, script)], check=True, cwd=HERE, stdout=subprocess.DEVNULL)
print("done")
