"""Compute the IRR of each cashflow stream in data.csv and write results.csv.

NPV(r) = sum_t c_t / (1+r)^t. Substituting x = 1/(1+r) gives the polynomial
sum_t c_t x^t, whose real positive roots x correspond to IRRs r = 1/x - 1 > -1.
Each root is polished with Newton's method on NPV(r).

- One real IRR: report it.
- Several real IRRs: report the one closest to zero (numpy-financial convention).
- No real IRR: write "nan".
"""
import csv

import numpy as np


def npv(rate, cfs):
    return sum(c / (1 + rate) ** t for t, c in enumerate(cfs))


def dnpv(rate, cfs):
    return sum(-t * c / (1 + rate) ** (t + 1) for t, c in enumerate(cfs))


def polish(rate, cfs, iters=50):
    for _ in range(iters):
        d = dnpv(rate, cfs)
        if d == 0:
            break
        step = npv(rate, cfs) / d
        new = rate - step
        if new <= -1:
            break
        rate = new
        if abs(step) < 1e-15:
            break
    return rate


def irr(cfs):
    roots = np.roots(cfs[::-1])  # highest-degree coefficient first
    rates = []
    for x in roots:
        if abs(x.imag) < 1e-9 and x.real > 0:
            rates.append(polish(1.0 / x.real - 1.0, cfs))
    if not rates:
        return float("nan")
    return min(rates, key=abs)


def main():
    out = []
    with open("data.csv", newline="") as f:
        for row in csv.reader(f):
            if not row:
                continue
            cfs = [float(v) for v in row]
            r = irr(cfs)
            out.append("nan" if np.isnan(r) else f"{r:.6f}")
    with open("results.csv", "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
