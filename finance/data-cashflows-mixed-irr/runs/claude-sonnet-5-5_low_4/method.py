import numpy as np

out = []
with open("data.csv") as f:
    for line in f:
        if not line.strip():
            continue
        cf = [float(x) for x in line.strip().split(",")]
        # NPV = sum cf[t]/(1+r)^t ; with x=1/(1+r) solve polynomial in x
        roots = np.roots(cf[::-1])
        cands = [1 / z.real - 1 for z in roots
                 if abs(z.imag) < 1e-9 and z.real > 0]
        # choose root closest to zero if several
        r = min(cands, key=abs) if cands else float("nan")
        out.append(f"{r:.6f}")
with open("results.csv", "w") as f:
    f.write("\n".join(out) + "\n")
