import csv
from scipy.optimize import brentq


def npv(rate, values):
    return sum(val / ((1.0 + rate) ** t) for t, val in enumerate(values))


def calculate_irr(values):
    return brentq(lambda r: npv(r, values), -0.9999, 100.0)


def main():
    results = []
    with open("data.csv", mode="r", newline="") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            values = [float(x.strip()) for x in row]
            rate = calculate_irr(values)
            results.append(f"{rate:.6f}")

    with open("results.csv", mode="w", newline="") as outfile:
        for res in results:
            outfile.write(f"{res}\n")


if __name__ == "__main__":
    main()
