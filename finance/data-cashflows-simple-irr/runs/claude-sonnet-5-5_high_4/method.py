import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs, lo=-0.999999, hi=1000.0, tol=1e-14, max_iter=1000):
    f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    if f_lo * f_hi > 0:
        return None
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


with open("data.csv", newline="") as f_in, open("results.csv", "w") as f_out:
    for row in csv.reader(f_in):
        if not row:
            continue
        cfs = [float(x) for x in row if x.strip() != ""]
        r = irr(cfs)
        f_out.write("" if r is None else f"{r:.6f}")
        f_out.write("\n")
