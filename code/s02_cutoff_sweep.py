"""
s02_cutoff_sweep.py   Analyses A1-A4 of the frozen protocol, both cohorts, both scores.
A1 distribution | A2 reclassification | A3 agreement with PAM50 | A4 prognostic sweep
"""
import time, warnings
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"; rng=np.random.default_rng(0)
GRID=np.arange(5,96,1)

def kappa(a,b):
    a=np.asarray(a); b=np.asarray(b)
    n=len(a); 
    if n==0: return np.nan
    po=(a==b).mean()
    la=np.unique(np.concatenate([a,b]))
    pe=sum((a==k).mean()*(b==k).mean() for k in la)
    return (po-pe)/(1-pe) if pe<1 else np.nan

def stage_group(c,s):
    s=str(s).upper()
    if c=="TCGA":
        for k,v in [("STAGE IV","III-IV"),("STAGE III","III-IV"),("STAGE II","II"),("STAGE I","I")]:
            if s.startswith(k): return v
        return "unk"
    try:
        f=float(s)
        return {0:"I",1:"I",2:"II"}.get(int(f),"III-IV")
    except: return "unk"

rows_a2=[]; rows_a3=[]; rows_a4=[]; rows_a1=[]
for cohort,f in [("TCGA","cohort_tcga.csv"),("METABRIC","cohort_metabric.csv")]:
    d=pd.read_csv(f"{R}/{f}",low_memory=False)
    d["STAGE_G"]=[stage_group(cohort,s) for s in d.get("AJCC_PATHOLOGIC_TUMOR_STAGE", d.get("TUMOR_STAGE"))]
    d=d[d["TIME"].notna() & (d["TIME"]>=0)]
    log(f"{'='*55}\n{cohort}: n={len(d)}, events={int(d['EVENT'].sum())}, endpoint={d['ENDPOINT'].iloc[0]}")
    log(f"  stage: {d['STAGE_G'].value_counts().to_dict()}")
    for score in ["P1","P2"]:
        v=d[score].values
        # ---- A1 distribution ----
        dip_sk=stats.skew(v[~np.isnan(v)]); kur=stats.kurtosis(v[~np.isnan(v)])
        sw=stats.shapiro(v[~np.isnan(v)][:4500])
        rows_a1.append(dict(cohort=cohort,score=score,n=len(v),skew=dip_sk,kurtosis=kur,
                            shapiro_p=sw.pvalue,q05=np.nanpercentile(v,5),q50=np.nanpercentile(v,50),
                            q95=np.nanpercentile(v,95)))
        log(f"  [A1] {score}: skew={dip_sk:+.2f} kurtosis={kur:+.2f} shapiro p={sw.pvalue:.2g}")
        # ---- sweep ----
        lum=d["PAM50"].isin(["LumA","LumB"]).values
        pam_b=(d["PAM50"]=="LumB").values
        best=(-1,None)
        for g in GRID:
            thr=np.nanpercentile(v,g)
            callB=(v>thr)
            rows_a2.append(dict(cohort=cohort,score=score,pct=g,thr=thr,
                                prop_lumB=float(np.nanmean(callB))))
            k=kappa(callB[lum],pam_b[lum])
            rows_a3.append(dict(cohort=cohort,score=score,pct=g,kappa=k,n_lum=int(lum.sum())))
            if k>best[0]: best=(k,g)
            # A4 Cox
            try:
                X=pd.DataFrame({"lumB":callB.astype(float),"age":d["AGE_N"].values})
                for s in sorted(set(d["STAGE_G"]))[1:]:
                    X[f"st_{s}"]=(d["STAGE_G"]==s).astype(float)
                ok=X.notna().all(axis=1).values
                mod=PHReg(d["TIME"].values[ok],X.values[ok],status=d["EVENT"].values[ok]).fit(disp=False)
                hr=float(np.exp(mod.params[0])); lo,hi=np.exp(mod.conf_int()[0])
                p=float(mod.pvalues[0])
            except Exception:
                hr=lo=hi=p=np.nan
            rows_a4.append(dict(cohort=cohort,score=score,pct=g,HR=hr,lo=lo,hi=hi,p=p))
        # bootstrap CI on kappa-optimal percentile
        opts=[]
        idx=np.arange(len(d))
        for b in range(2000):
            if b and b%500==0: log(f"    bootstrap {b}/2000 ({score})")
            s_=rng.choice(idx,len(idx),replace=True)
            vv=v[s_]; ll=lum[s_]; pb=pam_b[s_]
            ks=[kappa((vv>np.nanpercentile(vv,g))[ll],pb[ll]) for g in GRID]
            opts.append(GRID[int(np.nanargmax(ks))])
        ci=np.percentile(opts,[2.5,97.5])
        log(f"  [A3] {score}: peak kappa={best[0]:.3f} at {best[1]}th pct; "
            f"bootstrap 95% CI for optimum = [{ci[0]:.0f}, {ci[1]:.0f}] pct")
        rows_a3.append(dict(cohort=cohort,score=score,pct=-1,kappa=best[0],n_lum=int(lum.sum()),
                            opt_pct=best[1],ci_lo=ci[0],ci_hi=ci[1]))

for nm,rr in [("A1_distribution",rows_a1),("A2_reclassification",rows_a2),
              ("A3_agreement",rows_a3),("A4_prognostic",rows_a4)]:
    pd.DataFrame(rr).to_csv(f"{R}/{nm}.csv",index=False); log(f"wrote {nm}.csv")
log("done.")
