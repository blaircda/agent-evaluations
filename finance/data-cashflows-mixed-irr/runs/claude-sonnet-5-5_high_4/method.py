import csv
import numpy as np


def irr(cfs):
    # NPV(r) = sum cf_t / (1+r)^t. With x = 1/(1+r): polynomial in x. Find real roots with x > 0.
    coeffs = cfs[::-1]  # highest power first: cf_n x^n ... cf_0
    # strip leading zeros
    while len(coeffs) > 1 and coeffs[0] == 0:
        coeffs = coeffs[1:]
    if len(coeffs) < 2:
        return None
    roots = np.roots(coeffs)
    rates = []
    for x in roots:
        if abs(x.imag) < 1e-9 and x.real > 0:
            rates.append(1.0 / x.real - 1.0)
    if not rates:
        return None
    # if multiple, choose the one closest to zero
    return min(rates, key=abs)


with open("data.csv", newline="") as f:
    rows = [[float(v) for v in r] for r in csv.reader(f) if r]

with open("results.csv", "w") as f:
    for r in rows:
        v = irr(r)
        f.write("" if v is None else f"{v:.6f}")
        f.write("\n")
