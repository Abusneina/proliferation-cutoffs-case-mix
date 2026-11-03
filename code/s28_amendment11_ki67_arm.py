"""s28_amendment11_ki67_arm.py  Amendment 11, CONDITIONAL ARM: consensus Ki-67 in GSE81538.
Written 2026-11-03 after the Amendment 11 registration (osf.io/vhg4s) and after the RNA run; before any
Ki-67 result of this arm was computed. Implements the arm as registered:
  "O1 to O3 are run on consensus Ki-67 with n in {150, 232} and the same shares, eligibility and tie
   rule as Amendment 7."
Implementation choices fixed before the run:
 * Eligibility as Amendment 7 (s11): ER consensus in {1, 2, 3}, HER2 consensus = 0, PAM50 LumA or LumB,
   consensus Ki-67 present. Identity check: counts must equal Amendment 7 (256 eligible; 147 LumA, 85 LumB);
   the run stops otherwise. (No MD5 of the series matrix was recorded at the first download; this count
   check replaces the MD5 check named in the amendment; logged as a deviation.)
 * Rules, candidate thresholds, tie rule (lowest threshold), q_A scale, seed and outcome definitions are
   those of s27_amendment11.py, imported unchanged (SHA-256 aa17d477...). Shares 15-65%, 500 resamples.
 * O2/O3 use shares 25-65% as in s27. O4 and O5 are not part of the arm and are not run.
Usage: python3 -I s28_amendment11_ki67_arm.py <path to GSE81538_series_matrix.txt.gz>
"""
import os, sys, gzip, hashlib, importlib.util
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
S27 = os.path.join(HERE, "s27_amendment11.py")
assert hashlib.sha256(open(S27, "rb").read()).hexdigest().startswith("aa17d477f9c9bf4d"), "s27 changed"
REGLOG = os.path.normpath(os.path.join(HERE, "..", "results", "A11_run.log"))
_saved = open(REGLOG, "rb").read()                         # importing s27 reopens its log in "w" mode
sys_argv = sys.argv; sys.argv = [S27]                      # import s27 in registered mode, without running main
spec = importlib.util.spec_from_file_location("s27", S27); s27 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s27); sys.argv = sys_argv
s27.LOG.close(); open(REGLOG, "wb").write(_saved)          # restore the registered run log unchanged
s27.LOG = open(os.path.join(s27.R, "A11K_run.log"), "w")
R = s27.R; log = s27.log

def parse(path):
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
    return meta

def main(path):
    log(f"Ki-67 arm: file {os.path.basename(path)} md5 {hashlib.md5(open(path,'rb').read()).hexdigest()}")
    m = parse(path)
    el = m[m.ER.isin([1, 2, 3]) & (m.HER2 == 0)]
    lum = el[el.PAM50.isin(["LumA", "LumB"])].dropna(subset=["K"])
    nA, nB = int((lum.PAM50 == "LumA").sum()), int((lum.PAM50 == "LumB").sum())
    log(f"identity check: eligible {len(el)}, LumA {nA}, LumB {nB} (Amendment 7: 256, 147, 85)")
    if (len(el), nA, nB) != (256, 147, 85):
        log("identity check FAILED; arm not run"); sys.exit(1)
    x = lum.K.values.astype(float); y = (lum.PAM50.values == "LumB").astype(int)
    T = s27.Target(x, y, el.K.dropna().values.astype(float)); A, B = x[y == 0], x[y == 1]
    tt = s27.rule_thresholds(x, y, T.pi)
    tg = [dict(rule=r, t=tt[r], qA=T.qA(tt[r]), kappa=T.kappa(tt[r])) for r in s27.RULES]
    rng = np.random.default_rng(s27.SEED); D = []
    for n in [150, 232]:
        for pi in s27.PIS:
            nb = int(round(n * pi / 100)); na = n - nb
            for rep in range(s27.NREP):
                xx = np.r_[rng.choice(A, na, replace=True), rng.choice(B, nb, replace=True)]
                yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
                th = s27.rule_thresholds(xx, yy, T.pi)
                if th is None: continue
                for r in s27.RULES:
                    t = th[r]
                    D.append((n, pi, rep, r, t, T.qA(t), T.kappa(t), abs(T.F(T.L, t) - T.F(T.L, tt[r]))))
    D = pd.DataFrame(D, columns=["n", "pi", "rep", "rule", "t", "qA", "kappa_target", "label_diff_vs_target_opt"])
    D.to_csv(os.path.join(R, "A11K_derivations.csv.gz"), index=False)
    pd.DataFrame(tg).to_csv(os.path.join(R, "A11K_target_optima.csv"), index=False)
    med = D.groupby(["n", "pi", "rule"]).agg(qA=("qA", "median"), t=("t", "median")).reset_index()
    med.to_csv(os.path.join(R, "A11K_medians.csv"), index=False)
    o1 = (med[med.n == 232].groupby("rule").apply(lambda g: np.polyfit(g.pi, g.qA, 1)[0])
          .rename("slope_qA_per_point").reset_index())
    o1.to_csv(os.path.join(R, "A11K_O1_slopes.csv"), index=False)
    tq = {d["rule"]: d["qA"] for d in tg}; tk = {d["rule"]: d["kappa"] for d in tg}; rows = []
    for (n, r), g in D[D.pi.isin(s27.PI_LIT)].groupby(["n", "rule"]):
        means = g.groupby("pi").qA.mean(); within = g.groupby("pi").qA.var(ddof=1).mean()
        between = means.var(ddof=0); total = between + within; err = g.qA - tq[r]
        rows.append(dict(n=n, rule=r, sd_total=np.sqrt(total), sd_sampling=np.sqrt(within),
                         sd_casemix=np.sqrt(between), frac_casemix=between / total if total > 0 else np.nan,
                         bias=err.mean(), rmse=np.sqrt((err ** 2).mean()),
                         label_diff_pct=100 * g.label_diff_vs_target_opt.mean(),
                         kappa_target_mean=g.kappa_target.mean(), kappa_target_opt=tk[r]))
    pd.DataFrame(rows).to_csv(os.path.join(R, "A11K_O2_O3.csv"), index=False)
    log("Ki-67 arm done")

if __name__ == "__main__":
    main(sys.argv[1])
