"""
s20_online_resources.py  Builds Online Resources 1-4 (A4 PDFs) for the BCRT submission.
Colour theme: burgundy and ochre on warm grey (no blue).
Usage: python3 s20_online_resources.py <stamp YYYY-MM-DD_HHMM>
"""
import sys, os, glob, textwrap, time
import numpy as np, pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Image, KeepTogether, Preformatted)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib, PIL.Image

STAMP = sys.argv[1] if len(sys.argv) > 1 else time.strftime("%Y-%m-%d_%H%M")
W = "/home/claude/work"; R = f"{W}/results"; P = f"{W}/protocol"; L = f"{W}/litreview"; FG = f"{W}/figures"
OUT = f"{W}/online_resources"; os.makedirs(OUT, exist_ok=True)
T0 = time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)

fd = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data/fonts/ttf")
pdfmetrics.registerFont(TTFont("DV", f"{fd}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", f"{fd}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", f"{fd}/DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVM", f"{fd}/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

BURG = colors.HexColor("#7A2E2E"); OCHRE = colors.HexColor("#C27C0E"); INK = colors.HexColor("#2B2B2B")
BAND = colors.HexColor("#F3EEEA"); RULE = colors.HexColor("#CFC6BF")
H1 = ParagraphStyle("H1", fontName="DVB", fontSize=14, leading=18, textColor=BURG, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="DVB", fontSize=10.5, leading=14, textColor=BURG, spaceBefore=10, spaceAfter=4, keepWithNext=1)
BODY = ParagraphStyle("B", fontName="DV", fontSize=8.8, leading=12.2, textColor=INK, spaceAfter=4)
SMALL = ParagraphStyle("S", fontName="DV", fontSize=7.4, leading=9.6, textColor=INK, spaceAfter=3)
CAP = ParagraphStyle("C", fontName="DV", fontSize=8.2, leading=11, textColor=INK, spaceBefore=6, spaceAfter=3)
CELL = ParagraphStyle("CE", fontName="DV", fontSize=7.4, leading=9.2, textColor=INK)
CELLH = ParagraphStyle("CH", fontName="DVB", fontSize=7.4, leading=9.2, textColor=colors.white)
MONO = ParagraphStyle("M", fontName="DVM", fontSize=6.6, leading=8.2, textColor=INK)

def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def footer(title):
    def f(c, d):
        c.saveState(); c.setFont("DV", 7); c.setFillColor(colors.HexColor("#6B6B6B"))
        c.drawString(2*cm, 1.2*cm, title)
        c.drawRightString(A4[0]-2*cm, 1.2*cm, f"Page {d.page}")
        c.restoreState()
    return f

def head(esm, title, sub):
    return [Paragraph(f"Online Resource {esm}", ParagraphStyle("t", fontName="DV", fontSize=8.5, textColor=OCHRE, leading=11)),
            Paragraph(title, H1), Paragraph(sub, BODY), Spacer(1, 4)]

def tbl(header, rows, widths=None, merge_cols=(), zebra=True, fs=None):
    data = [[Paragraph(esc(h), CELLH) for h in header]]
    prev = None
    for r in rows:
        data.append([Paragraph(esc(c), CELL) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), BURG), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, -1), 0.25, RULE), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    # merge repeated category cells (blank out repeats, span vertically)
    for c in merge_cols:
        start = 1
        for i in range(2, len(data) + 1):
            same = i < len(data) and rows[i-1][c] == rows[start-1][c] and rows[i-1][c] != ""
            if not same:
                if i - 1 > start:
                    st.append(("SPAN", (c, start), (c, i - 1)))
                    for k in range(start + 1, i): data[k][c] = Paragraph("", CELL)
                start = i
    t = Table(data, colWidths=widths, repeatRows=1)
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), BAND))
    t.setStyle(TableStyle(st)); return t

def verbatim(path, title=None):
    out = []
    name = os.path.basename(path)
    out.append(Paragraph(f"<b>{esc(title or name)}</b>", H2))
    out.append(Paragraph(f"Source file: {esc(name)}", SMALL))
    raw = open(path, encoding="utf-8").read().replace("\t", "    ")
    lines = []
    for ln in raw.splitlines():
        if not ln.strip(): lines.append(""); continue
        ind = len(ln) - len(ln.lstrip())
        lines += textwrap.wrap(ln, width=118, subsequent_indent=" " * (ind + 4), break_long_words=True) or [""]
    out.append(Preformatted("\n".join(lines), MONO))
    out.append(Spacer(1, 6))
    return out

def img(path, width_cm=16.0):
    w, h = PIL.Image.open(path).size
    return Image(path, width=width_cm*cm, height=width_cm*cm*h/w)

def build(name, story, title):
    p = f"{OUT}/{STAMP}_{name}.pdf"
    d = SimpleDocTemplate(p, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.9*cm,
                          title=title, author="Abdelmuhsen M. Abusneina")
    d.build(story, onFirstPage=footer(title), onLaterPages=footer(title)); log(f"wrote {p}")
    return p

def f2(x, n=2):
    return "" if pd.isna(x) else f"{x:.{n}f}"
def ci(hr, lo, hi, n=2):
    return f"{hr:.{n}f} ({lo:.{n}f} to {hi:.{n}f})" if not pd.isna(lo) else f"{hr:.{n}f}"
def pv(p):
    return "" if pd.isna(p) else ("<0.001" if p < 0.001 else f"{p:.3f}")

TITLE = ("Agreement-optimized gene-expression proliferation cut-offs for luminal A versus luminal B breast cancer inherit the case mix of their derivation population: an analysis of six cohorts")
AUTH = "Abdelmuhsen M. Abusneina, University of Benghazi, Benghazi, Libya. ORCID 0000-0001-9909-5588"

# =========================================================== ESM 1: governance record
log("ESM 1")
s = head(1, "Governance record: frozen documents, amendments and error logs",
         f"Article: {esc(TITLE)}. Author: {AUTH}. Journal: Breast Cancer Research and Treatment.")
s.append(Paragraph(
    "This file reproduces, without editing, every document that was frozen before an analysis was run, the error logs, and the freeze records. "
    "Times are UTC+2. Times in the table are file-save times. The times written in the names and headers of the 13 October documents were entered by hand "
    "and are 4 to 42 minutes later than the save times; Error Log 3 lists both and shows that each document was saved before the analysis it governs. "
    "The gene list and Amendments 2 to 6 were posted on the Open Science Framework (project https://osf.io/cwkd9) on 15 October 2026, after their analyses, "
    "so their timing rests on the author's file records. The literature protocol was registered on 13 October 2026 at 21:51 (https://osf.io/pc9wm), "
    "Amendment 7 on 14 October 2026 at 12:47 (https://osf.io/p5hb7), and Amendments 8 and 9 were posted in osf.io/cwkd9 on 15 October 2026 at 18:13, "
    "before their analyses (started 18:15), and registered at https://osf.io/su2hg (DOI 10.17605/OSF.IO/SU2HG). "
    "Amendment 10 was frozen with its analysis script at 19:38, posted in osf.io/cwkd9 at 20:19, run at 20:22 and registered at 20:30 "
    "(https://osf.io/db7a8; the first registration version attached the pre-freeze draft by mistake, corrected in an update).", BODY))
