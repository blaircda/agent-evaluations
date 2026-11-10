import csv

import numpy as np


def irr(cfs):
    # NPV = sum c_t * x^t with x = 1/(1+r); find real roots x > 0.
    roots = np.roots(cfs[::-1])
    rates = []
    for x in roots:
        if abs(x.imag) < 1e-9 and x.real > 0:
            rates.append(1.0 / x.real - 1.0)
    if not rates:
        return float("nan")
    # If multiple IRRs exist, choose the one closest to zero.
    return min(rates, key=abs)


with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        cfs = [float(x) for x in row if x.strip()]
        out.write(f"{irr(cfs):.6f}\n")
