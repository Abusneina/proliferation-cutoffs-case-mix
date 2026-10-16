"""s22_amendment9.py  Amendment 9: overall survival as a common endpoint (O1 to O5).

Usage
  python3 -I s22_amendment9.py dryrun
      Code test only. Outcomes are randomly permuted within each cohort before any model is fit,
      so no real group-outcome association can be seen. Output goes to a separate _DRYRUN file.
  python3 -I s22_amendment9.py run <FROZEN_amendment_9_file>
      Registered analysis. Refuses to start unless the file name carries FROZEN.
Progress is printed throughout.
"""
import sys, time, warnings
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
RES = "/home/claude/pkg/results"; OUT = "/home/claude/work/results"
CUTS = {"P2": (59, 74), "P1": (64, 77)}; MARGIN = (0.67, 1.50)
ORDER = {"STABLE_A": 0, "DISCORDANT": 1, "STABLE_B": 2}

# ---------------- covariates (copied from s03 and s07 without change) ----------------
def stage_group(c, s):
    s = str(s).upper()
    if c == "TCGA":
        for k, v in [("STAGE IV", "III-IV"), ("STAGE III", "III-IV"), ("STAGE II", "II"), ("STAGE I", "I")]:
            if s.startswith(k): return v
        return "unk"
    try: return {0: "I", 1: "I", 2: "II"}.get(int(float(s)), "III-IV")
    except: return "unk"

def X_stage(sub, stages):
    X = pd.DataFrame(index=sub.index); X["age"] = sub["AGE_N"].values
    for s_ in stages:
        col = (sub["STAGE_G"] == s_).astype(float).values
        ev = int(sub["EVENT"].values[col == 1].sum())
        if 0 < col.sum() < len(col) and ev >= 5: X[f"st_{s_}"] = col
    return X

def X_scanb(sub, grade=False):
    X = pd.DataFrame(index=sub.index); X["age"] = sub.AGE_N.values; X["size"] = sub.SIZE.values
    for lv in ["SubMicroMet", "1to3", "4toX"]:
        col = (sub.NODE == lv).astype(float).values
        if 0 < col.sum() < len(col) and sub.EVENT.values[col == 1].sum() >= 3: X[f"n_{lv}"] = col
    X.loc[sub.NODE.isin(["NA"]).values | sub.NODE.isna().values, "age"] = np.nan
    if grade:
        for lv in ["G2", "G3"]: X[f"g_{lv}"] = (sub.NHG == lv).astype(float).values
        X.loc[(sub.NHG == "NA").values, "age"] = np.nan
    return X

def cox(t, e, X):
    ok = X.notna().all(axis=1).values & ~np.isnan(t) & (t >= 0)
    m = PHReg(t[ok], X.values[ok], status=e[ok]).fit(disp=False)
    ci = np.exp(m.conf_int())
    return dict(n=int(ok.sum()), ev=int(e[ok].sum()), hr=float(np.exp(m.params[0])), lo=float(ci[0][0]),
                hi=float(ci[0][1]), p=float(m.pvalues[0]), b=float(m.params[0]), se=float(m.bse[0]))

# ---------------- cohorts with overall survival ----------------
def load(cohort):
    if cohort == "TCGA":
        d = pd.read_csv(f"{RES}/cohort_tcga.csv", low_memory=False)
        d["STAGE_G"] = [stage_group("TCGA", s) for s in d.AJCC_PATHOLOGIC_TUMOR_STAGE]
    elif cohort == "METABRIC":
        d = pd.read_csv(f"{RES}/cohort_metabric.csv", low_memory=False)
        d["STAGE_G"] = [stage_group("METABRIC", s) for s in d.TUMOR_STAGE]
    else:
        d = pd.read_csv(f"{RES}/cohort_scanb.csv", low_memory=False, dtype={"NODE": str, "NHG": str})
        d["NODE"] = d.NODE.fillna("NA"); d["NHG"] = d.NHG.fillna("NA")
        return d.reset_index(drop=True)                      # TIME/EVENT already overall survival
    d["TIME"] = pd.to_numeric(d.OS_MONTHS, errors="coerce")
    d["EVENT"] = d.OS_STATUS.astype(str).str.startswith("1").astype(int)
    return d[d.TIME.notna() & (d.TIME >= 0)].reset_index(drop=True)