tl = [
 ["13 Oct 2026", "15:11", "Gene list (P1, P2)", "No expression value read", "…1515_proliferation_gene_list_FROZEN.txt"],
 ["", "15:40", "Amendment 2", "TCGA-BRCA and METABRIC optima known; no outcome comparison", "…1545_AMENDMENT-2_discordant-zone_FROZEN.txt"],
 ["", "15:48", "Amendment 3", "No SCAN-B file opened for outcome analyses", "…1630_AMENDMENT-3_SCAN-B-confirmatory_FROZEN.txt"],
 ["", "15:48", "Error Log 1", "Withdrawn test D3 (range restriction); passed by construction", "…1620_ERROR-LOG-1_D3-range-restriction.txt"],
 ["", "16:01", "Amendment 4", "SCAN-B clinical metadata only", "…1605_AMENDMENT-4_pooled-C1-and-SCANB-adjustment_FROZEN.txt"],
 ["", "17:30", "Amendment 5", "SCAN-B matrix verified; no score computed", "…1735_AMENDMENT-5_SCANB-sweep-and-transfer_FROZEN.txt"],
 ["", "17:33", "Error Log 2", "Absolute-scale transfer claim overstated; corrected", "…1750_ERROR-LOG-2_absolute-transfer-overstated.txt"],
 ["", "17:52", "Amendment 6", "Pattern seen after SCAN-B sweep (post hoc); resampling test specified before computation", "…1800_AMENDMENT-6_prevalence-mechanism_FROZEN.txt"],
 ["", "19:22", "Protocol v1.0 (literature)", "Search and title and abstract screening done before registration at 21:51 (Deviation 1, Online Resource 3)", "…1940_Protocol_…_v1.0.docx (registered at osf.io/pc9wm; not reproduced here)"],
 ["14 Oct 2026", "12:16", "Amendment 7", "Field names, value types and eligible count only; registered 12:47", "…1216_AMENDMENT-7_GSE81538-IHC-Ki67-confirmatory_FROZEN.txt"],
 ["", "16:41", "Amendment 8 and gene lists P3, P4", "Gene symbols only; P1 and P2 reproduced from fresh downloads; posted 15 Oct 18:13", "…1641_AMENDMENT-8_…_FROZEN.txt; …1641_GENE-LIST_P3…; …1641_GENE-LIST_P4…"],
 ["", "16:51", "Amendment 9", "Cohort death totals only, seen while testing the code on shuffled outcomes; posted 15 Oct 18:13", "…1651_AMENDMENT-9_overall-survival-harmonized-endpoint_FROZEN.txt"],
 ["15 Oct 2026", "18:27; v2 19:02", "Error Log 3", "Stated freeze times differ from save times (13 Oct documents)", "…1827_ERROR-LOG-3_…txt; …1902_ERROR-LOG-3_…_v2.txt"],
 ["", "19:38", "Amendment 10 and frozen script", "Field names, labels and gene coverage only; posted 20:19 in osf.io/cwkd9; run 20:22; registered 20:30 (osf.io/db7a8)", "…1938_AMENDMENT-10_…_FROZEN.txt; …1938_s23_amendment10_FROZEN.py"],
 ["", "20:23", "Error Log 4", "Amendment 10 ER field covers 310 of 508 samples; registered verdict not tested", "…2023_ERROR-LOG-4_Amendment-10-ER-field-covers-310-of-508.txt"],
 ["16 Oct 2026", "11:53; updated 11:57", "Error Log 5", "Percentile scale of the resampling slope includes a fixed-cut-off component; Youden fixed by design; denominator of observed optima", "…1153_ERROR-LOG-5_percentile-scale-and-denominator.txt"],
]
s.append(tbl(["Date", "Time", "Document", "State of knowledge when frozen", "File"], tl,
             [1.8*cm, 1.3*cm, 2.8*cm, 5.5*cm, 5.6*cm], merge_cols=(0,)))
s.append(Spacer(1, 4))
s.append(Paragraph("File integrity: the protocol file for the literature review (v1.0) has MD5 a16d2aedb9da0a8baf1213fdfb7283f4 and SHA-256 4d3ec22812f7e871fc6f6dc2cb53293c7bd35d60979f5b3de1d69ef31589e253. "
                   "SHA-256 values of all other documents are in the freeze and posting records reproduced at the end of this file.", SMALL))
s.append(Spacer(1, 6))
s.append(Paragraph("<b>Cohort and score definitions (moved from the article for length).</b> TCGA-BRCA receptor status came from the Firehose Legacy release; "
    "HER2-negative status required a negative immunohistochemistry result, or an equivocal result with negative in situ hybridization. METABRIC and SCAN-B receptor status "
    "was used as deposited. TCGA-BRCA RSEM values were log2(x + 1) transformed; METABRIC microarray values were used on their deposited log2 scale; SCAN-B values were the "
    "deposited gene-level estimates, computed by the submitters as log2(FPKM + 0.1), without further transformation. Where a gene had two rows (BIRC5 in METABRIC), the last "
    "row was used. The 18 genes of P2 are listed in the frozen gene list reproduced below; P3 and P4 lists follow Amendment 8.", BODY))
order = ["2026-10-13_1515_proliferation_gene_list_FROZEN.txt", "2026-10-13_1545_AMENDMENT-2_discordant-zone_FROZEN.txt",
         "2026-10-13_1630_AMENDMENT-3_SCAN-B-confirmatory_FROZEN.txt", "2026-10-13_1620_ERROR-LOG-1_D3-range-restriction.txt",
         "2026-10-13_1605_AMENDMENT-4_pooled-C1-and-SCANB-adjustment_FROZEN.txt", "2026-10-13_1735_AMENDMENT-5_SCANB-sweep-and-transfer_FROZEN.txt",
         "2026-10-13_1750_ERROR-LOG-2_absolute-transfer-overstated.txt", "2026-10-13_1800_AMENDMENT-6_prevalence-mechanism_FROZEN.txt",
         "2026-10-14_1216_AMENDMENT-7_GSE81538-IHC-Ki67-confirmatory_FROZEN.txt",
         "2026-10-14_1641_AMENDMENT-8_gene-disjoint-proliferation-score_FROZEN.txt",
         "2026-10-14_1641_GENE-LIST_P3-metaPCNA-minus-PAM50_FROZEN.txt", "2026-10-14_1641_GENE-LIST_P4-HallmarkG2M-minus-PAM50_FROZEN.txt",
         "2026-10-14_1641_FREEZE-RECORD_AMENDMENT-8_sha256.txt",
         "2026-10-14_1651_AMENDMENT-9_overall-survival-harmonized-endpoint_FROZEN.txt", "2026-10-14_1651_FREEZE-RECORD_AMENDMENT-9_sha256.txt",
         "2026-10-15_1827_ERROR-LOG-3_stated-freeze-times-vs-file-times.txt", "2026-10-15_1902_ERROR-LOG-3_stated-freeze-times-vs-file-times_v2.txt",
         "2026-10-15_1826_POSTING-RECORD_gene-list-amendments-2-6-error-logs_sha256.txt",
         "2026-10-15_1938_AMENDMENT-10_independent-RNA-cohort-GSE25066_FROZEN.txt", "2026-10-15_1938_FREEZE-RECORD_AMENDMENT-10_sha256.txt",
         "2026-10-15_2023_ERROR-LOG-4_Amendment-10-ER-field-covers-310-of-508.txt", "2026-10-16_1153_ERROR-LOG-5_percentile-scale-and-denominator.txt"]
for i, f in enumerate(order):
    log(f"  ESM 1 document {i+1}/{len(order)}: {f[:60]}")
    s.append(PageBreak()); s += verbatim(f"{P}/{f}")
build("ESM_1_governance-record", s, "Online Resource 1: governance record")

