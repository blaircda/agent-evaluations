import math


def npv(rate, cashflows):
    # cashflows[0] occurs at t=0, cashflows[t] at t=t
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def find_irr_roots(cashflows, lo=-0.99, hi=10.0, steps=110000):
    # Scan a grid of rates for sign changes of NPV, then refine each
    # bracket by bisection. Returns every real root with rate > -1 found.
    roots = []
    step = (hi - lo) / steps
    x0 = lo
    f0 = npv(x0, cashflows)
    for i in range(1, steps + 1):
        x1 = lo + i * step
        f1 = npv(x1, cashflows)
        if f0 * f1 < 0:
            a, b, fa = x0, x1, f0
            for _ in range(200):
                m = 0.5 * (a + b)
                fm = npv(m, cashflows)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
                if b - a < 1e-15:
                    break
            roots.append(0.5 * (a + b))
        x0, f0 = x1, f1
    return roots


def irr(cashflows):
    roots = find_irr_roots(cashflows)
    if not roots:
        return float("nan")
    # Where NPV has more than one root, report the one closest to zero.
    return min(roots, key=abs)


def main():
    with open("data.csv", "r") as fin:
        lines = [line.strip() for line in fin]
    with open("results.csv", "w") as fout:
        for line in lines:
            cashflows = [float(x) for x in line.split(",")]
            value = irr(cashflows)
            if math.isnan(value):
                fout.write("nan\n")
            else:
                fout.write(f"{value:.6f}\n")


if __name__ == "__main__":
    main()
