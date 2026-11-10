import numpy as np

# IRR r solves sum(cf[t] / (1+r)^t) = 0. With x = 1/(1+r) this is a polynomial in x;
# find all real roots x > 0 (r > -1). If several exist, take the one closest to 0.
# If none exist, the line is left empty.
out = []
with open("data.csv") as f:
    for line in f:
        if not line.strip():
            continue
        cf = [float(v) for v in line.strip().split(",")]
        roots = np.roots(cf[::-1])
        irrs = [1 / z.real - 1 for z in roots if abs(z.imag) < 1e-9 and z.real > 0]
        out.append(f"{min(irrs, key=abs):.6f}" if irrs else "")

with open("results.csv", "w") as f:
    f.write("\n".join(out) + "\n")
