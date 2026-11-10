import csv


def npv(rate, cfs):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cfs))


def all_roots(cfs, lo=-0.9999, hi=1000.0, steps=20000):
    """Scan rates (log-spaced in 1+r) for sign changes of NPV, refine each by bisection."""
    grid = [(1 + lo) * ((1 + hi) / (1 + lo)) ** (i / steps) - 1.0 for i in range(steps + 1)]
    roots = []
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


def main():
    results = []
    with open("data.csv", newline="") as f:
        for row in csv.reader(f):
            cfs = [float(c) for c in row if c.strip() != ""]
            roots = all_roots(cfs)
            if not roots:
                results.append("NA")  # no real IRR in search range
            else:
                # if several roots exist, take the one closest to zero
                results.append(f"{min(roots, key=abs):.6f}")
    with open("results.csv", "w") as f:
        for line in results:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
