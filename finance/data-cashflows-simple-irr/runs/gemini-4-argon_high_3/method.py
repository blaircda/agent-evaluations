import csv


def compute_irr(cashflows, tol=1e-15, max_iter=200):
    low = -0.999999
    high = 1000.0
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        if (high - low) / 2.0 < tol:
            return mid
        npv = sum(cf / ((1.0 + mid) ** t) for t, cf in enumerate(cashflows))
        if npv > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main():
    results = []
    with open("data.csv", "r", newline="") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr = compute_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w", newline="") as outfile:
        for res in results:
            outfile.write(res + "\n")


if __name__ == "__main__":
    main()
