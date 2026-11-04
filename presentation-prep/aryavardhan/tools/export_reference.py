"""Export reference values from code/model.py for checking the study page's model explorer.

Run from anywhere:  python3 export_reference.py   (writes explorer_reference.json next to this file)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "code"))
from model import largest_fixed_point, phi_star  # noqa: E402

rows = []
for k in (1, 2, 3):
    for m in (1, 2, 3):
        for n in (4, 6):
            for c in [d for d in range(1, n + 1) if n % d == 0]:
                for x in (0.6, 0.8, 0.9, 1.0):
                    rows.append({
                        "x": x, "m": m, "n": n, "k": k, "c": c,
                        "phi_star": phi_star(x, m, n, k, c),
                        "r_star_at": {f"{p:.2f}": largest_fixed_point(x, m, n, k, c, p) for p in (0.05, 0.15)},
                    })

with open(os.path.join(HERE, "explorer_reference.json"), "w") as f:
    json.dump(rows, f, indent=0)
print(f"wrote {len(rows)} reference rows")
