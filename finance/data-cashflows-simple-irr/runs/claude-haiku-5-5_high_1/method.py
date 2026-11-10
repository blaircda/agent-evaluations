import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.999999, hi=100.0, tol=1e-14):
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("NPV does not change sign over bracket; IRR not bracketed")
    for _ in range(500):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cashflows)
        if f_mid == 0 or (hi - lo) < tol:
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
            if not row:
                continue
            cashflows = [float(x) for x in row]
            results.append(irr(cashflows))
    with open("results.csv", "w") as f:
        for r in results:
            f.write(f"{r:.6f}\n")


if __name__ == "__main__":
    main()
