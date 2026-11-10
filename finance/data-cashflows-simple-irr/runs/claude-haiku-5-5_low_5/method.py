import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, lo=-0.999999, hi=10.0, tol=1e-12):
    f_lo = npv(lo, cashflows)
    f_hi = npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("No sign change in NPV over search interval")
    for _ in range(500):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol or (hi - lo) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def main():
    with open("data.csv", newline="") as fin:
        rows = [[float(x) for x in row] for row in csv.reader(fin) if row]
    with open("results.csv", "w", newline="") as fout:
        for cashflows in rows:
            fout.write(f"{irr(cashflows):.6f}\n")


if __name__ == "__main__":
    main()
