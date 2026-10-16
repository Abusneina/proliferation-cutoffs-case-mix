"""s11_gse81538_amendment7.py  Amendment 7 (frozen 2026-10-14 12:16), GSE81538. Run after OSF registration.
Implementation choices fixed before the run (not stated in the amendment):
 * classification K > c; candidates = distinct observed values; kappa-optimum ties -> lowest c;
   Youden ties -> lowest c (highest-c variant reported as sensitivity).
 * percentile of a cut-off = 100*share(K<=c) in the set being analysed (resample, or full stratum for observed).
 * resampling seed 0, 200 resamples per share, N = number of luminal tumors."""
import time, gzip, re, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"; rng=np.random.default_rng(0)

# ---- parse series matrix
rows=[]; 
with gzip.open("/home/claude/raw/gse81538/sm.txt.gz","rt") as f:
    for line in f:
        if line.startswith("!Sample_geo_accession"): gsm=[v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
        if line.startswith("!Sample_title"): ttl=[v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
        if line.startswith("!Sample_characteristics_ch1"):
            vals=[v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
            rows.append(vals)
meta=pd.DataFrame({"title":ttl,"gsm":gsm})
for vals in rows:
    k,_=vals[0].split(": ",1) if ": " in vals[0] else (vals[0],"")
    meta[k.strip()]=[v.split(": ",1)[1] if ": " in v else np.nan for v in vals]
def num(c): return pd.to_numeric(meta[c],errors="coerce")
meta["ER"]=num("er consensus"); meta["HER2"]=num("her2 consensus"); meta["K"]=num("ki67 consensus")
for i in (1,2,3): meta[f"K{i}"]=num(f"ki67 reading {i}")
meta["PAM50"]=meta["pam50 subtype"]
log(f"samples {len(meta)}")
# ---- expression
ex=pd.read_csv("/mnt/user-data/uploads/GSE81538_gene_expression_405_transformed_csv.gz",index_col=0)
P2G=["ANLN","BIRC5","CCNB1","CDC20","CENPF","CEP55","EXO1","KIF2C","MELK","MYBL2","NDC80","NUF2","ORC6","PTTG1","RRM2","TYMS","UBE2C","UBE2T"]
assert all(g in ex.index for g in P2G+["MKI67"]), [g for g in P2G+["MKI67"] if g not in ex.index]
meta=meta.set_index("title"); meta=meta.loc[ex.columns]

def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean())
    return (po-pe)/(1-pe) if pe<1 else np.nan
def cands(x): return np.unique(x)[:-1]   # c = max would call nobody positive
def kopt(x,y,ref=None):
    ref=x if ref is None else ref
    cs=cands(x); ks=np.array([kappa((x>c).astype(int),y) for c in cs])
    i=int(np.nanargmax(ks)); return cs[i],100*np.mean(ref<=cs[i]),ks[i]
def yopt(x,y,high=False):
    cs=cands(x); J=np.array([np.mean(x[y==1]>c)-np.mean(x[y==0]>c) for c in cs])
    idx=np.where(J>=J.max()-1e-12)[0]; i=idx[-1] if high else idx[0]
    return cs[i],100*np.mean(x[y==0]<=cs[i]),J[i]

def run(er_codes,tag):
    el=meta[(meta.ER.isin(er_codes))&(meta.HER2==0)].copy()
    lum=el[el.PAM50.isin(["LumA","LumB"])].copy()
    y=(lum.PAM50=="LumB").astype(int).values; share=y.mean()
    log(f"[{tag}] eligible {len(el)}; luminal {len(lum)}; LumB {y.sum()} ({share:.1%}); other PAM50 in eligible: {el.PAM50.value_counts().to_dict()}")
    # scores standardized within stratum (eligible)
    z=lambda g:(ex.loc[g,el.index]-ex.loc[g,el.index].mean())/ex.loc[g,el.index].std(ddof=1)
    el["P2"]=pd.concat([z(g) for g in P2G],axis=1).mean(axis=1); el["P1"]=z("MKI67")
    lum["P2"]=el.loc[lum.index,"P2"]; lum["P1"]=el.loc[lum.index,"P1"]
    out={}
    # ---- Ki-67 measures (K and readings)
    for m in ["K","K1","K2","K3"]:
        d=lum.dropna(subset=[m]); x=d[m].values; yy=(d.PAM50=="LumB").astype(int).values
        full=el[m].dropna().values
        ck,pk,kk=kopt(x,yy,full); cy,qy,jy=yopt(x,yy); cyh,qyh,_=yopt(x,yy,True)
        # bootstrap CI 2000
        bk=[];by=[]
        for b in range(2000):
            ii=rng.integers(0,len(x),len(x)); xb=x[ii]; yb=yy[ii]
            if yb.min()==yb.max() or len(np.unique(xb))<2: continue
            c1,_,_=kopt(xb,yb); c2,_,_=yopt(xb,yb); bk.append(c1); by.append(c2)
        ci=lambda a:(np.percentile(a,2.5),np.percentile(a,97.5))
        log(f"[{tag}] {m}: n={len(d)} kappa-opt K>{ck} (pct {pk:.0f}, kappa {kk:.3f}, boot CI {ci(bk)}) | Youden K>{cy} (LumA-q {qy:.0f}; high-tie K>{cyh}) J={jy:.3f} CI {ci(by)}")
        # resampling
        A=x[yy==0]; B=x[yy==1]; N=len(x); rec=[]
        for prev in [15,20,25,30,35,40,45]:
            nb=int(round(N*prev/100)); na=N-nb; kp=[];yq=[];kc=[];yc=[]
            for r in range(200):
                xa=rng.choice(A,na); xb_=rng.choice(B,nb)
                xx=np.r_[xa,xb_]; yz=np.r_[np.zeros(na,int),np.ones(nb,int)]
                c1,p1,_=kopt(xx,yz); c2,_,_=yopt(xx,yz)
                kp.append(p1); kc.append(c1); yc.append(c2); yq.append(100*np.mean(xa<=c2))
            rec.append(dict(measure=m,prev=prev,kappa_pct=np.median(kp),kappa_thr_med=np.median(kc),kappa_thr_lo=np.percentile(kc,2.5),kappa_thr_hi=np.percentile(kc,97.5),
                            youden_q=np.median(yq),youden_thr_med=np.median(yc),youden_thr_lo=np.percentile(yc,2.5),youden_thr_hi=np.percentile(yc,97.5)))
        rd=pd.DataFrame(rec); s1=np.polyfit(100-rd.prev,rd.kappa_pct,1)[0]; s2=np.polyfit(100-rd.prev,rd.youden_q,1)[0]
        log(f"[{tag}] {m} RESAMPLING slope kappa-pct on (100-share) = {s1:.2f}; slope Youden LumA-quantile = {s2:.2f}")
        out[m]=dict(rd=rd,s1=s1,s2=s2,n=len(d),ck=ck,pk=pk,kk=kk,ci_k=ci(bk),cy=cy,qy=qy,cyh=cyh,ci_y=ci(by),jy=jy)
    # ---- P1, P2
    sc={}
    for m in ["P2","P1"]:
        x=lum[m].values; full=el[m].values
        ks=[kappa((x>np.percentile(full,g)).astype(int),y) for g in range(5,96)]
        kp=5+int(np.nanargmax(ks)); kmax=np.nanmax(ks)
        A=x[y==0]; fpr_t=np.unique(x); 
        J=[np.mean(x[y==1]>t)-np.mean(x[y==0]>t) for t in fpr_t[:-1]]; t=fpr_t[int(np.argmax(J))]
        q=100*np.mean(A<=t); zz=(t-A.mean())/A.std(ddof=1)
        bq=[];bk=[]
        for b in range(2000):
            ii=rng.integers(0,len(x),len(x)); xb=x[ii]; yb=y[ii]
            if yb.min()==yb.max(): continue
            ut=np.unique(xb); Jb=[np.mean(xb[yb==1]>tt)-np.mean(xb[yb==0]>tt) for tt in ut[:-1]]
            tb=ut[int(np.argmax(Jb))]; bq.append(100*np.mean(xb[yb==0]<=tb))
            fb=full[rng.integers(0,len(full),len(full))]
            kb=[kappa((xb>np.percentile(fb,g)).astype(int),yb) for g in range(5,96,2)]; bk.append(5+2*int(np.nanargmax(kb)))
        sc[m]=dict(kappa_pct=kp,kappa_max=kmax,youden_q=q,youden_z=zz,q_ci=(np.percentile(bq,2.5),np.percentile(bq,97.5)),kp_ci=(np.percentile(bk,2.5),np.percentile(bk,97.5)))
        log(f"[{tag}] {m}: kappa-opt pct {kp} (kappa {kmax:.3f}; boot CI {sc[m]['kp_ci']}) vs 100-share {100-100*share:.1f} | Youden LumA-q {q:.0f} CI ({sc[m]['q_ci'][0]:.0f},{sc[m]['q_ci'][1]:.0f}), z {zz:.2f}")
    return dict(n_el=len(el),n_lum=len(lum),share=share,ki=out,sc=sc)

res={}
res["primary"]=run([1,2,3],"ER1-3")
res["sens"]=run([2,3],"ER2-3")
import pickle; pickle.dump(res,open(f"{R}/A7_results.pkl","wb"))
rows=[]
for tag,r in res.items():
    for m,o in r["ki"].items():
        d=o["rd"].copy(); d.insert(0,"analysis",tag); rows.append(d)
pd.concat(rows).to_csv(f"{R}/A7_resampling.csv",index=False)
log("done.")
