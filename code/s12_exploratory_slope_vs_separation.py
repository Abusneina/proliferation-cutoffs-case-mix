"""EXPLORATORY (not registered). Does the C1 slope depend on separation and ties? Run 2026-10-14 after A7 results."""
import numpy as np, pandas as pd, gzip, time
exec(open("s11_gse81538_amendment7.py").read().split("def kappa")[0].replace("res={}",""))   # reuse parsing only
def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe)
def kopt_pct(x,y):
    ref=x; cs=np.unique(np.percentile(x,np.arange(5,96)))
    ks=[kappa((x>c).astype(int),y) for c in cs]; i=int(np.argmax(ks)); return 100*np.mean(x<=cs[i]),ks[i]
def slope(A,B,N=40000,seed=1):
    r=np.random.default_rng(seed); pr=[15,20,25,30,35,40,45]; ps=[];km=[]
    for p in pr:
        nb=int(N*p/100); xa=r.choice(A,N-nb); xb=r.choice(B,nb); x=np.r_[xa,xb]; y=np.r_[np.zeros(N-nb),np.ones(nb)]
        pc,k=kopt_pct(x,y); ps.append(pc); km.append(k)
    return np.polyfit(100-np.array(pr),ps,1)[0],np.mean(km)
r=np.random.default_rng(0)
print("A. Binormal, continuous: slope vs separation d")
for d in [0.5,1,1.5,2,2.5,3]:
    A=r.normal(0,1,40000); B=r.normal(d,1,40000); s,k=slope(A,B); print(f"  d={d}: slope {s:.2f}, mean max kappa {k:.2f}")
el=meta[(meta.ER.isin([1,2,3]))&(meta.HER2==0)&meta.PAM50.isin(["LumA","LumB"])].dropna(subset=["K"])
A=el.K[el.PAM50=="LumA"].values; B=el.K[el.PAM50=="LumB"].values
s,k=slope(A,B); print(f"B. Observed consensus K distributions, N=40000 (no small-sample noise): slope {s:.2f}, mean max kappa {k:.2f}")
Aj=A+r.uniform(-2.5,2.5,len(A)); Bj=B+r.uniform(-2.5,2.5,len(B))
s,k=slope(Aj,Bj); print(f"C. Same, ties broken by +-2.5 jitter: slope {s:.2f}, mean max kappa {k:.2f}")
