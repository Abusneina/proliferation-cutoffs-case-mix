"""s07_scanb_confirmatory.py
SCAN-B: cohort build, P1/P2, A1-A6 (Amendment 5), C1/C2/C3 (Amendment 3) with the
Amendment 4 adjustment set, and the Amendment 4 pooled estimates. Progress printed throughout."""
import time, warnings
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"; EXPR="/home/claude/raw/scanb_expr/scanb_gene_expression.csv"
GENE_FILE="/home/claude/work/protocol/2026-10-13_1515_proliferation_gene_list_FROZEN.txt"
rng=np.random.default_rng(0); GRID=np.arange(5,96,1)
CUTS={"P1":(64,77),"P2":(59,74)}; KNOT={"P1":64,"P2":59}; MARGIN=(0.67,1.50)
OPT_PREV={"TCGA":{"P1":77,"P2":74},"METABRIC":{"P1":64,"P2":59}}

# ---------- frozen gene list ----------
p2=[];inp=False
for l in open(GENE_FILE):
    l=l.strip()
    if l=="##P2_START": inp=True; continue
    if l=="##P2_END": inp=False; continue
    if inp and l and not l.startswith("#"): p2.append(l)
assert len(p2)==18 and "MKI67" not in p2
ALIAS={"ORC6L":"ORC6"}
want={"MKI67"}|{ALIAS.get(g,g) for g in p2}

# ---------- clinical ----------
c=pd.read_csv(f"{R}/scanb_clinical_raw.csv",dtype=str)
c=c[c["is_repl"]!="True"]
log(f"non-replicate tumors: {len(c)}")
att=[("start: non-replicate tumors",len(c))]
c=c[c["er status"]=="1"]; att.append(("ER positive",len(c)))
c=c[c["her2 status"]=="0"]; att.append(("HER2 negative",len(c)))
c=c[c["overall survival days"].ne("NA") & c["overall survival event"].isin(["0","1"])]; att.append(("OS time and event present",len(c)))

# ---------- expression (stream, keep wanted genes) ----------
log("streaming SCAN-B expression matrix ...")
keep={}
with open(EXPR) as fh:
    hdr=[x.strip('"') for x in fh.readline().rstrip("\n").split(",")]
    samples=hdr[1:]
    for n,line in enumerate(fh,1):
        if n%10000==0: log(f"  {n} rows scanned, {len(keep)}/{len(want)} genes found")
        sym=line[:line.find(",")].strip('"')
        if sym in want: keep[sym]=np.array(line.rstrip("\n").split(",")[1:],dtype=float)
log(f"found {len(keep)}/{len(want)} genes")
E=pd.DataFrame(keep,index=samples)
c=c[c["title"].isin(E.index)]; att.append(("expression available",len(c)))
for a,n in att: log(f"  {a:<34} {n}")
E=E.loc[c["title"]]
def z(v): v=np.asarray(v,float); return (v-np.nanmean(v))/np.nanstd(v,ddof=1)
d=pd.DataFrame({"sample":c["title"].values})
d["P1"]=z(E["MKI67"].values)
d["P2"]=np.nanmean(np.vstack([z(E[ALIAS.get(g,g)].values) for g in p2]),axis=0)
d["PAM50"]=c["pam50 subtype"].values
d["TIME"]=pd.to_numeric(c["overall survival days"].values)/30.4375
d["EVENT"]=pd.to_numeric(c["overall survival event"].values).astype(int)
d["AGE_N"]=pd.to_numeric(c["age at diagnosis"].values,errors="coerce")
d["SIZE"]=pd.to_numeric(c["tumor size"].values,errors="coerce")
d["NODE"]=c["lymph node group"].values
d["NHG"]=c["nhg"].values
d["KI67"]=c["ki67 status"].values
d["CHEMO"]=c["chemo treated"].values
d.to_csv(f"{R}/cohort_scanb.csv",index=False)
log(f"SCAN-B cohort: n={len(d)}, OS events={int(d.EVENT.sum())}")

def kappa(a,b):
    a=np.asarray(a);b=np.asarray(b)
    if len(a)==0: return np.nan
    po=(a==b).mean(); la=np.unique(np.concatenate([a,b])); pe=sum((a==k).mean()*(b==k).mean() for k in la)
    return (po-pe)/(1-pe) if pe<1 else np.nan

def covars(sub,grade=False):
    X=pd.DataFrame(index=sub.index); X["age"]=sub.AGE_N.values; X["size"]=sub.SIZE.values
    for lv in ["SubMicroMet","1to3","4toX"]:
        col=(sub.NODE==lv).astype(float).values
        if 0<col.sum()<len(col) and sub.EVENT.values[col==1].sum()>=3: X[f"n_{lv}"]=col
    X.loc[sub.NODE.isin(["NA"]).values|sub.NODE.isna().values,"age"]=np.nan
    if grade:
        for lv in ["G2","G3"]:
            X[f"g_{lv}"]=(sub.NHG==lv).astype(float).values
        X.loc[(sub.NHG=="NA").values,"age"]=np.nan
    return X