def main(dry):
    rng = np.random.default_rng(1)
    rows = []
    for cohort in ["TCGA", "METABRIC", "SCAN-B"]:
        d = load(cohort)
        if dry:
            p = rng.permutation(len(d)); d["TIME"] = d.TIME.values[p]; d["EVENT"] = d.EVENT.values[p]
        stages = sorted(set(d.get("STAGE_G", pd.Series(["x"]))))[1:] if cohort != "SCAN-B" else None
        Xb = (lambda s: X_scanb(s)) if cohort == "SCAN-B" else (lambda s: X_stage(s, stages))
        log("=" * 70); log(f"{cohort}: n={len(d)}, overall-survival deaths={int(d.EVENT.sum())}")
        for sc, (cl, ch) in CUTS.items():
            v = d[sc].values; tl, th = np.nanpercentile(v, cl), np.nanpercentile(v, ch)
            g = np.where(v <= tl, "STABLE_A", np.where(v <= th, "DISCORDANT", "STABLE_B")); d["_g"] = g
            for grp in ["STABLE_A", "DISCORDANT", "STABLE_B"]:
                m = g == grp
                rows.append(dict(cohort=cohort, score=sc, test=f"O5_{grp}", n=int(m.sum()), ev=int(d.EVENT[m].sum()),
                                 hr=100*m.mean()))
            log(f"  {sc} zone {cl}-{ch}: " + ", ".join(f"{k} n={int((g==k).sum())} deaths={int(d.EVENT[g==k].sum())}" for k in ORDER))
            # O1 (TCGA, METABRIC); SCAN-B D1 = registered C1, carried over unchanged
            if cohort != "SCAN-B":
                for grp in ["STABLE_A", "STABLE_B"]:
                    sub = d[d._g.isin([grp, "DISCORDANT"])]; X = Xb(sub); X.insert(0, "grp", (sub._g == grp).astype(float).values)
                    r = cox(sub.TIME.values, sub.EVENT.values, X)
                    rows.append(dict(cohort=cohort, score=sc, test=f"O1_{grp}_vs_DISC", **r))
                    log(f"  [O1] {sc} {grp} vs DISC: HR {r['hr']:.2f} [{r['lo']:.2f}, {r['hi']:.2f}] p={r['p']:.3g} n={r['n']} deaths={r['ev']}")
            else:
                S = pd.read_csv(f"{RES}/SCANB_results.csv")
                for grp, tag in [("STABLE_A", "C1a"), ("STABLE_B", "C1b")]:
                    r = S[(S.block == tag) & (S.score == sc)].iloc[0]
                    rows.append(dict(cohort=cohort, score=sc, test=f"O1_{grp}_vs_DISC", n=r.n, ev=r.ev, hr=r.val, lo=r.lo,
                                     hi=r.hi, p=r.p, b=r.b, se=r.se))
                    log(f"  [O1] {sc} {grp} vs DISC (registered C1, carried over): HR {r.val:.2f} [{r.lo:.2f}, {r.hi:.2f}]")
            # O3 in zone and whole cohort
            sub = d[d._g == "DISCORDANT"]; X = Xb(sub); X.insert(0, "score", stats.zscore(sub[sc].values, nan_policy="omit"))
            r = cox(sub.TIME.values, sub.EVENT.values, X); rows.append(dict(cohort=cohort, score=sc, test="O3_continuous_in_zone", **r))
            empty = r["p"] > 0.05 and MARGIN[0] <= r["lo"] and r["hi"] <= MARGIN[1]
            log(f"  [O3] {sc} in zone: HR/SD {r['hr']:.2f} [{r['lo']:.2f}, {r['hi']:.2f}] p={r['p']:.3g} deaths={r['ev']} -> R1 empty: {empty}")
            X = Xb(d); X.insert(0, "score", stats.zscore(d[sc].values, nan_policy="omit"))
            r = cox(d.TIME.values, d.EVENT.values, X); rows.append(dict(cohort=cohort, score=sc, test="O3b_continuous_whole", **r))
            # O4 trend
            X = Xb(d); X.insert(0, "trend", [ORDER[x] for x in d._g])
            r = cox(d.TIME.values, d.EVENT.values, X); rows.append(dict(cohort=cohort, score=sc, test="O4_trend", **r))
            log(f"  [O4] {sc} trend: HR/step {r['hr']:.2f} [{r['lo']:.2f}, {r['hi']:.2f}] p={r['p']:.3g}")
    R = pd.DataFrame(rows)
    # BH within cohort over O1, O3, O4 (SCAN-B O1 carried over is included, as in R4)
    R["p_BH"] = np.nan
    for c in R.cohort.unique():
        mk = (R.cohort == c) & R.test.str.match(r"O1_|O3_continuous_in_zone|O4_")
        p = R.loc[mk, "p"].values.astype(float); o = np.argsort(p); m = len(p); adj = np.empty(m); prev = 1.0
        for i in range(m-1, -1, -1): prev = min(prev, p[o[i]]*m/(i+1)); adj[o[i]] = prev
        R.loc[mk, "p_BH"] = adj
    # O2 pooled
    pool = []
    for sc in ["P2", "P1"]:
        for grp, tag in [("STABLE_A", "C1a"), ("STABLE_B", "C1b")]:
            E = {c: R[(R.cohort == c) & (R.score == sc) & (R.test == f"O1_{grp}_vs_DISC")].iloc[0] for c in ["TCGA", "METABRIC", "SCAN-B"]}
            for setname, mem in [("all three (primary)", ["TCGA", "METABRIC", "SCAN-B"]), ("METABRIC+SCAN-B", ["METABRIC", "SCAN-B"])]:
                b = np.array([E[c].b for c in mem], float); se = np.array([E[c].se for c in mem], float); w = 1/se**2
                bf = (w*b).sum()/w.sum(); sef = np.sqrt(1/w.sum()); Q = (w*(b-bf)**2).sum(); k = len(b)-1
                I2 = max(0, (Q-k)/Q) if Q > 0 else 0; tau2 = max(0, (Q-k)/(w.sum()-(w**2).sum()/w.sum()))
                wr = 1/(se**2+tau2); br = (wr*b).sum()/wr.sum(); ser = np.sqrt(1/wr.sum())
                for mth, (e, s_) in [("fixed", (bf, sef)), ("random", (br, ser))]:
                    lo, hi = np.exp(e-1.96*s_), np.exp(e+1.96*s_); v = ""
                    if tag == "C1b":
                        v = ("B-like supported on a common endpoint" if MARGIN[0] <= lo and hi <= MARGIN[1]
                             else ("refuted" if lo > 1 or hi < 1 else "inconclusive"))
                    elif hi < 1: v = "discordant worse than stable A-like"
                    pool.append(dict(score=sc, test=tag, set=setname, method=mth, hr=np.exp(e), lo=lo, hi=hi, I2=I2, verdict=v))
                    log(f"[O2] {sc} {tag} {setname:<20} {mth:<6}: HR {np.exp(e):.2f} [{lo:.2f}, {hi:.2f}] I2={I2:.0%} {v}")
    sfx = "_DRYRUN-permuted-outcomes" if dry else ""
    R.to_csv(f"{OUT}/A9_overall_survival{sfx}.csv", index=False)
    pd.DataFrame(pool).to_csv(f"{OUT}/A9_pooled{sfx}.csv", index=False)
    log("done.")

if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    if sys.argv[1] == "dryrun": main(True)
    elif sys.argv[1] == "run":
        assert len(sys.argv) > 2 and "FROZEN" in sys.argv[2], "Amendment 9 must be frozen first"
        main(False)
