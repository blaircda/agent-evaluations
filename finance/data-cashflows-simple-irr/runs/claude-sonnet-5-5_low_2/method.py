import csv

def npv(r, cf):
    return sum(c / (1 + r) ** i for i, c in enumerate(cf))

def irr(cf):
    lo, hi = -0.999999, 1.0
    while npv(hi, cf) > 0 and hi < 1e6:
        hi *= 2
    flo, fhi = npv(lo, cf), npv(hi, cf)
    if flo * fhi > 0:
        return float('nan')
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = npv(mid, cf)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2

with open('data.csv') as f, open('results.csv', 'w') as o:
    for row in csv.reader(f):
        if not row:
            continue
        cf = [float(x) for x in row]
        o.write(f"{irr(cf):.6f}\n")
