"""s33_online_resources_revision.py  Online Resources 1, 2 and 4 for the revised Cancer Epidemiology manuscript
(13 Nov 2026). Edits copies of the 11 Nov 2026 Word files; Online Resource 3 is unchanged.
OR1: new article title; Amendment 12 row in the sequence table; Amendment 12 documents reproduced verbatim.
OR2: REMARK pointers updated for the revised article (outcome analysis moved to Online Resource 4).
OR4: Tables S29-S36 (Amendment 12) and Figs. S3-S5.
Usage: python3 -I code/s33_online_resources_revision.py <folder with 11 Nov ORs> <Amendment 12 folder> <output folder> <stamp>"""
import os, sys, copy, time
import numpy as np, pandas as pd, docx
from docx.shared import Pt, Mm, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from scipy.stats import norm
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(HERE, "..", "results"))
SRC, A12, OUT, STAMP = sys.argv[1:5]; os.makedirs(OUT, exist_ok=True)
TITLE = ("Case mix and agreement-optimized proliferation cut-offs for luminal A versus luminal B breast cancer: "
         "prevalence, spectrum and transfer")
TNR = "Times New Roman"

def para(doc, text="", size=10, bold=False, font=TNR, after=3, italic=False):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(0)
    if text:
        r = p.add_run(text); r.font.name = font; r.font.size = Pt(size); r.bold = bold; r.italic = italic
        r._element.rPr.rFonts.set(qn("w:hAnsi"), font)
    return p

def set_cell(cell, text, bold=False, white=False, size=8.5):
    cell.text = ""; p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(0); p.paragraph_format.space_before = Pt(0)
    r = p.add_run(text); r.font.name = TNR; r.font.size = Pt(size); r.bold = bold
    r._element.rPr.rFonts.set(qn("w:hAnsi"), TNR)
    if white: r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill); tcPr.append(sh)

def table(doc, header, rows, widths_mm, merge_cols=(0,)):
    t = doc.add_table(rows=1 + len(rows), cols=len(header)); t.autofit = False
    tblPr = t._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for side, sz, col in [("top", "12", "2B2B2B"), ("bottom", "12", "2B2B2B"), ("insideH", "4", "D9D5DE")]:
        e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), sz); e.set(qn("w:space"), "0"); e.set(qn("w:color"), col); b.append(e)
    tblPr.append(b)
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]; set_cell(c, h, bold=True, white=True); shade(c, "4E3D7A")
    for i, row in enumerate(rows):
        for j, v in enumerate(row): set_cell(t.rows[i + 1].cells[j], str(v))
    for j, w in enumerate(widths_mm): t.columns[j].width = Mm(w)
    for row in t.rows:
        for j, w in enumerate(widths_mm): row.cells[j].width = Mm(w)
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(sum(widths_mm) * 56.7))); tw.set(qn("w:type"), "dxa")
    old_tw = tblPr.find(qn("w:tblW"))
    if old_tw is not None: tblPr.remove(old_tw)
    tblPr.append(tw)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for j in merge_cols:                                   # vertical merge of repeated group labels
        i = 1
        while i <= len(rows):
            k = i
            while k + 1 <= len(rows) and rows[k][j] == rows[i - 1][j] and rows[i - 1][j] != "" and \
                    all(rows[k][jj] == rows[i - 1][jj] for jj in merge_cols[:merge_cols.index(j)]):
                k += 1
            if k > i:
                txt = rows[i - 1][j]; m = t.cell(i, j).merge(t.cell(k, j)); set_cell(m, txt)
            i = k + 1
    return t

def caption(doc, text): para(doc, text, size=11, bold=True, after=3)
def note(doc, text): para(doc, text, size=8.5, after=6)

# ========================================================================= OR1
d = docx.Document(os.path.join(SRC, "08_Online_Resource_1_Governance_Record_2026-11-11_2012.docx"))
p2 = d.paragraphs[2]; old = p2.text
assert old.startswith("Article: Case mix of the derivation series")
newtxt = old.replace("Case mix of the derivation series and Ki-67 cut-offs for luminal A versus luminal B breast cancer: "
                     "a predictive model and a correction", TITLE)
