import numpy as np


def compute_irr(cashflows):
    # Let x = 1 / (1 + r).
    # Then NPV = sum_{t=0}^n cashflows[t] * x^t = 0.
    # np.roots expects polynomial coefficients in descending order of powers.
    # So the polynomial is sum_{t=0}^n cashflows[t] * x^t = cashflows[n]*x^n + ... + cashflows[0].
    # Thus the coefficients array is cashflows[::-1].
    coeffs = cashflows[::-1]
    roots = np.roots(coeffs)
    real_positive_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
    if not real_positive_roots:
        raise ValueError("No positive real root found.")
    # For standard cashflows, there is one unique positive root
    x = real_positive_roots[0]
    r = 1.0 / x - 1.0
    return r


def main():
    results = []
    with open("data.csv", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cashflows = [float(x) for x in line.split(",")]
            irr = compute_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w") as f:
        for val in results:
            f.write(f"{val}\n")


if __name__ == "__main__":
    main()
