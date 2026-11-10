import math

import numpy as np


def irr_candidates(cashflows):
    # NPV(v) = sum_t cf[t] * v**t, where v = 1/(1+r).
    # np.roots expects coefficients with the highest power first.
    roots = np.roots(cashflows[::-1])
    rates = []
    for z in roots:
        if abs(z.imag) < 1e-9 and z.real > 0:
            rates.append(1.0 / z.real - 1.0)
    return rates


def irr(cashflows):
    rates = irr_candidates(cashflows)
    if not rates:
        return float("nan")
    # If several real IRRs exist, report the one closest to zero.
    return min(rates, key=abs)


def main():
    with open("data.csv") as f_in, open("results.csv", "w") as f_out:
        for line in f_in:
            cashflows = [float(x) for x in line.strip().split(",")]
            r = irr(cashflows)
            if math.isnan(r):
                f_out.write("nan\n")
            else:
                f_out.write(f"{r:.6f}\n")


if __name__ == "__main__":
    main()
