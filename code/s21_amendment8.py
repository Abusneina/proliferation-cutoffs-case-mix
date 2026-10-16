"""s21_amendment8.py  Amendment 8: gene-disjoint proliferation scores (P3, P3m, P4).

Usage
  python3 -I s21_amendment8.py check
      Reproduces stored P1 and P2 from the freshly downloaded matrices. Reads only MKI67 and the
      18 P2 genes (already analyzed). Allowed before the Amendment 8 freeze.
  python3 -I s21_amendment8.py run <FROZEN_P3_list> <FROZEN_P4_list>
      Full Amendment 8 analysis. Refuses to start unless both list files carry "FROZEN" in the name.
Progress is printed throughout.
"""
import sys, gzip, time, warnings, json
import numpy as np, pandas as pd
from sklearn.metrics import roc_curve
warnings.filterwarnings("ignore")
T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

RAW = "/home/claude/raw"; RES = "/home/claude/pkg/results"; OUT = "/home/claude/work/results"
MAT = {"TCGA": (f"{RAW}/tcga_rsem.txt", "\t", 2, True),            # path, sep, first data col, log2(x+1)
       "METABRIC": (f"{RAW}/metabric_illumina.txt", "\t", 2, False),
       "SCAN-B": (f"{RAW}/gse96058.csv.gz", ",", 1, False),
       "GSE81538": (f"{RAW}/gse81538.csv.gz", ",", 1, False)}
P2 = ["ANLN","BIRC5","CCNB1","CDC20","CENPF","CEP55","EXO1","KIF2C","MELK","MYBL2","NDC80","NUF2",
      "ORC6L","PTTG1","RRM2","TYMS","UBE2C","UBE2T"]
# Pre-specified alias table (list symbol -> alternatives tried in order). Pseudogenes and
# read-through transcripts (H3F3AP4, CKLF-CMTM1) are deliberately NOT used as stand-ins.
ALIAS = {"ORC6L":["ORC6"], "KIAA0101":["PCLAF"], "MLF1IP":["CENPU"], "WHSC1":["NSD2"], "SFRS2":["SRSF2"],
         "C21orf45":["MIS18A"], "DDX39":["DDX39A"], "H3F3A":["H3-3A"], "CDK1":["CDC2"],
         "DDX39A":["DDX39"], "H2AX":["H2AFX"], "H2AZ1":["H2AFZ"], "H2AZ2":["H2AFV"], "H2BC12":["HIST1H2BK"],
         "JPT1":["HN1"], "KMT5A":["SETD8"], "KNL1":["CASC5"], "MAP3K20":["ZAK"], "NSD2":["WHSC1"],
         "ORC5":["ORC5L"], "PRP4K":["PRPF4B"], "SRSF1":["SFRS1"], "SRSF10":["SFRS13A"], "SRSF2":["SFRS2"],
         "TENT4A":["PAPD7"]}
GRID = np.arange(5, 96)
rng = np.random.default_rng(20261014)

# ------------------------------------------------------------------ loading
def read_list(path, start=None, end=None):
    out, inside = [], start is None
    for l in open(path):
        l = l.strip()
        if start and l == start: inside = True; continue
        if end and l == end: inside = False; continue
        if inside and l and not l.startswith("#"): out.append(l)
    return out

def extract(cohort, genes):
    path, sep, c0, lg = MAT[cohort]
    want = set(genes) | {a for g in genes for a in ALIAS.get(g, [])}
    rows = {}
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", errors="replace") as fh:
        hdr = [h.strip('"') for h in fh.readline().rstrip("\n").split(sep)]
        for n, line in enumerate(fh, 1):
            if n % 10000 == 0: log(f"  {cohort}: {n} rows scanned, {len(rows)} symbols kept")
            sym = line[:line.find(sep)].strip('"')
            if sym in want:
                v = pd.to_numeric(pd.Series(line.rstrip("\n").split(sep)[c0:]), errors="coerce").values
                rows.setdefault(sym, []).append(v)
    # duplicate symbol rows (METABRIC only): LAST row kept, which is what the registered main analysis did (dict overwrite in s01)
    E = pd.DataFrame({s: v[-1] for s, v in rows.items()}, index=hdr[c0:]).T
    if lg: E = np.log2(E + 1.0)
    found, alias_used, missing = {}, [], []
    for g in genes:
        if g in E.index: found[g] = g
        else:
            hit = next((a for a in ALIAS.get(g, []) if a in E.index), None)
            if hit: found[g] = hit; alias_used.append(f"{g}->{hit}")
            else: missing.append(g)
    log(f"  {cohort}: {len(found)}/{len(genes)} genes; aliases {alias_used}; missing {missing}")
    return E, found, missing, alias_used

