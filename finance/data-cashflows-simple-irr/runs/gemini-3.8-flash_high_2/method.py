import csv

try:
    import numpy as np
except ImportError:
    np = None


def npv(rate, cash_flows):
    return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows))


def npv_prime(rate, cash_flows):
    return -sum(t * cf / ((1.0 + rate) ** (t + 1)) for t, cf in enumerate(cash_flows) if t > 0)


def calculate_irr(cash_flows):
    if np is not None:
        roots = np.roots(cash_flows)
        pos_real_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
        if pos_real_roots:
            return pos_real_roots[0] - 1.0

    # Fallback: Newton-Raphson method
    r = 0.1
    for _ in range(100):
        val = npv(r, cash_flows)
        if abs(val) < 1e-12:
            return r
        der = npv_prime(r, cash_flows)
        if der == 0:
            break
        r -= val / der
    return r


def main():
    results = []
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cash_flows = [float(x.strip()) for x in row if x.strip()]
            irr = calculate_irr(cash_flows)
            results.append(f"{irr:.6f}")

    with open('results.csv', 'w') as f:
        for res in results:
            f.write(f"{res}\n")


if __name__ == '__main__':
    main()
