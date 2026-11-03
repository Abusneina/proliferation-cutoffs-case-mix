"""s27_amendment11.py  Amendment 11: sources of variation in agreement-derived cut-offs,
comparison of derivation criteria, patient-level consequences, and a binormal model.

Usage:
  python3 -I s27_amendment11.py --dryrun   # PAM50 luminal labels permuted; code check only
  python3 -I s27_amendment11.py            # registered run (only after Amendment 11 is posted)

Inputs : results/cohort_tcga.csv, cohort_metabric.csv, cohort_scanb.csv (columns P1, P2, PAM50)
Outputs: results/A11_*.csv and results/A11_run.log (suffix _DRYRUN in dry-run mode)

Scale  : every threshold is expressed as q_A = 100 * F_A(t), the quantile of the full-cohort
         PAM50 luminal A distribution (score units; as in posthoc/ph1_scale_check.py).
Rules  : K   kappa maximum                      ACC minimum misclassification
         PM  proportion matching                YJ  Youden maximum
         BK  kappa maximum after 50:50 weighting of luminal A and B (equals YJ analytically; code check)
         SK  kappa maximum after weighting to the target (full-cohort) luminal B share
Candidate thresholds: observed values of the derivation sample between its 5th and 95th percentiles;
tumors with a score above the threshold are called luminal B-like; ties go to the lowest threshold.
"""
import os, sys, time, json
import numpy as np, pandas as pd
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(HERE, "..", "results"))
DRY = "--dryrun" in sys.argv
SUF = "_DRYRUN" if DRY else ""
SEED = 20261103
COH = {"TCGA-BRCA": "cohort_tcga.csv", "METABRIC": "cohort_metabric.csv", "SCAN-B": "cohort_scanb.csv"}
SCORES = ["P2", "P1"]                      # P2 primary, P1 secondary
NS = [150, 400, 1000]                      # derivation sizes
PIS = [15, 25, 35, 45, 55, 65]             # imposed luminal B shares (%)
PI_LIT = [25, 35, 45, 55, 65]              # design for O2/O3 (covers published range 27.6-62.8%)
NREP = 500
RULES = ["K", "ACC", "PM", "YJ", "BK", "SK"]
MODEL_TOL = 0.10                           # O5 criterion, q_A points per point of share

T0 = time.time()
LOG = open(os.path.join(R, f"A11_run{SUF}.log"), "w")
def log(m):
    s = f"[{time.time()-T0:7.1f}s] {m}"; print(s, flush=True); LOG.write(s + "\n"); LOG.flush()


def rule_thresholds(x, y, pi_target):
    """Return dict rule -> threshold for sample (x, y); y = 1 for luminal B."""
    n = len(x); o = np.argsort(-x, kind="mergesort"); xs = x[o]; ys = y[o]
    nB = ys.sum(); nA = n - nB
    if nB == 0 or nA == 0:
        return None
    TP = np.r_[0, np.cumsum(ys)]; k = np.arange(n + 1); FP = k - TP
    # valid k: 5th-95th percentile window and a value change between positions k-1 and k
    lo, hi = int(np.ceil(0.05 * n)), int(np.floor(0.95 * n))
    kk = np.arange(lo, hi + 1)
    kk = kk[(kk >= 1) & (kk <= n - 1)]
    kk = kk[xs[kk - 1] > xs[kk]]
    if len(kk) == 0:
        return None
    tp, fp = TP[kk].astype(float), FP[kk].astype(float)
    sens, spec = tp / nB, 1 - fp / nA
    p = nB / n; q = kk / n
    acc = (tp + nA - fp) / n
    pe = p * q + (1 - p) * (1 - q)
    kap = (acc - pe) / (1 - pe)
    def wkappa(pt):
        tpw, fpw = sens * pt, (1 - spec) * (1 - pt)
        po = tpw + (1 - pt) - fpw; qw = tpw + fpw
        pe_ = pt * qw + (1 - pt) * (1 - qw)
        return (po - pe_) / (1 - pe_)
    def pick(v):                           # maximum; ties -> lowest threshold = largest k
        v = np.where(np.isfinite(v), v, -np.inf)
        return kk[len(v) - 1 - int(np.argmax(v[::-1]))]
    out = {"K": pick(kap), "ACC": pick(acc), "YJ": pick(sens + spec - 1),
           "BK": pick(wkappa(0.5)), "SK": pick(wkappa(pi_target))}
    pm = kk[kk <= n * p]                   # largest valid k with proportion called positive <= share
    out["PM"] = pm.max() if len(pm) else kk.min()
    return {r: xs[out[r]] for r in RULES}


