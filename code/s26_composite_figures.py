"""s26_composite_figures.py  Composite multi-panel figures for the Breast Cancer submission (28 Oct 2026).
Journal limit: 7 tables and figures in total, so the former Figures 1 and 2 become panels a to e of Figure 1, the former Figure 3 becomes Figure 2
(panels a to c, adding SCAN-B), and the former Figure 4 becomes Figure 3 (panels a to c, adding the Ki-67 threshold by imposed share).
No titles inside figures, lowercase bold panel letters, legends inside the plot area, 174 mm wide, 600 dpi PNG plus RGB TIFF.
Palette: purple, amber and crimson on greys (no blue, green or brown)."""
import time, gzip, sys, warnings, datetime as dt
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from statsmodels.duration.survfunc import SurvfuncRight
warnings.filterwarnings("ignore"); T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R = "/home/claude/work/results"; F = "/home/claude/work/figures"; RAW = "/home/claude/raw"
STAMP = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
fam = next((f for f in ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"] if any(f == x.name for x in fm.fontManager.ttflist)), "DejaVu Sans"); log(f"font {fam}")
C_A, C_D, C_B = "#7B5EA7", "#C27C0E", "#A63D40"; INK = "#2B2B2B"; MUTED = "#6B6B6B"; GRID = "#E4E1DE"
plt.rcParams.update({"font.family": fam, "font.size": 7.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "savefig.dpi": 600})
W = 174 / 25.4   # 174 mm
def letter(ax, s, x=-0.16): ax.text(x, 1.04, s, transform=ax.transAxes, fontsize=10, fontweight="bold", color=INK, va="bottom")
def save(fig, name):
    p = f"{F}/{STAMP}_{name}"; fig.savefig(p + ".png"); fig.savefig(p + ".tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"}); plt.close(fig); log(f"wrote {p}.png/.tiff")

# ======================================================= Figure 1 (a to e)
a3 = pd.read_csv(f"{R}/A3_agreement.csv"); grid = a3[a3.pct > 0]; opt = a3[a3.pct == -1]
e3 = pd.read_csv(f"{R}/E3_prevalence_resampling.csv"); e1 = pd.read_csv(f"{R}/E1_youden_scales.csv")
STY = {"TCGA-BRCA": ("TCGA", dict(color="#1F1F1F", marker="o", ls="-")), "METABRIC": ("METABRIC", dict(color="#6E6E6E", marker="s", ls="--")),
       "SCAN-B": ("SCAN-B", dict(color="#A8A8A8", marker="^", ls="-."))}
fig = plt.figure(figsize=(W, 4.9)); gs = fig.add_gridspec(2, 6, height_ratios=[1, 1], hspace=0.62, wspace=1.35)
axs_top = [fig.add_subplot(gs[0, 0:3]), fig.add_subplot(gs[0, 3:6])]
for ax, (c, let) in zip(axs_top, [("TCGA", "a"), ("METABRIC", "b")]):
    for s, col, ls, lab in [("P2", C_B, "-", "18-gene proliferation score"), ("P1", C_A, "--", "MKI67 alone")]:
        g = grid[(grid.cohort == c) & (grid.score == s)]; ax.plot(g.pct, g.kappa, color=col, ls=ls, lw=1.8, label=lab)
        o = opt[(opt.cohort == c) & (opt.score == s)].iloc[0]; ax.axvspan(o.ci_lo, o.ci_hi, color=col, alpha=0.10, lw=0)
        ax.plot([o.opt_pct], [o.kappa], marker="o" if s == "P2" else "s", ms=6, color=col, mec="white", mew=1.2, zorder=5)
        ax.annotate(f"{int(o.opt_pct)}th", (o.opt_pct, o.kappa), xytext=(0, 6 if s == "P2" else -13), textcoords="offset points", ha="center", fontsize=7, color=INK)
    ax.set_xlabel("Cut-off (percentile within stratum)"); ax.set_xlim(5, 95); ax.set_ylim(0, 0.8); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.text(0.02, 0.96, "TCGA-BRCA" if c == "TCGA" else c, transform=ax.transAxes, fontsize=7.5, color=INK, va="top", fontweight="bold"); letter(ax, let, -0.10)
axs_top[0].set_ylabel("Cohen κ versus PAM50"); axs_top[1].legend(loc="lower center", fontsize=6.5)
log("Fig 1 a, b")
ax_c = fig.add_subplot(gs[1, 0:2]); ax_d = fig.add_subplot(gs[1, 2:4]); ax_e = fig.add_subplot(gs[1, 4:6])
for ax, col, ylab, let in [(ax_c, "kappa_pct", "κ-optimal cut-off (percentile)", "c"), (ax_d, "youden_q_lumA", "Youden cut-off (quantile of luminal A)", "d")]:
    for c, (lab, st) in STY.items():
        key = "TCGA" if c == "TCGA-BRCA" else c; g = e3[(e3.cohort == key) & (e3.score == "P2")]
        ax.plot(g.prev, g[col], lw=1.5, ms=4.5, mec="white", mew=0.7, label=c, **st)
    if col == "kappa_pct":
        xx = np.array([15, 45]); ax.plot(xx, 100 - xx, color=C_B, lw=1, ls=":", label="100 minus share")
        ax.legend(loc="lower left", fontsize=6)
    ax.set_xlabel("Imposed luminal B share (%)"); ax.set_ylabel(ylab); ax.set_xticks([15, 25, 35, 45]); ax.set_ylim(50, 100)
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True); letter(ax, let, -0.22)
y = 0; labs = []
for c, (lab, st) in STY.items():
    key = "TCGA" if c == "TCGA-BRCA" else c; r = e1[(e1.cohort == key) & (e1.score == "P2")].iloc[0]
    ax_e.plot([r.youden_q_lumA_lo, r.youden_q_lumA_hi], [y]*2, color=st["color"], lw=1.8); ax_e.plot(r.youden_q_lumA, y, marker=st["marker"], color=st["color"], ms=6, mec="white", mew=0.9)
    ax_e.plot([r.youden_pct_full_lo, r.youden_pct_full_hi], [y-0.32]*2, color=st["color"], lw=1.1, ls=":")
    ax_e.plot(r.youden_pct_full, y-0.32, marker=st["marker"], color=st["color"], ms=4.5, mfc="white", mew=1.1); labs.append((y-0.16, c)); y -= 1
