import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.999999, hi=1e6, tol=1e-12, max_iter=1000):
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("no sign change in NPV over bracket; IRR not bracketed")
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol or (hi - lo) / 2.0 < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def main():
    with open("data.csv", newline="") as fin, open("results.csv", "w", newline="") as fout:
        for row in csv.reader(fin):
            if not row or all(not c.strip() for c in row):
                continue
            cashflows = [float(c) for c in row if c.strip() != ""]
            fout.write(f"{irr(cashflows):.6f}\n")


if __name__ == "__main__":
    main()
