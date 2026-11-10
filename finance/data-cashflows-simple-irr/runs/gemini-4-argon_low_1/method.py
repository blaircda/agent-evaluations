import csv


def compute_irr(cashflows, tol=1e-12, max_iter=1000):
    low, high = -0.999999, 100.0
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        npv = sum(cf / ((1.0 + mid) ** t) for t, cf in enumerate(cashflows))
        if abs(npv) < tol or (high - low) / 2.0 < tol:
            return mid
        if npv > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main():
    results = []
    with open("data.csv", "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr = compute_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w", newline="") as f:
        for res in results:
            f.write(res + "\n")


if __name__ == "__main__":
    main()