# =========================================================== ESM 2: REMARK
log("ESM 2")
s = head(2, "REMARK checklist",
         "Reporting recommendations for tumor marker prognostic studies (McShane et al., 2006) [19 in the article]. "
         "The article's primary question is methodological (how the optimal cut-off depends on case mix), not the prognostic value of a marker, "
         "so items that concern prognostic modeling apply only to the secondary outcome analysis of the discordant group. "
         "Section names refer to the article.")
rem = [
 ["1", "Marker, objectives, pre-specified hypotheses", "Reported", "Introduction; Methods, Cut-off sweep and case mix, and Registered test in GSE81538 (C1 to C3); Online Resource 1"],
 ["2", "Patient characteristics, source, inclusion and exclusion", "Reported", "Methods, Cohorts and scores; Table 1; Online Resource 4, Table S1 (attrition)"],
 ["3", "Treatments received and how chosen", "Partly", "Endocrine therapy and chemotherapy (received or not) for METABRIC and SCAN-B, radiotherapy for METABRIC and TCGA-BRCA; cohort percentages in Results, Cohorts. Treatment was not modeled (Methods; Discussion, limitations)"],
 ["4", "Biological material, preservation, storage", "Reported by reference", "Methods, Cohorts and scores, and the cited source publications [20 to 25]"],
 ["5", "Assay method, protocol, QC, scoring, blinding", "Reported by reference", "Methods, Cohorts and scores, and Online Resource 1 (platform, transformation); GSE81538 Ki-67 scoring in Methods, Registered test in GSE81538. Interlaboratory reproducibility was not assessed"],
 ["6", "Case selection, prospective or retrospective, period, median follow-up", "Partly", "Retrospective analysis of public data (Methods, Design and reporting). Accrual period and median follow-up come from the source publications and are not re-stated"],
 ["7", "Clinical endpoints", "Reported", "Methods, Patients whose label depends on the cut-off (PFI, DSS as death from breast cancer recorded in vital status, OS); overall survival in all three cohorts as a secondary common endpoint (Amendment 9)"],
 ["8", "Candidate variables considered", "Reported", "Cox models adjusted for age and stage or age, tumor size and nodal group; grade as sensitivity analysis (Methods)"],
 ["9", "Sample size rationale", "Reported", "No sample size calculation. Equivalence margin 0.67 to 1.50 fixed in advance; TCGA-BRCA contributed few events (12 in the discordant group)"],
 ["10", "Statistical methods, model assumptions, missing data", "Partly", "Methods; Online Resource 1 (frozen amendments). Patients with missing endpoint data were excluded (Online Resource 4, Table S1)"],
 ["11", "Pre-specified versus exploratory", "Reported", "Methods (post hoc discovery stated; resampling test and fourth-cohort predictions pre-specified); Table 4; Exploratory simulation; gene-disjoint scores and common endpoint (Amendments 8 and 9); Online Resource 4 (post hoc analyses labeled)"],
 ["12", "Flow of patients, numbers and events per subgroup", "Reported", "Online Resource 4, Table S1; Results, Cohorts; Table 1; hazard-ratio table with events in Online Resource 4"],
 ["13", "Demographics, prognostic variables, marker distribution, missing values", "Partly", "Table 1 gives cohort sizes, subtype shares and receptor status. Age and stage tabulations are not reproduced"],
 ["14", "Relation of marker to standard prognostic variables", "Not reported", "Not a focus of the study; grade is addressed only as a sensitivity covariate (Methods)"],
 ["15", "Univariable analysis with Kaplan-Meier", "Reported", "Fig. 3 (METABRIC, TCGA-BRCA); Online Resource 4, Fig. S2 (SCAN-B)"],
 ["16", "Multivariable analysis with estimates and confidence intervals", "Partly", "Hazard ratios for the group contrasts with 95% CI (Results; Online Resource 4). Coefficients of covariates are not tabulated"],
 ["17", "Marker with standard prognostic variables, regardless of significance", "Reported", "Primary Cox models include age and stage (or size and nodal group); grade-adjusted version reported"],
 ["18", "Further investigations: assumptions, sensitivity, validation", "Reported", "Fourth-cohort test; ER 2 to 3 sensitivity; single pathologist readings; simulations; bootstrap intervals (Results; Online Resource 4)"],
 ["19", "Interpretation, strengths and weaknesses", "Reported", "Discussion, including limitations paragraph"],
 ["20", "Implications for research and clinical value", "Reported", "Discussion, practical consequences and conclusion"],
]
s.append(tbl(["Item", "Recommendation", "Status", "Where reported or why not"], rem, [1.0*cm, 5.0*cm, 2.4*cm, 8.6*cm]))
s.append(Spacer(1, 6))
s.append(Paragraph("Status key: Reported, in the article or its Online Resources; Partly, some elements only; Not available, data not used; Not reported, not part of the study question.", SMALL))
build("ESM_2_REMARK-checklist", s, "Online Resource 2: REMARK checklist")

# =========================================================== ESM 3: literature
log("ESM 3")
s = head(3, "Literature review material",
         "Search logs, screening record, citation searching, extraction record, protocol deviations and the extracted values in Table 3. "
         "The protocol is registered at https://osf.io/pc9wm. The review is descriptive: fewer than the eight studies required by the protocol met the criteria for a formal regression.")
s.append(Paragraph("<b>Flow of records</b>", H2))
flow = [
 ["PubMed, two queries (A 178, B 32, overlap 27)", "183 unique records", "SEARCH-LOG.txt"],
 ["Europe PMC (not in MEDLINE, preprints excluded)", "0 additional records", "SEARCH-LOG.txt"],
 ["Excluded at title and abstract", "167", "SCREENING-TA_pubmed.md"],
 ["Read in full from the database search", "16", ""],
 ["Citation searching (forward round 1, 49; backward, 194 unique; forward round 2, 36)", "279 records", "Citation search logs"],
 ["Forwarded to full text from citation searching (Noske 2020, Holm 2021, Lundgren 2019, Thakur 2018); Lundgren 2019 and Thakur 2018 excluded", "4 read in full; 2 added", "Citation search logs"],
 ["Total read in full", "20", ""],
 ["Included", "7 studies, 1 provisional", "Table 3"],
]
s.append(tbl(["Stage", "Number", "Record"], flow, [9.5*cm, 4.5*cm, 3.0*cm]))
s.append(Paragraph("The counts in the Results of the article (183 records, 16 read in full, two studies added, seven included, one provisional) follow this table; all 20 reports read in full were assessed by both reviewers (see Second review). Figure S-L1 shows the flow. "
                   "Exclusion reasons: E1, cut-off derived from survival or recurrence only; E2, cut-off adopted from earlier work; E5, neoadjuvant or post-treatment Ki-67; "
                   "NR, not reported; NM, not a Ki-67 cut-off study. Individual reasons are in the screening record below and in the screening workbook.", SMALL))
