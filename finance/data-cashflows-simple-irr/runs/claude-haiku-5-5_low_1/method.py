import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.99, hi=10.0, tol=1e-12):
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("IRR not bracketed in [%g, %g]" % (lo, hi))
    while hi - lo > tol:
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cashflows)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


with open("data.csv", newline="") as fin, open("results.csv", "w", newline="") as fout:
    for row in csv.reader(fin):
        if not row or all(not c.strip() for c in row):
            continue
        cashflows = [float(c) for c in row]
        fout.write("%.6f\n" % irr(cashflows))
