import csv
def npv(r, cf):
    return sum(c / (1 + r) ** i for i, c in enumerate(cf))

def bisect(cf, a, b):
    fa = npv(a, cf)
    for _ in range(300):
        m = (a + b) / 2
        fm = npv(m, cf)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2

def irr(cf):
    # scan r in (-0.99, 1000) for sign changes; return the root with the
    # largest rate (positive economically meaningful root); None if no root.
    grid = [-0.99 + i * 0.001 for i in range(0, 20000)]
    grid += [20 * 1.01 ** k for k in range(0, 700)]
    roots = []
    for a, b in zip(grid, grid[1:]):
        fa, fb = npv(a, cf), npv(b, cf)
        if fa == 0:
            roots.append(a)
        elif fa * fb < 0:
            roots.append(bisect(cf, a, b))
    nonneg = [r for r in roots if r >= 0]
    if nonneg:
        return nonneg[0]
    return roots[0] if roots else None

with open('data.csv') as f, open('results.csv', 'w') as o:
    for row in csv.reader(f):
        if not row:
            continue
        r = irr([float(x) for x in row])
        o.write("" if r is None else f"{r:.6f}")
        o.write("\n")
