"""s08_prevalence_mechanism.py  Amendment 6, analyses E1-E3, all three cohorts."""
import time, warnings
import numpy as np, pandas as pd
from sklearn.metrics import roc_curve
warnings.filterwarnings("ignore")
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"; rng=np.random.default_rng(0)
COH={"TCGA":"cohort_tcga.csv","METABRIC":"cohort_metabric.csv","SCAN-B":"cohort_scanb.csv"}

def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean())
    return (po-pe)/(1-pe) if pe<1 else np.nan
def youden_thr(x,y):
    fpr,tpr,thr=roc_curve(y,x); j=np.argmax(tpr-fpr); return thr[j]
def kappa_opt_pct(x,y,ref):
    """kappa-optimal percentile, percentile taken over `ref` values"""
    ks=[kappa(x>np.percentile(ref,g),y) for g in range(5,96)]
    return 5+int(np.nanargmax(ks))

e1=[]; e3=[]
for cname,f in COH.items():
    d=pd.read_csv(f"{R}/{f}",low_memory=False)
    for s in ["P2","P1"]:
        full=d[s].values
        m=d.PAM50.isin(["LumA","LumB"]).values
        x=full[m]; y=(d.PAM50.values[m]=="LumB").astype(int)
        A=x[y==0]; share=y.mean()
        def scales(t,AA,F):
            return (100*np.mean(F<=t), 100*np.mean(AA<=t), (t-AA.mean())/AA.std(ddof=1))
        ty=youden_thr(x,y); a_,b_,c_=scales(ty,A,full)
        kp=kappa_opt_pct(x,y,full); tk=np.percentile(full,kp); ka,kb,kc=scales(tk,A,full)
        boot=[]
        for bi in range(2000):
            if bi and bi%1000==0: log(f"   {cname} {s} bootstrap {bi}/2000")
            ii=rng.integers(0,len(x),len(x)); ff=full[rng.integers(0,len(full),len(full))]
            xx=x[ii]; yy=y[ii]; AA=xx[yy==0]
            if yy.min()==yy.max(): continue
            t=youden_thr(xx,yy); boot.append(scales(t,AA,ff))
        boot=np.array(boot); lo=np.percentile(boot,2.5,axis=0); hi=np.percentile(boot,97.5,axis=0)
        e1.append(dict(cohort=cname,score=s,lumB_share=share,
                       youden_pct_full=a_,youden_pct_full_lo=lo[0],youden_pct_full_hi=hi[0],
                       youden_q_lumA=b_,youden_q_lumA_lo=lo[1],youden_q_lumA_hi=hi[1],
                       youden_z_lumA=c_,youden_z_lumA_lo=lo[2],youden_z_lumA_hi=hi[2],
                       kappa_pct_full=kp,kappa_q_lumA=kb,kappa_z_lumA=kc))
        log(f"[E1] {cname:8s} {s}: lumB share {share:.1%} | Youden: full-pct {a_:.0f} [{lo[0]:.0f},{hi[0]:.0f}]  "
            f"LumA-quantile {b_:.0f} [{lo[1]:.0f},{hi[1]:.0f}]  LumA-z {c_:.2f} [{lo[2]:.2f},{hi[2]:.2f}] | "
            f"kappa-opt: full-pct {kp}  LumA-q {kb:.0f}  LumA-z {kc:.2f}")
        # E3 within-cohort prevalence resampling
        B=x[y==1]; N=len(x)
        for prev in [15,20,25,30,35,40,45]:
            nb=int(round(N*prev/100)); na=N-nb; kk=[]; yq=[]
            for r in range(200):
                xa=rng.choice(A,na,replace=True); xb=rng.choice(B,nb,replace=True)
                xx=np.r_[xa,xb]; yy=np.r_[np.zeros(na,int),np.ones(nb,int)]
                kk.append(kappa_opt_pct(xx,yy,xx))
                t=youden_thr(xx,yy); yq.append(100*np.mean(xa<=t))
            e3.append(dict(cohort=cname,score=s,prev=prev,kappa_pct=np.median(kk),youden_q_lumA=np.median(yq)))
        sub=pd.DataFrame([r for r in e3 if r["cohort"]==cname and r["score"]==s])
        sk=np.polyfit(100-sub.prev,sub.kappa_pct,1)[0]; sy=np.polyfit(100-sub.prev,sub.youden_q_lumA,1)[0]
        log(f"[E3] {cname:8s} {s}: slope of kappa-optimal pct on (100-prev) = {sk:.2f}; "
            f"slope of Youden LumA-quantile = {sy:.2f}")
pd.DataFrame(e1).to_csv(f"{R}/E1_youden_scales.csv",index=False)
pd.DataFrame(e3).to_csv(f"{R}/E3_prevalence_resampling.csv",index=False)
log("done.")