s.append(Spacer(1, 6))
s.append(img(f"{FG}/FigS-L1_PRISMA-flow.png", 13.5))
s.append(Paragraph("<b>Fig. S-L1</b> Flow of records for the literature component (PRISMA 2020 layout). The database arm and the citation-searching arm are shown separately. Records in the citation arm were not de-duplicated across rounds, and only the backward round recorded the split of its exclusions. Viale 2019 and Ziegler 2024 are counted among the 167 database records excluded on title and abstract; citation searching re-surfaced them and they were read in full, with the exclusion confirmed. Exclusion categories are summarized from the screening records in this resource.", SMALL))
s.append(Paragraph("<b>Second review.</b> A second reviewer (S.M.E.), blind to the first-pass decisions, screened the titles and abstracts of all 183 records: 6 were forwarded by both reviewers, 10 by the first pass only and none by the second reviewer only (agreement 94.5%; Cohen's kappa 0.52). Both reviewers assessed the 16 forwarded records and the 2 records from citation searching in full text and agreed on 15 of 18 (kappa 0.67). The three disagreements were resolved by discussion. Holm 2021 was kept as provisionally eligible, because its Supplementary Methods (lines 85 to 89) describe a cut-off obtained by cross-validation against PAM50. Ingoldsby 2013 was excluded under criterion 5, because its 15% split predicts a continuous recurrence score and no high-risk share exists. Kim 2024 was excluded (E2), because the derivation of its 20% threshold is not described. Four further reports were read in full by the first pass and excluded: Lundgren 2019 and Thakur 2018, forwarded by citation searching, and Viale 2019 and Ziegler 2024, database records excluded on title and abstract that citation searching re-surfaced. S.M.E. later read these four in full text and confirmed all four exclusions (16 October 2026); they are not part of the agreement statistics above. A second person (R.A.A.) checked the extracted values of the included studies against the papers. The luminal B share of Holm 2021, missing in the first pass, was added from Table 2 of that paper (27.6% and 30.6%).", BODY))
for f, t in [("SEARCH-LOG.txt", "Search log"), ("AMENDMENT-LOG_systematic-review.txt", "Registration and amendment log"),
             ("2026-10-13_2140_DEVIATION-1_search-before-registration.txt", "Protocol deviation 1"),
             ("SCREENING-TA_pubmed.md", "Title and abstract screening record"),
             ("2026-10-13_2156_FULLTEXT-PASS1_first-pass-extraction.md", "Full-text first-pass extraction (first file)"),
             ("2026-10-13_2226_FULLTEXT-PASS1_first-pass-extraction.md", "Full-text first-pass extraction (second file)"),
             ("2026-10-13_2235_CITATION-SEARCH-LOG_round1.md", "Citation searching, round 1"),
             ("2026-10-13_2234_CITATION-SEARCH-LOG_round2-backward.md", "Citation searching, round 2 (backward)"),
             ("2026-10-13_2240_OSF-UPDATE-NOTE_feasibility-descriptive-route.txt", "Feasibility note: descriptive route")]:
    s.append(PageBreak()); s += verbatim(f"{L}/{f}", t)
s.append(PageBreak())
s.append(Paragraph("<b>Table S-L1. Values extracted from the published studies (as in Table 3 of the article)</b>", H2))
t3 = [
 ["R1", "Cheang 2009", "PAM50 (qRT-PCR)", "144", "41.7%", "Minimum total misclassification (P)", "13.25%"],
 ["R1", "Fernandez-Martinez 2017", "Prosigna", "517", "41.8%", "Youden (Y)", "14%"],
 ["R1", "Holm 2021 (provisional)", "PAM50", "561; 237", "27.6%; 30.6%", "Cross-validated optimum against PAM50; metric not stated, package default accuracy (P, probable)", "20%; 40%"],
 ["R1", "Dix-Peek 2023", "Prosigna", "378", "62.8%", "Maximum kappa over five candidates (P)", "25%"],
 ["R1", "Lopez-Tarruella 2024", "Prosigna", "1,029", "34.0%", "Youden (Y)", "13%"],
 ["R2", "Chen 2016", "21-gene or 70-gene assay", "71", "40.8%", "Maximum concordance (P); maximum positive likelihood ratio (other)", "25%; 20%"],
 ["R2", "Fernandez-Martinez 2017", "Prosigna ROR", "400; 117", "63.8%; 53.8%", "Youden (Y)", "12%; 15%"],
 ["R2", "Ceccarelli 2019", "Oncotype DX RS", "156", "5.2% or 9.0%", "ROC, rule not stated (U)", "25%"],
 ["R2", "Noske 2020", "EndoPredict score", "307", "54.4%", "ROC, rule not stated (U)", "20%"],
]
s.append(tbl(["Class", "Study", "Reference assay", "n", "LumB or higher-risk share", "Criterion (stratum)", "Optimum"], t3,
             [1.1*cm, 3.2*cm, 2.8*cm, 1.5*cm, 2.3*cm, 4.5*cm, 1.6*cm], merge_cols=(0,)))
s.append(Paragraph("P, prevalence-dependent; Y, Youden-type; U, criterion not stated; NR, not reported; ROR, risk of recurrence; RS, recurrence score. "
                   "Footnotes to this table appear under Table 3 of the article.", SMALL))
build("ESM_3_literature-review-material", s, "Online Resource 3: literature review material")

# =========================================================== ESM 4: results tables
log("ESM 4")
a3 = pd.read_csv(f"{R}/A3_agreement.csv"); sc = pd.read_csv(f"{R}/SCANB_results.csv")
s = head(4, "Full results tables and supplementary figures",
         "All numbers are from the analysis scripts and result files of the study. Percentile cut-offs are percentiles of the ER-positive, HER2-negative stratum. "
         "P2 is the 18-gene score without MKI67; P1 is MKI67. Analyses labeled post hoc were not specified in advance.")
# S1 attrition
at = pd.read_csv(f"{R}/attrition.csv")
rows = []; coh = "TCGA-BRCA"
for _, r in at.iterrows():
    if r.step == "---": coh = "METABRIC"; continue
    rows.append([coh, r.step, f"{int(r.n_remaining):,}", f"{int(r.n_dropped):,}"])
s.append(Paragraph("<b>Table S1. Patient attrition (TCGA-BRCA and METABRIC)</b>", H2))
s.append(tbl(["Cohort", "Step", "Remaining", "Dropped"], rows, [3*cm, 9*cm, 2.5*cm, 2.5*cm], merge_cols=(0,)))
s.append(Paragraph("SCAN-B (GSE96058): 136 technical replicates were excluded and the 2,425 ER-positive, HER2-negative tumors were analyzed as deposited (Table 1 of the article).", SMALL))

# S2 optima
opt = a3[a3.pct == -1]
rows = []
for _, r in opt.iterrows():
    rows.append([r.cohort, {"P1": "MKI67", "P2": "18-gene"}[r.score], f"{r.opt_pct:.0f}", f"{r.ci_lo:.0f} to {r.ci_hi:.0f}", f"{r.kappa:.3f}", f"{int(r.n_lum):,}"])
for scr in ["P2", "P1"]:
    o = sc[(sc.block == "A3") & (sc.score == scr)].iloc[0]
    rows.append(["SCAN-B", {"P1": "MKI67", "P2": "18-gene"}[scr], f"{o.val:.0f}", f"{o.lo:.0f} to {o.hi:.0f}", f"{o.kappa:.3f}", f"{int(o.n):,}"])
order_c = {"TCGA": 0, "METABRIC": 1, "SCAN-B": 2}
rows.sort(key=lambda r: (order_c[r[0]], r[1] != "18-gene"))
s.append(Paragraph("<b>Table S2. Kappa-optimal percentile cut-off with bootstrap interval</b>", H2))
s.append(tbl(["Cohort", "Score", "Optimal percentile", "95% CI (2,000 bootstraps)", "Peak kappa", "Luminal tumors"], rows,
             [3*cm, 2.5*cm, 2.8*cm, 3.6*cm, 2.3*cm, 2.8*cm], merge_cols=(0,)))
s.append(Paragraph("SCAN-B intervals are those of the registered run (Amendment 5).", SMALL))

