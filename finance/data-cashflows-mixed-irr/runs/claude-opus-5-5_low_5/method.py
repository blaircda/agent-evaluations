import csv
import math


def npv(r, cfs):
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))


def bisect(lo, hi, cfs):
    flo = npv(lo, cfs)
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = npv(mid, cfs)
        if fm == 0:
            return mid
        if (flo < 0) == (fm < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def irr(cfs):
    # Scan rates in (-1, 100] for sign changes of NPV; bisect each bracket.
    grid = [-0.9999 + i * 0.0001 for i in range(10000)]  # -0.9999 .. ~0
    grid += [i * 0.001 for i in range(1, 100001)]  # 0.001 .. 100
    roots = []
    prev_r, prev_f = grid[0], npv(grid[0], cfs)
    for r in grid[1:]:
        f = npv(r, cfs)
        if f == 0:
            roots.append(r)
        elif prev_f != 0 and (f < 0) != (prev_f < 0):
            roots.append(bisect(prev_r, r, cfs))
        prev_r, prev_f = r, f
    if not roots:
        return float("nan")
    # If multiple IRRs exist, report the one closest to zero.
    return min(roots, key=abs)


with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        cfs = [float(x) for x in row if x.strip()]
        val = irr(cfs)
        out.write(("nan" if math.isnan(val) else f"{val:.6f}") + "\n")
