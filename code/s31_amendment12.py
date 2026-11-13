"""s31_amendment12.py  Amendment 12: additional analyses of transfer, misspecified prevalence, the Ki-67
prediction and model fit, prompted by pre-submission critiques of the manuscript (13 Nov 2026).
Written after all earlier results were known.

Analyses (numbering as in Amendment 12):
  N2  Transfer between natural clinical subgroups of SCAN-B (prevalence and spectrum both differ)
  N3  Target-weighted kappa (SK) with the target luminal B share misspecified
  N4  Binormal prediction of the Ki-67 cut-off in percentage points (GSE81538, consensus Ki-67)
  N5  Binormal goodness of fit (a, b, R^2, bootstrap CI of b; equal-variance comparison)
  N7  Case-mix share of variance over subsets of imposed shares (from Amendment 11 derivations)
  N8  Ki-67 near-optimal region of accuracy and kappa at each luminal B share (population weights)
  N9  Descriptive characteristics of each cohort

Rules, candidate thresholds, tie rule, q_A scale and the binormal fit are those of
s27_amendment11.py (Amendment 11), imported unchanged and checked by hash.

Usage:
  python3 -I s31_amendment12.py <GSE81538_series_matrix.txt.gz> --dryrun   # labels permuted; code check
  python3 -I s31_amendment12.py <GSE81538_series_matrix.txt.gz>            # registered run
Outputs: results/A12_*.csv, A12_decision.json, A12_run.log (suffix _DRYRUN in dry-run mode)
"""
import os, sys, gzip, json, time, hashlib, importlib.util
import numpy as np, pandas as pd
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(HERE, "..", "results"))
DRY = "--dryrun" in sys.argv
SUF = "_DRYRUN" if DRY else ""
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
SEED = 20261113
NREP = 500
NBOOT = 500

# ---- import Amendment 11 functions unchanged (as s28 does), protecting its registered log
S27 = os.path.join(HERE, "s27_amendment11.py")
assert hashlib.sha256(open(S27, "rb").read()).hexdigest().startswith("aa17d477f9c9bf4d"), "s27 changed"
REGLOG = os.path.join(R, "A11_run.log")
_saved = open(REGLOG, "rb").read()
_argv = sys.argv; sys.argv = [S27]
spec = importlib.util.spec_from_file_location("s27", S27); s27 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s27); sys.argv = _argv
s27.LOG.close(); open(REGLOG, "wb").write(_saved)
rule_thresholds, Target, binormal_fit, model_qA = s27.rule_thresholds, s27.Target, s27.binormal_fit, s27.model_qA

T0 = time.time()
LOG = open(os.path.join(R, f"A12_run{SUF}.log"), "w")
def log(m):
    s = f"[{time.time()-T0:7.1f}s] {m}"; print(s, flush=True); LOG.write(s + "\n"); LOG.flush()

COH = {"TCGA-BRCA": "cohort_tcga.csv", "METABRIC": "cohort_metabric.csv", "SCAN-B": "cohort_scanb.csv"}


def load(cname, rng_perm):
    d = pd.read_csv(os.path.join(R, COH[cname]), low_memory=False)
    m = d.PAM50.isin(["LumA", "LumB"]).values
    lab = d.PAM50.values[m].copy()
    if DRY:
        lab = rng_perm.permutation(lab)
    return d, m, (lab == "LumB").astype(int)


def evaluate(T, t, t_ref):
    """Transfer metrics of threshold t in target T against reference threshold t_ref."""
    return dict(qA=T.qA(t), err=T.qA(t) - T.qA(t_ref), kappa=T.kappa(t),
                label_diff=abs(T.F(T.L, t) - T.F(T.L, t_ref)))


