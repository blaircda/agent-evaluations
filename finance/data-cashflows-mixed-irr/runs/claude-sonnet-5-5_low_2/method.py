import csv
def npv(r, cf):
    return sum(c/(1+r)**i for i, c in enumerate(cf))
def irr(cf):
    # scan for sign changes on (-0.999, 10], refine by bisection; pick root closest to 0
    grid = [-0.999 + k*0.001 for k in range(0, 11000)]
    roots = []
    prev = npv(grid[0], cf)
    for a, b in zip(grid, grid[1:]):
        fb = npv(b, cf)
        if prev == 0:
            roots.append(a)
        elif prev*fb < 0:
            lo, hi = a, b
            flo = prev
            for _ in range(200):
                mid = (lo+hi)/2
                fm = npv(mid, cf)
                if flo*fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            roots.append((lo+hi)/2)
        prev = fb
    return min(roots, key=abs) if roots else None
with open('data.csv') as f, open('results.csv', 'w') as o:
    for row in csv.reader(f):
        if not row:
            continue
        r = irr([float(x) for x in row])
        o.write('' if r is None else f'{r:.6f}')
        o.write('\n')
