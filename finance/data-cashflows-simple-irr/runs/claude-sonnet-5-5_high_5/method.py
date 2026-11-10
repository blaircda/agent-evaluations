import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs, lo=-0.999999, hi=1.0, tol=1e-14):
    # expand the upper bracket until the sign changes
    f_lo = npv(lo, cfs)
    while npv(hi, cfs) * f_lo > 0 and hi < 1e9:
        hi *= 2
    f_hi = npv(hi, cfs)
    if f_lo * f_hi > 0:
        return float("nan")
    for _ in range(500):
        mid = (lo + hi) / 2
        f_mid = npv(mid, cfs)
        if f_mid == 0 or (hi - lo) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


with open("data.csv", newline="") as f_in, open("results.csv", "w") as f_out:
    for row in csv.reader(f_in):
        if not row:
            continue
        cfs = [float(x) for x in row]
        f_out.write(f"{irr(cfs):.6f}\n")
