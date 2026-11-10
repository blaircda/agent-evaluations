import numpy as np

try:
    import numpy_financial as npf

    def calculate_irr(cfs):
        return npf.irr(cfs)
except ImportError:
    def calculate_irr(cfs):
        g = np.roots(cfs)
        eirr = np.real(g[np.isreal(g)]) - 1
        eirr = eirr[eirr >= -1]
        if len(eirr) == 0:
            return np.nan
        elif len(eirr) == 1:
            return eirr[0]
        else:
            same_sign = np.all(eirr > 0) if eirr[0] > 0 else np.all(eirr < 0)
            if not same_sign:
                pos = sum(eirr[eirr > 0])
                neg = sum(eirr[eirr < 0])
                if pos >= neg:
                    eirr = eirr[eirr >= 0]
                else:
                    eirr = eirr[eirr < 0]
            abs_eirr = np.abs(eirr)
            return eirr[np.argmin(abs_eirr)]


def main():
    results = []
    with open("data.csv", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cfs = [float(x.strip()) for x in line.split(",")]
            irr = calculate_irr(cfs)
            if np.isnan(irr):
                results.append("nan")
            else:
                results.append(f"{irr:.6f}")

    with open("results.csv", "w") as f:
        for val in results:
            f.write(f"{val}\n")


if __name__ == "__main__":
    main()
