import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.999999, hi=10.0, tol=1e-12, max_iter=500):
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("IRR not bracketed in [%g, %g]" % (lo, hi))
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
    with open("data.csv", newline="") as fin:
        streams = [row for row in csv.reader(fin) if row]

    with open("results.csv", "w", newline="") as fout:
        for row in streams:
            cashflows = [float(x) for x in row]
            fout.write("%.6f\n" % irr(cashflows))


if __name__ == "__main__":
    main()