# ---------------------------------------------------------------- N2 natural subgroups (SCAN-B)
def n2(rng, rng_perm):
    d, m, y = load("SCAN-B", rng_perm)
    L = d[m].copy(); L["y"] = y
    node = L.NODE.map({"NodeNegative": 0, "1to3": 1, "4toX": 1})      # SubMicroMet and missing excluded
    splits = {
        "size_le20_vs_gt20": (L.SIZE <= 20, L.SIZE > 20),
        "node_neg_vs_pos": (node == 0, node == 1),
        "age_lt50_vs_ge50": (L.AGE_N < 50, L.AGE_N >= 50),
    }
    pop_pi = L.y.mean()                                                 # full SCAN-B luminal B share
    rows, info = [], []
    for score in ["P2", "P1"]:
        for sname, (g1, g2) in splits.items():
            for direction, (gd, gt) in {"1to2": (g1, g2), "2to1": (g2, g1)}.items():
                Dd, Dt = L[gd.fillna(False).values], L[gt.fillna(False).values]
                xd, yd = Dd[score].values.astype(float), Dd.y.values
                xt, yt = Dt[score].values.astype(float), Dt.y.values
                T = Target(xt, yt, xt)
                tt = rule_thresholds(xt, yt, T.pi)                     # target optima (same rule)
                ref_K = tt["K"]
                info.append(dict(score=score, split=sname, direction=direction, n_deriv=len(xd),
                                 pi_deriv=100 * yd.mean(), n_target=len(xt), pi_target=100 * T.pi,
                                 kappa_target_best=T.kappa(ref_K)))
                n = min(400, len(xd))
                for rep in range(-1, NREP):                             # rep -1: whole derivation subgroup
                    if rep < 0:
                        xx, yy = xd, yd
                    else:
                        i = rng.integers(0, len(xd), n); xx, yy = xd[i], yd[i]
                    for variant, pt in {"oracle": T.pi, "population": pop_pi}.items():
                        th = rule_thresholds(xx, yy, pt)
                        if th is None:
                            continue
                        rules = ["K", "ACC", "PM", "YJ", "SK"] if variant == "oracle" else ["SK"]
                        for r in rules:
                            name = r if r != "SK" else f"SK_{variant}"
                            ref = tt[r] if r in ("K", "ACC", "PM", "YJ") else ref_K
                            e1 = evaluate(T, th[r], ref); e2 = evaluate(T, th[r], ref_K)
                            rows.append(dict(score=score, split=sname, direction=direction, rep=rep, n=len(xx),
                                             rule=name, err_same_rule=e1["err"], err_vs_K=e2["err"],
                                             label_diff_vs_K=e2["label_diff"], kappa_target=e1["kappa"]))
                log(f"N2 {score} {sname} {direction}: n_deriv={len(xd)}, n_target={len(xt)} done")
    R2 = pd.DataFrame(rows); I2 = pd.DataFrame(info)
    R2.to_csv(os.path.join(R, f"A12_N2_derivations{SUF}.csv.gz"), index=False)
    I2.to_csv(os.path.join(R, f"A12_N2_subgroups{SUF}.csv"), index=False)
    b = R2[R2.rep >= 0]
    S = (b.groupby(["score", "split", "direction", "rule"])
         .apply(lambda g: pd.Series(dict(rmse_same_rule=np.sqrt((g.err_same_rule ** 2).mean()),
                                         rmse_vs_K=np.sqrt((g.err_vs_K ** 2).mean()),
                                         bias_vs_K=g.err_vs_K.mean(),
                                         label_diff_vs_K_pct=100 * g.label_diff_vs_K.mean(),
                                         kappa_target_mean=g.kappa_target.mean())))
         .reset_index())
    W = R2[R2.rep < 0][["score", "split", "direction", "rule", "err_vs_K", "kappa_target"]].rename(
        columns={"err_vs_K": "whole_subgroup_err_vs_K", "kappa_target": "whole_subgroup_kappa"})
    S = S.merge(W, on=["score", "split", "direction", "rule"], how="left").merge(
        I2, on=["score", "split", "direction"], how="left")
    S.to_csv(os.path.join(R, f"A12_N2_summary{SUF}.csv"), index=False)
    # primary split (fixed rule): largest absolute difference in luminal B share between subgroups, P2
    gap = I2[(I2.score == "P2") & (I2.direction == "1to2")].assign(gap=lambda z: (z.pi_deriv - z.pi_target).abs())
    primary = gap.sort_values("gap", ascending=False).split.iloc[0]
    P = S[(S.score == "P2") & (S.split == primary)].set_index(["direction", "rule"])
    better = {v: bool(all(P.loc[(dr, f"SK_{v}"), "rmse_vs_K"] < P.loc[(dr, "K"), "rmse_vs_K"]
                          for dr in ["1to2", "2to1"])) for v in ["oracle", "population"]}
    log(f"N2 primary split {primary} (gap {gap.gap.max():.1f} points); SK better than K in both directions: {better}")
    return dict(primary_split=primary, primary_gap_points=float(gap.gap.max()),
                sk_oracle_better_both_directions=better["oracle"],
                sk_population_better_both_directions=better["population"])


