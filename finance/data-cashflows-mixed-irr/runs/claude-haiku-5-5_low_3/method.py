import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.9999, hi=10.0, steps=20000):
    """Find the IRR by scanning for sign changes of the NPV, then bisecting.

    Returns the first root found in ascending order, or None if there is none.
    """
    roots = []
    prev_r = lo
    prev_v = npv(prev_r, cashflows)
    for i in range(1, steps + 1):
        r = lo + (hi - lo) * i / steps
        v = npv(r, cashflows)
        if prev_v == 0:
            roots.append(prev_r)
        elif prev_v * v < 0:
            a, b, fa = prev_r, r, prev_v
            for _ in range(200):
                m = (a + b) / 2.0
                fm = npv(m, cashflows)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            roots.append((a + b) / 2.0)
        prev_r, prev_v = r, v
    if not roots:
        return None, roots
    return roots[0], roots


def main():
    results = []
    with open("data.csv", newline="") as f:
        for line in csv.reader(f):
            if not line or all(x.strip() == "" for x in line):
                continue
            cashflows = [float(x) for x in line if x.strip() != ""]
            value, all_roots = irr(cashflows)
            results.append(value)
            if len(all_roots) != 1:
                print(f"note: {len(all_roots)} IRR roots for {line}: {all_roots}")
    with open("results.csv", "w", newline="") as f:
        for value in results:
            f.write("" if value is None else f"{value:.6f}")
            f.write("\n")


if __name__ == "__main__":
    main()
