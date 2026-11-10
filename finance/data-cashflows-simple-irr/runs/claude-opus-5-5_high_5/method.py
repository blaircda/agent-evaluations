import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.999999, hi=1.0, tol=1e-12, max_iter=1000):
    # Expand upper bound until a sign change is bracketed
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    while f_lo * f_hi > 0 and hi < 1e6:
        hi *= 2.0
        f_hi = npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("IRR not bracketed for cashflows: %r" % (cashflows,))
    # Bisection
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cashflows)
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
            if not row or all(not c.strip() for c in row):
                continue
            cashflows = [float(c) for c in row if c.strip() != ""]
            results.append("%.6f" % irr(cashflows))
    with open("results.csv", "w", newline="") as f:
        f.write("\n".join(results) + "\n")


if __name__ == "__main__":
    main()
