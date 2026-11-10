import csv

def compute_irr(cashflows, tol=1e-12, max_iter=1000):
    # Find IRR r such that sum(cf / (1 + r)^t for t, cf in enumerate(cashflows)) = 0
    # Using Newton-Raphson on f(r) = sum(cf * (1 + r)^(-t))
    r = 0.5
    for _ in range(max_iter):
        f_val = 0.0
        df_val = 0.0
        for t, cf in enumerate(cashflows):
            f_val += cf / ((1.0 + r) ** t)
            if t > 0:
                df_val -= t * cf / ((1.0 + r) ** (t + 1))
        if abs(f_val) < tol:
            break
        r = r - f_val / df_val
    return r

def main():
    results = []
    with open('data.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            cashflows = [float(x) for x in row]
            irr = compute_irr(cashflows)
            results.append(f"{irr:.6f}")

    with open('results.csv', 'w', newline='') as f:
        for res in results:
            f.write(res + '\n')

if __name__ == '__main__':
    main()
