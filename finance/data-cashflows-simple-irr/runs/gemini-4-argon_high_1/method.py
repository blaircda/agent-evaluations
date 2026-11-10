import csv


def calculate_irr(cashflows):
    low = -0.999999999
    high = 1000.0
    for _ in range(200):
        mid = (low + high) / 2.0
        npv = sum(cf / ((1.0 + mid) ** t) for t, cf in enumerate(cashflows))
        if npv > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main():
    with open("data.csv", "r", encoding="utf-8") as f_in, open(
        "results.csv", "w", encoding="utf-8"
    ) as f_out:
        reader = csv.reader(f_in)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr = calculate_irr(cashflows)
            f_out.write(f"{irr:.6f}\n")


if __name__ == "__main__":
    main()
