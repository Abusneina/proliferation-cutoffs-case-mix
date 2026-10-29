"""ph3b_ki67_ties_translation.py  POST HOC (2026-10-28), run after the registered analyses and after the BCRT decision.
Uses only the GSE81538 sample metadata (PAM50 call, consensus Ki-67, ER and HER2 consensus); no expression values.
Questions:
 (1) Does the registered Ki-67 slope (0.62, minimum 0.70) depend on how ties in the optimum are broken, and on how the percentile is defined?
     Tie rules for the kappa optimum: lowest tied cut-off (registered), middle of the tied cut-offs, highest tied cut-off.
     Percentile definitions: inclusive (share of values <= cut-off; registered) and mid-rank (share below + half the share equal).
 (2) How many Ki-67 points correspond to one luminal A quantile point near the RNA optima (illustrative translation)?
Everything here is labeled post hoc and carries no registered criterion."""
import gzip, time, numpy as np, pandas as pd
T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
RAW = "/home/claude/raw"; OUT = "/home/claude/work/posthoc"
rng = np.random.default_rng(20261028)

rows, ttl = [], None
with gzip.open(f"{RAW}/gse81538/sm.txt.gz", "rt") as f:
    for line in f:
        if line.startswith("!Sample_title"): ttl = [v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
        if line.startswith("!Sample_characteristics_ch1"): rows.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
meta = pd.DataFrame({"title": ttl})
for vals in rows:
    k = vals[0].split(": ", 1)[0]
    meta[k.strip()] = [v.split(": ", 1)[1] if ": " in v else np.nan for v in vals]
num = lambda c: pd.to_numeric(meta[c], errors="coerce")
meta["ER"] = num("er consensus"); meta["HER2"] = num("her2 consensus"); meta["K"] = num("ki67 consensus"); meta["PAM50"] = meta["pam50 subtype"]
el = meta[(meta.ER.isin([1, 2, 3])) & (meta.HER2 == 0)]
lum = el[el.PAM50.isin(["LumA", "LumB"])].dropna(subset=["K"])
x0 = lum.K.values; y0 = (lum.PAM50 == "LumB").astype(int).values
log(f"eligible {len(el)}; luminal with Ki-67 {len(lum)}; LumB share {100*y0.mean():.1f}%")
assert len(lum) == 232, len(lum)

def kappa(a, b):
    po = (a == b).mean(); pe = a.mean()*b.mean() + (1-a.mean())*(1-b.mean())
    return (po-pe)/(1-pe) if pe < 1 else np.nan
def cands(x): return np.unique(x)[:-1]
def kopt_all(x, y):
    cs = cands(x); ks = np.array([kappa((x > c).astype(int), y) for c in cs]); tied = cs[ks >= np.nanmax(ks) - 1e-12]
    return {"lowest": tied.min(), "middle": float(np.median(tied)), "highest": tied.max()}
def pct_incl(ref, c): return 100*np.mean(ref <= c)
def pct_mid(ref, c): return 100*(np.mean(ref < c) + 0.5*np.mean(ref == c))

A = x0[y0 == 0]; B = x0[y0 == 1]; N = len(x0)
res = []
SH = [15, 20, 25, 30, 35, 40, 45]
for r in range(1):
    pass
store = {(tr, pdn): {s: [] for s in SH} for tr in ["lowest", "middle", "highest"] for pdn in ["inclusive", "midrank"]}
thr = {tr: {s: [] for s in SH} for tr in ["lowest", "middle", "highest"]}
for s in SH:
    nb = int(round(N*s/100)); na = N - nb
    for b in range(200):
        xa = rng.choice(A, na); xb = rng.choice(B, nb); xx = np.r_[xa, xb]; yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
        t = kopt_all(xx, yy)
        for tr, c in t.items():
            thr[tr][s].append(c)
            store[(tr, "inclusive")][s].append(pct_incl(xx, c)); store[(tr, "midrank")][s].append(pct_mid(xx, c))
    log(f"  share {s}%: done")
out = []
for (tr, pdn), d in store.items():
    med = np.array([np.median(d[s]) for s in SH]); sl = np.polyfit(100 - np.array(SH), med, 1)[0]
    tm = np.array([np.median(thr[tr][s]) for s in SH]); st = np.polyfit(np.array(SH), tm, 1)[0]
    out.append(dict(tie_rule=tr, percentile=pdn, slope_pct_on_100_minus_share=round(sl, 2), thr_at_15=tm[0], thr_at_45=tm[-1], slope_threshold_points_per_share_point=round(st, 3)))
    log(f"  {tr:8s} {pdn:9s} slope {sl:.2f}  threshold 15% share {tm[0]:.1f} -> 45% share {tm[-1]:.1f}  (threshold slope {st:.3f} Ki-67 points per share point)")
pd.DataFrame(out).to_csv(f"{OUT}/PH3b_ki67_tie_rules.csv", index=False)

# fixed-cut-off slope on the same scale (what a cut-off that does not move would show), by percentile definition
c_fix = 15.0
for pdn, f in [("inclusive", pct_incl), ("midrank", pct_mid)]:
    pct = []
    for s in SH:
        nb = int(round(N*s/100)); na = N - nb; v = []
        for b in range(200):
            xx = np.r_[rng.choice(A, na), rng.choice(B, nb)]; v.append(f(xx, c_fix))
        pct.append(np.median(v))
    log(f"  fixed cut-off 15%: slope {np.polyfit(100-np.array(SH), np.array(pct), 1)[0]:.2f} ({pdn})")

# (2) translation: Ki-67 value at luminal A quantiles
qs = [60, 70, 75, 80, 85, 89, 90, 91, 94, 95]
tab = pd.DataFrame({"luminal_A_quantile": qs, "Ki67_value": [np.percentile(A, q, method="lower") for q in qs]})
tab.to_csv(f"{OUT}/PH3b_ki67_luminalA_quantiles.csv", index=False)
log("Luminal A (n=%d) consensus Ki-67 quantiles:\n%s" % (len(A), tab.to_string(index=False)))
log(f"luminal A Ki-67: share at 0-5%: {100*np.mean(A<=5):.0f}%, <=10: {100*np.mean(A<=10):.0f}%, <=15: {100*np.mean(A<=15):.0f}%, <=20: {100*np.mean(A<=20):.0f}%, <=25: {100*np.mean(A<=25):.0f}%")
log("done")