for r in p2.runs[1:]: r.text = ""
p2.runs[0].text = newtxt
t = d.tables[0]; last = t.rows[-1]._tr; new = copy.deepcopy(last); last.addnext(new)
cells = t.rows[-1].cells
for c, v in zip(cells, ["13 Nov 2026", "18:56; wording revised and frozen 19:36; registered 19:54",
                        "Amendment 12, frozen script, freeze record, reproduction record",
                        "All earlier results and four pre-submission critiques known; no new analysis on real labels before registration (osf.io/ezmdn)",
                        "…1936_AMENDMENT-12_additional-analyses_FROZEN.txt; …1936_s31_amendment12_FROZEN.py"]):
    for p in c.paragraphs:
        for r in p.runs[1:]: r.text = ""
        if p.runs: p.runs[0].text = v
para(d, "")
para(d, "Amendment 12 (13 November 2026; registered at https://osf.io/ezmdn)", size=11, bold=True)
para(d, "Amendment 12 was written after all earlier results were known and after four critiques of the manuscript obtained "
        "before resubmission (one written by the AI assistant used for the analyses, three supplied by the author; none is a "
        "journal peer review). Before it was frozen, the archived release v2.0 was rerun from the public data and every "
        "deposited table was reproduced exactly (reproduction record below). The documents are reproduced without editing; "
        "the results record was written after the registered run.", size=10)
for f in sorted(os.listdir(A12)):
    if not f.endswith((".txt", ".md")): continue
    para(d, ""); para(d, f, size=11, bold=True); para(d, f"Source file: {f}", size=8.5)
    for line in open(os.path.join(A12, f), encoding="utf-8").read().rstrip("\n").split("\n"):
        para(d, line, size=7.5, font="Courier New", after=0)
p1 = os.path.join(OUT, f"{STAMP}_Online_Resource_1_Governance_Record.docx"); d.save(p1); log(f"wrote {p1}")

# ========================================================================= OR2
d = docx.Document(os.path.join(SRC, "09_Online_Resource_2_REMARK_Checklist.docx")); t = d.tables[0]
upd = {
 "1": (None, "Introduction; Methods (Derivation criteria and scale; Resampling within cohorts; Transfer between natural subgroups; Binormal model; Pathologist-scored Ki-67 and other analyses); Online Resource 1"),
 "3": ("Partly", "Chemotherapy (received or not) for METABRIC and SCAN-B; percentages in Online Resource 4, Table S36. Treatment was not modeled (Discussion, limitations)"),
 "7": (None, "The article's primary question uses no endpoint. The outcome comparison is in Online Resource 4: PFI in TCGA-BRCA, DSS in METABRIC, OS in SCAN-B, and OS in all three cohorts as a common endpoint (Amendment 9)"),
 "8": (None, "Outcome models in Online Resource 4: age and stage, or age, tumor size and nodal group; grade as sensitivity analysis"),
 "9": ("Partly", "No sample size calculation; derivation-set sizes chosen to span published studies (Methods, Resampling within cohorts). Equivalence margin 0.67 to 1.50 fixed in advance for the outcome comparison; TCGA-BRCA had 12 events in the discordant group (Online Resource 4)"),
 "11": (None, "Methods, Design and registration (first comparison post hoc; Amendments 2 to 6 posted after their analyses; Amendments 7 to 12 registered before their runs); post hoc analyses labeled; Online Resources 1 and 4"),
 "12": (None, "Table 1; Online Resource 4, Tables S1 and S36; events per group in Online Resource 4"),
 "13": ("Reported", "Table 1 (sizes, subtype shares); Online Resource 4, Table S36 (age, tumor size, nodal status, grade, stage, chemotherapy)"),
 "15": (None, "Online Resource 4, Fig. S4 (METABRIC, TCGA-BRCA, SCAN-B)"),
 "16": ("Partly", "Hazard ratios with 95% CI for the group contrasts (Online Resource 4). Coefficients of covariates are not tabulated"),
 "17": (None, "Outcome models include age and stage (or size and nodal group); grade-adjusted version (Online Resource 4)"),
 "18": (None, "Registered test in GSE81538; transfer between natural subgroups and misspecified target prevalence (Amendment 12); binormal goodness of fit; ER 2 to 3 sensitivity; single-pathologist readings; bootstrap intervals (Results; Online Resource 4)"),
 "20": (None, "Discussion, practical rules and conclusion"),
}
def put(cell, v):
    ps = cell.paragraphs
    for p in ps[1:]: p._element.getparent().remove(p._element)
    rs = ps[0].runs
    for r in rs[1:]: r.text = ""
    rs[0].text = v
