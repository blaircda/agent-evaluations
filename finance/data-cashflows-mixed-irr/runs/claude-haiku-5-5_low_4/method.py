import csv
import math


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr_roots(cashflows, lo=-0.999999, hi=10.0, grid_steps=2000):
    # Scan a grid for sign changes of NPV, then bisect each bracket to refine the root.
    roots = []
    grid = [lo + (hi - lo) * i / grid_steps for i in range(grid_steps + 1)]
    prev_r, prev_v = grid[0], npv(grid[0], cashflows)
    for r in grid[1:]:
        v = npv(r, cashflows)
        if prev_v == 0:
            roots.append(prev_r)
        elif prev_v * v < 0:
            a, b, fa = prev_r, r, prev_v
            for _ in range(200):
                m = (a + b) / 2.0
                fm = npv(m, cashflows)
                if fm == 0 or (b - a) < 1e-14:
                    a = b = m
                    break
                if fa * fm < 0:
                    b = m
                else:
                    a, fa = m, fm
            roots.append((a + b) / 2.0)
        prev_r, prev_v = r, v
    return roots


def irr(cashflows):
    roots = irr_roots(cashflows)
    if not roots:
        return math.nan  # no real IRR exists for this stream
    # If several real IRRs exist, report the one closest to zero.
    return min(roots, key=abs)


def main():
    with open("data.csv", newline="") as fin, open("results.csv", "w", newline="") as fout:
        for row in csv.reader(fin):
            values = [v.strip() for v in row if v.strip() != ""]
            if not values:
                continue
            cashflows = [float(v) for v in values]
            value = irr(cashflows)
            fout.write("NaN\n" if math.isnan(value) else f"{value:.6f}\n")


if __name__ == "__main__":
    main()