class Target:
    """Full-cohort luminal set, used as the target of transfer."""
    def __init__(self, x, y, stratum):
        self.A = np.sort(x[y == 0]); self.B = np.sort(x[y == 1]); self.L = np.sort(x)
        self.S = np.sort(stratum); self.pi = y.mean()
    def qA(self, t):   return 100 * np.searchsorted(self.A, t, side="right") / len(self.A)
    def F(self, arr, t): return np.searchsorted(arr, t, side="right") / len(arr)
    def kappa(self, t):
        sens = 1 - self.F(self.B, t); fpr = 1 - self.F(self.A, t); p = self.pi
        q = p * sens + (1 - p) * fpr; po = p * sens + (1 - p) * (1 - fpr)
        pe = p * q + (1 - p) * (1 - q); return (po - pe) / (1 - pe)


def binormal_fit(T):
    """Probit-probit least squares of the empirical ROC (FPR and TPR in [0.05, 0.95])."""
    t = np.unique(T.L); fpr = 1 - T.F(T.A, t); tpr = 1 - T.F(T.B, t)
    m = (fpr >= .05) & (fpr <= .95) & (tpr >= .05) & (tpr <= .95)
    b, a = np.polyfit(norm.ppf(fpr[m]), norm.ppf(tpr[m]), 1)
    return a, b                             # latent: A ~ N(0,1), B ~ N(a/b, 1/b)


def model_qA(a, b, pi):
    """Population-level q_A of each rule under the binormal model, luminal B share pi (0-1)."""
    mu, sd = a / b, 1 / b; c = np.linspace(-4, 6, 20001)
    sens = 1 - norm.cdf((c - mu) / sd); spec = norm.cdf(c)
    acc = pi * sens + (1 - pi) * spec; q = pi * sens + (1 - pi) * (1 - spec)
    pe = pi * q + (1 - pi) * (1 - q); kap = (acc - pe) / (1 - pe)
    res = {"K": c[np.argmax(kap)], "ACC": c[np.argmax(acc)], "YJ": c[np.argmax(sens + spec - 1)],
           "PM": c[np.argmin(np.abs(q - pi))]}
    return {r: 100 * norm.cdf(v) for r, v in res.items()}


