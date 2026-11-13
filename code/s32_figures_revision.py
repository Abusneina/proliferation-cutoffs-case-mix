"""s32_figures_revision.py  Figures for the revised Cancer Epidemiology manuscript (13 Nov 2026).
Fig. 1: former Figure 1 without the percentile-scale panel (former panel c moved to Online Resource 4).
Fig. 3: new, Amendment 12 (a: transfer between tumor-size subgroups; b: Ki-67 predicted and observed thresholds).
Figures 2 and 4 are the former Figures 4 and 3, unchanged except for RGB conversion.
No titles inside figures, legends inside the plot area, 174 mm wide, 600 dpi, RGB TIFF (LZW).
Palette: purple, amber and crimson on greys (no blue, green or brown).
Usage: python3 -I code/s32_figures_revision.py <output folder>"""
import os, sys, time
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image
T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(HERE, "..", "results"))
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
fam = next((f for f in ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"] if any(f == x.name for x in fm.fontManager.ttflist)), "DejaVu Sans")
C_A, C_D, C_B = "#7B5EA7", "#C27C0E", "#A63D40"; INK = "#2B2B2B"; MUTED = "#6B6B6B"; GRID = "#E4E1DE"
plt.rcParams.update({"font.family": fam, "font.size": 7.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "savefig.dpi": 600})
W = 174 / 25.4
def letter(ax, s, x=-0.16): ax.text(x, 1.04, s, transform=ax.transAxes, fontsize=10, fontweight="bold", color=INK, va="bottom")
def save(fig, name):
    p = os.path.join(OUT, name); fig.savefig(p + "_preview.png", dpi=150)
    fig.savefig(p + ".png", dpi=600); Image.open(p + ".png").convert("RGB").save(p + ".tiff", compression="tiff_lzw", dpi=(600, 600))
    os.remove(p + ".png"); plt.close(fig); log(f"wrote {name}.tiff")

# ---------------- Figure 1 (a to d)
a3 = pd.read_csv(f"{R}/A3_agreement.csv"); grid = a3[a3.pct > 0]; opt = a3[a3.pct == -1]
e3 = pd.read_csv(f"{R}/E3_prevalence_resampling.csv"); e1 = pd.read_csv(f"{R}/E1_youden_scales.csv")
STY = {"TCGA-BRCA": dict(color="#1F1F1F", marker="o", ls="-"), "METABRIC": dict(color="#6E6E6E", marker="s", ls="--"),
       "SCAN-B": dict(color="#A8A8A8", marker="^", ls="-.")}
fig = plt.figure(figsize=(W, 4.9)); gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.30)
for k, (c, let) in enumerate([("TCGA", "a"), ("METABRIC", "b")]):
    ax = fig.add_subplot(gs[0, k])
    for s, col, ls, lab in [("P2", C_B, "-", "18-gene proliferation score"), ("P1", C_A, "--", "MKI67 alone")]:
        g = grid[(grid.cohort == c) & (grid.score == s)]; ax.plot(g.pct, g.kappa, color=col, ls=ls, lw=1.8, label=lab)
        o = opt[(opt.cohort == c) & (opt.score == s)].iloc[0]; ax.axvspan(o.ci_lo, o.ci_hi, color=col, alpha=0.10, lw=0)
        ax.plot([o.opt_pct], [o.kappa], marker="o" if s == "P2" else "s", ms=6, color=col, mec="white", mew=1.2, zorder=5)
        ax.annotate(f"{int(o.opt_pct)}th", (o.opt_pct, o.kappa), xytext=(0, 6 if s == "P2" else -13), textcoords="offset points", ha="center", fontsize=7, color=INK)
    ax.set_xlabel("Cut-off (percentile within stratum)"); ax.set_xlim(5, 95); ax.set_ylim(0, 0.8); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.text(0.02, 0.96, "TCGA-BRCA" if c == "TCGA" else c, transform=ax.transAxes, fontsize=7.5, color=INK, va="top", fontweight="bold")
    ax.set_ylabel("Cohen κ versus PAM50"); letter(ax, let, -0.12)
    if k == 1: ax.legend(loc="lower center", fontsize=6.5)
ax = fig.add_subplot(gs[1, 0])
for c, st in STY.items():
    key = "TCGA" if c == "TCGA-BRCA" else c; g = e3[(e3.cohort == key) & (e3.score == "P2")]
    ax.plot(g.prev, g["youden_q_lumA"], lw=1.5, ms=4.5, mec="white", mew=0.7, label=c, **st)
ax.set_xlabel("Imposed luminal B share (%)"); ax.set_ylabel("Youden cut-off (luminal A quantile)"); ax.set_xticks([15, 25, 35, 45]); ax.set_ylim(50, 100)
ax.legend(loc="lower left", fontsize=6); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True); letter(ax, "c", -0.12)
ax_e = fig.add_subplot(gs[1, 1]); y = 0; labs = []
for c, st in STY.items():
    key = "TCGA" if c == "TCGA-BRCA" else c; r = e1[(e1.cohort == key) & (e1.score == "P2")].iloc[0]
    ax_e.plot([r.youden_q_lumA_lo, r.youden_q_lumA_hi], [y]*2, color=st["color"], lw=1.8); ax_e.plot(r.youden_q_lumA, y, marker=st["marker"], color=st["color"], ms=6, mec="white", mew=0.9)
    ax_e.plot([r.youden_pct_full_lo, r.youden_pct_full_hi], [y-0.32]*2, color=st["color"], lw=1.1, ls=":")
    ax_e.plot(r.youden_pct_full, y-0.32, marker=st["marker"], color=st["color"], ms=4.5, mfc="white", mew=1.1); labs.append((y-0.16, c)); y -= 1
