import csv


def npv(r, cfs):
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))


def irr(cfs, lo=-0.9999, hi=100.0, tol=1e-12):
    flo, fhi = npv(lo, cfs), npv(hi, cfs)
    if flo * fhi > 0:
        return float("nan")
    for _ in range(500):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
        if hi - lo < tol:
            break
    return (lo + hi) / 2


with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        if not row:
            continue
        cfs = [float(x) for x in row if x.strip()]
        out.write(f"{irr(cfs):.6f}\n")
