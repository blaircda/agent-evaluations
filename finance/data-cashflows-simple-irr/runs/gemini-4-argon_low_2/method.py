import csv

def compute_irr(cashflows):
    def npv(r):
        return sum(cf / ((1.0 + r) ** t) for t, cf in enumerate(cashflows))
    
    low = -0.999999
    high = 1000.0
    for _ in range(200):
        mid = (low + high) / 2.0
        if npv(mid) > 0:
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
            cashflows = [float(x.strip()) for x in row]
            irr = compute_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open("results.csv", "w", newline="") as f:
        for res in results:
            f.write(res + "\n")

if __name__ == "__main__":
    main()
