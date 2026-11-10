import csv
import numpy as np


def irr(cfs):
    # NPV = sum c_t x^t with x = 1/(1+r); find real positive roots x.
    rates = []
    for x in np.roots(cfs[::-1]):
        if abs(x.imag) < 1e-10 and x.real > 0:
            rates.append(1.0 / x.real - 1.0)
    if not rates:
        return float("nan")
    # If multiple IRRs exist, report the one closest to zero.
    return min(rates, key=abs)


with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        vals = [float(x) for x in row if x.strip()]
        if not vals:
            continue
        out.write(f"{irr(vals):.6f}\n")