for row in t.rows[1:]:
    k = row.cells[0].text.strip()
    if k in upd:
        st, where = upd[k]
        if st: put(row.cells[2], st)
        put(row.cells[3], where)
p2_ = os.path.join(OUT, f"{STAMP}_Online_Resource_2_REMARK_Checklist.docx"); d.save(p2_); log(f"wrote {p2_}")

# ========================================================================= OR4
d = docx.Document(os.path.join(SRC, "11_Online_Resource_4_Results_Tables_and_Figures.docx"))
para(d, ""); para(d, "Amendment 12 (registered at https://osf.io/ezmdn; run on 13 November 2026)", size=12, bold=True, after=6)
S = pd.read_csv(f"{R}/A12_N2_summary.csv")
nm = {"size_le20_vs_gt20": ("Tumor size", "20 mm or less", "more than 20 mm"), "node_neg_vs_pos": ("Nodal status", "node-negative", "node-positive"),
      "age_lt50_vs_ge50": ("Age", "under 50 years", "50 years or older")}
rl = {"K": "Kappa", "ACC": "Accuracy", "PM": "Proportion matching", "YJ": "Youden", "SK_oracle": "Weighted kappa, target share", "SK_population": "Weighted kappa, regional share"}
for score, label, tn in [("P2", "18-gene score", "S29"), ("P1", "MKI67", "S30")]:
    rows = []
    for sp in nm:
        for dr in ["1to2", "2to1"]:
            g = S[(S.score == score) & (S.split == sp) & (S.direction == dr)]
            a, b = (nm[sp][1], nm[sp][2]) if dr == "1to2" else (nm[sp][2], nm[sp][1])
            for r in ["K", "ACC", "PM", "YJ", "SK_oracle", "SK_population"]:
                x = g[g.rule == r].iloc[0]
                rows.append([nm[sp][0], f"{a} ({x.n_deriv}; {x.pi_deriv:.1f}%) → {b} ({x.n_target}; {x.pi_target:.1f}%)", rl[r],
                             f"{x.rmse_vs_K:.1f}", f"{x.bias_vs_K:.1f}", f"{x.rmse_same_rule:.1f}", f"{x.label_diff_vs_K_pct:.1f}",
                             f"{x.kappa_target_mean:.3f}", f"{x.whole_subgroup_err_vs_K:.1f}", f"{x.kappa_target_best:.3f}"])
    caption(d, f"Table {tn}. Amendment 12 (N2): transfer between natural subgroups of SCAN-B, {label}")
    table(d, ["Split", "Derivation → target (n; luminal B share)", "Criterion", "RMSE vs target κ optimum", "Bias", "RMSE vs same criterion",
              "Relabeled vs target κ optimum (%)", "Mean κ", "Whole-subgroup error", "Best attainable κ"], rows,
          [16, 40, 24, 14, 11, 14, 16, 12, 14, 13], merge_cols=(0, 1))
    note(d, "Errors in luminal A quantile points of the target subgroup. Derivation: 500 bootstrap sets of up to 400 tumors drawn "
            "from the derivation subgroup with their natural case mix; whole-subgroup error: derivation in the whole subgroup. "
            "Regional share: luminal B share of all SCAN-B luminal tumors (29.5%). Registered criterion (primary split, tumor "
            "size): target-weighted kappa below kappa in both directions; not met for either version.")
N3 = pd.read_csv(f"{R}/A12_N3_summary.csv"); rows = []
for c in ["TCGA-BRCA", "METABRIC", "SCAN-B"]:
    g = N3[N3.cohort == c]
    k = g[g.rule == "K"].iloc[0]; rows.append([c, "Kappa", "", f"{k.rmse:.1f}", f"{k.bias:.1f}", f"{k.label_diff_pct:.1f}", f"{k.kappa_mean:.3f}"])
    for _, x in g[g.rule == "SK"].sort_values("delta").iterrows():
        rows.append([c, "Weighted kappa", f"{int(x.delta):+d}", f"{x.rmse:.1f}", f"{x.bias:.1f}", f"{x.label_diff_pct:.1f}", f"{x.kappa_mean:.3f}"])
