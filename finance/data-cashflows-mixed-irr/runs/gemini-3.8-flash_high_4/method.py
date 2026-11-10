import numpy as np

try:
    import numpy_financial as npf
    calc_irr = npf.irr
except ImportError:
    def calc_irr(values):
        values = np.asarray(values, dtype=float)
        same_sign = np.all(values > 0) if values[0] > 0 else np.all(values < 0)
        if same_sign:
            return np.nan
        roots = np.roots(values)
        real_roots = np.real(roots[np.isreal(roots)]) - 1
        real_roots = real_roots[real_roots >= -1]
        if len(real_roots) == 0:
            return np.nan
        elif len(real_roots) == 1:
            return float(real_roots[0])
        else:
            same_sign = np.all(real_roots > 0) if real_roots[0] > 0 else np.all(real_roots < 0)
            if not same_sign:
                pos = sum(real_roots[real_roots > 0])
                neg = sum(real_roots[real_roots < 0])
                if pos >= neg:
                    real_roots = real_roots[real_roots >= 0]
                else:
                    real_roots = real_roots[real_roots < 0]
            abs_roots = np.abs(real_roots)
            return float(real_roots[np.argmin(abs_roots)])

def main():
    with open("data.csv", "r") as f_in, open("results.csv", "w") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            cashflows = [float(x) for x in line.split(",")]
            rate = calc_irr(cashflows)
            f_out.write(f"{rate:.6f}\n")

if __name__ == "__main__":
    main()
