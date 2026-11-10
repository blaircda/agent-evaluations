import numpy_financial as npf


def main():
    with open('data.csv', 'r') as f_in, open('results.csv', 'w') as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            cash_flows = [float(x.strip()) for x in line.split(',') if x.strip()]
            irr = npf.irr(cash_flows)
            f_out.write(f"{irr:.6f}\n")


if __name__ == '__main__':
    main()
