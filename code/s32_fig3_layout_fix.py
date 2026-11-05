"""s32_fig3_layout_fix.py  Figure 3 (Ki-67 registered test), layout fix: panel letters and right-hand axis label no longer clipped. Data and statistics unchanged from s26."""
import time, gzip, sys, warnings, datetime as dt
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
warnings.filterwarnings("ignore"); T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R = "/home/claude/work/repo/results"; F = "/home/claude/work/figs_new"; RAW = "/home/claude/work/pkg/proliferation-cutoffs-paper/inputs"
STAMP = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
fam = next((f for f in ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"] if any(f == x.name for x in fm.fontManager.ttflist)), "DejaVu Sans"); log(f"font {fam}")
C_A, C_D, C_B = "#7B5EA7", "#C27C0E", "#A63D40"; INK = "#2B2B2B"; MUTED = "#6B6B6B"; GRID = "#E4E1DE"
plt.rcParams.update({"font.family": fam, "font.size": 7.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "savefig.dpi": 600})
W = 174 / 25.4   # 174 mm
def letter(ax, s, x=-0.20): ax.text(x, 1.06, s, transform=ax.transAxes, fontsize=10, fontweight="bold", color=INK, va="bottom")
def save(fig, name):
    p = f"{F}/{STAMP}_{name}"; fig.savefig(p + ".png"); fig.savefig(p + ".tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"}); plt.close(fig); log(f"wrote {p}.png/.tiff")

# ======================================================= Figure 3 (a to c): GSE81538
rows, ttl = [], None
with gzip.open(f"{RAW}/GSE81538_series_matrix.txt.gz", "rt") as fh:
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
fig, axs = plt.subplots(1, 3, figsize=(W, 2.9))
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
fig.subplots_adjust(left=0.075, right=0.975, top=0.88, bottom=0.17, wspace=0.42); save(fig, "Fig3_Ki67-registered-test_layoutfix")
log("done")
