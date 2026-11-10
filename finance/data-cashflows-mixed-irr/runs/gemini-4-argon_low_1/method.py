import numpy as np
import numpy_financial as npf


def main():
    with open("data.csv", "r") as infile, open("results.csv", "w") as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            cashflows = [float(x) for x in line.split(",")]
            irr_val = npf.irr(cashflows)
            if np.isnan(irr_val):
                outfile.write("nan\n")
            else:
                outfile.write(f"{irr_val:.6f}\n")


if __name__ == "__main__":
    main()
