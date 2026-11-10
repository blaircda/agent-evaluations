import csv


def npv(r, cfs):
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))


def irr(cfs):
    # Scan a grid for sign changes; bisect each, return the root closest to 0.
    grid = [-0.99 + i * 0.001 for i in range(11000)]
    roots = []
    for a, b in zip(grid, grid[1:]):
        if npv(a, cfs) * npv(b, cfs) <= 0:
            roots.append(bisect(cfs, a, b))
    if not roots:
        return float("nan")
    return min(roots, key=abs)


def bisect(cfs, lo, hi, tol=1e-12):
    flo = npv(lo, cfs)
    for _ in range(500):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if abs(fm) < tol or (hi - lo) < tol:
            break
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        cfs = [float(x) for x in row if x.strip()]
        out.write(f"{irr(cfs):.6f}\n")
