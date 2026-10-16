import numpy as np
exec(open("s13_fig4.py").read().split("r=np.random.default_rng(0)")[0])
el=meta[(meta.ER.isin([1,2,3]))&(meta.HER2==0)&meta.PAM50.isin(["LumA","LumB"])].dropna(subset=["K"])
A=el.K[el.PAM50=="LumA"].values; B=el.K[el.PAM50=="LumB"].values
xs=100-np.array(PR); res={}
for w in [1.0,2.5]:
    sl=[]
    for s in range(30):
        r=np.random.default_rng(100+s)
        c=curve(A+r.uniform(-w,w,len(A)),B+r.uniform(-w,w,len(B)),N=20000,seed=s)
        sl.append(np.polyfit(xs,c,1)[0])
    print(f"jitter +-{w}: slope median {np.median(sl):.2f}, range {min(sl):.2f} to {max(sl):.2f}",flush=True)
sl=[np.polyfit(xs,curve(A,B,N=20000,seed=s),1)[0] for s in range(10)]
print(f"ties kept, 10 seeds: median {np.median(sl):.2f}, range {min(sl):.2f} to {max(sl):.2f}")
