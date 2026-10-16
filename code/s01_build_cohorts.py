"""
s01_build_cohorts.py
Builds the two analysis cohorts and computes the two proliferation scores.
Writes: results/cohort_tcga.csv, results/cohort_metabric.csv, results/attrition.csv
Progress is printed at every stage so a long run is visibly alive.
"""
import sys, csv, time
import numpy as np, pandas as pd

T0=time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

GENE_FILE="/home/claude/work/protocol/2026-10-13_1515_proliferation_gene_list_FROZEN.txt"
UP="/root/.claude/uploads/ec3ec192-a217-5587-af1a-bcdb9332ed30"
TCGA_EXPR="/mnt/user-data/uploads/data_mrna_seq_v2_rsem.txt"
META_EXPR="/home/claude/raw/meta/data_mrna_illumina_microarray.txt"
OUT="/home/claude/work/results"

# ---------- frozen gene list ----------
lines=[l.strip() for l in open(GENE_FILE)]
p2=[]; inp2=False
for l in lines:
    if l=="##P2_START": inp2=True; continue
    if l=="##P2_END": inp2=False; continue
    if inp2 and l and not l.startswith("#"): p2.append(l)
P1="MKI67"
ALIAS={"ORC6L":["ORC6L","ORC6"],"NDC80":["NDC80","KNTC2"],"NUF2":["NUF2","CDCA1"]}
log(f"frozen list: P1={P1}, P2={len(p2)} genes")
assert len(p2)==18 and P1 not in p2, "gene list integrity check failed"

def read_clin(path):
    rows=[l.rstrip("\n").split("\t") for l in open(path,encoding="utf-8",errors="replace")
          if not l.startswith("#")]
    return pd.DataFrame(rows[1:], columns=rows[0])

def extract_genes(expr_path, wanted, label):
    """Stream the matrix, keep only wanted symbols. Returns DataFrame genes x samples."""
    want=set()
    for g in wanted:
        want.update(ALIAS.get(g,[g]))
    log(f"{label}: scanning expression matrix for {len(want)} symbols ...")
    with open(expr_path, encoding="utf-8", errors="replace") as fh:
        hdr=fh.readline().rstrip("\n").split("\t")
        samples=hdr[2:]
        keep={}
        for n,line in enumerate(fh,1):
            if n % 5000 == 0: log(f"  {label}: {n} rows scanned, {len(keep)} hits")
            tab1=line.find("\t")
            sym=line[:tab1]
            if sym in want:
                f=line.rstrip("\n").split("\t")
                keep[sym]=pd.to_numeric(pd.Series(f[2:]), errors="coerce").values
    log(f"{label}: found {len(keep)}/{len(want)} symbols across {len(samples)} samples")
    df=pd.DataFrame(keep, index=samples).T
    # resolve aliases to canonical name
    for canon,alts in ALIAS.items():
        for a in alts:
            if a in df.index and canon not in df.index:
                df=df.rename(index={a:canon})
    return df

def zscore(v):
    v=np.asarray(v,dtype=float)
    m=np.nanmean(v); s=np.nanstd(v,ddof=1)
    return (v-m)/s if s>0 else np.full_like(v,np.nan)

# ======================= TCGA =======================
log("="*60); log("TCGA-BRCA")
pan=read_clin(f"{UP}/541507c2-data_clinical_patient.txt")
leg=read_clin("/home/claude/work/data/tcga_legacy_clinical_patient.txt")
leg=leg[["PATIENT_ID","ER_STATUS_BY_IHC","PR_STATUS_BY_IHC","IHC_HER2","HER2_FISH_STATUS"]]
t=pan.merge(leg,on="PATIENT_ID",how="left")
log(f"merged PanCanAtlas x Firehose Legacy: {len(t)} patients, "
    f"{t['ER_STATUS_BY_IHC'].notna().sum()} with receptor record")

def her2_rule(r):
    ihc=str(r.get("IHC_HER2","")).strip(); fish=str(r.get("HER2_FISH_STATUS","")).strip()
    if ihc=="Positive" or fish=="Positive": return "pos"
    if ihc=="Negative": return "neg"
    if ihc=="Equivocal" and fish=="Negative": return "neg"
    if fish=="Negative": return "neg"
    return "unk"
t["HER2_CALL"]=t.apply(her2_rule,axis=1)

te=extract_genes(TCGA_EXPR,[P1]+p2+["ESR1","PGR","ERBB2"],"TCGA")
te.columns=[c[:12] for c in te.columns]
expr_pat=set(te.columns)

attr=[]
def step(df,name,mask):
    before=len(df); df=df[mask].copy(); attr.append((name,len(df),before-len(df)))
    log(f"  {name:<40} {len(df):>5}  (-{before-len(df)})"); return df
