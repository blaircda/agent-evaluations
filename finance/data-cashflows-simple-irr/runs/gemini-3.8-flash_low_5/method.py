import csv
import numpy as np


def irr(values):
    # Roots of polynomial sum_{t=0}^n values[t] * x^t where x = 1 / (1 + r)
    # np.roots expects coefficients in descending order of power: values[::-1]
    res = np.roots(values[::-1])
    # Find real, positive roots for x
    mask = (res.imag == 0) & (res.real > 0)
    if not mask.any():
        return np.nan
    res = res[mask].real
    rates = 1.0 / res - 1.0
    # Choose rate closest to 0
    rate = rates[np.argmin(np.abs(rates))]
    return rate


def main():
    results = []
    with open("data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cf = [float(x.strip()) for x in row]
            rate = irr(cf)
            results.append(f"{rate:.6f}")

    with open("results.csv", "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"{r}\n")


if __name__ == "__main__":
    main()
