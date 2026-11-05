"""s31_online_resources_jce.py  Online Resources 1-4 as Word files for the Journal of Clinical Epidemiology submission
(same as s30 except the journal name and the article section names).
Runs the table and text code of s20_online_resources.py unchanged through a small layer that writes .docx instead of
PDF, updates the article title, journal and section cross-references, and adds the Amendment 11 records (Online
Resource 1) and tables (Online Resource 4). Usage: python3 s30_online_resources_docx.py <stamp YYYY-MM-DD_HHMM>"""
import os, re, sys, html, time, glob, textwrap
import numpy as np, pandas as pd
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, ".."))
STAMP = sys.argv[1]
OUTDIR = os.path.join(REPO, "online_resources_jce"); os.makedirs(OUTDIR, exist_ok=True)
BURG_HEX = "4E3D7A"; HEAD_HEX = "4E3D7A"; BAND_HEX = "F3F0F8"; RULE_HEX = "D9D5DE"; INK_HEX = "2B2B2B"; FONT = "Times New Roman"

# ------------------------------------------------------------------ layer replacing reportlab
class ParagraphStyle:
    def __init__(self, name, fontName="DV", fontSize=9, **kw):
        self.name, self.bold, self.size = name, fontName in ("DVB",), fontSize
        self.mono = fontName == "DVM"; self.color = kw.get("textColor")
class _Color:
    def __init__(self, h): self.h = h.lstrip("#")
class colors:
    white = _Color("#FFFFFF")
    @staticmethod
    def HexColor(h): return _Color(h)
cm = 1.0; A4 = (21.0, 29.7)
class Spacer:
    def __init__(self, *a): pass
class PageBreak: pass
class Paragraph:
    def __init__(self, text, style): self.text, self.style = text, style
class Preformatted:
    def __init__(self, text, style): self.text, self.style = text, style
class Image:
    def __init__(self, path, width=16, height=None): self.path, self.width = path, width
class TableStyle:
    def __init__(self, st): self.st = st
class Table:
    def __init__(self, data, colWidths=None, repeatRows=0): self.data, self.w = data, colWidths
    def setStyle(self, s): pass
class KeepTogether(list): pass
def SimpleDocTemplate(*a, **k): return None

def runs(par, text, size, bold=False, color=None, mono=False):
    text = text.replace("<br/>", "\n")
    for part in re.split(r"(<b>.*?</b>|<i>.*?</i>)", text, flags=re.S):
        if not part: continue
        b = part.startswith("<b>"); it = part.startswith("<i>")
        t = html.unescape(re.sub(r"</?[^>]+>", "", part))
        r = par.add_run(t); r.font.size = Pt(size); r.font.name = "Courier New" if mono else FONT
        r.bold = bold or b; r.italic = it
        if color: r.font.color.rgb = RGBColor.from_string(color)