# ---------------------------------------------------------------- N3 misspecified target share
def n3(rng, rng_perm):
    deltas = [-15, -10, -5, 0, 5, 10, 15]; shares = [25, 35, 45, 55, 65]; n = 400
    rows = []
    for cname in COH:
        d, m, y = load(cname, rng_perm)
        x = d.P2.values.astype(float)[m]; T = Target(x, y, d.P2.values.astype(float))
        A, B = x[y == 0], x[y == 1]; tt = rule_thresholds(x, y, T.pi); ref = tt["K"]
        for pi in shares:
            nb = int(round(n * pi / 100)); na = n - nb
            for rep in range(NREP):
                xx = np.r_[rng.choice(A, na, replace=True), rng.choice(B, nb, replace=True)]
                yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
                base = rule_thresholds(xx, yy, T.pi)
                if base is None:
                    continue
                e = evaluate(T, base["K"], ref)
                rows.append((cname, pi, rep, "K", np.nan, e["err"], e["label_diff"], e["kappa"]))
                for dl in deltas:
                    pt = min(max(T.pi + dl / 100, 0.05), 0.95)
                    th = rule_thresholds(xx, yy, pt)
                    e = evaluate(T, th["SK"], ref)
                    rows.append((cname, pi, rep, "SK", dl, e["err"], e["label_diff"], e["kappa"]))
        log(f"N3 {cname}: done")
    D = pd.DataFrame(rows, columns=["cohort", "pi", "rep", "rule", "delta", "err_vs_K", "label_diff", "kappa"])
    D.to_csv(os.path.join(R, f"A12_N3_derivations{SUF}.csv.gz"), index=False)
    S = (D.groupby(["cohort", "rule", "delta"], dropna=False)
         .apply(lambda g: pd.Series(dict(rmse=np.sqrt((g.err_vs_K ** 2).mean()), bias=g.err_vs_K.mean(),
                                         label_diff_pct=100 * g.label_diff.mean(), kappa_mean=g.kappa.mean())))
         .reset_index())
    S.to_csv(os.path.join(R, f"A12_N3_summary{SUF}.csv"), index=False)
    tol = {}
    for c in COH:
        k = S[(S.cohort == c) & (S.rule == "K")].rmse.iloc[0]
        ok = S[(S.cohort == c) & (S.rule == "SK") & (S.rmse < k)].delta.abs()
        tol[c] = float(ok.max()) if len(ok) else None
    # tolerance: largest |delta| such that every |delta'| <= |delta| (both signs) keeps SK below K
    tol_all = None
    for a in [0, 5, 10, 15]:
        sub = S[(S.rule == "SK") & (S.delta.abs() <= a)]
        kk = S[S.rule == "K"].set_index("cohort").rmse
        if all(sub[sub.cohort == c].rmse.max() < kk[c] for c in COH):
            tol_all = a
    log(f"N3 tolerance (largest |delta| with SK RMSE below K in all cohorts, both directions): {tol_all}")
    return dict(n3_tolerance_points=tol_all)