log("TCGA attrition:")
attr.append(("start: PanCanAtlas patients",len(t),0)); log(f"  {'start':<40} {len(t):>5}")
t=step(t,"female",t["SEX"]=="Female")
t=step(t,"expression available",t["PATIENT_ID"].isin(expr_pat))
t=step(t,"ER positive by IHC",t["ER_STATUS_BY_IHC"]=="Positive")
t=step(t,"HER2 negative (IHC/FISH rule)",t["HER2_CALL"]=="neg")
t=step(t,"PFS time and status present",
       t["PFS_STATUS"].astype(str).str.len().gt(0) & t["PFS_MONTHS"].astype(str).str.strip().ne("")
       & t["PFS_MONTHS"].astype(str).str.strip().ne("NA"))

sub=te[t["PATIENT_ID"].tolist()]
log("computing P1 and P2 within the TCGA stratum ...")
t["P1"]=zscore(np.log2(sub.loc[P1].values+1.0))
p2_present=[g for g in p2 if g in sub.index]
log(f"  P2 genes found in TCGA: {len(p2_present)}/18  missing: {sorted(set(p2)-set(p2_present))}")
t["P2"]=np.nanmean(np.vstack([zscore(np.log2(sub.loc[g].values+1.0)) for g in p2_present]),axis=0)
t["PAM50"]=t["SUBTYPE"].str.replace("BRCA_","",regex=False)
t["EVENT"]=t["PFS_STATUS"].str.startswith("1").astype(int)
t["TIME"]=pd.to_numeric(t["PFS_MONTHS"],errors="coerce")
t["AGE_N"]=pd.to_numeric(t["AGE"],errors="coerce")
t["COHORT"]="TCGA"; t["ENDPOINT"]="PFI"
t.to_csv(f"{OUT}/cohort_tcga.csv",index=False)
log(f"TCGA cohort saved: n={len(t)}, events={int(t['EVENT'].sum())}")

# ======================= METABRIC =======================
log("="*60); log("METABRIC")
mp=read_clin(f"{UP}/bb7dec7f-data_clinical_patient.txt")
ms=read_clin(f"{UP}/1a5013ed-data_clinical_sample.txt")[
    ["PATIENT_ID","ER_STATUS","HER2_STATUS","PR_STATUS","GRADE","TUMOR_STAGE","TUMOR_SIZE"]]
m=mp.merge(ms,on="PATIENT_ID",how="left")
me=extract_genes(META_EXPR,[P1]+p2+["ESR1","PGR","ERBB2"],"METABRIC")
expr_m=set(me.columns)

log("METABRIC attrition:")
attr_m=[("start: METABRIC patients",len(m),0)]; log(f"  {'start':<40} {len(m):>5}")
def stepm(df,name,mask):
    before=len(df); df=df[mask].copy(); attr_m.append((name,len(df),before-len(df)))
    log(f"  {name:<40} {len(df):>5}  (-{before-len(df)})"); return df
m=stepm(m,"expression available",m["PATIENT_ID"].isin(expr_m))
m=stepm(m,"ER positive",m["ER_STATUS"]=="Positive")
m=stepm(m,"HER2 negative",m["HER2_STATUS"]=="Negative")
m=stepm(m,"vital status and OS time present",
        m["VITAL_STATUS"].astype(str).str.len().gt(0) &
        m["OS_MONTHS"].astype(str).str.strip().ne("") & m["OS_MONTHS"].astype(str).str.strip().ne("NA"))

subm=me[m["PATIENT_ID"].tolist()]
log("computing P1 and P2 within the METABRIC stratum ...")
m["P1"]=zscore(subm.loc[P1].values)                      # already log-scale microarray
p2m=[g for g in p2 if g in subm.index]
log(f"  P2 genes found in METABRIC: {len(p2m)}/18  missing: {sorted(set(p2)-set(p2m))}")
m["P2"]=np.nanmean(np.vstack([zscore(subm.loc[g].values) for g in p2m]),axis=0)
m["PAM50"]=m["CLAUDIN_SUBTYPE"]
m["EVENT"]=(m["VITAL_STATUS"]=="Died of Disease").astype(int)   # derived DSS
m["TIME"]=pd.to_numeric(m["OS_MONTHS"],errors="coerce")
m["AGE_N"]=pd.to_numeric(m["AGE_AT_DIAGNOSIS"],errors="coerce")
m["COHORT"]="METABRIC"; m["ENDPOINT"]="DSS(derived)"
m.to_csv(f"{OUT}/cohort_metabric.csv",index=False)
log(f"METABRIC cohort saved: n={len(m)}, DSS events={int(m['EVENT'].sum())}")

pd.DataFrame(attr+[("---",0,0)]+attr_m,columns=["step","n_remaining","n_dropped"]).to_csv(
    f"{OUT}/attrition.csv",index=False)
log("done.")