# S3 sweep every 5
g = a3[a3.pct > 0].copy()
sg = sc[sc.block == "A3grid"].copy(); sg["pct"] = sg.key.astype(int); sg["cohort"] = "SCAN-B"; sg["kappa"] = sg.val
g = pd.concat([g[["cohort", "score", "pct", "kappa"]], sg[["cohort", "score", "pct", "kappa"]]])
pv_ = g[g.pct % 5 == 0].pivot_table(index="pct", columns=["cohort", "score"], values="kappa")
cols = [("TCGA", "P2"), ("TCGA", "P1"), ("METABRIC", "P2"), ("METABRIC", "P1"), ("SCAN-B", "P2"), ("SCAN-B", "P1")]
rows = [[f"{int(p)}"] + [f2(pv_.loc[p, c], 3) for c in cols] for p in pv_.index]
s.append(Paragraph("<b>Table S3. Cohen kappa against PAM50 by cut-off percentile (every fifth percentile; full grid in the result files)</b>", H2))
s.append(tbl(["Percentile", "TCGA 18-gene", "TCGA MKI67", "METABRIC 18-gene", "METABRIC MKI67", "SCAN-B 18-gene", "SCAN-B MKI67"], rows,
             [2.0*cm] + [2.5*cm]*6))

# S4 Youden scales
e1 = pd.read_csv(f"{R}/E1_youden_scales.csv")
rows = []
for _, r in e1.iterrows():
    rows.append([r.cohort, {"P1": "MKI67", "P2": "18-gene"}[r.score], f"{100*r.lumB_share:.1f}%",
                 f"{r.youden_pct_full:.0f} ({r.youden_pct_full_lo:.0f} to {r.youden_pct_full_hi:.0f})",
                 f"{r.youden_q_lumA:.0f} ({r.youden_q_lumA_lo:.0f} to {r.youden_q_lumA_hi:.0f})",
                 f"{r.youden_z_lumA:.2f} ({r.youden_z_lumA_lo:.2f} to {r.youden_z_lumA_hi:.2f})",
                 f"{r.kappa_pct_full:.0f}", f"{r.kappa_q_lumA:.0f}", f"{r.kappa_z_lumA:.2f}"])
rows.sort(key=lambda r: (order_c[r[0]], r[1] != "18-gene"))
s.append(Paragraph("<b>Table S4. Youden and kappa optima on three scales</b>", H2))
s.append(tbl(["Cohort", "Score", "LumB share", "Youden, percentile of stratum", "Youden, quantile of luminal A", "Youden, z vs luminal A", "Kappa, percentile", "Kappa, luminal A quantile", "Kappa, z"], rows,
             [2.0*cm, 1.6*cm, 1.5*cm, 2.4*cm, 2.4*cm, 2.6*cm, 1.4*cm, 1.7*cm, 1.4*cm], merge_cols=(0,)))
s.append(Paragraph("95% intervals in parentheses are from 2,000 bootstrap resamples. The luminal A quantile of the Youden boundary stays at 80 to 89 across cohorts and scores.", SMALL))

# S5 resampling
e3 = pd.read_csv(f"{R}/E3_prevalence_resampling.csv")
rows = []
for (c, scr), d in e3.groupby(["cohort", "score"], sort=False):
    d = d.sort_values("prev")
    for _, r in d.iterrows():
        rows.append([c, {"P1": "MKI67", "P2": "18-gene"}[scr], f"{int(r.prev)}%", f"{r.kappa_pct:.1f}", f"{r.youden_q_lumA:.1f}"])
rows.sort(key=lambda r: (order_c[r[0]], r[1] != "18-gene", int(r[2][:-1])))
s.append(Paragraph("<b>Table S5. Median optimum at imposed luminal B shares (200 resamples each)</b>", H2))
s.append(tbl(["Cohort", "Score", "Imposed LumB share", "Kappa optimum (percentile)", "Youden optimum (luminal A quantile)"], rows,
             [3*cm, 2.5*cm, 3.2*cm, 4*cm, 4.3*cm], merge_cols=(0, 1)))
s.append(Paragraph("Slopes of the median optimum on 100 minus the imposed share are in Table 2 of the article (kappa: 0.89 to 1.12; Youden on the luminal A scale: -0.02 to 0.02).", SMALL))

# S6 discordant zone
d = pd.read_csv(f"{R}/D_discordant_zone.csv")
names = {"D1_STABLE_A_vs_DISC": "Stable luminal A-like vs discordant (HR)", "D1_STABLE_B_vs_DISC": "Stable luminal B-like vs discordant (HR)",
         "D3_continuous_in_zone": "Continuous score inside the zone (HR per SD)", "D3b_continuous_whole_cohort": "Continuous score, whole stratum (HR per SD)",
         "D4_trend": "Trend across the three groups (HR per step)", "D5_zone_size": "Zone size (% of stratum)"}
rows = []
for _, r in d.iterrows():
    est = f"{r.hr:.1f}%" if r.test == "D5_zone_size" else ci(r.hr, r.lo, r.hi)
    rows.append([r.cohort, {"P1": "MKI67", "P2": "18-gene"}[r.score], names[r.test], f"{int(r.n):,}", f"{int(r.ev)}", est, pv(r.p)])
rows.sort(key=lambda r: (order_c[r[0]], r[1] != "18-gene"))
s.append(Paragraph("<b>Table S6. Prognostic contrasts around the discordant zone (TCGA-BRCA and METABRIC)</b>", H2))
s.append(tbl(["Cohort", "Score", "Contrast", "n", "Events", "Estimate (95% CI)", "P"], rows,
             [2.0*cm, 1.6*cm, 6.0*cm, 1.4*cm, 1.4*cm, 3.5*cm, 1.3*cm], merge_cols=(0, 1)))
s.append(Paragraph("Cox models with age and stage. TCGA-BRCA had 12 events in the discordant group. Zone definitions are in Amendment 2 (Online Resource 1). "
                   "Test D3 inside the zone was withdrawn as a confirmatory test (Error log 1); values are shown for completeness.", SMALL))

# S7 SCAN-B outcomes
lab = {"C1a": "Stable luminal A-like vs discordant", "C1b": "Stable luminal B-like vs discordant",
       "C1a_grade": "Stable luminal A-like vs discordant, grade added", "C1b_grade": "Stable luminal B-like vs discordant, grade added"}
rows = []
for scr in ["P2", "P1"]:
    for b in ["C1a", "C1b", "C1a_grade", "C1b_grade"]:
        r = sc[(sc.block == b) & (sc.score == scr)].iloc[0]
        rows.append([{"P1": "MKI67", "P2": "18-gene"}[scr], lab[b], f"{int(r.n):,}", f"{int(r.ev)}", ci(r.val, r.lo, r.hi), pv(r.p),
                     "inconclusive" if str(r.verdict) == "inconclusive" else ""])
s.append(Paragraph("<b>Table S7. SCAN-B overall survival, hazard ratios against the discordant group</b>", H2))
s.append(tbl(["Score", "Contrast", "n", "Events", "HR (95% CI)", "P", "Equivalence"], rows,
             [1.6*cm, 6.2*cm, 1.4*cm, 1.4*cm, 3.6*cm, 1.3*cm, 2.0*cm], merge_cols=(0,)))
rows = []
for scr in ["P2", "P1"]:
    pc = {k: sc[(sc.block == "C3") & (sc.score == scr) & (sc.key == k)].val.iloc[0] for k in sc[(sc.block == "C3") & (sc.score == scr)].key}
    rows.append([{"P1": "MKI67", "P2": "18-gene"}[scr],
                 f"{100*pc['pctKi67high_STABLE_A']:.1f}%", f"{100*pc['pctKi67high_DISCORDANT']:.1f}%", f"{100*pc['pctKi67high_STABLE_B']:.1f}%"])
