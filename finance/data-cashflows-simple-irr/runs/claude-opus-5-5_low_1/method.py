import csv


def npv(r, cfs):
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))


def irr(cfs):
    lo, hi = -0.9999, 1.0
    while npv(hi, cfs) > 0 and hi < 1e6:
        hi *= 2
    flo = npv(lo, cfs)
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        if not row:
            continue
        cfs = [float(x) for x in row if x.strip()]
        out.write(f"{irr(cfs):.6f}\n")
