import csv

import numpy as np


def irr(cashflows):
    """IRR as the real root r > -1 of sum(c_t / (1+r)^t) = 0.

    Multiplying through by (1+r)^n gives a polynomial in x = 1+r with
    coefficients c_0, c_1, ..., c_n (highest power first). Only real roots
    with x > 0 (r > -1) are valid. If several exist, the one closest to zero
    is returned (numpy-financial convention); if none exist, NaN is returned.
    """
    roots = np.roots(cashflows)
    candidates = []
    for x in roots:
        if abs(x.imag) < 1e-9 and x.real > 0:
            r = x.real - 1.0
            # Polish the root with Newton's method on the NPV function.
            for _ in range(50):
                t = np.arange(len(cashflows))
                disc = (1.0 + r) ** -t
                npv = np.dot(cashflows, disc)
                d_npv = np.dot(cashflows, -t * disc / (1.0 + r))
                if d_npv == 0:
                    break
                step = npv / d_npv
                r -= step
                if abs(step) < 1e-15:
                    break
            candidates.append(r)
    if not candidates:
        return float("nan")
    return min(candidates, key=abs)


def main():
    with open("data.csv", newline="") as f:
        rows = [row for row in csv.reader(f) if row]
    with open("results.csv", "w", newline="") as f:
        for row in rows:
            cashflows = np.array([float(v) for v in row])
            value = irr(cashflows)
            f.write(("nan" if np.isnan(value) else f"{value:.6f}") + "\n")


if __name__ == "__main__":
    main()
