"""ph2_score_units_P3.py  POST HOC (2026-10-16). Extends ph1 to P3 (gene-disjoint score) and to GSE81538,
using the Amendment 8 scoring functions unchanged (s21_amendment8.py imported, not modified)."""
import sys, importlib.util, time, numpy as np, pandas as pd
spec = importlib.util.spec_from_file_location("s21", "/home/claude/work/code/s21_amendment8.py")
s21 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s21)
log = s21.log; rng = np.random.default_rng(20261016)
P3 = s21.read_list("/home/claude/work/protocol/2026-10-14_1641_GENE-LIST_P3-metaPCNA-minus-PAM50_FROZEN.txt", "##P3_START", "##P3_END")
assert len(P3) == 120
def kopt_thr(x, y, ref):
    T = np.percentile(ref, s21.GRID); k = s21.kappa_vec(x[None, :] > T[:, None], y); i = int(np.nanargmax(k)); return T[i]
rows = []
for c in ["TCGA", "METABRIC", "SCAN-B", "GSE81538"]:
    log("=" * 60); log(c)
    E, found, miss, al = s21.extract(c, ["MKI67"] + s21.P2 + P3)
    d = s21.cohort_rows(c, list(E.columns)); pam = d.PAM50.values
    S = {"P2": s21.scores(E, d, {g: found[g] for g in s21.P2 if g in found}, "mean"),
         "P3": s21.scores(E, d, {g: found[g] for g in P3 if g in found}, "median")}
    for s, full in S.items():
        m = np.isin(pam, ["LumA", "LumB"]); x = full[m]; y = (pam[m] == "LumB").astype(int); A = x[y == 0]; B = x[y == 1]
        t = kopt_thr(x, y, full); sh = 100 * y.mean()
        r = dict(cohort=c, score=s, lumB_share=round(sh, 1), kopt_pct_stratum=round(100*np.mean(full <= t), 1),
                 kopt_pct_luminal=round(100*np.mean(x <= t), 1), expected=round(100 - sh, 1),
                 kopt_qA=round(100*np.mean(A <= t), 1), fixed_slope=round(np.mean(A <= t) - np.mean(B <= t), 2))
        N = len(x); E3 = []
        for prev in [15, 20, 25, 30, 35, 40, 45]:
            nb = int(round(N*prev/100)); na = N - nb; pp, qq = [], []
            for _ in range(200):
                xa = rng.choice(A, na, replace=True); xb = rng.choice(B, nb, replace=True)
                xx = np.r_[xa, xb]; yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
                tt = kopt_thr(xx, yy, xx); pp.append(100*np.mean(xx <= tt)); qq.append(100*np.mean(A <= tt))
            E3.append((prev, np.median(pp), np.median(qq)))
        E3 = np.array(E3)
        r.update(slope_pct=round(np.polyfit(100-E3[:, 0], E3[:, 1], 1)[0], 2), slope_qA=round(np.polyfit(100-E3[:, 0], E3[:, 2], 1)[0], 2),
                 qA_15=round(E3[0, 2], 1), qA_45=round(E3[-1, 2], 1))
        rows.append(r); log(f"  {c} {s}: {r}")
out = pd.DataFrame(rows); out.to_csv("/home/claude/work/posthoc/PH2_score_units_P2_P3.csv", index=False); print(out.to_string()); log("done")
