import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs, lo=-0.9999, hi=10.0, tol=1e-12, max_iter=1000):
    f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    while f_lo * f_hi > 0 and hi < 1e6:
        hi *= 2
        f_hi = npv(hi, cfs)
    if f_lo * f_hi > 0:
        raise ValueError("IRR not bracketed for %r" % (cfs,))
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


with open("data.csv", newline="") as f:
    rows = [[float(x) for x in row] for row in csv.reader(f) if row]

with open("results.csv", "w", newline="") as f:
    for cfs in rows:
        f.write("%.6f\n" % irr(cfs))
