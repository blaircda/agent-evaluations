import csv
import numpy as np
from scipy.optimize import brentq


def npv(r, cfs):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))


def irr(cfs):
    # Roots of sum cf_t * x^t = 0 with x = 1/(1+r), keep real x > 0 (r > -1)
    roots = np.roots(cfs[::-1])
    cands = []
    for z in roots:
        if abs(z.imag) < 1e-9 and z.real > 0:
            cands.append(1 / z.real - 1)
    if not cands:
        return None
    # Polish each root, then pick the root closest to zero if several exist
    polished = []
    for r in cands:
        try:
            lo, hi = r - 1e-6, r + 1e-6
            if lo <= -1:
                lo = -1 + 1e-12
            polished.append(brentq(lambda q: npv(q, cfs), lo, hi, xtol=1e-14) if npv(lo, cfs) * npv(hi, cfs) < 0 else r)
        except Exception:
            polished.append(r)
    return min(polished, key=abs)


with open("data.csv", newline="") as f:
    rows = [[float(x) for x in row] for row in csv.reader(f) if row]

with open("results.csv", "w") as f:
    for cfs in rows:
        r = irr(cfs)
        f.write("" if r is None else f"{r:.6f}")
        f.write("\n")
