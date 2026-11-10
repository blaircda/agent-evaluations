import csv
import math
import numpy_financial as npf

def main():
    results = []
    with open("data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cashflows = [float(val) for val in row]
            rate = npf.irr(cashflows)
            if math.isnan(rate):
                results.append("")
            else:
                results.append(f"{rate:.6f}")

    with open("results.csv", "w", encoding="utf-8") as f:
        for val in results:
            f.write(f"{val}\n")

if __name__ == "__main__":
    main()
