"""EXPLORATORY. Patient-level bootstrap CI of the registered C1 slope (consensus K)."""
import numpy as np, time
exec(open("s11_gse81538_amendment7.py").read().split("def kappa")[0].replace("res={}",""))
def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe) if pe<1 else np.nan
def kopt_pct(x,y):
    cs=np.unique(x)[:-1]; ks=[kappa((x>c).astype(int),y) for c in cs]; return 100*np.mean(x<=cs[int(np.nanargmax(ks))])
el=meta[(meta.ER.isin([1,2,3]))&(meta.HER2==0)&meta.PAM50.isin(["LumA","LumB"])].dropna(subset=["K"])
A=el.K[el.PAM50=="LumA"].values; B=el.K[el.PAM50=="LumB"].values; N=len(el)
PR=[15,20,25,30,35,40,45]; xs=100-np.array(PR); r=np.random.default_rng(0); sl=[]
for b in range(300):
    if b%50==0: print(f"  bootstrap {b}/300",flush=True)
    Ab=r.choice(A,len(A)); Bb=r.choice(B,len(B)); med=[]
    for p in PR:
        nb=int(round(N*p/100)); v=[]
        for k in range(40):
            xa=r.choice(Ab,N-nb); xb=r.choice(Bb,nb); v.append(kopt_pct(np.r_[xa,xb],np.r_[np.zeros(N-nb,int),np.ones(nb,int)]))
        med.append(np.median(v))
    sl.append(np.polyfit(xs,med,1)[0])
print(f"C1 slope bootstrap: median {np.median(sl):.2f}, 95% CI {np.percentile(sl,2.5):.2f} to {np.percentile(sl,97.5):.2f}; share below 0.7: {np.mean(np.array(sl)<0.7):.2f}")
