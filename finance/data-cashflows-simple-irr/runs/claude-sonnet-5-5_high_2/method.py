import csv

def npv(r, cfs):
    return sum(cf / (1.0 + r) ** t for t, cf in enumerate(cfs))

def irr(cfs):
    lo, hi = -0.999999, 1.0
    flo = npv(lo, cfs)
    while npv(hi, cfs) * flo > 0 and hi < 1e6:
        hi *= 2
    fhi = npv(hi, cfs)
    if flo * fhi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2

with open("data.csv", newline="") as f:
    rows = [[float(x) for x in row] for row in csv.reader(f) if row]

with open("results.csv", "w") as f:
    for cfs in rows:
        r = irr(cfs)
        f.write("" if r is None else f"{r:.6f}")
        f.write("\n")
