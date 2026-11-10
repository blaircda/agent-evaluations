import csv
def npv(r,cf):
    return sum(c/(1+r)**i for i,c in enumerate(cf))
def irr(cf):
    # scan for sign changes on (-0.99, 10], bisect each; pick root closest to 0
    grid=[-0.99+i*0.001 for i in range(0,11000)]
    roots=[]
    for a,b in zip(grid,grid[1:]):
        fa,fb=npv(a,cf),npv(b,cf)
        if fa==0: roots.append(a)
        elif fa*fb<0:
            for _ in range(100):
                m=(a+b)/2
                if npv(a,cf)*npv(m,cf)<=0: b=m
                else: a=m
            roots.append((a+b)/2)
    if not roots: return None
    return min(roots,key=abs)
out=[]
with open('data.csv') as f:
    for row in csv.reader(f):
        if not row: continue
        r=irr([float(x) for x in row])
        out.append('' if r is None else f'{r:.6f}')
with open('results.csv','w') as f:
    f.write('\n'.join(out)+'\n')
