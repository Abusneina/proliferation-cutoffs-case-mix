import gzip,sys,time
T0=time.time()
def rows(path,sep,col):
    op=gzip.open if path.endswith('.gz') else open
    s=set()
    with op(path,'rt',errors='replace') as f:
        f.readline()
        for n,l in enumerate(f,1):
            if n%10000==0: print(f"[{time.time()-T0:5.0f}s] {path.split('/')[-1]}: {n} rows",flush=True)
            s.add(l.split(sep,1)[0].strip('"'))
    return s
P3=[l.strip() for l in open('p3.txt') if l.strip()]; P4=[l.strip() for l in open('p4.txt') if l.strip()]
ALIAS={"KIAA0101":"PCLAF","MLF1IP":"CENPU","WHSC1":"NSD2","SFRS2":"SRSF2","C21orf45":"MIS18A","DDX39":"DDX39A","H3F3A":"H3-3A","CDK1":"CDC2","DDX39A":"DDX39","PCLAF":"KIAA0101"}
M={"TCGA":rows('/home/claude/raw/tcga_rsem.txt','\t',0),"METABRIC":rows('/home/claude/raw/metabric_illumina.txt','\t',0),
   "GSE96058":rows('/home/claude/raw/gse96058.csv.gz',',',0),"GSE81538":rows('/home/claude/raw/gse81538.csv.gz',',',0)}
for name,L in [("P3",P3),("P4",P4)]:
    for c,S in M.items():
        hit=[g for g in L if g in S]; ali=[f"{g}->{ALIAS[g]}" for g in L if g not in S and ALIAS.get(g) in S]
        miss=[g for g in L if g not in S and ALIAS.get(g) not in S]
        n=len(hit)+len(ali)
        print(f"{name} {c:9s} found {n}/{len(L)} ({100*n/len(L):.1f}%) | via alias: {ali} | missing: {miss}")
