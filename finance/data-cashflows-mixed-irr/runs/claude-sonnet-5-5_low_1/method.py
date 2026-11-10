import csv

def npv(r, cf):
    return sum(c / (1 + r) ** i for i, c in enumerate(cf))

def irr(cf):
    # scan for sign changes on a grid, then bisect; pick root closest to zero
    grid = [-0.9999 + k * 0.001 for k in range(0, 100000)]
    roots = []
    prev = grid[0]
    fp = npv(prev, cf)
    for x in grid[1:]:
        fx = npv(x, cf)
        if fp == 0:
            roots.append(prev)
        elif fp * fx < 0:
            lo, hi = prev, x
            for _ in range(200):
                mid = (lo + hi) / 2
                if npv(lo, cf) * npv(mid, cf) <= 0:
                    hi = mid
                else:
                    lo = mid
            roots.append((lo + hi) / 2)
        prev, fp = x, fx
    if not roots:
        return None
    return min(roots, key=abs)

with open("data.csv") as f, open("results.csv", "w") as out:
    for row in csv.reader(f):
        if not row:
            out.write("\n")
            continue
        r = irr([float(v) for v in row])
        out.write("" if r is None else f"{r:.6f}")
        out.write("\n")
