import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs, lo=-0.999999, hi=1.0, tol=1e-12, max_iter=1000):
    # Expand the upper bracket until a sign change is found
    f_lo = npv(lo, cfs)
    f_hi = npv(hi, cfs)
    while f_lo * f_hi > 0 and hi < 1e6:
        hi *= 2.0
        f_hi = npv(hi, cfs)
    if f_lo * f_hi > 0:
        return float("nan")
    # Bisection
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cfs)
        if f_mid == 0 or (hi - lo) / 2.0 < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def main():
    results = []
    with open("data.csv", newline="") as f:
        for row in csv.reader(f):
            values = [float(x) for x in row if x.strip() != ""]
            if not values:
                continue
            results.append(irr(values))
    with open("results.csv", "w", newline="") as f:
        for r in results:
            f.write(f"{r:.6f}\n")


if __name__ == "__main__":
    main()