def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcol); tcPr.append(sh)
def render(doc, items, cell=None):
    for it in items:
        if isinstance(it, (list, KeepTogether)): render(doc, it, cell); continue
        tgt = cell if cell is not None else doc
        if isinstance(it, Paragraph):
            st = it.style; p = tgt.add_paragraph(); p.paragraph_format.space_after = Pt(3)
            col = None
            if st.name in ("H1", "H2"): col = BURG_HEX
            if st.name == "CH": col = "FFFFFF"
            runs(p, it.text, {"H1": 14, "H2": 11}.get(st.name, min(st.size + 1.5, 10.5)), bold=st.bold, color=col)
            if st.name == "H2": p.paragraph_format.keep_with_next = True
        elif isinstance(it, Preformatted):
            for ln in it.text.split("\n"):
                p = tgt.add_paragraph(); p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
                runs(p, ln if ln else " ", 7.5, mono=True)
        elif isinstance(it, Image):
            p = tgt.add_paragraph(); p.add_run().add_picture(it.path, width=Cm(it.width))
        elif isinstance(it, PageBreak):
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif isinstance(it, Table):
            rows = it.data; ncol = max(len(r) for r in rows)
            ctext = lambda c: c.text if isinstance(c, Paragraph) else ("" if c is None else str(c))
            plain = lambda c: html.unescape(re.sub(r"</?[^>]+>", "", ctext(c).replace("<br/>", " "))).strip()
            T = [[plain(r[j]) if j < len(r) else "" for j in range(ncol)] for r in rows]
            GROUP_HDR = {"Cohort", "Cohort and run", "Cohort, score", "Class", "Date", "Score", "n", "Stage", "Contrast"}
            fill = [False] * ncol
            for j in (0, 1):
                fill[j] = j < ncol and T[0][j] in GROUP_HDR and (j == 0 or T[0][0] in GROUP_HDR)
            last1 = [T[0][1] and T[1][1] if len(T) > 1 else '']; repeated = [[False] * ncol for _ in T]; start = [True] * len(T)
            for i in range(1, len(T)):
                if fill[0] and T[i][0] == "" and not all(c == "" for c in T[i]):
                    T[i][0] = T[i-1][0]; repeated[i][0] = True; start[i] = False
                    if fill[1] and T[i][1] == "" and last1[0]: T[i][1] = last1[0]; repeated[i][1] = True
                if fill[1] and T[i][1] != "" and not repeated[i][1]: last1[0] = T[i][1]
                if start[i]: last1[0] = T[i][1] if fill[1] else ""
            numre = re.compile(r"^[\u2212\-+<>\u2264\u2265~]?\s?\d[\d,]*\.?\d*\s?%?(\s?[(\[].*[)\]])?$")
            isnum = [sum(bool(numre.match(T[i][j])) for i in range(1, len(T)) if T[i][j]) >= 0.6 * max(1, sum(1 for i in range(1, len(T)) if T[i][j])) for j in range(ncol)]
            t = doc.add_table(rows=len(rows), cols=ncol); t.autofit = False
            tblPr = t._tbl.tblPr; bd = OxmlElement("w:tblBorders")
            for side, sz, col in (("top", 12, INK_HEX), ("bottom", 12, INK_HEX), ("insideH", 4, RULE_HEX)):
                e = OxmlElement("w:" + side); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz)); e.set(qn("w:space"), "0"); e.set(qn("w:color"), col); bd.append(e)
            tblPr.append(bd)
            cm = OxmlElement("w:tblCellMar")
            for side, w in (("top", 45), ("left", 80), ("bottom", 45), ("right", 80)):
                e = OxmlElement("w:" + side); e.set(qn("w:w"), str(w)); e.set(qn("w:type"), "dxa"); cm.append(e)
            tblPr.append(cm)
            grp = 0
            for i, r in enumerate(rows):
                row = t.rows[i]; trPr = row._tr.get_or_add_trPr()
                cs = OxmlElement("w:cantSplit"); trPr.append(cs)
                if i == 0: th = OxmlElement("w:tblHeader"); trPr.append(th)
                if i > 0 and start[i] and fill[0]: grp += 1
                for j in range(ncol):
                    c = r[j] if j < len(r) else None; ce = t.cell(i, j); ce.paragraphs[0].text = ""
                    par = ce.paragraphs[0]; par.paragraph_format.space_after = Pt(0); par.paragraph_format.space_before = Pt(0)
                    if isinstance(c, Image):
                        par.add_run().add_picture(c.path, width=Cm(c.width)); continue
                    if i == 0:
                        runs(par, ctext(c), 8.5, bold=True, color="FFFFFF"); shade(ce, HEAD_HEX)
                    else:
                        bold = bool(isinstance(c, Paragraph) and c.style.bold) or (j == 0 and fill[0] and start[i])
                        if not repeated[i][j]: runs(par, ctext(c), 8.5, bold=bold)
                        if (grp % 2 == 1 and fill[0]) or (not fill[0] and i % 2 == 0): shade(ce, BAND_HEX)
                    if isnum[j] or (i == 0 and isnum[j]): par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    if i > 0 and start[i] and fill[0] and i > 1:
                        tcPr = ce._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders"); e = OxmlElement("w:top")
                        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "8"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "6B6B6B"); b.append(e); tcPr.append(b)
            from docx.enum.table import WD_ALIGN_VERTICAL
            for j in (0, 1):
                i = 1
                while i < len(T):
                    if repeated[i][j]:
                        k = i - 1
                        while i < len(T) and repeated[i][j]: i += 1
                        m = t.cell(k, j).merge(t.cell(i - 1, j))
                        for pp in list(m.paragraphs)[1:]:
                            if not pp.text.strip(): pp._p.getparent().remove(pp._p)
                        m.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                    else: i += 1
            if it.w:
                for j, w in enumerate(it.w[:ncol]):
                    t.columns[j].width = Cm(w)
                    for rr in t.rows: rr.cells[j].width = Cm(w)
                lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
            sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(4)