ax_e.set_yticks([l[0] for l in labs]); ax_e.set_yticklabels([l[1] for l in labs], color=INK, fontsize=6.5); ax_e.tick_params(axis="y", length=0)
ax_e.spines["left"].set_visible(False); ax_e.set_xlim(45, 100); ax_e.set_ylim(y+0.35, 1.25); ax_e.set_xlabel("Youden cut-off, 18-gene score"); ax_e.grid(axis="x", color=GRID, lw=0.6); ax_e.set_axisbelow(True)
ax_e.plot([], [], "o-", color=MUTED, lw=1.8, label="Luminal A quantile"); ax_e.plot([], [], "o:", color=MUTED, mfc="white", lw=1.1, label="Percentile of stratum")
ax_e.legend(loc="upper left", fontsize=6, bbox_to_anchor=(-0.02, 1.0)); letter(ax_e, "d", -0.12)
fig.subplots_adjust(left=0.08, right=0.985, top=0.95, bottom=0.10); save(fig, "Fig1")

# ---------------- Figure 3 (a, b), Amendment 12
S = pd.read_csv(f"{R}/A12_N2_summary.csv"); S = S[(S.score == "P2") & (S.split == "size_le20_vs_gt20")]
rules = [("K", "Kappa"), ("ACC", "Accuracy"), ("SK_oracle", "Weighted \u03ba,\ntarget share"), ("SK_population", "Weighted \u03ba,\nregional share"), ("YJ", "Youden")]
fig, axs = plt.subplots(1, 2, figsize=(W, 2.9), gridspec_kw=dict(width_ratios=[1.35, 1]))
a = axs[0]; xx = np.arange(len(rules)); wbar = 0.38
for j, (dr, lab, col, hatch) in enumerate([("1to2", "Small → large tumors (23.7% → 42.3% luminal B)", C_D, None),
                                         ("2to1", "Large → small tumors (42.3% → 23.7% luminal B)", C_A, "///")]):
    g = S[S.direction == dr].set_index("rule")
    a.bar(xx + (j - 0.5) * wbar, [g.loc[r, "rmse_vs_K"] for r, _ in rules], wbar, color=col, alpha=0.85, hatch=hatch, edgecolor="white", label=lab)
a.set_xticks(xx); a.set_xticklabels([l for _, l in rules], fontsize=6.3); a.set_ylabel("RMSE vs target κ optimum\n(luminal A quantile points)", fontsize=7)
a.legend(loc="upper left", fontsize=6); a.grid(axis="y", color=GRID, lw=0.6); a.set_axisbelow(True); a.set_ylim(0, 18); letter(a, "a", -0.12)
P = pd.read_csv(f"{R}/A12_N4_ki67_prediction.csv").set_index("quantity"); Mx = pd.read_csv(f"{R}/A11K_medians.csv"); Mx = Mx[Mx.n == 232]
b = axs[1]
for j, (r, lab, col, mk) in enumerate([("K", "Kappa", C_B, "o"), ("ACC", "Accuracy", C_D, "s")]):
    off = (j - 0.5) * 3
    est = [P.loc[f"{r}_25", "estimate"], P.loc[f"{r}_65", "estimate"]]
    lo = [P.loc[f"{r}_25", "ci_lo"], P.loc[f"{r}_65", "ci_lo"]]; hi = [P.loc[f"{r}_25", "ci_hi"], P.loc[f"{r}_65", "ci_hi"]]
    xs = np.array([25, 65]) + off
    b.errorbar(xs, est, yerr=[np.array(est) - lo, np.array(hi) - est], fmt=mk + "-", color=col, ms=5, lw=1.3, capsize=2.5, label=f"{lab}, model (95% interval)")
    obs = [Mx[(Mx.pi == p) & (Mx.rule == r)].t.iloc[0] for p in (25, 65)]
    b.plot(xs + 1.5, obs, mk, color=col, mfc="white", mew=1.2, ms=5, ls="none", label=f"{lab}, observed median")
b.set_xticks([25, 65]); b.set_xlim(12, 78); b.set_ylim(0, 35); b.set_xlabel("Luminal B share (%)"); b.set_ylabel("Consensus Ki-67 threshold (%)")
b.legend(loc="upper right", fontsize=5.8); b.grid(axis="y", color=GRID, lw=0.6); b.set_axisbelow(True); letter(b, "b", -0.18)
fig.subplots_adjust(left=0.08, right=0.985, top=0.93, bottom=0.20, wspace=0.32); save(fig, "Fig3")

# ---------------- Figures 2 and 4: former Figures 4 and 3, flattened to RGB
for src, name in [(sys.argv[2] if len(sys.argv) > 2 else None, "Fig2"), (sys.argv[3] if len(sys.argv) > 3 else None, "Fig4")]:
    if src:
        im = Image.open(src); log(f"{name}: source mode {im.mode}, size {im.size}")
        if im.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); im = bg
        im.convert("RGB").save(os.path.join(OUT, name + ".tiff"), compression="tiff_lzw", dpi=(600, 600)); log(f"wrote {name}.tiff")
log("done")