s.append(Paragraph("<b>Table S8. SCAN-B routine pathology Ki-67 reported high, by group</b>", H2))
s.append(tbl(["Score", "Stable luminal A-like", "Discordant", "Stable luminal B-like"], rows, [3*cm, 4*cm, 4*cm, 4*cm]))
s.append(Paragraph("The main text gives the 18-gene grouping (31.5%, 69.8%, 84.2%; 1,140 patients with recorded status).", SMALL))

# S9 pooled
pc = pd.read_csv(f"{R}/pooled_C1.csv")
nm = {"C1a": "Stable luminal A-like vs discordant", "C1b": "Stable luminal B-like vs discordant"}
rows = []
for _, r in pc.iterrows():
    rows.append([{"P1": "MKI67", "P2": "18-gene"}[r.score], nm[r.test], r.set, r.method, ci(r.hr, r.lo, r.hi), f"{100*r.I2:.0f}%" if r.I2 <= 1 else f"{r.I2:.0f}%"])
s.append(Paragraph("<b>Table S9. Pooled hazard ratios, as specified in Amendment 4</b>", H2))
s.append(tbl(["Score", "Contrast", "Cohorts pooled", "Model", "HR (95% CI)", "I²"], rows,
             [1.6*cm, 5.0*cm, 3.2*cm, 1.6*cm, 4.0*cm, 1.4*cm], merge_cols=(0, 1, 2)))
s.append(Paragraph("The endpoints differ between cohorts (DSS, OS, PFI), so the pooled values are not an estimate of one quantity. "
                   "Verdicts recorded by the script for a pooled interval inside 0.67 to 1.50 are not interpreted in the article.", SMALL))

# S10 post hoc
s.append(Paragraph("<b>Table S10. Post hoc analyses (labeled as such in the article)</b>", H2))
s2 = pd.read_csv(f"{R}/S2_piecewise_slopes_POSTHOC.csv")
rows = [[r.cohort, {"P1": "MKI67", "P2": "18-gene"}[r.score], r.part, ci(r.hr, r.lo, r.hi), pv(r.p)] for _, r in s2.iterrows()]
s.append(tbl(["Cohort", "Score", "Segment", "HR per SD (95% CI)", "P"], rows, [3*cm, 2.5*cm, 3*cm, 5*cm, 2*cm], merge_cols=(0,)))
s.append(Paragraph("Piecewise slopes of the hazard on the score below and above the zone. The flattening above the zone in METABRIC (ratio of slopes 0.69) did not replicate in SCAN-B (Table S11).", SMALL))
rows = []
for scr in ["P2", "P1"]:
    b, a_, df = [sc[(sc.block == "C2") & (sc.score == scr) & (sc.key == k)].iloc[0] for k in ["below", "above", "diff"]]
    rows.append(["SCAN-B", {"P1": "MKI67", "P2": "18-gene"}[scr], ci(b.val, b.lo, b.hi), ci(a_.val, a_.lo, a_.hi), ci(df.val, df.lo, df.hi), pv(df.p)])
s.append(Paragraph("<b>Table S11. SCAN-B piecewise slopes (replication attempt of the METABRIC flattening)</b>", H2))
s.append(tbl(["Cohort", "Score", "HR below zone", "HR above zone", "Ratio above/below", "P"], rows, [2*cm, 2*cm, 4*cm, 4*cm, 4*cm, 1.4*cm]))

# S12 Amendment 7
s.append(PageBreak())
s.append(Paragraph("<b>Table S12. Amendment 7: pre-specified predictions in GSE81538 (405 tumors)</b>", H2))
pred = [["C1", "Consensus Ki-67: slope of median kappa-optimal percentile on 100 minus imposed share", "0.7 to 1.3", "0.62 (ER 2 to 3: 0.61)", "Not met"],
        ["C2", "Consensus Ki-67: slope of Youden cut-off on luminal A quantile scale", "-0.3 to 0.3", "0.00 (ER 2 to 3: -0.04)", "Met"],
        ["C3a", "18-gene score: kappa-optimal percentile within 5 points of 100 minus observed share", "within 5", "65 vs 63.4", "Met"],
        ["C3b", "18-gene score: Youden luminal A quantile, bootstrap CI overlaps 82 to 85", "overlap", "89 (95% CI 73 to 97)", "Met"]]
s.append(tbl(["Test", "Prediction", "Criterion", "Result", "Verdict"], pred, [1.1*cm, 8.2*cm, 2.2*cm, 3.8*cm, 1.7*cm]))
s.append(Paragraph("Decision rule fixed in advance: the mechanism counts as confirmed on immunohistochemistry only if C1 and C2 both hold. C1 did not hold. Registered verdict: not confirmed on immunohistochemistry. "
                   "Population: ER consensus 1 to 3, HER2 consensus 0, 256 tumors; PAM50 luminal 232 (147 luminal A, 85 luminal B; luminal B share 36.6%). The ER 2 to 3 sensitivity analysis has the same 232 luminal tumors. "
                   "Other PAM50 calls among eligible tumors: Normal 15, HER2-enriched 7, Basal 2.", SMALL))
a7 = pd.read_csv(f"{R}/A7_resampling.csv")
for an, label in [("primary", "Table S13. Consensus Ki-67 (K) by imposed luminal B share, primary analysis (ER 1 to 3)"),
                  ("sens", "Table S14. Same analysis, sensitivity (ER 2 to 3)")]:
    d_ = a7[(a7.analysis == an) & (a7.measure == "K")].sort_values("prev")
    rows = [[f"{int(r.prev)}%", f"{r.kappa_pct:.1f}", f"{r.kappa_thr_med:.0f} ({r.kappa_thr_lo:.0f} to {r.kappa_thr_hi:.0f})",
             f"{r.youden_q:.1f}", f"{r.youden_thr_med:.0f} ({r.youden_thr_lo:.0f} to {r.youden_thr_hi:.0f})"] for _, r in d_.iterrows()]
    s.append(Paragraph(f"<b>{label}</b>", H2))
    s.append(tbl(["Imposed share", "Kappa optimum (percentile)", "Kappa-optimal Ki-67, % (2.5 to 97.5%)", "Youden optimum (LumA quantile)", "Youden Ki-67, % (2.5 to 97.5%)"], rows,
                 [2.4*cm, 3.4*cm, 4.2*cm, 3.6*cm, 3.4*cm]))
rows = []
for m, nm_ in [("K", "Consensus"), ("K1", "Pathologist 1"), ("K2", "Pathologist 2"), ("K3", "Pathologist 3")]:
    d_ = a7[(a7.analysis == "primary") & (a7.measure == m)].sort_values("prev")
    x = 100 - d_.prev.values
    sl_k = np.polyfit(x, d_.kappa_pct.values, 1)[0]; sl_y = np.polyfit(x, d_.youden_q.values, 1)[0]
    rows.append([nm_, f"{sl_k:.2f}", f"{sl_y:.2f}"])
