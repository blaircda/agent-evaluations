import csv

def compute_irr(cf):
    # NPV(r) = sum_{t=0}^{n} cf[t] / (1 + r)^t = 0
    # Using Newton-Raphson method starting at r = 0.1
    r = 0.1
    for _ in range(1000):
        npv = sum(c / ((1.0 + r) ** t) for t, c in enumerate(cf))
        if abs(npv) < 1e-12:
            break
        d_npv = sum(-t * c / ((1.0 + r) ** (t + 1)) for t, c in enumerate(cf) if t > 0)
        r -= npv / d_npv
    return r

with open('data.csv', 'r', newline='') as infile, open('results.csv', 'w', newline='\n') as outfile:
    reader = csv.reader(infile)
    for row in reader:
        if not row:
            continue
        cf = [float(x) for x in row]
        irr = compute_irr(cf)
        outfile.write(f"{irr:.6f}\n")
