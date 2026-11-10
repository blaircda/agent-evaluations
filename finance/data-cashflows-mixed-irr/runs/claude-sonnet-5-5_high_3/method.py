import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def irr(cfs, lo=-0.999999, hi=1000.0, steps=200000):
    """Find all roots by scanning for sign changes + bisection; return all roots."""
    import math
    roots = []
    # scan on a transformed grid for resolution near -1 and large rates
    grid = [lo + (hi - lo) * (i / steps) ** 3 for i in range(steps + 1)]
    prev_r, prev_v = grid[0], npv(grid[0], cfs)
    for r in grid[1:]:
        v = npv(r, cfs)
        if prev_v == 0:
            roots.append(prev_r)
        elif prev_v * v < 0:
            a, b, fa = prev_r, r, prev_v
            for _ in range(200):
                m = (a + b) / 2
                fm = npv(m, cfs)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            roots.append((a + b) / 2)
        prev_r, prev_v = r, v
    return roots


rows = []
with open("data.csv", newline="") as f:
    for line in csv.reader(f):
        if line:
            rows.append([float(x) for x in line])

with open("results.csv", "w") as f:
    for cfs in rows:
        roots = irr(cfs)
        if not roots:
            f.write("\n")
            continue
        # if several roots exist, pick the one closest to zero
        r = min(roots, key=abs)
        f.write(f"{r:.6f}\n")