s.append(Paragraph("<b>Table S15. Slopes by reader (descriptive; the registered measure is the consensus)</b>", H2))
s.append(tbl(["Reading", "C1 slope (kappa optimum)", "C2 slope (Youden, LumA quantile)"], rows, [4*cm, 5.5*cm, 6*cm]))
s.append(Paragraph("Slopes are least-squares fits of the median optimum on 100 minus the imposed share over the seven shares; they reproduce the values in the article (0.62; 0.95, 0.86, 1.26).", SMALL))
s.append(Paragraph("<b>Table S16. Exploratory analyses after the registered result (no pre-specified criteria)</b>", H2))
ex = [["Bootstrap of the C1 slope, 300 patient-level resamples", "Median 0.67; 95% CI 0.54 to 1.57; 58% of resamples below 0.7"],
      ["Normal scores, separation 0.5 to 3 SD, shares 15% to 45%", "Slopes 0.96 to 1.04 at every separation"],
      ["Observed Ki-67 distributions resampled within subtype, N = 40,000", "Slope 0.54 (0.54 to 0.59 across seeds)"],
      ["Same, ties broken by random jitter", "Median slope 0.65 (0.54 to 1.22)"],
      ["Agreement at own optimum, consensus Ki-67 / MKI67 / 18-gene score", "Kappa 0.530 / 0.464 / 0.688"],
      ["Kappa-optimal percentile, 18-gene score; MKI67 (GSE81538)", "65th (CI 55 to 77); 61st (CI 43 to 81)"],
      ["Youden luminal A quantile, 18-gene score; MKI67 (GSE81538)", "89 (CI 73 to 97); 72 (CI 60 to 95)"]]
s.append(tbl(["Analysis", "Result"], ex, [8.2*cm, 8.8*cm]))
s.append(Paragraph("Source scripts: s11 (registered analysis), s12 and s14 (simulations), s15 (bootstrap interval). The consensus Ki-67 takes few distinct values (modal 10, 15, 20), which keeps the kappa-optimal threshold at 15% for imposed shares of 25% to 45%.", SMALL))

# S17 to S20: Amendments 8 and 9
log("ESM 4: Amendments 8 and 9")
a8 = pd.read_csv(f"{R}/A8_results.csv"); m8 = a8[a8.block == "main"]
CO = {"TCGA": "TCGA-BRCA", "METABRIC": "METABRIC", "SCAN-B": "SCAN-B", "GSE81538": "GSE81538"}
SN = {"P1": "P1 (MKI67)", "P2": "P2 (18 PAM50 genes)", "P3": "P3 (gene-disjoint, median)", "P3m": "P3m (gene-disjoint, mean)", "P4": "P4 (Hallmark G2M, disjoint)"}
rows = []
for c in ["TCGA", "METABRIC", "SCAN-B", "GSE81538"]:
    for sc_ in ["P1", "P2", "P3", "P3m", "P4"]:
        r = m8[(m8.cohort == c) & (m8.score == sc_)].iloc[0]
        rows.append([CO[c], SN[sc_], f"{r.target:.1f}", f"{int(r.kappa_opt_pct)} ({r.kappa_opt_pct_lo:.0f} to {r.kappa_opt_pct_hi:.0f})",
                     f"{r.peak_kappa:.3f} ({r.peak_kappa_lo:.3f} to {r.peak_kappa_hi:.3f})", f"{r.slope_kappa:.2f}", f"{(r.slope_youden if abs(r.slope_youden) >= 0.005 else 0.0):.2f}",
                     f"{r.youden_q_lumA:.0f} ({r.youden_q_lumA_lo:.0f} to {r.youden_q_lumA_hi:.0f})"])
s.append(PageBreak())
s.append(Paragraph("<b>Table S17. Amendment 8: gene-disjoint proliferation scores in four cohorts</b>", H2))
s.append(tbl(["Cohort", "Score", "Target (100 − LumB %)", "Kappa optimum, percentile (95% CI)", "Peak kappa (95% CI)", "Slope, kappa", "Slope, Youden", "Youden, LumA quantile (95% CI)"],
             rows, [1.8*cm, 2.8*cm, 1.5*cm, 2.5*cm, 2.7*cm, 1.3*cm, 1.4*cm, 3.0*cm], merge_cols=(0,)))
s.append(Paragraph("Registered verdict for P3: confirmed for a gene-disjoint score (criteria G1 to G3 met in TCGA-BRCA, METABRIC and SCAN-B; supporting criterion G4 met in GSE81538). "
                   "P3m and P4 met the same criteria. P1 and P2 were rerun through the same code and reproduce the registered optima. "
                   "Intervals are from 2,000 bootstrap resamples; slopes are of the median optimum over 200 resamples at each of seven luminal B shares. "
                   "Genes found: P3 119 or 120 of 120; P4 186 or 187 of 187 (missing: CKLF in METABRIC; H3F3A in SCAN-B and GSE81538; PTTG3P in GSE81538).", SMALL))
h2 = a8[a8.block == "H2"].pivot_table(index=["cohort", "score"], columns="stratum", values="spearman_vs_P2").reset_index()
rows = [[CO[r.cohort], SN[r.score], f"{r['ER+/HER2-']:.2f}", f"{r['LumA']:.2f}", f"{r['LumB']:.2f}"]
        for _, r in h2.sort_values(["cohort", "score"], key=lambda x: x.map({"TCGA": 0, "METABRIC": 1, "SCAN-B": 2, "GSE81538": 3, "P3": 0, "P3m": 1, "P4": 2})).iterrows()]
s.append(Paragraph("<b>Table S18. Spearman correlation of the gene-disjoint scores with P2</b>", H2))
s.append(tbl(["Cohort", "Score", "ER+/HER2− stratum", "Luminal A", "Luminal B"], rows, [2.6*cm, 4.6*cm, 3.2*cm, 3.2*cm, 3.2*cm], merge_cols=(0,)))
a9 = pd.read_csv(f"{R}/A9_overall_survival.csv")
TN = {"O1_STABLE_A_vs_DISC": "Stable luminal A-like vs discordant", "O1_STABLE_B_vs_DISC": "Stable luminal B-like vs discordant",
      "O3_continuous_in_zone": "Continuous score within discordant group (per SD)", "O3b_continuous_whole": "Continuous score, whole cohort (per SD)", "O4_trend": "Trend across three groups (per step)"}
rows = []
for c in ["TCGA", "METABRIC", "SCAN-B"]:
    for t_ in TN:
        r = a9[(a9.cohort == c) & (a9.score == "P2") & (a9.test == t_)].iloc[0]
        bh = "" if pd.isna(r.p_BH) else ("<0.001" if r.p_BH < 0.001 else f"{r.p_BH:.3f}")
        rows.append([CO[c], TN[t_], f"{r.hr:.2f} ({r.lo:.2f} to {r.hi:.2f})", f"{int(r.ev)}", ("<0.001" if r.p < 0.001 else f"{r.p:.3f}"), bh])
s.append(Paragraph("<b>Table S19. Amendment 9: overall survival in all three cohorts, 18-gene score (P2)</b>", H2))
s.append(tbl(["Cohort", "Contrast", "Hazard ratio (95% CI)", "Deaths", "p", "p, BH within cohort"], rows,
             [2.2*cm, 6.0*cm, 3.2*cm, 1.4*cm, 1.4*cm, 2.8*cm], merge_cols=(0,)))
s.append(Paragraph("Overall survival, death from any cause. Adjustment: age and stage group (TCGA-BRCA, METABRIC); age, tumor size and nodal group (SCAN-B). "
                   "SCAN-B group contrasts are the registered C1 estimates (Amendments 3 and 4), which already used overall survival. "
                   "Rule R1 of Amendment 2 (zone prognostically empty: p > 0.05 and CI within 0.67 to 1.50) is met in METABRIC and SCAN-B and not in TCGA-BRCA (7 deaths in the zone). "
                   "Results for P1 are in the result file A9_overall_survival.csv.", SMALL))
pl = pd.read_csv(f"{R}/A9_pooled.csv")
rows = [[r.score, "Stable A-like vs discordant" if r.test == "C1a" else "Stable B-like vs discordant", r.set, r.method,
         f"{r.hr:.2f} ({r.lo:.2f} to {r.hi:.2f})", f"{100*r.I2:.0f}%", r.verdict if isinstance(r.verdict, str) else ""] for _, r in pl.iterrows()]