def z(v):
    v = np.asarray(v, float); return (v - np.nanmean(v)) / np.nanstd(v, ddof=1)

# ------------------------------------------------------------------ cohorts (row sets as analyzed)
def gse81538_meta():
    rows = []
    with gzip.open(f"{RAW}/gse81538/sm.txt.gz", "rt") as f:
        for line in f:
            if line.startswith("!Sample_title"): ttl = [v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
            if line.startswith("!Sample_characteristics_ch1"):
                rows.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
    meta = pd.DataFrame({"title": ttl})
    for vals in rows:
        k = vals[0].split(": ", 1)[0]
        meta[k.strip()] = [v.split(": ", 1)[1] if ": " in v else np.nan for v in vals]
    meta["ER"] = pd.to_numeric(meta["er consensus"], errors="coerce")
    meta["HER2"] = pd.to_numeric(meta["her2 consensus"], errors="coerce")
    el = meta[(meta.ER.isin([1, 2, 3])) & (meta.HER2 == 0)]          # registered primary stratum
    return pd.DataFrame({"sample": el.title.values, "PAM50": el["pam50 subtype"].values})

def cohort_rows(cohort, cols):
    if cohort == "TCGA":
        d = pd.read_csv(f"{RES}/cohort_tcga.csv", low_memory=False)
        first = {}
        for c in cols:
            first.setdefault(c[:12], c)                                # first sample per patient
        d["col"] = d.PATIENT_ID.map(first)
    elif cohort == "METABRIC":
        d = pd.read_csv(f"{RES}/cohort_metabric.csv", low_memory=False); d["col"] = d.PATIENT_ID
    elif cohort == "SCAN-B":
        d = pd.read_csv(f"{RES}/cohort_scanb.csv", low_memory=False); d["col"] = d["sample"]
    else:
        d = gse81538_meta(); d["col"] = d["sample"]
    assert d.col.notna().all() and d.col.isin(cols).all(), f"{cohort}: unmatched samples"
    return d

def scores(E, d, found, how):
    Z = np.vstack([z(E.loc[found[g], d.col].values) for g in found])
    return np.nanmedian(Z, axis=0) if how == "median" else np.nanmean(Z, axis=0)

# ------------------------------------------------------------------ statistics (as Amendments 5 and 6)
def kappa_vec(pred, y):
    """pred: thresholds x n boolean; y: n binary. Cohen's kappa per row."""
    p = pred.mean(1); q = y.mean(); po = (pred == y).mean(1); pe = p*q + (1-p)*(1-q)
    with np.errstate(invalid="ignore", divide="ignore"): return np.where(pe < 1, (po-pe)/(1-pe), np.nan)
def kappa_opt_pct(x, y, ref):
    T = np.percentile(ref, GRID); k = kappa_vec(x[None, :] > T[:, None], y)
    i = int(np.nanargmax(k)); return int(GRID[i]), float(k[i])
def youden_thr(x, y):
    fpr, tpr, thr = roc_curve(y, x); return thr[int(np.argmax(tpr - fpr))]

def analyze(cname, full, pam):
    m = np.isin(pam, ["LumA", "LumB"]); x = full[m]; y = (pam[m] == "LumB").astype(int)
    share = 100*y.mean(); A = x[y == 0]; B = x[y == 1]; N = len(x)
    kp, kk = kappa_opt_pct(x, y, full)
    ty = youden_thr(x, y); yq = 100*np.mean(A <= ty)
    bk, bq, bp = [], [], []
    for b in range(2000):
        if b and b % 500 == 0: log(f"     bootstrap {b}/2000")
        ii = rng.integers(0, N, N); ff = full[rng.integers(0, len(full), len(full))]
        xx, yy = x[ii], y[ii]
        if yy.min() == yy.max(): continue
        p_, k_ = kappa_opt_pct(xx, yy, ff); bk.append(k_); bp.append(p_)
        t_ = youden_thr(xx, yy); bq.append(100*np.mean(xx[yy == 0] <= t_))
    ci = lambda a: (float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)))
    E3 = []
    for prev in [15, 20, 25, 30, 35, 40, 45]:
        nb = int(round(N*prev/100)); na = N - nb; ks, qs = [], []
        for r in range(200):
            xa = rng.choice(A, na, replace=True); xb = rng.choice(B, nb, replace=True)
            xx = np.r_[xa, xb]; yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
            ks.append(kappa_opt_pct(xx, yy, xx)[0]); t_ = youden_thr(xx, yy); qs.append(100*np.mean(xa <= t_))
        E3.append((prev, np.median(ks), np.median(qs)))
    E3 = np.array(E3)
    sk = np.polyfit(100 - E3[:, 0], E3[:, 1], 1)[0]; sy = np.polyfit(100 - E3[:, 0], E3[:, 2], 1)[0]
    return dict(cohort=cname, n_stratum=len(full), n_luminal=N, lumB_share=share, target=100-share,
                kappa_opt_pct=kp, kappa_opt_pct_lo=ci(bp)[0], kappa_opt_pct_hi=ci(bp)[1],
                peak_kappa=kk, peak_kappa_lo=ci(bk)[0], peak_kappa_hi=ci(bk)[1],
                youden_q_lumA=yq, youden_q_lumA_lo=ci(bq)[0], youden_q_lumA_hi=ci(bq)[1],
                slope_kappa=sk, slope_youden=sy), E3

