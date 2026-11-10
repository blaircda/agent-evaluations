import csv
import numpy as np


def calculate_irr(values):
    """
    Calculate the Internal Rate of Return (IRR) for a sequence of cash flows.
    The IRR is the rate r such that sum_{t=0}^N values[t] / (1 + r)^t = 0.
    Letting g = 1 + r, this is equivalent to finding the roots of the polynomial:
    values[0] * g^N + values[1] * g^(N-1) + ... + values[N] = 0.
    """
    roots = np.roots(values)
    real_roots = roots[np.isreal(roots)].real
    rates = real_roots - 1
    valid_rates = rates[rates >= -1]
    if len(valid_rates) == 1:
        return float(valid_rates[0])
    elif len(valid_rates) > 1:
        # Standard numpy-financial selection logic: rate closest to zero
        return float(valid_rates[np.argmin(np.abs(valid_rates))])
    else:
        raise ValueError("No real solution found for IRR with rate >= -1.")


def main():
    with open("data.csv", mode="r", newline="") as infile:
        reader = csv.reader(infile)
        results = []
        for row in reader:
            if not row:
                continue
            cashflows = [float(x.strip()) for x in row]
            rate = calculate_irr(cashflows)
            results.append(f"{rate:.6f}")

    with open("results.csv", mode="w", newline="") as outfile:
        for r in results:
            outfile.write(f"{r}\n")


if __name__ == "__main__":
    main()
