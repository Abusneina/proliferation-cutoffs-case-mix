"""Prepare ms_ce.json for build_ce.js: number citations, build Tables 1-6, legends, counts.
Inputs: content_ce.py; the Cancer Epidemiology manuscript of 11 Nov 2026 (reference list, Tables 1 and 3);
results of Amendments 11 and 12 in the v2 repository clone."""
import re, json, sys, os
import docx, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import content_ce as C

OLD = ("/tmp/claude-0/-home-claude/65323bc2-e910-5ee8-ada1-1fa62309a0fd/scratchpad/pkg/"
       "Submission_Package_CancerEpidemiology_2026-11-11_2012/03_Manuscript_CancerEpidemiology_2026-11-11_2008.docx")
R = "/home/claude/work/v2/repo/results"
KEYS = ["goldhirsch2011", "goldhirsch2013", "coates2015", "cheang2009", "prat2013", "nielsen2021", "fernandez2017",
        "lopez2024", "dixpeek2023", "abusneina2026", "dowsett2011", "polley2013", "feinstein1990", "byrt1993",
        "leeflang2013", "youden1950", "brenner1997", "metz1978", "remark2006", "hoadley2018", "curtis2012",
        "pereira2016", "cerami2012", "brueffer2018", "parker2009", "venet2011", "hatzis2011", "kan2018", "osfprotocol",
        "holm2021", "chen2016", "maisonneuve2014", "lundgren2019", "fluss2005", "altman1994", "ceccarelli2019",
        "noske2020"]
d = docx.Document(OLD)
paras = [p.text for p in d.paragraphs]
i0 = paras.index("References"); refs_old = {}
for t in paras[i0 + 1:]:
    m = re.match(r"^(\d+)\.\s+(.*)$", t)
    if m: refs_old[int(m.group(1))] = m.group(2)
    if t.startswith("Figure legends"): break
assert len(refs_old) == 37
REF = {k: refs_old[i + 1] for i, k in enumerate(KEYS)}
assert REF["metz1978"].startswith("Metz CE") and REF["noske2020"].startswith("Noske A")

order = []
def fmt(nums):
    nums = sorted(set(nums)); out = []; j = 0
    while j < len(nums):
        k = j
        while k + 1 < len(nums) and nums[k + 1] == nums[k] + 1: k += 1
        out.append(f"{nums[j]}" if k == j else (f"{nums[j]}, {nums[k]}" if k == j + 1 else f"{nums[j]}-{nums[k]}"))
        j = k + 1
    return "[" + ", ".join(out) + "]"
def number(text):
    def rep(m):
        ks = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        for k in ks:
            assert k in REF, k
            if k not in order: order.append(k)
        return fmt([order.index(k) + 1 for k in ks])
    return re.sub(r"\[(@[^\]]+)\]", rep, text)

body = [(t, number(x)) for t, x in C.BODY]
f2 = lambda v: (f"{v:.2f}".replace("-0.00", "0.00")).replace("-", "−")

# Table 1 (cohorts), endpoint column removed (outcome analysis now in Online Resource 4)
T1raw = [[c.text for c in r.cells] for r in d.tables[0].rows]
drop = T1raw[0].index("Endpoint (events)")
T1 = [[c for j, c in enumerate(r) if j != drop] for r in T1raw]

# Table 2 (criteria)
T2 = [["Criterion", "Rule", "Depends on prevalence", "Under within-subtype resampling", "Role here"],
      ["Kappa", "Maximum Cohen's kappa against PAM50", "Yes", "Moves with the share", "Main agreement criterion"],
      ["Accuracy", number("Minimum misclassification, as in Cheang et al. [@cheang2009]"), "Yes", "Moves with the share",
       "Published criterion"],
      ["Proportion matching", "Lowest cut-off calling no more tumors positive than the luminal B share", "Yes, by definition",
       "Moves with the share", "Definitional reference"],
      ["Youden", "Maximum sensitivity + specificity − 1", "No", "Cannot move (sampling only)", "Prevalence-free comparator"],
      ["Balanced kappa", "Kappa with luminal A and B weighted equally", "No", "Equals the Youden cut-off", "Code check"],
      ["Target-weighted kappa", "Kappa with the derivation set weighted to the target luminal B share", "No",
       "Cannot move", "Reweighting adjustment"]]