# ---------------------------------------------------------------- GSE81538 parsing (as s28)
def parse81538(path):
    rows = []; gsm = ttl = None
    with gzip.open(path, "rt") as f:
        for line in f:
            if line.startswith("!Sample_geo_accession"): gsm = [v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
            if line.startswith("!Sample_title"): ttl = [v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
            if line.startswith("!Sample_characteristics_ch1"):
                rows.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
    meta = pd.DataFrame({"title": ttl, "gsm": gsm})
    for vals in rows:
        k = vals[0].split(": ", 1)[0] if ": " in vals[0] else vals[0]
        meta[k.strip()] = [v.split(": ", 1)[1] if ": " in v else np.nan for v in vals]
    num = lambda c: pd.to_numeric(meta[c], errors="coerce")
    meta["ER"] = num("er consensus"); meta["HER2"] = num("her2 consensus"); meta["K"] = num("ki67 consensus")
    meta["PAM50"] = meta["pam50 subtype"]
    el = meta[meta.ER.isin([1, 2, 3]) & (meta.HER2 == 0)]
    lum = el[el.PAM50.isin(["LumA", "LumB"])].dropna(subset=["K"])
    return el, lum


def qa_to_value(A_sorted, q):
    """Score value at luminal A quantile q (0-100), linear interpolation between order statistics."""
    return float(np.percentile(A_sorted, q, method="linear"))


def fit_r2(T):
    t = np.unique(T.L); fpr = 1 - T.F(T.A, t); tpr = 1 - T.F(T.B, t)
    msk = (fpr >= .05) & (fpr <= .95) & (tpr >= .05) & (tpr <= .95)
    X, Y = norm.ppf(fpr[msk]), norm.ppf(tpr[msk])
    if msk.sum() < 3:
        return np.nan, int(msk.sum()), np.nan
    b, a = np.polyfit(X, Y, 1); res = Y - (a + b * X)
    r2 = 1 - (res ** 2).sum() / ((Y - Y.mean()) ** 2).sum()
    a_eq = float(np.mean(Y - X))                                       # equal-variance fit (b = 1)
    return r2, int(msk.sum()), a_eq


# ---------------------------------------------------------------- N4 + N5 + N8
def n4_n5_n8(rng, rng_perm, path81538):
    out = {}
    # N5 binormal goodness of fit, RNA cohorts
    fits = []
    o1 = pd.read_csv(os.path.join(R, "A11_O1_slopes.csv"))
    for cname in COH:
        d, m, y = load(cname, rng_perm)
        for s in ["P2", "P1"]:
            x = d[s].values.astype(float)[m]; T = Target(x, y, d[s].values.astype(float))
            a, b = binormal_fit(T); r2, npts, a_eq = fit_r2(T)
            A, B = x[y == 0], x[y == 1]; bs = []
            for _ in range(NBOOT):
                xx = np.r_[rng.choice(A, len(A)), rng.choice(B, len(B))]; yy = np.r_[np.zeros(len(A), int), np.ones(len(B), int)]
                bs.append(binormal_fit(Target(xx, yy, xx))[1])
            sl = {}
            for lab, (aa, bb) in {"free": (a, b), "equal_var": (a_eq, 1.0)}.items():
                for r in ["K", "ACC"]:
                    q = [model_qA(aa, bb, p / 100)[r] for p in [15, 25, 35, 45, 55, 65]]
                    sl[f"slope_model_{lab}_{r}"] = np.polyfit([15, 25, 35, 45, 55, 65], q, 1)[0]
            row = dict(cohort=cname, score=s, a=a, b=b, b_ci_lo=np.percentile(bs, 2.5), b_ci_hi=np.percentile(bs, 97.5),
                       r2=r2, n_points=npts, a_equal_var=a_eq, **sl)
            for r in ["K", "ACC"]:
                v = o1[(o1.cohort == cname) & (o1.score == s) & (o1.rule == r)].slope_qA_per_point
                row[f"slope_resampled_{r}"] = float(v.iloc[0]) if len(v) else np.nan
            fits.append(row)
            log(f"N5 {cname} {s}: a={a:.3f} b={b:.3f} R2={r2:.3f}")
    # Ki-67 (GSE81538)
    el, lum = parse81538(path81538)
    x = lum.K.values.astype(float); lab = lum.PAM50.values.copy()
    if DRY:
        lab = rng_perm.permutation(lab)
    y = (lab == "LumB").astype(int)
    log(f"GSE81538 identity check: eligible {len(el)}, LumA {(y==0).sum()}, LumB {(y==1).sum()} (expected 256, 147, 85)")
    if not DRY and (len(el), int((y == 0).sum()), int((y == 1).sum())) != (256, 147, 85):
        log("identity check FAILED; Ki-67 analyses not run"); return out, pd.DataFrame(fits)
    T = Target(x, y, el.K.dropna().values.astype(float)); A, B = np.sort(x[y == 0]), np.sort(x[y == 1])
    a, b = binormal_fit(T); r2, npts, a_eq = fit_r2(T)
    fits.append(dict(cohort="GSE81538", score="Ki67", a=a, b=b, r2=r2, n_points=npts, a_equal_var=a_eq,
                     n_distinct=len(np.unique(x))))
    pd.DataFrame(fits).to_csv(os.path.join(R, f"A12_N5_binormal_fit{SUF}.csv"), index=False)
    # N4 prediction in Ki-67 percentage points
    def predict(aa, bb, Asort):
        res = {}
        for r in ["K", "ACC", "PM", "YJ"]:
            for p in [25, 65]:
                res[f"{r}_{p}"] = qa_to_value(Asort, model_qA(aa, bb, p / 100)[r])
            res[f"{r}_diff"] = res[f"{r}_25"] - res[f"{r}_65"]
        return res
    point = predict(a, b, A); boot = []
    for _ in range(NBOOT * 2):
        xa, xb = rng.choice(A, len(A)), rng.choice(B, len(B))
        xx = np.r_[xa, xb]; yy = np.r_[np.zeros(len(A), int), np.ones(len(B), int)]
        aa, bb = binormal_fit(Target(xx, yy, xx)); boot.append(predict(aa, bb, np.sort(xa)))
    Bt = pd.DataFrame(boot)
    rows = [dict(quantity=k, estimate=v, ci_lo=np.percentile(Bt[k], 2.5), ci_hi=np.percentile(Bt[k], 97.5)) for k, v in point.items()]
    pd.DataFrame(rows).to_csv(os.path.join(R, f"A12_N4_ki67_prediction{SUF}.csv"), index=False)
    log("N4 Ki-67 predicted thresholds (%): " + ", ".join(f"{k}={v:.1f}" for k, v in point.items()))
    out["n4_K_diff_25_minus_65"] = point["K_diff"]; out["n4_ACC_diff_25_minus_65"] = point["ACC_diff"]
    # N8 near-optimal region, population weights, candidate thresholds as in s27 (observed values)
    cand = np.unique(x); cand = cand[(cand >= np.percentile(x, 5)) & (cand <= np.percentile(x, 95))]
    rows = []
    for p in [15, 25, 35, 45, 55, 65]:
        pi = p / 100
        sens = np.array([(B > c).mean() for c in cand]); fpr = np.array([(A > c).mean() for c in cand])
        acc = pi * sens + (1 - pi) * (1 - fpr); q = pi * sens + (1 - pi) * fpr
        pe = pi * q + (1 - pi) * (1 - q); kap = (acc - pe) / (1 - pe)
        for nm, v in {"accuracy": acc, "kappa": kap}.items():
            best = v.max(); near = cand[v >= best - 0.01]
            rows.append(dict(share=p, criterion=nm, best=best, argmax_lowest=cand[np.where(v == best)[0].min()],
                             near_lo=near.min(), near_hi=near.max(), n_near=len(near)))
    pd.DataFrame(rows).to_csv(os.path.join(R, f"A12_N8_ki67_near_optimal{SUF}.csv"), index=False)
    log("N8 done")
    return out, pd.DataFrame(fits)


# ---------------------------------------------------------------- N7 variance share subsets
def n7():
    subsets = {"registered_25_65": [25, 35, 45, 55, 65], "inner_35_55": [35, 45, 55],
               "low_25_45": [25, 35, 45], "high_45_65": [45, 55, 65]}
    rows = []
    for fname, label in [("A11_derivations.csv.gz", "RNA"), ("A11K_derivations.csv.gz", "Ki67")]:
        p = os.path.join(R, fname.replace(".csv.gz", f"{SUF}.csv.gz")) if DRY and label == "RNA" else os.path.join(R, fname)
        if not os.path.exists(p):
            log(f"N7: {fname} not found; skipped"); continue
        D = pd.read_csv(p)
        if "cohort" not in D.columns:
            D["cohort"] = "GSE81538"
        if "score" not in D.columns:
            D["score"] = "Ki67"
        for sname, ss in subsets.items():
            g0 = D[D.pi.isin(ss)]
            for (c, s, n, r), g in g0.groupby(["cohort", "score", "n", "rule"]):
                means = g.groupby("pi").qA.mean(); within = g.groupby("pi").qA.var(ddof=1).mean()
                between = means.var(ddof=0); tot = between + within
                rows.append(dict(source=label, subset=sname, cohort=c, score=s, n=n, rule=r,
                                 frac_casemix=between / tot if tot > 0 else np.nan))
        log(f"N7 {label}: done")
    pd.DataFrame(rows).to_csv(os.path.join(R, f"A12_N7_variance_subsets{SUF}.csv"), index=False)


# ---------------------------------------------------------------- N9 descriptive table
def n9():
    rows = []
    for cname, f in COH.items():
        d = pd.read_csv(os.path.join(R, f), low_memory=False)
        age = pd.to_numeric(d.AGE_N, errors="coerce")
        row = dict(cohort=cname, n=len(d), luminal_A=int((d.PAM50 == "LumA").sum()), luminal_B=int((d.PAM50 == "LumB").sum()),
                   age_median=age.median(), age_q1=age.quantile(.25), age_q3=age.quantile(.75))
        if cname == "SCAN-B":
            sz = pd.to_numeric(d.SIZE, errors="coerce")
            row.update(size_median_mm=sz.median(), node_positive_pct=100 * d.NODE.isin(["1to3", "4toX"]).mean(),
                       grade3_pct=100 * (d.NHG == "G3").mean(), chemo_pct=100 * pd.to_numeric(d.CHEMO, errors="coerce").mean())
        if cname == "METABRIC":
            row.update(size_median_mm=pd.to_numeric(d.TUMOR_SIZE, errors="coerce").median(),
                       node_positive_pct=100 * (pd.to_numeric(d.LYMPH_NODES_EXAMINED_POSITIVE, errors="coerce") > 0).mean(),
                       grade3_pct=100 * (pd.to_numeric(d.GRADE, errors="coerce") == 3).mean(),
                       chemo_pct=100 * d.CHEMOTHERAPY.astype(str).str.upper().eq("YES").mean())
        if cname == "TCGA-BRCA":
            st = d.AJCC_PATHOLOGIC_TUMOR_STAGE.astype(str)
            row.update(stage_I_pct=100 * st.str.match(r"STAGE I[ABC]?$").mean(),
                       stage_II_pct=100 * st.str.match(r"STAGE II[ABC]?$").mean(),
                       stage_III_IV_pct=100 * st.str.match(r"STAGE (III|IV)").mean(),
                       node_positive_pct=100 * d.PATH_N_STAGE.astype(str).str.match(r"N[1-3]").mean())
        rows.append(row)
    pd.DataFrame(rows).to_csv(os.path.join(R, f"A12_N9_cohorts{SUF}.csv"), index=False)
    log("N9 done")


def main():
    if not ARGS:
        sys.exit("give the path to GSE81538_series_matrix.txt.gz")
    rng = np.random.default_rng(SEED); rng_perm = np.random.default_rng(1)
    log(f"Amendment 12 run, mode={'DRY RUN (permuted labels)' if DRY else 'REGISTERED'}, seed={SEED}")
    log(f"s27 SHA-256 {hashlib.sha256(open(S27,'rb').read()).hexdigest()}")
    log(f"s31 SHA-256 {hashlib.sha256(open(os.path.abspath(__file__),'rb').read()).hexdigest()}")
    dec = {"mode": "dryrun" if DRY else "registered"}
    dec.update(n2(rng, rng_perm))
    dec.update(n3(rng, rng_perm))
    o, _ = n4_n5_n8(rng, rng_perm, ARGS[0]); dec.update(o)
    n7(); n9()
    json.dump(dec, open(os.path.join(R, f"A12_decision{SUF}.json"), "w"), indent=1, default=float)
    log("done")


if __name__ == "__main__":
    main()
