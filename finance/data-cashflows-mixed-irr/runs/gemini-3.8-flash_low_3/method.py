import csv
import numpy_financial as npf

def main():
    results = []
    with open("data.csv", mode="r", newline="") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x.strip()) for x in row]
            rate = npf.irr(cashflows)
            results.append(rate)

    with open("results.csv", mode="w", newline="") as outfile:
        for rate in results:
            outfile.write(f"{rate:.6f}\n")

if __name__ == "__main__":
    main()