# Table 3 (slopes) from Amendment 11
o5 = pd.read_csv(f"{R}/A11_O5_model_check.csv")
coh = ["TCGA-BRCA", "METABRIC", "SCAN-B"]
rl = [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion matching"), ("YJ", "Youden")]
T3 = [["Score", "Criterion", "TCGA-BRCA", "TCGA-BRCA", "METABRIC", "METABRIC", "SCAN-B", "SCAN-B"],
      ["", "", "Resampled", "Model", "Resampled", "Model", "Resampled", "Model"]]
for s, sl in [("P2", "18-gene"), ("P1", "MKI67")]:
    for r, lab in rl:
        row = [sl, lab]
        for c in coh:
            g = o5[(o5.cohort == c) & (o5.score == s) & (o5.rule == r)].iloc[0]
            row += [f2(g.slope_qA_per_point), f2(g.slope_model)]
        T3.append(row)

# Table 4 (case mix against sampling; transfer) from Amendments 11 and 12
o = pd.read_csv(f"{R}/A11_O2_O3.csv"); k = pd.read_csv(f"{R}/A11K_O2_O3.csv"); n7 = pd.read_csv(f"{R}/A12_N7_variance_subsets.csv")
rl4 = [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion matching"), ("YJ", "Youden"), ("SK", "Target-weighted kappa")]
T4 = [["Set", "Criterion", "Case-mix share, 25%–65%", "Case-mix share, 35%–55%", "RMSE", "Relabeled (%)",
       "Mean kappa", "Best attainable kappa"]]
def add(df, name, src, cohort, score, n):
    for r, lab in rl4:
        g = df[df.rule == r].iloc[0]
        inner = n7[(n7.source == src) & (n7.cohort == cohort) & (n7.score == score) & (n7.n == n) & (n7.rule == r) &
                   (n7.subset == "inner_35_55")].frac_casemix.iloc[0]
        T4.append([name, lab, f"{g.frac_casemix:.2f}", f"{inner:.2f}", f"{g.rmse:.1f}", f"{g.label_diff_pct:.1f}",
                   f"{g.kappa_target_mean:.3f}", f"{g.kappa_target_opt:.3f}" if r == "K" else ""])
for c in coh: add(o[(o.cohort == c) & (o.score == "P2") & (o.n == 400)], c, "RNA", c, "P2", 400)
add(k[k.n == 232], "GSE81538, Ki-67", "Ki67", "GSE81538", "Ki67", 232)

# Table 5 (natural subgroups, Amendment 12)
S = pd.read_csv(f"{R}/A12_N2_summary.csv"); S = S[S.score == "P2"]
names = {"size_le20_vs_gt20": ("Tumor size", "20 mm or less", "more than 20 mm"),
         "node_neg_vs_pos": ("Nodal status", "node-negative", "node-positive"),
         "age_lt50_vs_ge50": ("Age", "under 50 years", "50 years or older")}
cols = [("K", "Kappa"), ("ACC", "Accuracy"), ("SK_oracle", "Target-weighted kappa, target share"),
        ("SK_population", "Target-weighted kappa, regional share"), ("YJ", "Youden")]
T5 = [["Split", "Derivation → target (luminal B share)"] + [c[1] for c in cols]]
for sp in ["size_le20_vs_gt20", "node_neg_vs_pos", "age_lt50_vs_ge50"]:
    nm, g1, g2 = names[sp]
    for dr in ["1to2", "2to1"]:
        g = S[(S.split == sp) & (S.direction == dr)].set_index("rule")
        a, b = (g1, g2) if dr == "1to2" else (g2, g1)
        pd_, pt = g.pi_deriv.iloc[0], g.pi_target.iloc[0]
        T5.append([nm, f"{a} ({pd_:.1f}%) → {b} ({pt:.1f}%)"] + [f"{g.loc[c, 'rmse_vs_K']:.1f}" for c, _ in cols])

# Table 6 (published studies) from the 11 Nov manuscript, citations renumbered
oldnum = {i + 1: kk for i, kk in enumerate(KEYS)}
def renum_cell(s):
    def rep(m):
        kk = oldnum[int(m.group(1))]
        if kk not in order: order.append(kk)
        return f"[{order.index(kk) + 1}]"
    return re.sub(r"\[(\d+)\]", rep, s)
T6 = [[renum_cell(c) for c in r.cells and [x.text for x in r.cells]] for r in d.tables[2].rows]

refs = [f"{i + 1}. {REF[kk]}" for i, kk in enumerate(order)]
unused = [kk for kk in KEYS if kk not in order]

TT = {"1": "Table 1 Analysis cohorts and agreement of the proliferation-defined luminal B call with PAM50",
      "2": "Table 2 Derivation criteria compared",
      "3": "Table 3 Case-mix slope of the derived cut-off by criterion: resampled and predicted by the binormal model",
      "4": "Table 4 Case mix against sampling variation, and transfer of derived cut-offs within cohorts",
      "5": "Table 5 Transfer of derived cut-offs between natural subgroups of SCAN-B (Amendment 12)",
      "6": "Table 6 Published studies that derived a Ki-67 cut-off against a multigene reference"}
TN = {"1": ("ER+/HER2−, estrogen receptor-positive, HER2-negative. Luminal B share is the PAM50 luminal B proportion among "
            "PAM50 luminal tumors. Cut-offs are percentiles of the ER+/HER2− stratum; confidence intervals are from "
            "2,000 bootstrap resamples. The last column gives the optimum as a percentile of the PAM50 luminal tumors and "
            "as a luminal A quantile. 18-gene, PAM50 proliferation genes with MKI67 excluded."),
      "2": ("Candidate cut-offs were the observed values between the 5th and 95th percentiles of the derivation set; tumors "
            "above the cut-off were luminal B-like; ties went to the lowest value. Within-subtype resampling holds each "
            "subtype's score distribution fixed, so criteria that do not depend on prevalence can move only by sampling."),
      "3": ("Slope: change in the median derived cut-off, in luminal A quantile points, per point of luminal B share, over "
            "imposed shares of 15% to 65% (derivation sets of 1,000 tumors, 500 resamples per share; Amendment 11). "
            "Negative values mean the cut-off falls as the share rises. Model: slope of the population cut-off under a "
            "binormal model fitted to each cohort. Registered criterion: for the 18-gene score, |resampled − model| "
            "≤ 0.10 for kappa and accuracy in all three cohorts (met). The Youden cut-off cannot move under "
            "within-subtype resampling; its model slope is zero."),
      "4": ("RNA cohorts: 18-gene score, derivation sets of 400 tumors. Ki-67: consensus Ki-67 in GSE81538, derivation sets "
            "of 232 tumors. Case-mix share: fraction of the variance of the derived cut-off explained by the imposed "
            "luminal B share over the range shown (25% to 65% registered in Amendment 11; 35% to 55% added in Amendment 12). "
            "RMSE: root-mean-square difference, in luminal A quantile points, from the same criterion applied to the full "
            "set. Relabeled: mean percentage of luminal tumors in the full set labeled differently from that criterion's "
            "full-set cut-off. Mean kappa: against PAM50 in the full set; best attainable kappa: kappa optimum in the full luminal "
            "set (Table 1 gives the peak for the whole stratum). Target-weighted kappa uses the true luminal B "
            "share of the full set, the population on which its error is measured."),
      "5": ("18-gene score. Values are root-mean-square differences, in luminal A quantile points of the target subgroup, "
            "between the cut-off derived in the derivation subgroup (500 bootstrap sets of up to 400 tumors with their "
            "natural case mix) and the kappa optimum of the whole target subgroup. Target share: kappa weighted to the "
            "target subgroup's luminal B share; regional share: weighted to the share of all SCAN-B luminal tumors "
            "(29.5%). Registered criterion: target-weighted kappa lower than kappa in both directions of the split with the "
            "largest difference in luminal B share (tumor size); not met."),
      "6": ("P, prevalence-dependent criterion; Y, Youden-type; U, criterion not stated; ROR, risk of recurrence; RS, "
            "recurrence score. a Luminal B among PAM50 luminal tumors; the reported comparison was luminal A against all "
            "other subtypes. b Prolif surrogate in the STO-3 and Clinseq cohorts. c All subtypes, of which 196 PAM50 "
            "luminal; kappa was computed across the full IHC classification. d Share not at low risk. e Tumors ≤ 2 cm "
            "and > 2 cm; share at intermediate or high ROR. f High risk under traditional or TAILORx categories.")}
LEG = [
("Fig. 1", "Agreement with PAM50 and the Youden cut-off. (a, b) Cohen's kappa between the proliferation-defined luminal B "
 "call and PAM50 across cut-offs in TCGA-BRCA (a) and METABRIC (b). Solid line, 18-gene proliferation score; dashed line, "
 "MKI67 alone. Markers show the kappa-optimal cut-off for each score and shaded bands its bootstrap 95% confidence "
 "interval. (c) Youden-optimal cut-off, as a luminal A quantile, under resampling to fixed luminal B shares within each "
 "cohort, which keeps it fixed by design. (d) Youden-optimal cut-off with bootstrap 95% confidence intervals, as a "
 "luminal A quantile (filled markers, solid lines) and as a percentile of the whole stratum (open markers, dotted "
 "lines). Two-column width."),
("Fig. 2", "Case mix, sampling and transfer of derived cut-offs (Amendment 11). (a) Median kappa-optimal cut-off for the "
 "18-gene score, as a luminal A quantile, in derivation sets of 1,000 tumors resampled to each luminal B share; bands, "
 "10th to 90th percentile of 500 resamples; dotted lines, binormal model prediction for each cohort. (b) Share of the "
 "variance of the derived cut-off due to case mix, over luminal B shares of 25% to 65%, by criterion (derivation sets of "
 "400 tumors). (c) Transfer error: root-mean-square difference, in luminal A quantile points, between the cut-off "
 "derived at 400 tumors and the same criterion applied to the full cohort. (d) Pathologist-scored consensus Ki-67 in "
 "GSE81538: median derived threshold by imposed luminal B share for three criteria (derivation sets of 232 tumors); "
 "markers are offset horizontally where lines coincide. Cohorts are distinguished by marker, line style or hatching. "
 "Two-column width."),
("Fig. 3", "Transfer between natural subgroups and the Ki-67 prediction (Amendment 12). (a) Root-mean-square error, in "
 "luminal A quantile points of the target subgroup, of cut-offs derived in one SCAN-B subgroup and applied to the other, "
 "for the tumor-size split in both directions, by criterion (18-gene score). (b) Consensus Ki-67 thresholds predicted "
 "by the binormal model at luminal B shares of 25% and 65% for kappa and accuracy (markers, with bootstrap 95% "
 "intervals) and the medians observed in resampled sets of 232 tumors (open markers). Two-column width."),
("Fig. 4", "Registered test of the cut-off mechanism in GSE81538 (consensus Ki-67, 232 luminal tumors; Amendment 7). (a) "
 "Kappa-optimal percentile against 100 minus the imposed luminal B share for simulated continuous scores (circles), the "
 "observed Ki-67 distributions resampled at N = 40,000 (triangles), a threshold fixed at 15% (dashed; post hoc) and the "
 "registered test (diamonds); dotted line, slope 1. On this percentile scale a fixed threshold already shows a slope "
 "of 0.56 (Error Log 5). (b) Youden cut-off for consensus Ki-67, as a luminal A quantile. (c) Kappa-optimal Ki-67 "
 "threshold; line, median of 200 resamples; band, 2.5th to 97.5th percentile; dotted line, 15%. Two-column width."),
]

def wc(s): return len(re.findall(r"\S+", s))
counts = dict(abstract=sum(wc(x) for _, x in C.ABSTRACT), main=sum(wc(x) for t, x in body if t == "p"),
              highlights=sum(wc(h) for h in C.HIGHLIGHTS), refs=len(refs), tables=6, figures=4)
print("references", len(refs), "unused", unused, counts)
json.dump(dict(title=C.TITLE, running=C.RUNNING, abstract=C.ABSTRACT, keywords=C.KEYWORDS, body=body, ack=C.ACK,
               statements=C.STATEMENTS, refs=refs, legends=LEG,
               tables={"1": T1, "2": T2, "3": T3, "4": T4, "5": T5, "6": T6}, ttitles=TT, tnotes=TN, counts=counts,
               highlights=C.HIGHLIGHTS), open(os.path.join(HERE, "ms_ce.json"), "w"), indent=1)
