import csv
def npv(r,cf): return sum(c/(1+r)**i for i,c in enumerate(cf))
def irr(cf):
    lo,hi=-0.999999,10.0
    flo,fhi=npv(lo,cf),npv(hi,cf)
    if flo*fhi>0: return float('nan')
    for _ in range(300):
        m=(lo+hi)/2; fm=npv(m,cf)
        if flo*fm<=0: hi=m
        else: lo,flo=m,fm
    return (lo+hi)/2
with open('data.csv') as f:
    rows=[[float(x) for x in r] for r in csv.reader(f) if r]
with open('results.csv','w') as f:
    for r in rows: f.write(f"{irr(r):.6f}\n")
