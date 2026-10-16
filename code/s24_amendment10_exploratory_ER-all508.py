"""s24_amendment10_exploratory_ER-all508.py  POST HOC EXPLORATORY variant of the frozen s23 (Amendment 10).
Only change: ER field er_status_ihc (all 508 samples) instead of er_status_ihc_esr1_for indeterminate (310). No confirmatory verdict.
Original header follows. Amendment 10: test in an independent RNA cohort (GSE25066; SMC 2018 secondary).

Usage
  python3 -I s23_amendment10.py simulate
      Writes synthetic files in the GSE25066 and cBioPortal formats (synthetic values and labels) and
      runs the full analysis on them. No real data are read.
  python3 -I s23_amendment10.py structure
      Parses the real files and checks field names, label sets and gene matching. Prints no count,
      share or expression value.
  python3 -I s23_amendment10.py run <FROZEN_amendment_10_file>
      Registered analysis. Refuses to start unless the file name carries FROZEN.
Progress is printed throughout.
"""
import sys, os, gzip, json, time, random, importlib.util
import numpy as np, pandas as pd
T0 = time.time()
def log(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

HERE = "/home/claude/work/code"
spec = importlib.util.spec_from_file_location("s21", f"{HERE}/s21_amendment8.py"); s21 = importlib.util.module_from_spec(spec)
sys.argv_saved = sys.argv; spec.loader.exec_module(s21)
kappa_opt_pct, youden_thr, z, ALIAS = s21.kappa_opt_pct, s21.youden_thr, s21.z, s21.ALIAS

REAL = {"sm": "/home/claude/dl/geo2/GSE25066_series_matrix.txt.gz", "annot": "/home/claude/dl/geo2/GPL96.annot.gz",
        "smc": "/home/claude/raw/smc"}
P3FILE = "/home/claude/work/protocol/2026-10-14_1641_GENE-LIST_P3-metaPCNA-minus-PAM50_FROZEN.txt"
P4FILE = "/home/claude/work/protocol/2026-10-14_1641_GENE-LIST_P4-HallmarkG2M-minus-PAM50_FROZEN.txt"
OUT = "/home/claude/work/results"
P2 = ["ANLN","BIRC5","CCNB1","CDC20","CENPF","CEP55","EXO1","KIF2C","MELK","MYBL2","NDC80","NUF2",
      "ORC6L","PTTG1","RRM2","TYMS","UBE2C","UBE2T"]
MIN_PER_SUBTYPE = 60

def read_list(path, start, end):
    out, inside = [], False
    for l in open(path):
        l = l.strip()
        if l == start: inside = True; continue
        if l == end: inside = False; continue
        if inside and l and not l.startswith("#"): out.append(l)
    return out

def resolve(genes, available):
    found, miss = {}, []
    for g in genes:
        if g in available: found[g] = g
        else:
            h = next((a for a in ALIAS.get(g, []) if a in available), None)
            if h: found[g] = h
            else: miss.append(g)
    return found, miss

# ------------------------------------------------------------------ GSE25066
def load_gse(sm, annot):
    meta, probes, vals = {}, [], []
    with gzip.open(sm, "rt", errors="replace") as fh:
        for l in fh:
            if l.startswith("!Sample_geo_accession"):
                gsm = [v.strip('"') for v in l.rstrip("\n").split("\t")[1:]]; meta = {g: {} for g in gsm}
            elif l.startswith("!Sample_characteristics_ch1"):
                for g, v in zip(gsm, l.rstrip("\n").split("\t")[1:]):
                    v = v.strip('"')
                    if ": " in v:
                        k, x = v.split(": ", 1); meta[g][k.strip()] = x.strip()      # parsed by field name
            elif l.startswith("!series_matrix_table_begin"):
                hdr = [h.strip('"') for h in fh.readline().rstrip("\n").split("\t")]
                for n, r in enumerate(fh, 1):
                    if r.startswith("!series_matrix_table_end"): break
                    if n % 5000 == 0: log(f"  GSE25066 matrix: {n} probes read")
                    f = r.rstrip("\n").split("\t"); probes.append(f[0].strip('"'))
                    vals.append(pd.to_numeric(pd.Series(f[1:]), errors="coerce").values)
    M = pd.DataFrame(np.log2(np.maximum(np.vstack(vals), 1.0)), index=probes, columns=hdr[1:])
    # probe -> single gene symbol
    sym, inside, h = {}, False, None
    with gzip.open(annot, "rt", errors="replace") as fh:
        for l in fh:
            if l.startswith("!platform_table_begin"): inside = True; continue
            if not inside: continue
            if l.startswith("!platform_table_end"): break
            f = l.rstrip("\n").split("\t")
            if h is None: h = f; i = h.index("Gene symbol"); continue
            s = f[i].strip()
            if s and "///" not in s: sym[f[0]] = s
    M = M.loc[[p for p in M.index if p in sym]]
    mean = M.mean(axis=1)                                   # highest-mean probe per gene, all samples, no labels
    best = pd.DataFrame({"g": [sym[p] for p in M.index], "m": mean.values}, index=M.index).sort_values("m").groupby("g").tail(1)
    E = M.loc[best.index]; E.index = best.g.values
    D = pd.DataFrame.from_dict(meta, orient="index")
    D["ER"] = D.get("er_status_ihc"); D["HER2"] = D.get("her2_status"); D["PAM50"] = D.get("pam50_class")   # EXPLORATORY (post hoc): ER field present for all 508 samples (Error Log 4)
    el = D[(D.ER == "P") & (D.HER2 == "N") & D.PAM50.isin(["LumA", "LumB", "Her2", "Basal", "Normal"])]
    el = el[el.index.isin(E.columns)]
    return E, pd.DataFrame({"col": el.index, "PAM50": el.PAM50.values})

# ------------------------------------------------------------------ SMC 2018
def load_smc(d):
    def rd(p):
        rows = [l.rstrip("\n").split("\t") for l in open(p) if not l.startswith("#")]
        return pd.DataFrame(rows[1:], columns=rows[0])
    s = rd(f"{d}/data_clinical_sample.txt")
    rows = [l.rstrip("\n").split("\t") for l in open(f"{d}/data_mrna_seq_tpm.txt")]
    hdr = rows[0]; body = [r for r in rows[1:] if r[0]]
    E = pd.DataFrame([pd.to_numeric(pd.Series(r[2:]), errors="coerce").values for r in body], index=[r[0] for r in body], columns=hdr[2:])
    E = E.groupby(level=0).mean() if E.index.duplicated().any() else E
    E = np.log2(E + 1.0)
    m = s[(s.IHC_SUBTYPE == "ER+") & s.PAM50_SUBTYPE.isin(["LuminalA", "LuminalB", "Her2", "Basal", "Normal"]) & s.SAMPLE_ID.isin(E.columns)]
    lab = m.PAM50_SUBTYPE.replace({"LuminalA": "LumA", "LuminalB": "LumB"})
    return E, pd.DataFrame({"col": m.SAMPLE_ID.values, "PAM50": lab.values})

# ------------------------------------------------------------------ analysis
def build_scores(E, d, P3, P4):
    av = set(E.index); out = {}; info = {}
    f1, _ = resolve(["MKI67"], av); f2, m2 = resolve(P2, av); f3, m3 = resolve(P3, av); f4, m4 = resolve(P4, av)
    info = {"P2_found": len(f2), "P2_missing": m2, "P3_found": len(f3), "P3_missing": m3, "P4_found": len(f4), "P4_missing": m4}
    Zs = lambda f: np.vstack([z(E.loc[f[g], d.col].values) for g in f])
    out["P1"] = z(E.loc[f1["MKI67"], d.col].values)
    out["P2"] = np.nanmean(Zs(f2), axis=0)
    out["P3"] = np.nanmedian(Zs(f3), axis=0)
    if len(f4) >= 0.8 * len(P4): out["P4"] = np.nanmedian(Zs(f4), axis=0)
    return out, info

def analyze(full, pam, rng, nboot=2000):
    m = np.isin(pam, ["LumA", "LumB"]); x = full[m]; y = (pam[m] == "LumB").astype(int)
    A, B, N = x[y == 0], x[y == 1], len(x); share = 100 * y.mean()
    kp, kk = kappa_opt_pct(x, y, full); ty = youden_thr(x, y); yq = 100 * np.mean(A <= ty)
    bk, bq = [], []
    for b in range(nboot):
        if b and b % 500 == 0: log(f"     bootstrap {b}/{nboot}")
        ii = rng.integers(0, N, N); ff = full[rng.integers(0, len(full), len(full))]; xx, yy = x[ii], y[ii]
        if yy.min() == yy.max(): continue
        bk.append(kappa_opt_pct(xx, yy, ff)[1]); t_ = youden_thr(xx, yy); bq.append(100 * np.mean(xx[yy == 0] <= t_))
    E3 = []
    for prev in [15, 20, 25, 30, 35, 40, 45]:
        nb = int(round(N * prev / 100)); na = N - nb; ks, qs = [], []
        for r in range(200):
            xa = rng.choice(A, na, replace=True); xb = rng.choice(B, nb, replace=True)
            xx = np.r_[xa, xb]; yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
            ks.append(kappa_opt_pct(xx, yy, xx)[0]); t_ = youden_thr(xx, yy); qs.append(100 * np.mean(xa <= t_))
        E3.append((prev, np.median(ks), np.median(qs)))
    E3 = np.array(E3)
    sk = np.polyfit(100 - E3[:, 0], E3[:, 1], 1)[0]; sy = np.polyfit(100 - E3[:, 0], E3[:, 2], 1)[0]
    qlo, qhi = np.percentile(bq, [2.5, 97.5])
    return dict(n_stratum=len(full), n_lumA=int((y == 0).sum()), n_lumB=int(y.sum()), lumB_share=share, target=100 - share,
                kappa_opt_pct=kp, peak_kappa=kk, peak_kappa_lo=np.percentile(bk, 2.5), peak_kappa_hi=np.percentile(bk, 97.5),
                youden_q_lumA=yq, youden_q_lo=qlo, youden_q_hi=qhi, slope_kappa=sk, slope_youden=sy,
                R1=abs(kp - (100 - share)) <= 5, R2=0.7 <= sk <= 1.3, R3=-0.3 <= sy <= 0.3, R4=(qlo <= 85 and qhi >= 82))

def run_all(paths, tag, nboot=2000):
    rng = np.random.default_rng(20261015)   # same seed as the registered run
    P3 = read_list(P3FILE, "##P3_START", "##P3_END"); P4 = read_list(P4FILE, "##P4_START", "##P4_END")
    res = []; verdict = {}
    for cohort, loader in [("GSE25066", lambda: load_gse(paths["sm"], paths["annot"])), ("SMC2018", lambda: load_smc(paths["smc"]))]:
        log("=" * 70); log(f"{cohort}: loading")
        E, d = loader(); S, info = build_scores(E, d, P3, P4); pam = d.PAM50.values
        log(f"  genes: P2 {info['P2_found']}/18 (missing {info['P2_missing']}); P3 {info['P3_found']}/120 (missing {info['P3_missing']}); P4 {info['P4_found']}/187")
        nA, nB = int((pam == "LumA").sum()), int((pam == "LumB").sum())
        if min(nA, nB) < MIN_PER_SUBTYPE: log(f"  fewer than {MIN_PER_SUBTYPE} tumors in a luminal subtype: reported as underpowered")
        for sc in S:
            log(f"  {cohort} {sc}: sweep, {nboot} bootstraps, 7 x 200 resamples ...")
            r = analyze(S[sc], pam, rng, nboot); r.update(cohort=cohort, score=sc, **{k: str(v) for k, v in info.items()}); res.append(r)
            log(f"  {cohort} {sc}: LumB {r['lumB_share']:.1f}% target {r['target']:.1f} | kappa-opt {r['kappa_opt_pct']} (kappa {r['peak_kappa']:.3f}) "
                f"| slopes {r['slope_kappa']:.2f}, {r['slope_youden']:.2f} | Youden LumA-q {r['youden_q_lumA']:.0f} ({r['youden_q_lo']:.0f} to {r['youden_q_hi']:.0f}) "
                f"| R1 {r['R1']} R2 {r['R2']} R3 {r['R3']} R4 {r['R4']}")
        if cohort == "GSE25066":
            if min(nA, nB) < MIN_PER_SUBTYPE: verdict["GSE25066"] = "EXPLORATORY ONLY; would be underpowered"
            else:
                ok = all(x["R1"] and x["R2"] and x["R3"] for x in res if x["cohort"] == "GSE25066" and x["score"] in ("P2", "P3"))
                verdict["GSE25066"] = "EXPLORATORY ONLY; criteria " + ("all met" if ok else "not all met")
            rho = pd.Series(S["P3"]).corr(pd.Series(S["P2"]), method="spearman"); log(f"  Spearman P3 vs P2: {rho:.2f}")
    log(f"DECISION: {verdict}")
    pd.DataFrame(res).to_csv(f"{OUT}/A10_results{tag}.csv", index=False)
    json.dump(verdict, open(f"{OUT}/A10_decision{tag}.json", "w"), indent=1)
    return res, verdict

# ------------------------------------------------------------------ simulated files
def simulate(d):
    rng = np.random.default_rng(7); random.seed(7); os.makedirs(f"{d}/smc", exist_ok=True)
    # annotation subset: keep the real GPL96 annotation (no data), synthetic matrix over its probes
    probes, sym, inside, h = [], {}, False, None
    with gzip.open(REAL["annot"], "rt", errors="replace") as fh:
        for l in fh:
            if l.startswith("!platform_table_begin"): inside = True; continue
            if not inside: continue
            if l.startswith("!platform_table_end"): break
            f = l.rstrip("\n").split("\t")
            if h is None: h = f; i = h.index("Gene symbol"); continue
            probes.append(f[0]); sym[f[0]] = f[i]
    n = 300; lab = rng.choice(["LumA", "LumB", "Her2", "Basal", "Normal"], n, p=[.5, .3, .08, .07, .05])
    prolif = np.where(lab == "LumB", 1.5, np.where(lab == "LumA", 0.0, 1.0)) + rng.normal(0, 1, n)
    gsm = [f"GSM{9000000+i}" for i in range(n)]
    with gzip.open(f"{d}/sim_series_matrix.txt.gz", "wt") as fh:
        fh.write('!Series_title\t"SIMULATED"\n!Sample_geo_accession\t' + "\t".join(f'"{g}"' for g in gsm) + "\n")
        fields = [("er_status_ihc_esr1_for indeterminate", rng.choice(["P", "N"], n, p=[.8, .2])),
                  ("her2_status", rng.choice(["N", "P", "I"], n, p=[.85, .1, .05])), ("pam50_class", lab)]
        for j in range(3):   # shuffle field order per sample, as in the real file
            row = []
            for s in range(n):
                k, v = fields[(j + s) % 3]; row.append(f'"{k}: {v[s]}"')
            fh.write("!Sample_characteristics_ch1\t" + "\t".join(row) + "\n")
        fh.write("!series_matrix_table_begin\n" + '"ID_REF"\t' + "\t".join(f'"{g}"' for g in gsm) + "\n")
        for k, p in enumerate(probes):
            base = rng.uniform(5, 12); load = 0.8 if k % 7 == 0 else 0.0
            v = 2 ** (base + load * prolif + rng.normal(0, .5, n))
            fh.write(f'"{p}"\t' + "\t".join(f"{x:.1f}" for x in v) + "\n")
        fh.write("!series_matrix_table_end\n")
    genes = sorted(set(s for s in sym.values() if s and "///" not in s))
    m = 150; lab2 = rng.choice(["LuminalA", "LuminalB", "Her2", "Basal", "NA"], m, p=[.5, .3, .1, .05, .05])
    pr2 = np.where(lab2 == "LuminalB", 1.5, 0.0) + rng.normal(0, 1, m); ids = [f"SIM_{i}" for i in range(m)]
    pd.DataFrame({"SAMPLE_ID": ids, "PATIENT_ID": ids, "IHC_SUBTYPE": rng.choice(["ER+", "TN", "HER2+", "UA"], m, p=[.75, .1, .1, .05]),
                  "PAM50_SUBTYPE": lab2}).to_csv(f"{d}/smc/data_clinical_sample.txt", sep="\t", index=False)
    with open(f"{d}/smc/data_mrna_seq_tpm.txt", "w") as fh:
        fh.write("Hugo_Symbol\tEntrez_Gene_Id\t" + "\t".join(ids) + "\n")
        for k, g in enumerate(genes):
            v = 2 ** (rng.uniform(0, 8) + (0.8 if k % 7 == 0 else 0) * pr2 + rng.normal(0, .5, m)) - 1
            fh.write(f"{g}\t0\t" + "\t".join(f"{max(x,0):.2f}" for x in v) + "\n")
    return {"sm": f"{d}/sim_series_matrix.txt.gz", "annot": REAL["annot"], "smc": f"{d}/smc"}

def structure():
    E, d = load_gse(REAL["sm"], REAL["annot"])
    P3 = read_list(P3FILE, "##P3_START", "##P3_END"); P4 = read_list(P4FILE, "##P4_START", "##P4_END")
    f2, m2 = resolve(P2, set(E.index)); f3, m3 = resolve(P3, set(E.index)); f4, m4 = resolve(P4, set(E.index))
    log(f"GSE25066 parsed: genes after probe rule {E.shape[0]}; eligibility fields present; P2 {len(f2)}/18 missing {m2}; P3 {len(f3)}/120 missing {m3}; P4 {len(f4)}/187")
    E2, d2 = load_smc(REAL["smc"])
    f2, m2 = resolve(P2, set(E2.index)); f3, m3 = resolve(P3, set(E2.index))
    log(f"SMC 2018 parsed: genes {E2.shape[0]}; P2 {len(f2)}/18; P3 {len(f3)}/120 missing {m3}")
    log("structure check done (no counts, shares or values printed)")

if __name__ == "__main__":
    mode = sys.argv_saved[1]
    if mode == "simulate":
        d = "/tmp/claude-0/-home-claude/0c0aa417-8279-5d02-911f-de8e4a5730f0/scratchpad/sim10"; os.makedirs(d, exist_ok=True)
        log("writing simulated files"); paths = simulate(d); run_all(paths, "_SIMULATED", nboot=300)
    elif mode == "structure": structure()
    elif mode == "run":
        run_all(REAL, "_EXPLORATORY-ER-all508")
