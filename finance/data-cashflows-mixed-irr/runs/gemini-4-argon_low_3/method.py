import csv
import numpy_financial as npf


def main():
    with open("data.csv", "r", newline="") as infile, open(
        "results.csv", "w", newline=""
    ) as outfile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr_val = npf.irr(cashflows)
            outfile.write(f"{irr_val:.6f}\n")


if __name__ == "__main__":
    main()
