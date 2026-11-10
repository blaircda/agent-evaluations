import csv

def npv(r, cf):
    return sum(c / (1 + r) ** i for i, c in enumerate(cf))

def irr(cf):
    lo, hi = -0.999999, 1.0
    while npv(hi, cf) > 0 and hi < 1e9:
        hi *= 2
    flo = npv(lo, cf)
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = npv(mid, cf)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2

with open("data.csv") as f, open("results.csv", "w") as o:
    for row in csv.reader(f):
        if not row:
            continue
        o.write(f"{irr([float(x) for x in row]):.6f}\n")
