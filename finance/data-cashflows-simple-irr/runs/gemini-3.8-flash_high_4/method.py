import csv

try:
    import numpy as np

    def calculate_irr(cash_flows):
        roots = np.roots(cash_flows[::-1])
        real_pos = roots[np.isreal(roots) & (roots.real > 0)].real
        if len(real_pos) == 0:
            raise ValueError("No positive real root found.")
        rates = 1.0 / real_pos - 1.0
        return rates[np.argmin(np.abs(rates))]

except ImportError:
    def npv(r, values):
        return sum(v / ((1.0 + r) ** t) for t, v in enumerate(values))

    def npv_prime(r, values):
        return sum(-t * v / ((1.0 + r) ** (t + 1)) for t, v in enumerate(values))

    def calculate_irr(cash_flows, guess=0.1, max_iter=1000, tol=1e-12):
        r = guess
        for _ in range(max_iter):
            f = npv(r, cash_flows)
            f_prime = npv_prime(r, cash_flows)
            if abs(f_prime) < 1e-14:
                break
            r_next = r - f / f_prime
            if abs(r_next - r) < tol:
                return r_next
            r = r_next
        return r


def main():
    results = []
    with open("data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cash_flows = [float(x.strip()) for x in row if x.strip()]
            irr = calculate_irr(cash_flows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w", encoding="utf-8") as f:
        for val in results:
            f.write(f"{val}\n")


if __name__ == "__main__":
    main()
