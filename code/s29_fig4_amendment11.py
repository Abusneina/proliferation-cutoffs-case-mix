"""s29_fig4_amendment11.py  Figure 4: Amendment 11 results (RNA cohorts and the Ki-67 arm). 600 dpi TIFF.
Palette as s16 (validated): cohorts TCGA-BRCA #7B5EA7, METABRIC #C27C0E, SCAN-B #A63D40; redundant marker shapes
and line styles so the figure reads in greyscale. Panel d (rules, not cohorts) uses ink and grey only."""
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(HERE, "..", "results")); F = os.path.normpath(os.path.join(HERE, "..", "figures"))
INK, MUTED, GRID = "#2B2B2B", "#6B6B6B", "#E4E1DE"
COH = [("TCGA-BRCA", "#7B5EA7", "o", "-"), ("METABRIC", "#C27C0E", "s", "--"), ("SCAN-B", "#A63D40", "^", "-.")]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.linewidth": 0.8, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False, "savefig.dpi": 600})
def letter(ax, s): ax.text(-0.14, 1.03, s, transform=ax.transAxes, fontsize=11, fontweight="bold", color=INK, va="bottom")

D = pd.read_csv(os.path.join(R, "A11_derivations.csv.gz"))
M = pd.read_csv(os.path.join(R, "A11_model.csv"))
O = pd.read_csv(os.path.join(R, "A11_O2_O3.csv"))
KM = pd.read_csv(os.path.join(R, "A11K_derivations.csv.gz"))

fig, axs = plt.subplots(2, 2, figsize=(7.2, 6.0))
# a: kappa-derived cut-off vs share, P2, n = 1000, with binormal model
ax = axs[0, 0]
for c, col, mk, ls in COH:
    g = D[(D.cohort == c) & (D.score == "P2") & (D.rule == "K") & (D.n == 1000)].groupby("pi").qA
    med, lo, hi = g.median(), g.quantile(.1), g.quantile(.9)
    ax.fill_between(med.index, lo, hi, color=col, alpha=0.10, lw=0)
    ax.plot(med.index, med.values, color=col, ls=ls, lw=2, marker=mk, ms=6, mec="white", mew=1.2, label=c)
    mm = M[(M.cohort == c) & (M.score == "P2") & (M.rule == "K")]
    ax.plot(mm.pi, mm.qA_model, color=col, ls=":", lw=1.2)
ax.plot([], [], color=MUTED, ls=":", lw=1.2, label="Binormal model")
ax.set_xlabel("Luminal B share of derivation set (%)"); ax.set_ylabel("Kappa-optimal cut-off\n(luminal A quantile)")
ax.set_xticks([15, 25, 35, 45, 55, 65]); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(loc="lower left", fontsize=7); letter(ax, "a")

# b: fraction of cut-off variance due to case mix, P2, n = 400
ax = axs[0, 1]; rules = [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion\nmatching"), ("YJ", "Youden")]
w = 0.25
for j, (c, col, mk, ls) in enumerate(COH):
    v = [O[(O.cohort == c) & (O.score == "P2") & (O.n == 400) & (O.rule == r)].frac_casemix.iloc[0] for r, _ in rules]
    ax.bar(np.arange(4) + (j - 1) * w, v, width=w - 0.03, color=col, label=c,
           hatch=[None, "///", ".."][j], edgecolor="white", lw=0)
ax.set_xticks(np.arange(4)); ax.set_xticklabels([l for _, l in rules], fontsize=7.5)
ax.text(3, 0.03, "<0.01", ha="center", va="bottom", fontsize=7, color=INK)
ax.set_ylim(0, 1.15); ax.set_yticks([0, .2, .4, .6, .8, 1]); ax.set_ylabel("Share of cut-off variance\ndue to case mix")
ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(loc="upper center", fontsize=7, ncol=3, bbox_to_anchor=(0.5, 1.05)); letter(ax, "b")

# c: transfer error, P2, n = 400
ax = axs[1, 0]; rules_c = [("K", "Kappa"), ("YJ", "Youden"), ("SK", "Kappa weighted\nto target share")]
for j, (c, col, mk, ls) in enumerate(COH):
    v = [O[(O.cohort == c) & (O.score == "P2") & (O.n == 400) & (O.rule == r)].rmse.iloc[0] for r, _ in rules_c]
    ax.bar(np.arange(3) + (j - 1) * w, v, width=w - 0.03, color=col, label=c,
           hatch=[None, "///", ".."][j], edgecolor="white", lw=0)
ax.set_xticks(np.arange(3)); ax.set_xticklabels([l for _, l in rules_c], fontsize=7.5)
ax.set_ylabel("Transfer error, RMSE\n(luminal A quantile points)"); ax.grid(axis="y", color=GRID, lw=0.6)
ax.set_axisbelow(True); ax.legend(loc="upper right", fontsize=7); letter(ax, "c")

# d: Ki-67 IHC, median derived threshold by share, n = 232
ax = axs[1, 1]
for r, lab, col, mk, ls, off in [("K", "Kappa", INK, "o", "-", -0.6), ("ACC", "Minimum misclassification", MUTED, "s", "--", 0),
                                 ("PM", "Proportion matching", "#9A9A9A", "^", "-.", 0.6)]:
    g = KM[(KM.n == 232) & (KM.rule == r)].groupby("pi").t
    ax.plot(g.median().index + off, g.median().values, color=col, ls=ls, lw=2, marker=mk, ms=6, mec="white", mew=1.2, label=lab)
ax.set_xlabel("Luminal B share of derivation set (%)"); ax.set_ylabel("Derived Ki-67 cut-off (%)")
ax.set_xticks([15, 25, 35, 45, 55, 65]); ax.set_yticks([10, 15, 20, 25]); ax.set_ylim(7, 28)
ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True); ax.legend(loc="upper right", fontsize=7); letter(ax, "d")

fig.tight_layout(h_pad=2.2, w_pad=2.0)
os.makedirs(F, exist_ok=True)
fig.savefig(os.path.join(F, "Fig4_amendment11.tiff"), dpi=600, pil_kwargs={"compression": "tiff_lzw"})
fig.savefig(os.path.join(F, "Fig4_amendment11_preview.png"), dpi=150)
print("saved")
