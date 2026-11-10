import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def all_roots(cfs, lo=-0.999999, hi=100.0, steps=20000):
    """Find every sign change of NPV on a rate grid, then bisect each."""
    roots = []
    step = (hi - lo) / steps
    x0 = lo
    f0 = npv(x0, cfs)
    for i in range(1, steps + 1):
        x1 = lo + i * step
        f1 = npv(x1, cfs)
        if f0 == 0:
            roots.append(x0)
        elif f0 * f1 < 0:
            a, b, fa = x0, x1, f0
            for _ in range(200):
                m = 0.5 * (a + b)
                fm = npv(m, cfs)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            roots.append(0.5 * (a + b))
        x0, f0 = x1, f1
    return roots


def irr(cfs):
    roots = all_roots(cfs)
    if not roots:
        return None
    # If several rates satisfy NPV=0, report the one closest to zero.
    return min(roots, key=abs)


with open("data.csv", newline="") as fin, open("results.csv", "w", newline="") as fout:
    for row in csv.reader(fin):
        if not row or all(c.strip() == "" for c in row):
            continue
        cfs = [float(c) for c in row]
        r = irr(cfs)
        fout.write("NaN\n" if r is None else f"{r:.6f}\n")
