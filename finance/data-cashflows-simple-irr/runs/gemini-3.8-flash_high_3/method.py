import csv
import numpy as np


def calculate_irr(cashflows):
    roots = np.roots(cashflows)
    real_roots = np.real(roots[np.isreal(roots)]) - 1
    valid_rates = real_roots[real_roots >= -1]
    return float(valid_rates[0])


def main():
    results = []
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cashflows = [float(val.strip()) for val in row if val.strip()]
            irr = calculate_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open('results.csv', 'w') as f:
        for val in results:
            f.write(f"{val}\n")


if __name__ == '__main__':
    main()