def cox(sub,expo,grade=False):
    X=covars(sub,grade); X.insert(0,"x",expo)
    ok=X.notna().all(axis=1).values
    m=PHReg(sub.TIME.values[ok],X.values[ok],status=sub.EVENT.values[ok]).fit(disp=False)
    ci=np.exp(m.conf_int()[0])
    return dict(n=int(ok.sum()),ev=int(sub.EVENT.values[ok].sum()),hr=float(np.exp(m.params[0])),
                lo=float(ci[0]),hi=float(ci[1]),p=float(m.pvalues[0]),b=float(m.params[0]),se=float(m.bse[0]),model=m)

out=[]
lum=d.PAM50.isin(["LumA","LumB"]).values; pb=(d.PAM50=="LumB").values
for s in ["P1","P2"]:
    v=d[s].values
    sk=stats.skew(v); out.append(dict(block="A1",score=s,key="skew",val=sk))
    ks=[kappa((v>np.nanpercentile(v,g))[lum],pb[lum]) for g in GRID]
    gi=int(np.nanargmax(ks)); opt=GRID[gi]
    opts=[]
    idx=np.arange(len(d))
    for b in range(2000):
        if b and b%500==0: log(f"  bootstrap {b}/2000 ({s})")
        si=rng.choice(idx,len(idx),replace=True); vv=v[si]; ll=lum[si]; pp=pb[si]
        kk=[kappa((vv>np.nanpercentile(vv,g))[ll],pp[ll]) for g in GRID]; opts.append(GRID[int(np.nanargmax(kk))])
    ci=np.percentile(opts,[2.5,97.5])
    log(f"[A3] {s}: peak kappa {ks[gi]:.3f} at {opt}th pct, bootstrap 95% CI [{ci[0]:.0f}, {ci[1]:.0f}], n_luminal={int(lum.sum())}")
    out.append(dict(block="A3",score=s,key="opt",val=opt,lo=ci[0],hi=ci[1],kappa=ks[gi],n=int(lum.sum())))
    for g,k in zip(GRID,ks): out.append(dict(block="A3grid",score=s,key=int(g),val=k))
    out.append(dict(block="A2",score=s,key="prev_at_own_opt",val=float(np.mean(v>np.nanpercentile(v,opt)))))
    # A5 transfer into SCAN-B
    for src in ["TCGA","METABRIC"]:
        pr=OPT_PREV[src][s]
        k_pct=kappa((v>np.nanpercentile(v,pr))[lum],pb[lum])
        src_d=pd.read_csv(f"{R}/cohort_{src.lower()}.csv",low_memory=False)
        thr_abs=np.nanpercentile(src_d[s].values,pr)
        k_abs=kappa((v>thr_abs)[lum],pb[lum])
        log(f"[A5] {s}: {src} optimum {pr}th -> SCAN-B: kappa pct {k_pct:.3f} (loss {ks[gi]-k_pct:+.3f}), "
            f"abs {k_abs:.3f} (loss {ks[gi]-k_abs:+.3f})")
        out.append(dict(block="A5",score=s,key=f"{src}_pct",val=k_pct,kappa=ks[gi]))
        out.append(dict(block="A5",score=s,key=f"{src}_abs",val=k_abs,kappa=ks[gi]))

    # ---------- C1 ----------
    cl,ch=CUTS[s]; tl,th=np.nanpercentile(v,cl),np.nanpercentile(v,ch)
    g=np.where(v<=tl,"STABLE_A",np.where(v<=th,"DISCORDANT","STABLE_B")); d["_g"]=g
    log(f"[C1] {s} zone {cl}-{ch}th: STABLE_A={int((g=='STABLE_A').sum())} DISC={int((g=='DISCORDANT').sum())} "
        f"STABLE_B={int((g=='STABLE_B').sum())}; events in zone={int(d.EVENT[g=='DISCORDANT'].sum())}")
    for grade in [False,True]:
        for grp in ["STABLE_A","STABLE_B"]:
            sub=d[d._g.isin([grp,"DISCORDANT"])]
            r=cox(sub,(sub._g==grp).astype(float).values,grade)
            tag="C1a" if grp=="STABLE_A" else "C1b"
            inside=MARGIN[0]<=r["lo"] and r["hi"]<=MARGIN[1]
            verdict=("" if tag=="C1a" else ("B-like confirmed" if inside else ("refuted" if (r['lo']>1 or r['hi']<1) else "inconclusive")))
            log(f"   {tag}{' [grade-adj]' if grade else ''} {grp} vs DISC: HR {r['hr']:.2f} [{r['lo']:.2f}, {r['hi']:.2f}] "
                f"p={r['p']:.3g} n={r['n']} ev={r['ev']} {verdict}")
            out.append(dict(block=tag+("_grade" if grade else ""),score=s,key=grp,val=r["hr"],lo=r["lo"],hi=r["hi"],p=r["p"],
                            b=r["b"],se=r["se"],n=r["n"],ev=r["ev"],verdict=verdict))
    # ---------- C2 piecewise ----------
    zW=z(v); k=np.nanpercentile(zW,KNOT[s])
    X=covars(d); X.insert(0,"hinge",np.maximum(zW-k,0)); X.insert(0,"lin",zW)
    ok=X.notna().all(axis=1).values
    m=PHReg(d.TIME.values[ok],X.values[ok],status=d.EVENT.values[ok]).fit(disp=False)
    bb=m.params; V=m.cov_params()
    below=(bb[0],np.sqrt(V[0,0])); above=(bb[0]+bb[1],np.sqrt(V[0,0]+V[1,1]+2*V[0,1])); diff=(bb[1],np.sqrt(V[1,1]))
    for nm,(e,se) in [("below",below),("above",above),("diff",diff)]:
        lo,hi=np.exp(e-1.96*se),np.exp(e+1.96*se); p=2*(1-stats.norm.cdf(abs(e/se)))
        out.append(dict(block="C2",score=s,key=nm,val=np.exp(e),lo=lo,hi=hi,p=p))
    conf = diff[0] < 0 and (diff[0]+1.96*diff[1]) < 0
    log(f"[C2] {s} knot {KNOT[s]}th: slope below HR/SD {np.exp(below[0]):.2f}, above {np.exp(above[0]):.2f}, "
        f"ratio {np.exp(diff[0]):.2f} [{np.exp(diff[0]-1.96*diff[1]):.2f}, {np.exp(diff[0]+1.96*diff[1]):.2f}] "
        f"-> {'CONFIRMED' if conf else 'not confirmed'}")
    # ---------- C3 Ki-67 bridge ----------
    kk=d.KI67.isin(["0","1"]).values; kp=(d.KI67=="1").values
    for pc in [cl,ch]:
        kap=kappa((v>np.nanpercentile(v,pc))[kk],kp[kk])
        out.append(dict(block="C3",score=s,key=f"kappa_vs_pathKi67_at_{pc}th",val=kap,n=int(kk.sum())))
        log(f"[C3] {s}: kappa vs pathology Ki-67 at {pc}th = {kap:.3f} (n={int(kk.sum())})")
    for grp in ["STABLE_A","DISCORDANT","STABLE_B"]:
        mm=(d._g==grp).values&kk
        out.append(dict(block="C3",score=s,key=f"pctKi67high_{grp}",val=float(kp[mm].mean()),n=int(mm.sum())))
        log(f"     pathology Ki-67 high in {grp}: {kp[mm].mean():.1%} (n={int(mm.sum())})")

