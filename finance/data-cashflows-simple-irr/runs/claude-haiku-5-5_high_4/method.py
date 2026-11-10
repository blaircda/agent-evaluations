import csv


def npv(rate, flows):
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))


def irr(flows):
    # For conventional cashflows (one sign change), NPV is strictly
    # decreasing in the rate on (-1, inf), so bisection finds the unique root.
    lo = -0.999999999
    hi = 1.0
    while npv(hi, flows) > 0:
        hi *= 2.0
    for _ in range(300):
        mid = (lo + hi) / 2.0
        if npv(mid, flows) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-14:
            break
    return (lo + hi) / 2.0


with open("data.csv", newline="") as f_in, open("results.csv", "w", newline="") as f_out:
    for row in csv.reader(f_in):
        if not row:
            continue
        flows = [float(x) for x in row]
        f_out.write(f"{irr(flows):.6f}\n")
