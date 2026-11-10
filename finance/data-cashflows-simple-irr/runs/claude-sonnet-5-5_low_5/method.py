import csv
def npv(r,c): return sum(x/(1+r)**i for i,x in enumerate(c))
def irr(c):
    lo,hi=-0.9999,10.0
    flo=npv(lo,c)
    for _ in range(300):
        m=(lo+hi)/2; fm=npv(m,c)
        if (fm>0)==(flo>0): lo,flo=m,fm
        else: hi=m
    return (lo+hi)/2
with open('data.csv') as f, open('results.csv','w') as o:
    for row in csv.reader(f):
        if row: o.write(f"{irr([float(x) for x in row]):.6f}\n")
