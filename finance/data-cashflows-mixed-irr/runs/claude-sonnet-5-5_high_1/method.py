import numpy as np

# IRR = r such that sum(cf[t] / (1+r)^t) = 0.
# Substituting x = 1/(1+r) gives a polynomial in x; take all real roots with x > 0
# (i.e. r > -1). If several IRRs exist, the one closest to zero is reported.
# If no real IRR exists, the line is left empty.

def irr(cf):
    roots = np.roots(cf[::-1])  # coefficients highest power first
    rs = [1 / x.real - 1 for x in roots if abs(x.imag) < 1e-9 and x.real > 0]
    return min(rs, key=abs) if rs else None

with open("data.csv") as f, open("results.csv", "w") as out:
    for line in f:
        if not line.strip():
            continue
        cf = [float(v) for v in line.strip().split(",")]
        r = irr(cf)
        out.write("" if r is None else f"{r:.6f}")
        out.write("\n")
