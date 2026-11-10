import csv
import numpy as np


def irr(cashflows):
    # NPV(r) = sum c_t * x^t with x = 1/(1+r); find real roots x > 0 (i.e. r > -1).
    roots = np.roots(cashflows[::-1])
    rates = [1.0 / x.real - 1.0 for x in roots if abs(x.imag) < 1e-10 and x.real > 0]
    if not rates:
        return float("nan")
    # If multiple IRRs exist, pick the one closest to zero (numpy_financial convention).
    return min(rates, key=abs)


with open("data.csv", newline="") as f:
    rows = [[float(v) for v in row] for row in csv.reader(f) if row]

with open("results.csv", "w") as f:
    for cf in rows:
        r = irr(cf)
        f.write(("nan" if np.isnan(r) else f"{r + 0.0:.6f}") + "\n")
