import math

import numpy as np


def irr(cashflows):
    """Return the IRR closest to zero, or NaN if no real IRR exists.

    The IRR r solves sum_t cf_t / (1 + r)**t = 0. Substituting x = 1/(1 + r)
    turns this into a polynomial in x with coefficients cf_t, so its real
    positive roots x give real rates r = 1/x - 1 with r > -1.
    """
    coeffs = np.array(cashflows, dtype=float)[::-1]  # highest power first
    rates = []
    for z in np.roots(coeffs):
        if abs(z.imag) <= 1e-9 * max(1.0, abs(z.real)) and z.real > 0:
            rates.append(1.0 / z.real - 1.0)
    if not rates:
        return math.nan
    return min(rates, key=abs)


def main():
    results = []
    with open('data.csv', newline='') as f:
        for line in f:
            cashflows = [float(x) for x in line.strip().split(',')]
            r = irr(cashflows)
            results.append('NaN' if math.isnan(r) else f'{r:.6f}')
    with open('results.csv', 'w', newline='') as f:
        f.write('\n'.join(results) + '\n')


if __name__ == '__main__':
    main()