caption(d, "Table S31. Amendment 12 (N3): target-weighted kappa with the target luminal B share misspecified")
table(d, ["Cohort", "Criterion", "Error in target share (points)", "RMSE", "Bias", "Relabeled (%)", "Mean κ"], rows, [24, 26, 26, 16, 16, 18, 16], merge_cols=(0, 1))
note(d, "18-gene score; derivation sets of 400 tumors resampled within subtype to luminal B shares of 25% to 65% (500 per share). "
        "RMSE and bias in luminal A quantile points against the full-cohort kappa optimum. Tolerance (largest misspecification "
        "with weighted kappa below kappa in all cohorts, both directions): 10 points.")
N4 = pd.read_csv(f"{R}/A12_N4_ki67_prediction.csv").set_index("quantity"); rows = []
for r, lab in [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion matching"), ("YJ", "Youden")]:
    f = lambda q: f"{N4.loc[q, 'estimate']:.0f} ({N4.loc[q, 'ci_lo']:.0f} to {N4.loc[q, 'ci_hi']:.0f})"
    rows.append([lab, f(f"{r}_25"), f(f"{r}_65"), f(f"{r}_diff")])
caption(d, "Table S32. Amendment 12 (N4): binormal prediction of the consensus Ki-67 cut-off (GSE81538)")
table(d, ["Criterion", "25% luminal B", "65% luminal B", "Difference"], rows, [40, 35, 35, 35])
note(d, "Ki-67 %, with bootstrap 95% intervals (1,000 resamples within subtype, refitting the model). The binormal model was fitted "
        "to five operating points (R2 0.90); consensus Ki-67 took 12 distinct values, and the conversion through the luminal A "
        "distribution returns values on its 5-point grid. Model predictions, not observed movements.")
N5 = pd.read_csv(f"{R}/A12_N5_binormal_fit.csv"); rows = []
for _, x in N5.iterrows():
    sc = {"P2": "18-gene", "P1": "MKI67", "Ki67": "Consensus Ki-67"}[x.score]
    bci = "" if pd.isna(x.get("b_ci_lo", np.nan)) else f"{x.b_ci_lo:.2f} to {x.b_ci_hi:.2f}"
    fmt = lambda v: "" if pd.isna(v) else f"{v:.2f}"
    rows.append([x.cohort, sc, f"{x.a:.2f}", f"{x.b:.2f}", bci, f"{x.r2:.3f}", str(int(x.n_points)),
                 fmt(x.get("slope_resampled_K")), fmt(x.get("slope_model_free_K")), fmt(x.get("slope_model_equal_var_K")),
                 fmt(x.get("slope_resampled_ACC")), fmt(x.get("slope_model_free_ACC")), fmt(x.get("slope_model_equal_var_ACC"))])
caption(d, "Table S33. Amendment 12 (N5): binormal goodness of fit and the equal-variance assumption")
table(d, ["Cohort", "Score", "a", "b", "b, 95% interval", "R2", "Points", "κ slope, resampled", "κ slope, model", "κ slope, b = 1",
          "Accuracy slope, resampled", "Accuracy slope, model", "Accuracy slope, b = 1"], rows, [18, 16, 9, 9, 17, 10, 10, 14, 13, 13, 15, 14, 14])
note(d, "Probit-probit least-squares fit of the empirical ROC between 0.05 and 0.95 (as in Amendment 11). b, ratio of the luminal "
        "A to luminal B standard deviations on the latent scale (b = 1, equal variances); interval from 500 bootstrap resamples "
        "within subtype. Slopes in luminal A quantile points per point of luminal B share (resampled slopes from Amendment 11).")
N7 = pd.read_csv(f"{R}/A12_N7_variance_subsets.csv"); rows = []
sub = [("registered_25_65", "25%–65%"), ("inner_35_55", "35%–55%"), ("low_25_45", "25%–45%"), ("high_45_65", "45%–65%")]
for (src, coh, sc, n) in [("RNA", "TCGA-BRCA", "P2", 400), ("RNA", "METABRIC", "P2", 400), ("RNA", "SCAN-B", "P2", 400), ("Ki67", "GSE81538", "Ki67", 232)]:
    for r, lab in [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion matching"), ("YJ", "Youden"), ("SK", "Target-weighted kappa")]:
        g = N7[(N7.source == src) & (N7.cohort == coh) & (N7.score == sc) & (N7.n == n) & (N7.rule == r)].set_index("subset")
        rows.append([coh, lab] + [f"{g.loc[s, 'frac_casemix']:.2f}" for s, _ in sub])
caption(d, "Table S34. Amendment 12 (N7): case-mix share of variance by range of imposed luminal B shares")
table(d, ["Set", "Criterion"] + [s for _, s in sub], rows, [30, 40, 22, 22, 22, 22])
note(d, "Fraction of the variance of the derived cut-off due to the imposed share, B/(B + W), recomputed from the Amendment 11 "
        "derivations. RNA cohorts: 18-gene score, sets of 400; GSE81538: consensus Ki-67, sets of 232.")
N8 = pd.read_csv(f"{R}/A12_N8_ki67_near_optimal.csv"); rows = []
for _, x in N8.iterrows():
    rows.append(["Accuracy" if x.criterion == "accuracy" else "Kappa", f"{x.share}%", f"{x.best:.3f}", f"{x.argmax_lowest:.0f}%",
                 f"{x.near_lo:.0f}%" if x.near_lo == x.near_hi else f"{x.near_lo:.0f}% to {x.near_hi:.0f}%"])
rows.sort(key=lambda z: (z[0] != "Accuracy", int(z[1][:-1])))
caption(d, "Table S35. Amendment 12 (N8): near-optimal region of the consensus Ki-67 cut-off by luminal B share")
table(d, ["Criterion", "Luminal B share", "Maximum", "Optimal threshold (lowest tie)", "Thresholds within 0.01 of maximum"], rows, [28, 26, 22, 38, 42])
note(d, "Full GSE81538 luminal set (147 luminal A, 85 luminal B) weighted to each luminal B share; candidate thresholds as in "
        "Amendment 11. Registered rule: the accuracy optimum is described as moving robustly if the regions at 25% and 65% do "
        "not overlap (met).")
N9 = pd.read_csv(f"{R}/A12_N9_cohorts.csv"); rows = []
fmtv = lambda v, s="": "" if pd.isna(v) else f"{v:.0f}{s}" if s else f"{v:.1f}"
for _, x in N9.iterrows():
    rows.append([x.cohort, f"{int(x.n):,}", f"{int(x.luminal_A):,} / {int(x.luminal_B):,}", f"{x.age_median:.0f} ({x.age_q1:.0f} to {x.age_q3:.0f})",
                 "" if pd.isna(x.get("size_median_mm")) else f"{x.size_median_mm:.0f}",
                 "" if pd.isna(x.get("node_positive_pct")) else f"{x.node_positive_pct:.1f}",
                 "" if pd.isna(x.get("grade3_pct")) else f"{x.grade3_pct:.1f}",
                 "" if pd.isna(x.get("stage_I_pct")) else f"I {x.stage_I_pct:.1f}; II {x.stage_II_pct:.1f}; III-IV {x.stage_III_IV_pct:.1f}",
                 "" if pd.isna(x.get("chemo_pct")) else f"{x.chemo_pct:.1f}"])
caption(d, "Table S36. Amendment 12 (N9): characteristics of the ER-positive, HER2-negative strata")
table(d, ["Cohort", "Patients", "Luminal A / B", "Age, median (IQR)", "Tumor size, median (mm)", "Node-positive (%)", "Grade 3 (%)",
          "Stage (%)", "Chemotherapy (%)"], rows, [22, 16, 22, 24, 20, 18, 16, 34, 18], merge_cols=())
note(d, "Percentages of the whole stratum, with missing values counted in the denominator. Empty cells: variable not available "
        "in that cohort's files.")

# Figures S3-S5
def fig_par(doc, path, cap, width_mm=170):
    para(doc, ""); doc.add_picture(path, width=Mm(width_mm)); p = para(doc, "", after=6)
    r = p.add_run(cap.split(" ", 2)[0] + " " + cap.split(" ", 2)[1] + " "); r.bold = True; r.font.size = Pt(9.5); r.font.name = TNR
    r2 = p.add_run(cap.split(" ", 2)[2]); r2.font.size = Pt(9.5); r2.font.name = TNR
from PIL import Image
for src, png in [("04_Fig1.tiff", "FigS3.png"), ("05_Fig2.tiff", "FigS4.png")]:
    Image.open(os.path.join(SRC, src)).convert("RGB").save(os.path.join(OUT, png), dpi=(300, 300))
fig_par(d, os.path.join(OUT, "FigS3.png"), "Fig. S3 Figure 1 of the 11 November 2026 version, with panel c on the percentile scale of the resampled "
        "luminal set (registered scale of Amendment 6), now replaced by the luminal A quantile scale (Error Log 5). On this scale "
        "a cut-off that does not move has slopes of 0.65 to 0.70 for the 18-gene score.")
fig_par(d, os.path.join(OUT, "FigS4.png"), "Fig. S4 Kaplan-Meier estimates by group defined on the 18-gene score: disease-specific survival in METABRIC (a), "
        "progression-free interval in TCGA-BRCA (b) and overall survival in SCAN-B (c). Stable luminal A-like, at or below the "
        "59th percentile; discordant, between the 59th and 74th percentiles; stable luminal B-like, above the 74th percentile. "
        "TCGA-BRCA had 12 events in the discordant group, so panel b is descriptive. Formerly Figure 2 of the article.")
# Fig S5 probit plots
sys.argv = [os.path.join(HERE, "s27_amendment11.py")]
import importlib.util
spec = importlib.util.spec_from_file_location("s27", sys.argv[0]); s27 = importlib.util.module_from_spec(spec)
_saved = open(os.path.join(R, "A11_run.log"), "rb").read(); spec.loader.exec_module(s27); s27.LOG.close()
open(os.path.join(R, "A11_run.log"), "wb").write(_saved)
plt.rcParams.update({"font.size": 7.5, "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})
fig, axs = plt.subplots(1, 3, figsize=(174 / 25.4, 2.5))
for ax, (c, f) in zip(axs, [("TCGA-BRCA", "cohort_tcga.csv"), ("METABRIC", "cohort_metabric.csv"), ("SCAN-B", "cohort_scanb.csv")]):
    dd = pd.read_csv(os.path.join(R, f), low_memory=False); m = dd.PAM50.isin(["LumA", "LumB"]).values
    x = dd.P2.values.astype(float)[m]; y = (dd.PAM50.values[m] == "LumB").astype(int)
    T = s27.Target(x, y, x); tt = np.unique(T.L); fpr = 1 - T.F(T.A, tt); tpr = 1 - T.F(T.B, tt)
    ok = (fpr >= .05) & (fpr <= .95) & (tpr >= .05) & (tpr <= .95); a, b = s27.binormal_fit(T)
    ax.plot(norm.ppf(fpr[ok]), norm.ppf(tpr[ok]), ".", ms=2, color="#7B5EA7", label="Empirical ROC points")
    xx = np.linspace(-1.7, 1.7, 50); ax.plot(xx, a + b * xx, "-", color="#A63D40", lw=1.2, label=f"Fit: a = {a:.2f}, b = {b:.2f}")
    ax.plot(xx, a + xx, ":", color="#6B6B6B", lw=1, label="Equal variance (b = 1)")
    ax.set_xlabel("probit(1 − specificity)"); ax.set_ylabel("probit(sensitivity)"); ax.legend(loc="lower right", fontsize=5.8)
    ax.text(0.03, 0.95, c, transform=ax.transAxes, fontweight="bold", va="top")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "FigS5.png"), dpi=300); plt.close(fig)
fig_par(d, os.path.join(OUT, "FigS5.png"), "Fig. S5 Binormal fit for the 18-gene score (Amendment 12, N5): empirical ROC operating points on the probit "
        "scale (sensitivity and 1 − specificity between 0.05 and 0.95), the least-squares line and the equal-variance line.")
p4 = os.path.join(OUT, f"{STAMP}_Online_Resource_4_Results_Tables_and_Figures.docx"); d.save(p4); log(f"wrote {p4}")
for f in ["FigS3.png", "FigS4.png", "FigS5.png"]: os.remove(os.path.join(OUT, f)) if f != "FigS5.png" else None
log("done")
