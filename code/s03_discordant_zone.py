"""
s03_discordant_zone.py   Amendment 2, analyses D1-D5.
Specification frozen 2026-10-13 15:45 before any outcome comparison was computed.
"""
import time, warnings
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"
CUTS={"P1":(64,77), "P2":(59,74)}      # (c_low, c_high) from A3, frozen in Amendment 2
MARGIN=(0.67,1.50)

def stage_group(c,s):
    s=str(s).upper()
    if c=="TCGA":
        for k,v in [("STAGE IV","III-IV"),("STAGE III","III-IV"),("STAGE II","II"),("STAGE I","I")]:
            if s.startswith(k): return v
        return "unk"
    try: return {0:"I",1:"I",2:"II"}.get(int(float(s)),"III-IV")
    except: return "unk"

def cox(time_,event,X):
    ok=X.notna().all(axis=1).values & ~np.isnan(time_) & (time_>=0)
    m=PHReg(time_[ok],X.values[ok],status=event[ok]).fit(disp=False)
    ci=np.exp(m.conf_int())
    return dict(n=int(ok.sum()),ev=int(event[ok].sum()),
                hr=float(np.exp(m.params[0])),lo=float(ci[0][0]),hi=float(ci[0][1]),
                p=float(m.pvalues[0]),model=m,ok=ok)

out=[]
for cohort,f in [("TCGA","cohort_tcga.csv"),("METABRIC","cohort_metabric.csv")]:
    d=pd.read_csv(f"{R}/{f}",low_memory=False)
    d["STAGE_G"]=[stage_group(cohort,s) for s in d.get("AJCC_PATHOLOGIC_TUMOR_STAGE",d.get("TUMOR_STAGE"))]
    d=d[d["TIME"].notna()&(d["TIME"]>=0)].reset_index(drop=True)
    stages=sorted(set(d["STAGE_G"]))[1:]
    log("="*70); log(f"{cohort}  n={len(d)}  events={int(d['EVENT'].sum())}  endpoint={d['ENDPOINT'].iloc[0]}")
    for score,(cl,ch) in CUTS.items():
        v=d[score].values
        tl,th=np.nanpercentile(v,cl),np.nanpercentile(v,ch)
        grp=np.where(v<=tl,"STABLE_A",np.where(v<=th,"DISCORDANT","STABLE_B"))
        d["_g"]=grp
        n_disc=int((grp=="DISCORDANT").sum()); pct=100*n_disc/len(grp)
        log(f"\n--- {score}  zone = {cl}th to {ch}th pct ---")
        log(f"  [D5] group sizes: STABLE_A={int((grp=='STABLE_A').sum())}  "
            f"DISCORDANT={n_disc} ({pct:.1f}%)  STABLE_B={int((grp=='STABLE_B').sum())}")
        ev_d=int(d.loc[grp=='DISCORDANT','EVENT'].sum())
        log(f"       events in discordant zone: {ev_d}")

        def Xbase(sub):
            """Adjustment covariates. Stage dummies are dropped when a level is absent,
            constant, or carries fewer than 5 events inside the subset, which otherwise
            makes the Cox information matrix singular in small strata."""
            X=pd.DataFrame(index=sub.index); X["age"]=sub["AGE_N"].values
            for s_ in stages:
                col=(sub["STAGE_G"]==s_).astype(float).values
                ev=int(sub["EVENT"].values[col==1].sum())
                if 0 < col.sum() < len(col) and ev >= 5:
                    X[f"st_{s_}"]=col
            return X
        # D1: each stable group vs DISCORDANT
        for g in ["STABLE_A","STABLE_B"]:
            sub=d[d["_g"].isin([g,"DISCORDANT"])]
            X=Xbase(sub); X.insert(0,"grp",(sub["_g"]==g).astype(float).values)
            r=cox(sub["TIME"].values,sub["EVENT"].values,X)
            inside = MARGIN[0]<=r["lo"] and r["hi"]<=MARGIN[1]
            log(f"  [D1] {g:9s} vs DISCORDANT: HR={r['hr']:.2f} [{r['lo']:.2f}, {r['hi']:.2f}] "
                f"p={r['p']:.3g}  n={r['n']} ev={r['ev']}  {'(within margin)' if inside else ''}")
            out.append(dict(cohort=cohort,score=score,test=f"D1_{g}_vs_DISC",**{k:r[k] for k in ('n','ev','hr','lo','hi','p')}))
        # D3: continuous score WITHIN the zone
        sub=d[d["_g"]=="DISCORDANT"]
        X=Xbase(sub); X.insert(0,"score",stats.zscore(sub[score].values,nan_policy="omit"))
        r=cox(sub["TIME"].values,sub["EVENT"].values,X)
        inside = MARGIN[0]<=r["lo"] and r["hi"]<=MARGIN[1]
        log(f"  [D3] continuous {score} INSIDE zone: HR per SD = {r['hr']:.2f} "
            f"[{r['lo']:.2f}, {r['hi']:.2f}] p={r['p']:.3g}  n={r['n']} ev={r['ev']}")
        log(f"       -> p>0.05: {r['p']>0.05} | CI within [0.67,1.50]: {inside}")
        out.append(dict(cohort=cohort,score=score,test="D3_continuous_in_zone",**{k:r[k] for k in ('n','ev','hr','lo','hi','p')}))
        # D3b: same model in the whole cohort, for contrast
        X=Xbase(d); X.insert(0,"score",stats.zscore(d[score].values,nan_policy="omit"))
        rw=cox(d["TIME"].values,d["EVENT"].values,X)
        log(f"  [D3b] continuous {score} in WHOLE cohort: HR per SD = {rw['hr']:.2f} "
            f"[{rw['lo']:.2f}, {rw['hi']:.2f}] p={rw['p']:.3g}")
        out.append(dict(cohort=cohort,score=score,test="D3b_continuous_whole_cohort",**{k:rw[k] for k in ('n','ev','hr','lo','hi','p')}))
        # D4: trend across ordered groups
        order={"STABLE_A":0,"DISCORDANT":1,"STABLE_B":2}
        X=Xbase(d); X.insert(0,"trend",[order[g] for g in d["_g"]])
        rt=cox(d["TIME"].values,d["EVENT"].values,X)
        log(f"  [D4] trend across 3 groups: HR per step = {rt['hr']:.2f} "
            f"[{rt['lo']:.2f}, {rt['hi']:.2f}] p={rt['p']:.3g}")
        out.append(dict(cohort=cohort,score=score,test="D4_trend",**{k:rt[k] for k in ('n','ev','hr','lo','hi','p')}))
        out.append(dict(cohort=cohort,score=score,test="D5_zone_size",n=n_disc,ev=ev_d,
                        hr=pct,lo=np.nan,hi=np.nan,p=np.nan))

df=pd.DataFrame(out); df.to_csv(f"{R}/D_discordant_zone.csv",index=False)
# BH within cohort over D1/D3/D4 family
log("\n"+"="*70); log("BH-adjusted p-values (family = D1, D3, D4 within cohort)")
for c,g in df[df.test.str.startswith(("D1","D3_","D4"))].groupby("cohort"):
    p=g.p.values; o=np.argsort(p); adj=np.empty_like(p); m=len(p)
    prev=1.0
    for i in range(m-1,-1,-1):
        prev=min(prev,p[o[i]]*m/(i+1)); adj[o[i]]=prev
    for (idx,row),a in zip(g.iterrows(),adj):
        log(f"  {c:9s} {row.score} {row.test:28s} p={row.p:.3g}  BH={a:.3g}")
log("done.")