def build(name, story, title):
    d = docx.Document(); s = d.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    for a in ("left_margin", "right_margin"): setattr(s, a, Cm(2))
    s.top_margin = s.bottom_margin = Cm(1.8)
    st = d.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(10)
    fp = s.footer.paragraphs[0]; fp.text = title + "    Page "
    fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); r = OxmlElement("w:r"); t = OxmlElement("w:t")
    t.text = "1"; r.append(t); fld.append(r); fp._p.append(fld)
    for rr in fp.runs: rr.font.size = Pt(8)
    render(d, story)
    p = os.path.join(OUTDIR, f"{STAMP}_{name}.docx"); d.save(p); print("wrote", p); return p

# ------------------------------------------------------------------ load and adapt s20
src = open(os.path.join(HERE, "s20_online_resources.py"), encoding="utf-8").read()
cut = src.index("STAMP = sys.argv[1]")
body = src[cut:]
body = body.replace('STAMP = sys.argv[1] if len(sys.argv) > 1 else time.strftime("%Y-%m-%d_%H%M")', "")
body = body.replace('W = "/home/claude/work"', f'W = "{REPO}"')
body = body.replace('"/home/claude/work/posthoc/', f'"{REPO}/posthoc/')
body = re.sub(r'OUT = f"\{W\}/online_resources"; os.makedirs\(OUT, exist_ok=True\)', "OUT = OUTDIR", body)
body = re.sub(r"fd = os\.path\.join.*?pdfmetrics\.registerFontFamily\([^\n]*\n", "", body, flags=re.S)
body = re.sub(r"\ndef footer\(title\):.*?return f\n", "\n", body, flags=re.S)
body = re.sub(r"\ndef build\(name, story, title\):.*?return p\n", "\n", body, flags=re.S)
body = re.sub(r"\ndef img\(path, width_cm=16\.0\):.*?return Image\([^\n]*\n", "\ndef img(path, width_cm=16.0):\n    return Image(path, width=width_cm)\n", body, flags=re.S)
NEWTITLE = ("Case mix of the derivation series and Ki-67 cut-offs for luminal A versus luminal B breast cancer: "
            "a predictive model and a correction")
body = re.sub(r'TITLE = \(".*?"\)', f'TITLE = ("{NEWTITLE}")', body, flags=re.S)
body = body.replace("Journal: Breast Cancer.", "Journal: Journal of Clinical Epidemiology.")
SECT = [("Materials and Methods, Cut-off sweep and case mix, and Registered test in GSE81538 (C1 to C3)",
         "Methods, Derivation criteria and scale, Resampling design and outcomes, Binormal model, and Additional analyses"),
        ("Materials and Methods, Cohorts and scores", "Methods, Cohorts and scores"),
        ("Materials and Methods, Registered test in GSE81538", "Methods, Additional analyses"),
        ("Materials and Methods, Patients whose label depends on the cut-off", "Methods, Additional analyses"),
        ("Materials and Methods, Design and reporting", "Methods, Design and registration"),
        ("Materials and Methods;", "Methods;"),
        ("Materials and Methods)", "Methods)"),
        ("Results, Cohorts", "Results, Agreement-optimal cut-offs"),
        ("agree within 0.02 with Table S22 (0.20 to 0.37), the values reported in the article.",
         "agree within 0.02 with Table S22 (0.20 to 0.37). The article now reports the Amendment 11 slopes over shares of 15% to 65% (Table S25), which are steeper above a share of 45%.")]
for a, b in SECT:
    n = body.count(a); assert n >= 1, a; body = body.replace(a, b)

# Online Resource 1: Amendment 11 rows in the timeline and its documents
A11ROWS = '''
tl += [
 ["3 Nov 2026", "18:03; frozen 18:05", "Amendment 11 and frozen script", "All earlier results known; cohort files opened only for column names and first rows; script run only on permuted labels and synthetic data; posted 18:41 in osf.io/cwkd9; registered 18:55 (osf.io/vhg4s); run 18:56", "…1805_AMENDMENT-11_…_FROZEN.txt; …1805_s27_amendment11_FROZEN.py"],
 ["", "19:04", "Error Log 6", "GSE81538 series matrix had no recorded MD5; identity checked by Amendment 7 counts; wrapper script s28 hashed before the Ki-67 arm was run (19:05)", "…1904_ERROR-LOG-6_A11-Ki67-arm-identity-check-and-wrapper.txt"],
]
'''
body = body.replace('s.append(tbl(["Date", "Time", "Document", "State of knowledge when frozen", "File"], tl,', A11ROWS + 's.append(tbl(["Date", "Time", "Document", "State of knowledge when frozen", "File"], tl,')
body = body.replace(
    '"(https://osf.io/db7a8; the first registration version attached the pre-freeze draft by mistake, corrected in an update).", BODY))',
    '"(https://osf.io/db7a8; the first registration version attached the pre-freeze draft by mistake, corrected in an update). "\n'
    '    "Amendment 11 was written on 3 November 2026 after all earlier results were known, frozen with its analysis script at 18:05, posted in osf.io/cwkd9 at 18:41, "\n'
    '    "registered at 18:55 (https://osf.io/vhg4s) and run at 18:56; its conditional Ki-67 arm was run at 19:05 after Error Log 6 was recorded.", BODY))')
