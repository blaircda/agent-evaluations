import csv


def compute_irr(cashflows):
    low = 0.0
    high = 100.0

    def npv(rate):
        return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cashflows))

    for _ in range(200):
        mid = (low + high) / 2.0
        if npv(mid) > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main():
    with open("data.csv", "r", newline="") as infile, open("results.csv", "w", newline="") as outfile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr = compute_irr(cashflows)
            outfile.write(f"{irr:.6f}\n")


if __name__ == "__main__":
    main()
