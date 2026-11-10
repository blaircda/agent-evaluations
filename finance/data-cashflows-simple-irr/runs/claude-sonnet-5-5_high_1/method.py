import csv

def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))

def irr(cfs, lo=-0.999999, hi=1.0):
    # expand upper bound until sign change
    flo = npv(lo, cfs)
    while npv(hi, cfs) * flo > 0 and hi < 1e9:
        hi *= 2
    flo, fhi = npv(lo, cfs), npv(hi, cfs)
    if flo * fhi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if fm == 0:
            return mid
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2

with open("data.csv", newline="") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        if not row:
            continue
        cfs = [float(x) for x in row]
        r = irr(cfs)
        out.write("" if r is None else f"{r:.6f}")
        out.write("\n")