# ------------------------------------------------------------------ modes
def check():
    log("CHECK MODE: reproducing stored P1 and P2 (MKI67 + 18 P2 genes only)")
    rep = []
    for c in ["TCGA", "METABRIC", "SCAN-B"]:
        E, found, miss, _ = extract(c, ["MKI67"] + P2)
        d = cohort_rows(c, list(E.columns))
        p1 = z(E.loc["MKI67", d.col].values)
        p2 = np.nanmean(np.vstack([z(E.loc[found[g], d.col].values) for g in P2 if g in found]), axis=0)
        for s, v in [("P1", p1), ("P2", p2)]:
            dif = np.nanmax(np.abs(v - d[s].values)); r = np.corrcoef(v, d[s].values)[0, 1]
            log(f"  {c:9s} {s}: n={len(d)}  max |new - stored| = {dif:.2e}  r = {r:.8f}")
            rep.append(dict(cohort=c, score=s, n=len(d), max_abs_diff=dif, r=r))
    pd.DataFrame(rep).to_csv(f"{OUT}/A8_precheck_P1P2_reproduction.csv", index=False)
    log("check done.")

def run(p3file, p4file):
    assert "FROZEN" in p3file and "FROZEN" in p4file, "lists must be frozen before data are read"
    P3 = read_list(p3file, "##P3_START", "##P3_END"); P4 = read_list(p4file, "##P4_START", "##P4_END")
    assert len(P3) == 120 and len(P4) == 187, (len(P3), len(P4))
    res, e3rows, avail = [], [], []
    for c in ["TCGA", "METABRIC", "SCAN-B", "GSE81538"]:
        log("=" * 70); log(c)
        E, found3, miss3, al3 = extract(c, ["MKI67"] + P2 + P3 + P4)
        d = cohort_rows(c, list(E.columns)); pam = d.PAM50.values
        f3 = {g: found3[g] for g in P3 if g in found3}; f4 = {g: found3[g] for g in P4 if g in found3}
        fp2 = {g: found3[g] for g in P2 if g in found3}
        avail += [dict(cohort=c, score="P3", n_found=len(f3), n_list=len(P3), missing=";".join(g for g in P3 if g not in f3)),
                  dict(cohort=c, score="P4", n_found=len(f4), n_list=len(P4), missing=";".join(g for g in P4 if g not in f4))]
        S = {"P1": z(E.loc["MKI67", d.col].values), "P2": scores(E, d, fp2, "mean")}
        if len(f3) >= 0.8*len(P3): S["P3"] = scores(E, d, f3, "median"); S["P3m"] = scores(E, d, f3, "mean")
        else: log(f"  P3 not analyzed in {c}: {len(f3)}/{len(P3)} genes (<80%)")
        if len(f4) >= 0.8*len(P4): S["P4"] = scores(E, d, f4, "median")
        else: log(f"  P4 not analyzed in {c}: {len(f4)}/{len(P4)} genes (<80%)")
        lum = np.isin(pam, ["LumA", "LumB"])
        for s in ["P3", "P3m", "P4"]:
            if s in S and "P2" in S:
                for stratum, mk in [("ER+/HER2-", np.ones(len(d), bool)), ("LumA", pam == "LumA"), ("LumB", pam == "LumB")]:
                    rho = pd.Series(S[s][mk]).corr(pd.Series(S["P2"][mk]), method="spearman")
                    res.append(dict(block="H2", cohort=c, score=s, stratum=stratum, spearman_vs_P2=rho))
        for s, v in S.items():
            log(f"  {c} {s}: kappa sweep, 2,000 bootstraps, 7 x 200 resamples ...")
            r, E3 = analyze(c, v, pam); r.update(block="main", score=s); res.append(r)
            for prev, kpct, yq in E3: e3rows.append(dict(cohort=c, score=s, prev=prev, kappa_pct=kpct, youden_q_lumA=yq))
            log(f"  {c} {s}: LumB {r['lumB_share']:.1f}% target {r['target']:.1f} | kappa-opt pct {r['kappa_opt_pct']} "
                f"(peak kappa {r['peak_kappa']:.3f} [{r['peak_kappa_lo']:.3f}, {r['peak_kappa_hi']:.3f}]) | "
                f"Youden LumA-q {r['youden_q_lumA']:.0f} | slopes kappa {r['slope_kappa']:.2f}, Youden {r['slope_youden']:.2f}")
    R = pd.DataFrame(res); R.to_csv(f"{OUT}/A8_results.csv", index=False)
    pd.DataFrame(e3rows).to_csv(f"{OUT}/A8_resampling.csv", index=False)
    pd.DataFrame(avail).to_csv(f"{OUT}/A8_gene_availability.csv", index=False)
    # ---- registered decision rules (G1-G4)
    M = R[R.block == "main"]; verdict = {}
    for s in ["P3", "P3m", "P4"]:
        g = {}
        for c in ["TCGA", "METABRIC", "SCAN-B"]:
            r = M[(M.cohort == c) & (M.score == s)]
            if r.empty: g[c] = None; continue
            r = r.iloc[0]
            g[c] = dict(G1=abs(r.kappa_opt_pct - r.target) <= 5, G2=0.7 <= r.slope_kappa <= 1.3,
                        G3=-0.3 <= r.slope_youden <= 0.3)
        r4 = M[(M.cohort == "GSE81538") & (M.score == s)]
        G4 = None if r4.empty else bool(abs(r4.iloc[0].kappa_opt_pct - r4.iloc[0].target) <= 5)
        ok = all(v is not None and all(v.values()) for v in g.values())
        verdict[s] = dict(per_cohort=g, G4=G4, decision="CONFIRMED FOR A GENE-DISJOINT SCORE" if ok else "NOT CONFIRMED")
        log(f"DECISION {s}: {verdict[s]['decision']}  {g}  G4={G4}")
    json.dump(verdict, open(f"{OUT}/A8_decision.json", "w"), indent=1, default=bool)
    log("done.")

if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    if sys.argv[1] == "check": check()
    elif sys.argv[1] == "run": run(sys.argv[2], sys.argv[3])
