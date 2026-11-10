import numpy_financial as npf

def main():
    results = []
    with open('data.csv', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cashflows = [float(x) for x in line.split(',')]
            val = npf.irr(cashflows)
            results.append(f"{val:.6f}")

    with open('results.csv', 'w') as f:
        for res in results:
            f.write(f"{res}\n")

if __name__ == '__main__':
    main()
