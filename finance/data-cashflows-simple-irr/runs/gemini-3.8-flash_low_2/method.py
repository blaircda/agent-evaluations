import numpy as np

def calculate_irr(cashflows):
    # Let x = 1 / (1 + r).
    # Then sum_{t=0}^n C_t * x^t = 0.
    # In np.roots, coefficients are given from highest degree to lowest degree:
    # C_n * x^n + ... + C_1 * x + C_0 = 0
    # Thus, the polynomial coefficients are cashflows[::-1].
    roots = np.roots(cashflows[::-1])
    # We look for real roots where x > 0 (corresponding to r > -1)
    real_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
    if not real_roots:
        raise ValueError("No valid positive root found for IRR calculation.")
    # For standard cashflows starting with negative followed by positive values,
    # Descartes' Rule of Signs guarantees exactly one positive root.
    rate = 1.0 / real_roots[0] - 1.0
    return rate

def main():
    results = []
    with open("data.csv", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cashflows = [float(x) for x in line.split(",")]
            irr = calculate_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"{r}\n")

if __name__ == "__main__":
    main()