ax_e.set_yticks([l[0] for l in labs]); ax_e.set_yticklabels([l[1] for l in labs], color=INK, fontsize=6.5); ax_e.tick_params(axis="y", length=0)
ax_e.spines["left"].set_visible(False); ax_e.set_xlim(45, 100); ax_e.set_ylim(y+0.35, 1.25); ax_e.set_xlabel("Youden cut-off, 18-gene score"); ax_e.grid(axis="x", color=GRID, lw=0.6); ax_e.set_axisbelow(True)
ax_e.plot([], [], "o-", color=MUTED, lw=1.8, label="Quantile of luminal A"); ax_e.plot([], [], "o:", color=MUTED, mfc="white", lw=1.1, label="Percentile of stratum")
ax_e.legend(loc="upper left", fontsize=6, bbox_to_anchor=(-0.02, 1.0)); letter(ax_e, "e", -0.10)
fig.subplots_adjust(left=0.07, right=0.985, top=0.95, bottom=0.10); save(fig, "Fig1_composite_agreement-and-case-mix")

# ======================================================= Figure 2 (a to c): Kaplan-Meier
CUTS = (59, 74)
def groups(v): tl, th = np.nanpercentile(v, CUTS[0]), np.nanpercentile(v, CUTS[1]); return np.where(v <= tl, "STABLE_A", np.where(v <= th, "DISCORDANT", "STABLE_B"))
fig, axs = plt.subplots(1, 3, figsize=(W, 3.3))
spec = [("METABRIC", "cohort_metabric.csv", "Disease-specific survival", "a", 240, 0.25), ("TCGA-BRCA", "cohort_tcga.csv", "Progression-free interval", "b", 120, 0.2), ("SCAN-B", "cohort_scanb.csv", "Overall survival", "c", 84, 0.58)]
for ax, (c, f, ylab, let, tmax, ylo) in zip(axs, spec):
    d = pd.read_csv(f"{R}/{f}", low_memory=False); g_all = groups(d["P2"].values); ok = (d.TIME.notna() & (d.TIME >= 0)).values; d = d[ok]; g = g_all[ok]
    ticks = np.arange(0, tmax+1, tmax//4 if tmax != 84 else 21); risk = {}
    for key, col, ls, lab in [("STABLE_A", C_A, "-", "Stable luminal A-like"), ("DISCORDANT", C_D, "--", "Discordant"), ("STABLE_B", C_B, "-.", "Stable luminal B-like")]:
        sub = d[g == key]; sf = SurvfuncRight(sub.TIME.values, sub.EVENT.values)
        ax.step(np.r_[0, sf.surv_times], np.r_[1, sf.surv_prob], where="post", color=col, ls=ls, lw=1.6, label=f"{lab} (n = {len(sub)})")
        risk[key] = [int((sub.TIME >= tt).sum()) for tt in ticks]
    ax.set_xlim(0, tmax); ax.set_ylim(ylo, 1.01); ax.set_xticks(ticks); ax.set_xlabel("Months"); ax.set_ylabel(ylab); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.legend(loc="lower left", fontsize=6); ax.text(0.98, 0.97, c, transform=ax.transAxes, ha="right", va="top", fontsize=7.5, fontweight="bold", color=INK)
    for k, (key, col) in enumerate([("STABLE_A", C_A), ("DISCORDANT", C_D), ("STABLE_B", C_B)]):
        for tt, n in zip(ticks, risk[key]): ax.text(tt, -0.27-0.06*k, str(n), transform=ax.get_xaxis_transform(), ha="center", fontsize=6, color=col)
    ax.text(-0.02, -0.27+0.06, "At risk", transform=ax.transAxes, ha="right", fontsize=6, color=MUTED); letter(ax, let, -0.20)
    log(f"Fig 2 {let} {c}: n {len(d)}")
fig.subplots_adjust(left=0.07, right=0.985, top=0.93, bottom=0.34, wspace=0.42); save(fig, "Fig2_composite_survival-by-group")

# ======================================================= Figure 3 (a to c): GSE81538
rows, ttl = [], None
with gzip.open(f"{RAW}/gse81538/sm.txt.gz", "rt") as fh:
    for line in fh:
        if line.startswith("!Sample_title"): ttl = [v.strip('"') for v in line.rstrip("\n").split("\t")[1:]]
        if line.startswith("!Sample_characteristics_ch1"): rows.append([v.strip('"') for v in line.rstrip("\n").split("\t")[1:]])
meta = pd.DataFrame({"title": ttl})
for vals in rows:
    k = vals[0].split(": ", 1)[0]; meta[k.strip()] = [v.split(": ", 1)[1] if ": " in v else np.nan for v in vals]
num = lambda c: pd.to_numeric(meta[c], errors="coerce")
meta["ER"] = num("er consensus"); meta["HER2"] = num("her2 consensus"); meta["K"] = num("ki67 consensus"); meta["PAM50"] = meta["pam50 subtype"]
el = meta[(meta.ER.isin([1, 2, 3])) & (meta.HER2 == 0) & meta.PAM50.isin(["LumA", "LumB"])].dropna(subset=["K"])
A = el.K[el.PAM50 == "LumA"].values; B = el.K[el.PAM50 == "LumB"].values; assert len(A) + len(B) == 232
def kappa(a, b):
    po = (a == b).mean(); pe = a.mean()*b.mean() + (1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe)
def kopt_pct(x, y):
    cs = np.unique(np.percentile(x, np.arange(5, 96))); ks = [kappa((x > c).astype(int), y) for c in cs]; return 100*np.mean(x <= cs[int(np.argmax(ks))])
PR = [15, 20, 25, 30, 35, 40, 45]; xs = 100 - np.array(PR)
def curve(A_, B_, N=40000, seed=1):
    r = np.random.default_rng(seed); out = []
    for p in PR:
        nb = int(N*p/100); x = np.r_[r.choice(A_, N-nb), r.choice(B_, nb)]; y = np.r_[np.zeros(N-nb), np.ones(nb)]; out.append(kopt_pct(x, y))
    return np.array(out)
r0 = np.random.default_rng(0); c_norm = curve(r0.normal(0, 1, 40000), r0.normal(2, 1, 40000)); c_tie = curve(A, B); log("simulated and tied curves done")
rr = np.random.default_rng(5); fixed = []
for p in PR:
    nb = int(round(232*p/100)); fixed.append(np.median([100*np.mean(np.r_[rr.choice(A, 232-nb), rr.choice(B, nb)] <= 15.0) for _ in range(200)]))
fixed = np.array(fixed); d7 = pd.read_csv(f"{R}/A7_resampling.csv"); d7 = d7[(d7.analysis == "primary") & (d7.measure == "K")]
sl = lambda yv: np.polyfit(xs, yv, 1)[0]; log(f"slopes: normal {sl(c_norm):.2f}, tied N=40000 {sl(c_tie):.2f}, registered {sl(d7.kappa_pct.values):.2f}, fixed 15% {sl(fixed):.2f}")
fig, axs = plt.subplots(1, 3, figsize=(W, 2.7))
a = axs[0]; a.plot([50, 85], [50, 85], ls=":", c=MUTED, lw=1, label="Slope 1")
a.plot(xs, c_norm, "o-", c=C_A, ms=3.5, lw=1.2, label=f"Simulated, continuous ({sl(c_norm):.2f})")
a.plot(xs, c_tie, "^-.", c=C_D, ms=3.5, lw=1.2, label=f"Ki-67 distributions, N = 40,000 ({sl(c_tie):.2f})")
a.plot(xs, fixed, "--", c=C_B, lw=1.2, label=f"Fixed 15% threshold ({sl(fixed):.2f})")
a.plot(xs, d7.kappa_pct.values, "D-", c=INK, ms=3, lw=1.0, label=f"Registered test, n = 232 ({sl(d7.kappa_pct.values):.2f})")
a.set_ylim(48, 104); a.set_yticks([50, 60, 70, 80, 90]); a.set_xlabel("100 minus imposed luminal B share (%)"); a.set_ylabel("κ-optimal cut-off (percentile)"); a.legend(loc="upper left", fontsize=5.6); letter(a, "a", -0.20)
b = axs[1]; b.plot(xs, d7.youden_q.values, "D-", c=INK, ms=3, lw=1.0, label="Youden cut-off, consensus Ki-67"); b.set_ylim(50, 100)
b.set_xlabel("100 minus imposed luminal B share (%)"); b.set_ylabel("Youden cut-off (quantile of luminal A)"); b.legend(loc="lower left", fontsize=6); letter(b, "b", -0.20)
c = axs[2]; c.fill_between(100-d7.prev.values+0, d7.kappa_thr_lo.values, d7.kappa_thr_hi.values, color=C_D, alpha=0.18, lw=0)
c.plot(100-d7.prev.values, d7.kappa_thr_med.values, "D-", c=INK, ms=3, lw=1.0, label="Median (band: 2.5th to 97.5th percentile)"); c.axhline(15, color=C_B, lw=0.9, ls=":")
c.set_ylim(5, 40); c.set_xlabel("100 minus imposed luminal B share (%)"); c.set_ylabel("κ-optimal Ki-67 threshold (%)"); c.legend(loc="upper left", fontsize=5.6); letter(c, "c", -0.20)
for ax in axs: ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
fig.subplots_adjust(left=0.07, right=0.985, top=0.93, bottom=0.17, wspace=0.40); save(fig, "Fig3_composite_Ki67-registered-test")
log("done")
