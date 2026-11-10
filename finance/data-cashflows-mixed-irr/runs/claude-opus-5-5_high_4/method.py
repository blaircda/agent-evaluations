import csv

import numpy as np


def npv(rate, cfs):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs):
    # NPV(r) = sum cf_t * x^t with x = 1/(1+r); find real roots x > 0.
    coeffs = list(reversed(cfs))  # highest power first for np.roots
    roots = np.roots(coeffs)
    rates = []
    for x in roots:
        if abs(x.imag) < 1e-10 and x.real > 0:
            r = 1.0 / x.real - 1.0
            # refine with Newton's method
            for _ in range(100):
                f = npv(r, cfs)
                df = sum(-t * cf / (1 + r) ** (t + 1) for t, cf in enumerate(cfs))
                if df == 0:
                    break
                step = f / df
                r -= step
                if abs(step) < 1e-14:
                    break
            rates.append(r)
    if not rates:
        return None
    # If multiple IRRs exist, choose the one closest to zero.
    return min(rates, key=abs)


with open("data.csv", newline="") as f_in, open("results.csv", "w", newline="") as f_out:
    for row in csv.reader(f_in):
        if not row:
            continue
        cfs = [float(v) for v in row]
        r = irr(cfs)
        f_out.write(("%.6f" % r if r is not None else "NA") + "\n")
