import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.999999, hi=1000.0, iterations=500):
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo == 0:
        return lo
    if f_hi == 0:
        return hi
    if (f_lo > 0) == (f_hi > 0):
        raise ValueError("IRR not bracketed by [lo, hi]")
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cashflows)
        if f_mid == 0 or (hi - lo) < 1e-15:
            return mid
        if (f_mid > 0) == (f_lo > 0):
            lo, f_lo = mid, f_mid
        else:
            hi, f_hi = mid, f_mid
    return (lo + hi) / 2.0


def main():
    with open("data.csv", newline="") as fin, open("results.csv", "w", newline="") as fout:
        for row in csv.reader(fin):
            if not row or all(not cell.strip() for cell in row):
                continue
            cashflows = [float(cell) for cell in row]
            fout.write(f"{irr(cashflows):.6f}\n")


if __name__ == "__main__":
    main()
