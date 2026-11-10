import csv
import math

import numpy as np


def irr(cashflows):
    """Return the per-period IRR (decimal) for one cashflow stream.

    NPV(r) = sum(cf_t / (1 + r)**t) is zero when x = 1/(1 + r) is a root of
    the polynomial sum(cf_t * x**t). Only real, positive roots give r > -1.
    If several IRRs exist, the one closest to zero is returned (the same
    convention as numpy_financial.irr). Returns NaN if no IRR exists.
    """
    roots = np.roots(cashflows[::-1])
    real_positive = [z.real for z in roots if abs(z.imag) < 1e-9 and z.real > 0]
    if not real_positive:
        return math.nan
    rates = [1.0 / x - 1.0 for x in real_positive]
    return min(rates, key=abs)


def main():
    with open("data.csv", newline="") as f:
        streams = [[float(v) for v in row] for row in csv.reader(f) if row]

    with open("results.csv", "w", newline="") as f:
        for cashflows in streams:
            rate = irr(cashflows)
            f.write("nan\n" if math.isnan(rate) else f"{rate:.6f}\n")


if __name__ == "__main__":
    main()