def main():
    rng = np.random.default_rng(SEED)
    log(f"Amendment 11 run, mode={'DRY RUN (permuted labels)' if DRY else 'REGISTERED'}, seed={SEED}")
    derivs, targets, models, o4 = [], [], [], []
    for cname, f in COH.items():
        d = pd.read_csv(os.path.join(R, f), low_memory=False)
        m = d.PAM50.isin(["LumA", "LumB"]).values
        lab = d.PAM50.values[m]
        if DRY:
            lab = np.random.default_rng(1).permutation(lab)
        y = (lab == "LumB").astype(int)
        for s in SCORES:
            stratum = d[s].values.astype(float); x = stratum[m]
            T = Target(x, y, stratum); A, B = x[y == 0], x[y == 1]
            tt = rule_thresholds(x, y, T.pi)
            for r in RULES:
                targets.append(dict(cohort=cname, score=s, rule=r, lumB_share=100 * T.pi,
                                    t=tt[r], qA=T.qA(tt[r]), kappa=T.kappa(tt[r])))
            for n in NS:
                for pi in PIS:
                    nb = int(round(n * pi / 100)); na = n - nb
                    for rep in range(NREP):
                        xx = np.r_[rng.choice(A, na, replace=True), rng.choice(B, nb, replace=True)]
                        yy = np.r_[np.zeros(na, int), np.ones(nb, int)]
                        th = rule_thresholds(xx, yy, T.pi)
                        if th is None:
                            continue
                        for r in RULES:
                            t = th[r]
                            derivs.append((cname, s, n, pi, rep, r, T.qA(t), T.kappa(t),
                                           abs(T.F(T.L, t) - T.F(T.L, tt[r])), t))
                log(f"{cname} {s} n={n}: done")
            # O5 binormal model
            a, b = binormal_fit(T)
            for pi in PIS:
                for r, v in model_qA(a, b, pi / 100).items():
                    models.append(dict(cohort=cname, score=s, a=a, b=b, pi=pi, rule=r, qA_model=v))
    D = pd.DataFrame(derivs, columns=["cohort", "score", "n", "pi", "rep", "rule", "qA", "kappa_target",
                                      "label_diff_vs_target_opt", "t"])
    TG = pd.DataFrame(targets); M = pd.DataFrame(models)
    D.to_csv(os.path.join(R, f"A11_derivations{SUF}.csv.gz"), index=False)
    TG.to_csv(os.path.join(R, f"A11_target_optima{SUF}.csv"), index=False)
    M.to_csv(os.path.join(R, f"A11_model{SUF}.csv"), index=False)

    # O1 case-mix slope (n = 1000), median q_A on pi
    med = D.groupby(["cohort", "score", "n", "pi", "rule"]).qA.median().reset_index()
    o1 = (med[med.n == 1000].groupby(["cohort", "score", "rule"])
          .apply(lambda g: np.polyfit(g.pi, g.qA, 1)[0]).rename("slope_qA_per_point").reset_index())
    o1.to_csv(os.path.join(R, f"A11_O1_slopes{SUF}.csv"), index=False)

    # O2 variance decomposition and O3 transfer error, over PI_LIT
    rows = []
    sub = D[D.pi.isin(PI_LIT)]
    tq = TG.set_index(["cohort", "score", "rule"]).qA
    tk = TG.set_index(["cohort", "score", "rule"]).kappa
    for (c, s, n, r), g in sub.groupby(["cohort", "score", "n", "rule"]):
        means = g.groupby("pi").qA.mean(); within = g.groupby("pi").qA.var(ddof=1).mean()
        between = means.var(ddof=0); total = between + within
        err = g.qA - tq[(c, s, r)]
        rows.append(dict(cohort=c, score=s, n=n, rule=r,
                         sd_total=np.sqrt(total), sd_sampling=np.sqrt(within), sd_casemix=np.sqrt(between),
                         frac_casemix=between / total if total > 0 else np.nan,
                         bias=err.mean(), rmse=np.sqrt((err ** 2).mean()),
                         label_diff_pct=100 * g.label_diff_vs_target_opt.mean(),
                         kappa_target_mean=g.kappa_target.mean(), kappa_target_opt=tk[(c, s, r)]))
    O23 = pd.DataFrame(rows); O23.to_csv(os.path.join(R, f"A11_O2_O3{SUF}.csv"), index=False)

    # BK = YJ code check
    w = D[D.rule.isin(["BK", "YJ"])].pivot_table(index=["cohort", "score", "n", "pi", "rep"],
                                                   columns="rule", values="t")
    agree = float(np.mean(np.isclose(w.BK, w.YJ)))
    log(f"Code check: BK equals YJ in {100*agree:.2f}% of derivations")

    # O4 patient-level consequence: K thresholds derived at pi = 25 and 65 (n = 1000, median t)
    for cname, f in COH.items():
        d = pd.read_csv(os.path.join(R, f), low_memory=False)
        m = d.PAM50.isin(["LumA", "LumB"]).values
        for s in SCORES:
            g = D[(D.cohort == cname) & (D.score == s) & (D.rule == "K") & (D.n == 1000)]
            t25, t65 = g[g.pi == 25].t.median(), g[g.pi == 65].t.median()
            lo_, hi_ = min(t25, t65), max(t25, t65)
            v = d[s].values.astype(float)
            between = (v > lo_) & (v <= hi_)
            row = dict(cohort=cname, score=s, t_pi25=t25, t_pi65=t65,
                       pct_stratum_relabelled=100 * between.mean(),
                       pct_luminal_relabelled=100 * between[m].mean(),
                       n_stratum_relabelled=int(between.sum()), n_stratum=len(v))
            if "CHEMO" in d.columns:
                ch = pd.to_numeric(d.CHEMO, errors="coerce")
                row["pct_chemo_among_relabelled"] = 100 * ch[between].mean()
            o4.append(row)
    pd.DataFrame(o4).to_csv(os.path.join(R, f"A11_O4_relabelling{SUF}.csv"), index=False)

    # O5 model check: model slope vs resampled slope (n = 1000), K and ACC, P2
    ms = (M.groupby(["cohort", "score", "rule"]).apply(lambda g: np.polyfit(g.pi, g.qA_model, 1)[0])
          .rename("slope_model").reset_index())
    o5 = o1.merge(ms, on=["cohort", "score", "rule"])
    o5["abs_diff"] = (o5.slope_qA_per_point - o5.slope_model).abs()
    o5.to_csv(os.path.join(R, f"A11_O5_model_check{SUF}.csv"), index=False)
    crit = o5[(o5.score == "P2") & o5.rule.isin(["K", "ACC"])]
    ok = bool((crit.abs_diff <= MODEL_TOL).all())
    json.dump(dict(mode="dryrun" if DRY else "registered", model_criterion_met=ok,
                   bk_equals_yj_fraction=agree), open(os.path.join(R, f"A11_decision{SUF}.json"), "w"), indent=1)
    log(f"O5 criterion (P2, K and ACC, |model - resampled| <= {MODEL_TOL} in all cohorts): {'met' if ok else 'not met'}")
    log("done")


if __name__ == "__main__":
    main()
