import csv

def npv(r, cfs):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))

def irr(cfs, lo=-0.999999, hi=10.0, tol=1e-14):
    flo, fhi = npv(lo, cfs), npv(hi, cfs)
    if flo * fhi > 0:
        raise ValueError("No sign change in bracket")
    for _ in range(500):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if fm == 0 or (hi - lo) / 2 < tol:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2

with open("data.csv", newline="") as f:
    rows = [[float(x) for x in row] for row in csv.reader(f) if row]

with open("results.csv", "w") as f:
    for cfs in rows:
        f.write(f"{irr(cfs):.6f}\n")
