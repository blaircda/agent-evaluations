import csv

import numpy as np


def irr(cashflows):
    """IRR as the real root r > -1 of sum(cf_t / (1+r)^t) = 0.

    Roots are found via the polynomial in x = 1 + r:
    cf_0 x^n + cf_1 x^(n-1) + ... + cf_n = 0.
    If several valid roots exist, return the one closest to zero
    (same convention as numpy_financial.irr). If none exist, return NaN.
    """
    roots = np.roots(cashflows)
    rates = [x.real - 1 for x in roots if abs(x.imag) < 1e-9 and x.real > 0]
    if not rates:
        return float("nan")
    r = min(rates, key=abs)
    # Polish with a few Newton steps on NPV(r).
    t = np.arange(len(cashflows))
    cf = np.asarray(cashflows, dtype=float)
    for _ in range(50):
        npv = np.sum(cf / (1 + r) ** t)
        d = np.sum(-t * cf / (1 + r) ** (t + 1))
        if d == 0:
            break
        step = npv / d
        r -= step
        if abs(step) < 1e-15:
            break
    return r


with open("data.csv", newline="") as f:
    rows = [[float(v) for v in row] for row in csv.reader(f) if row]

with open("results.csv", "w", newline="") as f:
    for row in rows:
        f.write(f"{irr(row):.6f}\n")