A11DOCS = ["2026-11-03_1805_AMENDMENT-11_cutoff-variation-criteria-relabelling-model_FROZEN.txt",
           "2026-11-03_1805_FREEZE-RECORD_AMENDMENT-11_sha256.txt", "2026-11-03_1856_POSTING-RECORD_AMENDMENT-11.txt",
           "2026-11-03_1904_ERROR-LOG-6_A11-Ki67-arm-identity-check-and-wrapper.txt"]
body = body.replace('"2026-10-16_1153_ERROR-LOG-5_percentile-scale-and-denominator.txt"]',
                    '"2026-10-16_1153_ERROR-LOG-5_percentile-scale-and-denominator.txt"] + ' + repr(A11DOCS))

# Online Resource 4: Amendment 11 tables before the supplementary figures
A11TABLES = r'''
o5 = pd.read_csv(f"{R}/A11_O5_model_check.csv"); o23 = pd.read_csv(f"{R}/A11_O2_O3.csv"); o4 = pd.read_csv(f"{R}/A11_O4_relabelling.csv")
k23 = pd.read_csv(f"{R}/A11K_O2_O3.csv"); kmed = pd.read_csv(f"{R}/A11K_medians.csv"); ktg = pd.read_csv(f"{R}/A11K_target_optima.csv")
RN = {"K": "Kappa", "ACC": "Accuracy", "PM": "Proportion matching", "YJ": "Youden", "BK": "50:50-weighted kappa", "SK": "Target-weighted kappa"}
SN = {"P2": "18-gene", "P1": "MKI67"}
s.append(PageBreak())
s.append(Paragraph("<b>Table S25. Amendment 11 (O1, O5): case-mix slope of the derived cut-off and the binormal model</b>", H2))
CO = {"TCGA-BRCA": 0, "METABRIC": 1, "SCAN-B": 2}; SO = {"P2": 0, "P1": 1}; RO = {"K": 0, "ACC": 1, "PM": 2, "YJ": 3, "SK": 4, "BK": 5}
def g2(v, n=2): return f2(v, n).replace("-0.00", "0.00").replace("-0.0", "0.0") if f2(v, n) in ("-0.00", "-0.0") else f2(v, n)
o5 = o5.assign(_c=o5.cohort.map(CO), _s=o5.score.map(SO), _r=o5.rule.map(RO)).sort_values(["_c", "_s", "_r"])
rows = [[r.cohort, SN[r.score], RN[r.rule], g2(r.slope_qA_per_point), g2(r.slope_model), g2(r.abs_diff)] for r in o5.itertuples()]
s.append(tbl(["Cohort", "Score", "Criterion", "Resampled slope", "Model slope", "Difference"], rows, [2.6*cm, 1.8*cm, 3.6*cm, 2.6*cm, 2.4*cm, 2.2*cm], merge_cols=(0, 1)))
s.append(Paragraph("Slope: change in the median derived cut-off, in luminal A quantile points, per point of luminal B share over 15% to 65% (derivation sets of 1,000 tumors; 500 resamples per share; seed 20261103). Registered criterion: for the 18-gene score, difference <= 0.10 for kappa and accuracy in all three cohorts (met). The 50:50-weighted kappa selected the same cut-off as the Youden index in 99.53% of derivations. Script s27_amendment11.py.", SMALL))
s.append(Paragraph("<b>Table S26. Amendment 11 (O2, O3): case mix against sampling, and transfer to the full cohort, all sizes</b>", H2))
rows = []
o23 = o23[o23.rule != "BK"]
o23 = o23.assign(_c=o23.cohort.map(CO), _s=o23.score.map(SO), _r=o23.rule.map(RO)).sort_values(["_c", "_s", "n", "_r"])
for r in o23.itertuples():
    rows.append([f"{r.cohort}, {SN[r.score]}", f"{r.n:,}", RN[r.rule], g2(r.sd_sampling, 1), g2(r.sd_casemix, 1), g2(r.frac_casemix), g2(r.bias, 1), g2(r.rmse, 1), g2(r.label_diff_pct, 1), f"{r.kappa_target_mean:.3f} ({r.kappa_target_opt:.3f})"])
s.append(tbl(["Cohort, score", "n", "Criterion", "SD sampling", "SD case mix", "Case-mix share", "Bias", "RMSE", "Relabelled (%)", "Kappa, mean (full-set optimum)"], rows, [2.4*cm, 1.1*cm, 2.9*cm, 1.4*cm, 1.4*cm, 1.4*cm, 1.3*cm, 1.3*cm, 1.6*cm, 2.2*cm], merge_cols=(0, 1)))
s.append(Paragraph("Shares 25% to 65%. SD and bias in luminal A quantile points; total variance is the sum of the sampling and case-mix variances. The 50:50-weighted kappa is omitted because it selected the same cut-off as the Youden index. Bias and RMSE are against the same criterion applied to the full cohort luminal set; relabelled is the mean percentage of full-set luminal tumors labeled differently from that cut-off; kappa is against PAM50 in the full set. TCGA-BRCA cells at n = 1,000 and shares of 45% or more repeat luminal B tumors heavily.", SMALL))
s.append(Paragraph("<b>Table S27. Amendment 11 (O4): patients relabelled between kappa cut-offs derived at 25% and 65% luminal B</b>", H2))
o4 = o4.assign(_c=o4.cohort.map(CO), _s=o4.score.map(SO)).sort_values(["_c", "_s"])
rows = [[r.cohort, SN[r.score], f"{r.t_pi25:.2f}", f"{r.t_pi65:.2f}", f"{r.n_stratum_relabelled:,} of {r.n_stratum:,}", f2(r.pct_stratum_relabelled, 1), f2(r.pct_luminal_relabelled, 1), "" if pd.isna(r.pct_chemo_among_relabelled) else f2(r.pct_chemo_among_relabelled, 1)] for r in o4.itertuples()]
s.append(tbl(["Cohort", "Score", "Cut-off at 25% (score)", "Cut-off at 65% (score)", "Relabelled, n", "Relabelled, % of stratum", "Relabelled, % of luminal", "Chemotherapy among relabelled (%)"], rows, None, merge_cols=(0,)))
s.append(Paragraph("Median thresholds from derivation sets of 1,000 tumors, in standardized score units. Chemotherapy is shown where recorded as received or not in the cohort file used (SCAN-B).", SMALL))
s.append(Paragraph("<b>Table S28. Amendment 11, Ki-67 arm (GSE81538, consensus Ki-67): derived thresholds and transfer</b>", H2))
rows = []
for r in ["K", "ACC", "PM", "YJ", "SK"]:
    g = kmed[(kmed.n == 232) & (kmed.rule == r)].sort_values("pi")
    rows.append([RN[r]] + [f"{v:.0f}" for v in g.t])
s.append(tbl(["Criterion", "15%", "25%", "35%", "45%", "55%", "65%"], rows, [4.2*cm] + [1.8*cm]*6))
s.append(Paragraph("Median derived consensus Ki-67 threshold (%) by imposed luminal B share, derivation sets of 232 tumors (147 luminal A and 85 luminal B tumors resampled within subtype, 500 times per share). Full-set optima: kappa, accuracy and Youden 15% (kappa 0.530); proportion matching 20%.", SMALL))
k23 = k23[k23.rule != "BK"].assign(_r=lambda x: x.rule.map(RO)).sort_values(["n", "_r"])
rows = [[f"{r.n:,}", RN[r.rule], g2(r.frac_casemix), g2(r.rmse, 1), g2(r.label_diff_pct, 1), f2(r.kappa_target_mean, 3)] for r in k23.itertuples()]
s.append(tbl(["n", "Criterion", "Case-mix share", "RMSE", "Relabelled (%)", "Kappa (mean)"], rows, [1.6*cm, 4.4*cm, 2.6*cm, 2.0*cm, 2.6*cm, 2.4*cm], merge_cols=(0,)))
s.append(Paragraph("Identity of the series matrix was confirmed by reproducing the Amendment 7 counts (Error Log 6). Script s28_amendment11_ki67_arm.py, importing s27 unchanged.", SMALL))
'''
body = body.replace("# Figures\ns.append(PageBreak())", A11TABLES + "\n# Figures\ns.append(PageBreak())")
body = body.replace('s += verbatim(f"{L}/{f}", t)',
    's += verbatim(f"{L}/{f}" if os.path.exists(f"{L}/{f}") else f"{L}/recovered/{f}", t)')
assert "Table S25" in body and "Amendment 11 and frozen script" in body
exec(compile(body, "s20_adapted", "exec"))