s.append(Paragraph("<b>Table S20. Amendment 9: pooled overall survival</b>", H2))
s.append(tbl(["Score", "Contrast", "Pooled set", "Model", "Hazard ratio (95% CI)", "I²", "Registered reading"], rows,
             [1.1*cm, 3.4*cm, 3.0*cm, 1.4*cm, 2.8*cm, 1.0*cm, 4.3*cm], merge_cols=(0, 1)))
s.append(Paragraph("Primary pooled set: all three cohorts, fixed effect. Overall survival includes deaths from other causes; METABRIC (811 deaths) carries most of the weight. "
                   "This dilution pulls hazard ratios toward 1, which weakens the stable A-like contrast and makes an equivalence verdict for the stable B-like contrast easier to reach. "
                   "The registered primary results with their original endpoints (Tables S6, S7 and S9) are not replaced.", SMALL))

# S21: Amendment 10
log("ESM 4: Amendment 10")
reg = pd.read_csv(f"{R}/A10_results.csv"); reg["run"] = "Registered (ER field in 310 of 508)"
exp_ = pd.read_csv(f"{R}/A10_results_EXPLORATORY-ER-all508.csv"); exp_ = exp_[exp_.cohort == "GSE25066"]; exp_["run"] = "Exploratory, post hoc (ER field in all 508)"
rows = []
for _, r in pd.concat([reg[reg.cohort == "GSE25066"], exp_, reg[reg.cohort == "SMC2018"]]).iterrows():
    co = "GSE25066" if r.cohort == "GSE25066" else "SMC 2018"
    rows.append([f"{co}: {r.run if co == 'GSE25066' else 'secondary'} (n = {int(r.n_stratum)}; {int(r.n_lumA)} A, {int(r.n_lumB)} B)", r.score,
                 f"{r.target:.1f}", f"{int(r.kappa_opt_pct)}", f"{r.peak_kappa:.2f}", f"{r.slope_kappa:.2f}",
                 f"{(r.slope_youden if abs(r.slope_youden) >= 0.005 else 0.0):.2f}", f"{r.youden_q_lumA:.0f} ({r.youden_q_lo:.0f} to {r.youden_q_hi:.0f})"])
s.append(PageBreak())
s.append(Paragraph("<b>Table S21. Amendment 10: independent cohorts (GSE25066; SMC 2018)</b>", H2))
s.append(tbl(["Cohort and run", "Score", "Target (100 − LumB %)", "Kappa optimum, percentile", "Peak kappa", "Slope, kappa", "Slope, Youden", "Youden, LumA quantile (95% CI)"],
             rows, [4.3*cm, 1.3*cm, 1.6*cm, 1.8*cm, 1.4*cm, 1.4*cm, 1.4*cm, 3.0*cm], merge_cols=(0,)))
s.append(Paragraph("Registered verdict (GSE25066): NOT TESTED (underpowered); the ER field specified in Amendment 10 is present for 310 of 508 samples, leaving 38 luminal B tumors against a minimum of 60 (Error Log 4, Online Resource 1). "
                   "The exploratory rerun changes only the ER field and was run after the registered result was known; it has no confirmatory weight. "
                   "P2 uses 15 of 18 genes on the Affymetrix U133A array; P3 uses 118 of 120. SMC 2018 is secondary and descriptive. "
                   "Intervals from 2,000 bootstrap resamples; slopes from 200 resamples at each of seven luminal B shares.", SMALL))

# Post hoc: score units (Error Log 5)
s.append(Spacer(1, 8))
s.append(Paragraph("<b>Table S22. Post hoc (Error Log 5): kappa-optimal cut-off in score units</b>", H2))
_p1 = pd.read_csv("/home/claude/work/posthoc/PH1_scale_check.csv"); _p2 = pd.read_csv("/home/claude/work/posthoc/PH2_score_units_P2_P3.csv")
_lab = {"TCGA": "TCGA-BRCA", "METABRIC": "METABRIC", "SCAN-B": "SCAN-B", "GSE81538": "GSE81538"}
rows = []
for c in ["TCGA", "METABRIC", "SCAN-B", "GSE81538"]:
    for sc, nm in [("P2", "18-gene"), ("P1", "MKI67"), ("P3", "P3")]:
        src = _p1 if sc == "P1" else _p2
        r = src[(src.cohort == c) & (src.score == sc)]
        if r.empty: continue
        r = r.iloc[0]
        pct = r.kopt_pct_luminal; slp = r.slope_pct_luminal if sc == "P1" else r.slope_pct; sq = r.slope_qA_raw if sc == "P1" else r.slope_qA
        fx = r.fixed_cutoff_slope if sc == "P1" else r.fixed_slope; q15 = r.qA_at15 if sc == "P1" else r.qA_15; q45 = r.qA_at45 if sc == "P1" else r.qA_45
        exp_ = r.expected_luminal if sc == "P1" else r.expected
        rows.append([_lab[c], nm, f"{pct:.1f}", f"{exp_:.1f}", f"{r.kopt_qA:.1f}", f"{slp:.2f}", f"{fx:.2f}", f"{sq:.2f}", f"{q15:.0f} to {q45:.0f}"])
s.append(tbl(["Cohort", "Score", "κ optimum, percentile of luminal set", "100 minus luminal B share", "κ optimum, luminal A quantile", "Percentile slope", "Slope of a fixed cut-off", "Slope in score units", "Luminal A quantile at shares 15% to 45%"],
             rows, [2.0*cm, 1.4*cm, 2.0*cm, 1.8*cm, 1.8*cm, 1.5*cm, 1.6*cm, 1.6*cm, 2.3*cm], merge_cols=(0,)))
s.append(Paragraph("Not pre-specified. Resampling as in Amendment 6 (200 resamples at each of seven luminal B shares; seed 20261016); percentile slopes differ slightly from the registered values because the random draws differ. "
                   "The slope of a fixed cut-off is F_A(c) minus F_B(c) at the observed optimum c, the change in its percentile per point of luminal B share when c does not move. "
                   "Score-unit slopes express the kappa-optimal cut-off as a quantile of the full luminal A distribution. P3 computed with the Amendment 8 scoring functions unchanged. "
                   "Scripts ph1_scale_check.py and ph2_score_units_P3.py.", SMALL))

# Figures
s.append(PageBreak())
s.append(Paragraph("<b>Fig. S1</b> Hazard ratio by twentieth of the 18-gene score in METABRIC (post hoc, descriptive). Reference is the lowest twentieth; model adjusted for age. The shaded band is the discordant zone (59th to 74th percentile).", CAP))
s.append(img(f"{FG}/2026-10-14_1520_FigS1_gradient_by_twentieth_POSTHOC.png", 12.5))
s.append(Spacer(1, 10))
s.append(Paragraph("<b>Fig. S2</b> SCAN-B (GSE96058). Left: Cohen kappa against PAM50 by cut-off percentile; markers show the kappa-optimal cut-offs (18-gene score 71st percentile, kappa 0.724; MKI67 66th, kappa 0.609); shaded bands are the registered bootstrap intervals. Right: overall survival by the three groups defined with the 59th and 74th percentile cut-offs of the 18-gene score.", CAP))
t = Table([[img(f"{FG}/2026-10-14_1520_FigS_SCANB_agreement_sweep.png", 8.2), img(f"{FG}/2026-10-14_1520_FigS_SCANB_KM.png", 8.2)]], colWidths=[8.4*cm, 8.4*cm])
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
s.append(t)
build("ESM_4_results-tables-and-figures", s, "Online Resource 4: results tables and figures")
log("done")