res=pd.DataFrame(out); res.to_csv(f"{R}/SCANB_results.csv",index=False)

# ---------- Amendment 4 pooled ----------
log("="*60); log("Amendment 4 pooled estimates (P2 primary)")
D=pd.read_csv(f"{R}/D_discordant_zone.csv")
def from_D(cohort,s,grp):
    r=D[(D.cohort==cohort)&(D.score==s)&(D.test==f"D1_{grp}_vs_DISC")].iloc[0]
    b=np.log(r.hr); se=(np.log(r.hi)-np.log(r.lo))/(2*1.96); return b,se
pool=[]
for s in ["P2","P1"]:
    for grp,tag in [("STABLE_A","C1a"),("STABLE_B","C1b")]:
        sc=res[(res.block==tag)&(res.score==s)].iloc[0]
        ests={"METABRIC":from_D("METABRIC",s,grp),"SCAN-B":(sc.b,sc.se),"TCGA":from_D("TCGA",s,grp)}
        for setname,members in [("METABRIC+SCAN-B",["METABRIC","SCAN-B"]),("all three",["METABRIC","SCAN-B","TCGA"])]:
            b=np.array([ests[m][0] for m in members]); se=np.array([ests[m][1] for m in members]); w=1/se**2
            bf=(w*b).sum()/w.sum(); sef=np.sqrt(1/w.sum())
            Q=(w*(b-bf)**2).sum(); dfq=len(b)-1; I2=max(0,(Q-dfq)/Q) if Q>0 else 0
            tau2=max(0,(Q-dfq)/(w.sum()-(w**2).sum()/w.sum()))
            wr=1/(se**2+tau2); br=(wr*b).sum()/wr.sum(); ser=np.sqrt(1/wr.sum())
            for mth,(e,sE) in [("fixed",(bf,sef)),("random",(br,ser))]:
                lo,hi=np.exp(e-1.96*sE),np.exp(e+1.96*sE)
                verdict=""
                if tag=="C1b": verdict="B-like confirmed" if (MARGIN[0]<=lo and hi<=MARGIN[1]) else ("refuted" if (lo>1 or hi<1) else "inconclusive")
                log(f"  {s} {tag} {setname:<16} {mth:<6}: HR {np.exp(e):.2f} [{lo:.2f}, {hi:.2f}] I2={I2:.0%} {verdict}")
                pool.append(dict(score=s,test=tag,set=setname,method=mth,hr=np.exp(e),lo=lo,hi=hi,I2=I2,verdict=verdict))
pd.DataFrame(pool).to_csv(f"{R}/pooled_C1.csv",index=False)
log("done.")
