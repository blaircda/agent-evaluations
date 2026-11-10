import numpy as np

def irr(values):
    # Solve for g = 1 + r using polynomial roots of cashflows:
    # sum_{t=0}^n values[t] * g^{n-t} = 0
    roots = np.roots(values)
    real_roots = np.real(roots[np.isreal(roots)])
    rates = real_roots - 1.0
    # Filter for economically meaningful IRR (r >= -1, i.e., g >= 0)
    valid_rates = rates[rates >= -1.0]
    if len(valid_rates) == 0:
        return np.nan
    # In case of multiple valid rates, pick the one closest to 0
    return valid_rates[np.argmin(np.abs(valid_rates))]

def main():
    with open("data.csv", "r") as infile, open("results.csv", "w") as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            cashflows = [float(x.strip()) for x in line.split(",") if x.strip()]
            rate = irr(cashflows)
            outfile.write(f"{rate:.6f}\n")

if __name__ == "__main__":
    main()
