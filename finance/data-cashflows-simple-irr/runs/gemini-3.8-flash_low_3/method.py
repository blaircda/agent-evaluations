import numpy as np

def irr(values):
    """
    Compute the internal rate of return for a cashflow series.
    """
    # np.roots finds the roots of polynomial: values[0]*x^n + ... + values[n] = 0
    # where x = 1 + r.
    res = np.roots(values)
    mask = (res.imag == 0) & (res.real > 0)
    if not np.any(mask):
        return np.nan
    res = res[mask].real
    rates = res - 1
    # Pick the rate closest to zero if multiple positive roots exist
    rate = rates[np.argmin(np.abs(rates))]
    return rate

def main():
    results = []
    with open('data.csv', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = [float(x.strip()) for x in line.split(',')]
            rate = irr(values)
            results.append(rate)

    with open('results.csv', 'w') as f:
        for rate in results:
            f.write(f"{rate:.6f}\n")

if __name__ == '__main__':
    main()
