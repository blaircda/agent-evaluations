import csv


def npv(rate, cashflows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows):
    # Scan a grid of rates for a sign change in NPV, then bisect within it.
    lo_bound, hi_bound = -0.999999, 1000.0
    steps = 20000
    prev_r = lo_bound
    prev_v = npv(prev_r, cashflows)
    for i in range(1, steps + 1):
        r = lo_bound + (hi_bound - lo_bound) * i / steps
        v = npv(r, cashflows)
        if prev_v == 0:
            return prev_r
        if prev_v * v < 0:
            lo, hi = prev_r, r
            for _ in range(200):
                mid = (lo + hi) / 2
                vm = npv(mid, cashflows)
                if npv(lo, cashflows) * vm <= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
        prev_r, prev_v = r, v
    return None


def main():
    results = []
    with open("data.csv", newline="") as f:
        for row in csv.reader(f):
            values = [float(x) for x in row if x.strip() != ""]
            if not values:
                results.append("")
                continue
            r = irr(values)
            results.append("" if r is None else f"{r:.6f}")
    with open("results.csv", "w", newline="") as f:
        for line in results:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
