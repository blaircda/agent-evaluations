import csv


def compute_irr(cf):
    # NPV(r) = sum_{t=0}^n cf[t] / (1 + r)^t = 0
    # Using Newton-Raphson with bisection fallback
    low, high = -0.999999, 100.0
    for _ in range(1000):
        mid = (low + high) / 2
        npv = sum(c / ((1 + mid) ** t) for t, c in enumerate(cf))
        if npv > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


with open("data.csv", "r", newline="") as infile, open(
    "results.csv", "w", newline=""
) as outfile:
    reader = csv.reader(infile)
    for row in reader:
        if not row:
            continue
        cf = [float(x) for x in row]
        irr = compute_irr(cf)
        outfile.write(f"{irr:.6f}\n")
