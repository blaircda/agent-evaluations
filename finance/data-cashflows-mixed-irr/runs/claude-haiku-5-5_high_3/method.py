import csv
import math

GRID_POINTS = 8000
LOG10_MIN, LOG10_MAX = -4.0, 4.0  # search (1 + r) over [1e-4, 1e4]


def npv_at_growth(x, cashflows):
    """NPV with x = 1 + r, using cashflows[t] discounted by x**t."""
    return sum(cf * x ** (-t) for t, cf in enumerate(cashflows))


def bisect_root(lo, hi, f_lo, cashflows):
    for _ in range(200):
        mid = math.sqrt(lo * hi)  # bisect in log space
        f_mid = npv_at_growth(mid, cashflows)
        if f_mid == 0:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return math.sqrt(lo * hi)


def all_irrs(cashflows):
    """All real IRRs (roots of NPV(r) = 0 with r > -1) found on the search grid."""
    grid = [10 ** (LOG10_MIN + (LOG10_MAX - LOG10_MIN) * k / GRID_POINTS)
            for k in range(GRID_POINTS + 1)]
    values = [npv_at_growth(x, cashflows) for x in grid]
    roots = []
    for k in range(GRID_POINTS):
        a, b = grid[k], grid[k + 1]
        fa, fb = values[k], values[k + 1]
        if fa == 0:
            roots.append(a)
        elif fa * fb < 0:
            roots.append(bisect_root(a, b, fa, cashflows))
    if values[-1] == 0:
        roots.append(grid[-1])
    return [x - 1.0 for x in roots]


def irr(cashflows):
    """IRR as a decimal. If several IRRs exist, the one closest to zero is used.
    Returns NaN when no real IRR exists."""
    if not any(cf != 0 for cf in cashflows):
        return float("nan")
    roots = all_irrs(cashflows)
    if not roots:
        return float("nan")
    return min(roots, key=abs)


def main():
    with open("data.csv", newline="") as f:
        streams = list(csv.reader(f))
    with open("results.csv", "w", newline="") as f:
        for cashflows in streams:
            values = [float(v) for v in cashflows if v.strip() != ""]
            result = irr(values)
            f.write(f"{result:.6f}\n")


if __name__ == "__main__":
    main()
