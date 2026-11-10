import csv


def compute_irr(cashflows, tol=1e-12, max_iter=1000):
    low = -0.999999
    high = 1000.0

    def npv(rate):
        return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cashflows))

    for _ in range(max_iter):
        mid = (low + high) / 2.0
        val = npv(mid)
        if abs(val) < tol or (high - low) / 2.0 < tol:
            return mid
        if val > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main():
    with open("data.csv", "r", newline="") as infile, open(
        "results.csv", "w", newline=""
    ) as outfile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr = compute_irr(cashflows)
            outfile.write(f"{irr:.6f}\n")


if __name__ == "__main__":
    main()
