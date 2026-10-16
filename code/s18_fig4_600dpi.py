import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
exec(open("s11_gse81538_amendment7.py").read().split("def kappa")[0].replace("res={}",""))
def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe)
def kopt_pct(x,y):
    cs=np.unique(np.percentile(x,np.arange(5,96))); ks=[kappa((x>c).astype(int),y) for c in cs]
    return 100*np.mean(x<=cs[int(np.argmax(ks))])
PR=[15,20,25,30,35,40,45]
def curve(A,B,N=40000,seed=1):
    r=np.random.default_rng(seed); out=[]
    for p in PR:
        nb=int(N*p/100); x=np.r_[r.choice(A,N-nb),r.choice(B,nb)]; y=np.r_[np.zeros(N-nb),np.ones(nb)]; out.append(kopt_pct(x,y))
    return np.array(out)
r=np.random.default_rng(0)
el=meta[(meta.ER.isin([1,2,3]))&(meta.HER2==0)&meta.PAM50.isin(["LumA","LumB"])].dropna(subset=["K"])
A=el.K[el.PAM50=="LumA"].values; B=el.K[el.PAM50=="LumB"].values
c_norm=curve(r.normal(0,1,40000),r.normal(2,1,40000))
c_tie=curve(A,B)
c_jit=curve(A+r.uniform(-2.5,2.5,len(A)),B+r.uniform(-2.5,2.5,len(B)))
d=pd.read_csv("/home/claude/work/results/A7_resampling.csv"); d=d[(d.analysis=="primary")&(d.measure=="K")]
x=100-np.array(PR)
fig,ax=plt.subplots(1,2,figsize=(7.2,3.1))
a=ax[0]; a.plot([50,85],[50,85],ls=":",c="grey",lw=1,label="Slope 1")
a.plot(x,c_norm,"o-",c="#238b45",ms=4,lw=1.2,label="Simulated, continuous (slope 0.99)")
a.plot(x,c_tie,"^-.",c="#6a3d9a",ms=4,lw=1.2,label="Observed K distributions, N = 40,000 (0.54)")
a.plot(x,d.kappa_pct.values,"D-",c="black",ms=3.5,lw=1.0,label="Registered test, n = 232 (0.62)")
a.set_xlabel("100 minus imposed luminal B share (%)",fontsize=8); a.set_ylabel("Kappa-optimal cut-off (percentile)",fontsize=8)
a.legend(fontsize=6,loc="upper left",frameon=False); a.tick_params(labelsize=8); a.text(0.97,0.04,"A",transform=a.transAxes,fontsize=10,fontweight="bold",ha="right")
b=ax[1]; b.plot(x,d.youden_q.values,"D-",c="black",ms=3.5,lw=1.0,label="Youden boundary, consensus Ki-67")
b.set_ylim(50,100); b.set_xlabel("100 minus imposed luminal B share (%)",fontsize=8); b.set_ylabel("Youden cut-off (quantile of luminal A)",fontsize=8)
b.legend(fontsize=6.5,loc="lower left",frameon=False); b.tick_params(labelsize=8); b.text(0.97,0.04,"B",transform=b.transAxes,fontsize=10,fontweight="bold",ha="right")
for s in ("top","right"):
    a.spines[s].set_visible(False); b.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("/home/claude/work/figures/2026-10-14_1520_Fig4_GSE81538-ties.png",dpi=600); print(c_norm.round(1),c_jit.round(1),c_tie.round(1),d.kappa_pct.values.round(1))
