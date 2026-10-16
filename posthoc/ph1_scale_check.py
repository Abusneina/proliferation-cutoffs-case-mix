"""ph1_scale_check.py  POST HOC (2026-10-16), prompted by external review.
Q1: observed kappa-optimal cut-off as a percentile of the LUMINAL set (A+B) vs the stratum.
Q2: in the Amendment 6 resampling design, how far does the kappa-optimal cut-off move in RAW
    units (expressed as luminal A quantile, the scale used for Youden), and what slope would a
    FIXED raw cut-off produce on the luminal-set percentile scale (scale artifact)?"""
import time, numpy as np, pandas as pd
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"; rng=np.random.default_rng(20261016)
COH={"TCGA":"cohort_tcga.csv","METABRIC":"cohort_metabric.csv","SCAN-B":"cohort_scanb.csv"}
def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean())
    return (po-pe)/(1-pe) if pe<1 else np.nan
def kopt_thr(x,y,ref):
    th=[np.percentile(ref,g) for g in range(5,96)]
    ks=[kappa((x>t).astype(int),y) for t in th]; i=int(np.nanargmax(ks)); return th[i],5+i
rows=[]; res=[]
for cname,f in COH.items():
    d=pd.read_csv(f"{R}/{f}",low_memory=False)
    for s in ["P2","P1"]:
        full=d[s].values; m=d.PAM50.isin(["LumA","LumB"]).values
        x=full[m]; y=(d.PAM50.values[m]=="LumB").astype(int); A=x[y==0]; B=x[y==1]; sh=100*y.mean()
        t,pfull=kopt_thr(x,y,full)
        plum=100*np.mean(x<=t); qA=100*np.mean(A<=t); qB=100*np.mean(B<=t)
        stratum_share=100*y.sum()/len(full)
        rows.append(dict(cohort=cname,score=s,lumB_share_luminal=round(sh,1),lumB_share_stratum=round(stratum_share,1),
            kopt_pct_stratum=pfull,expected_stratum=round(100-stratum_share,1),kopt_pct_luminal=round(plum,1),
            expected_luminal=round(100-sh,1),kopt_qA=round(qA,1),kopt_qB=round(qB,1),fixed_cutoff_slope=round((qA-qB)/100,2)))
        log(f"{cname} {s}: luminal-set pct {plum:.1f} vs 100-share {100-sh:.1f} | stratum pct {pfull} vs {100-stratum_share:.1f}")
        N=len(x)
        for prev in [15,20,25,30,35,40,45]:
            nb=int(round(N*prev/100)); na=N-nb; pq=[]; pp=[]
            for r in range(200):
                xa=rng.choice(A,na,replace=True); xb=rng.choice(B,nb,replace=True)
                xx=np.r_[xa,xb]; yy=np.r_[np.zeros(na,int),np.ones(nb,int)]
                tt,pc=kopt_thr(xx,yy,xx); pp.append(pc); pq.append(100*np.mean(A<=tt))
            res.append(dict(cohort=cname,score=s,prev=prev,kopt_pct_luminal=np.median(pp),kopt_qA_fullA=np.median(pq)))
        sub=pd.DataFrame([r for r in res if r["cohort"]==cname and r["score"]==s])
        s1=np.polyfit(100-sub.prev,sub.kopt_pct_luminal,1)[0]; s2=np.polyfit(100-sub.prev,sub.kopt_qA_fullA,1)[0]
        rows[-1].update(slope_pct_luminal=round(s1,2),slope_qA_raw=round(s2,2),
                        qA_at15=round(sub.kopt_qA_fullA.iloc[0],1),qA_at45=round(sub.kopt_qA_fullA.iloc[-1],1))
        log(f"   resampling: slope on luminal pct {s1:.2f}; slope in raw units (luminal A quantile) {s2:.2f}; fixed-cutoff slope {rows[-1]['fixed_cutoff_slope']}")
out=pd.DataFrame(rows); out.to_csv("/home/claude/work/posthoc/PH1_scale_check.csv",index=False)
pd.DataFrame(res).to_csv("/home/claude/work/posthoc/PH1_resampling.csv",index=False)
print(out.to_string()); log("done")
