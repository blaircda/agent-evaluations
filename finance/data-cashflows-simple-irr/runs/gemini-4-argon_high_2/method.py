import csv


def calculate_irr(cashflows, tol=1e-12, max_iter=1000):
    r = 0.1
    for _ in range(max_iter):
        npv = sum(c / ((1.0 + r) ** t) for t, c in enumerate(cashflows))
        if abs(npv) < tol:
            break
        d_npv = sum(
            -t * c / ((1.0 + r) ** (t + 1))
            for t, c in enumerate(cashflows)
            if t > 0
        )
        r -= npv / d_npv
    return r


def main():
    results = []
    with open("data.csv", "r", newline="") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x.strip()) for x in row]
            irr = calculate_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w", newline="") as outfile:
        for res in results:
            outfile.write(f"{res}\n")


if __name__ == "__main__":
    main()
