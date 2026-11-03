"""Prepare manuscript JSON: number citations, extract Tables 1 and 3 from the submitted manuscript, build Tables 2 and 4
from result files. Output: ms.json for build_docx.js."""
import re, json, sys
import docx, pandas as pd
sys.path.insert(0, "/home/claude/work/ms")
import content as C

OLD = "/mnt/user-data/attachments/a7b57c6a-e976-5695-9c98-df16e019d7c0/f47d454d-02_Manuscript.docx"
R = "/home/claude/work/repo/results"
OLDKEYS = ["goldhirsch2011", "goldhirsch2013", "coates2015", "cheang2009", "prat2013", "nielsen2021", "fernandez2017",
           "lopez2024", "dixpeek2023", "abusneina2026", "dowsett2011", "polley2013", "feinstein1990", "byrt1993",
           "leeflang2013", "youden1950", "brenner1997", "metz1978", "remark2006", "hoadley2018", "curtis2012",
           "pereira2016", "cerami2012", "brueffer2018", "parker2009", "liu2018", "dersimonian1986", "venet2011",
           "liberzon2015", "hatzis2011", "kan2018", "osfprotocol", "chen2016", "ceccarelli2019", "noske2020", "holm2021",
           "maisonneuve2014", "lundgren2019", "fluss2005", "altman1994"]

d = docx.Document(OLD)
paras = [p.text for p in d.paragraphs]
i0 = paras.index("References"); refs_old = {}
for t in paras[i0 + 1:]:
    m = re.match(r"^(\d+)\.\s+(.*)$", t)
    if m: refs_old[int(m.group(1))] = m.group(2)
    if t.startswith("Figure legends"): break
assert len(refs_old) == 40, len(refs_old)
REF = {k: refs_old[i + 1] for i, k in enumerate(OLDKEYS)}

order = []
def number(text):
    def rep(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        nums = []
        for k in keys:
            assert k in REF, k
            if k not in order: order.append(k)
            nums.append(order.index(k) + 1)
        nums = sorted(set(nums)); out = []; j = 0
        while j < len(nums):
            k = j
            while k + 1 < len(nums) and nums[k + 1] == nums[k] + 1: k += 1
            out.append(f"{nums[j]}" if k == j else (f"{nums[j]}, {nums[k]}" if k == j + 1 else f"{nums[j]}-{nums[k]}"))
            j = k + 1
        return "[" + ", ".join(out) + "]"
    return re.sub(r"\[(@[^\]]+)\]", rep, text)

body = [(t, number(x)) for t, x in C.BODY]

# ---- Tables 1 and 3 from the submitted manuscript
def tab(t): return [[c.text for c in r.cells] for r in t.rows]
T1, T3 = tab(d.tables[0]), tab(d.tables[2])
oldnum = {i + 1: k for i, k in enumerate(OLDKEYS)}
def renum_cell(s):
    def rep(m):
        k = oldnum[int(m.group(1))]
        if k not in order: order.append(k)
        return f"[{order.index(k) + 1}]"
    return re.sub(r"\[(\d+)\]", rep, s)
T3 = [[renum_cell(c) for c in r] for r in T3]

# ---- Table 2 from A11 outputs
o5 = pd.read_csv(f"{R}/A11_O5_model_check.csv")
coh = ["TCGA-BRCA", "METABRIC", "SCAN-B"]; rl = [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion matching"), ("YJ", "Youden")]
T2 = [["Score", "Criterion"] + [f"{c} resampled" if j == 0 else f"{c} model" for c in coh for j in (0, 1)]]
T2 = [["Score", "Criterion", "TCGA-BRCA", "", "METABRIC", "", "SCAN-B", ""],
      ["", "", "Resampled", "Model", "Resampled", "Model", "Resampled", "Model"]]
for s, sl in [("P2", "18-gene"), ("P1", "MKI67")]:
    for r, lab in rl:
        row = [sl if r == "K" else "", lab]
        for c in coh:
            g = o5[(o5.cohort == c) & (o5.score == s) & (o5.rule == r)].iloc[0]
            f2=lambda v:(f"{v:.2f}".replace("-0.00","0.00")).replace("-","−")
            row += [f2(g.slope_qA_per_point), f2(g.slope_model)]
        T2.append(row)

# ---- Table 4 from A11 outputs
o = pd.read_csv(f"{R}/A11_O2_O3.csv"); k = pd.read_csv(f"{R}/A11K_O2_O3.csv")
rl4 = [("K", "Kappa"), ("ACC", "Accuracy"), ("PM", "Proportion matching"), ("YJ", "Youden"), ("SK", "Target-weighted kappa")]
T4 = [["Set", "Criterion", "Case-mix share", "RMSE", "Relabelled (%)", "Kappa"]]
def add(df, name):
    for r, lab in rl4:
        g = df[df.rule == r].iloc[0]
        kap = f"{g.kappa_target_mean:.3f}" + (f" ({g.kappa_target_opt:.3f})" if r == "K" else "")
        T4.append([name if r == "K" else "", lab, f"{g.frac_casemix:.2f}", f"{g.rmse:.1f}", f"{g.label_diff_pct:.1f}", kap])
for c in coh: add(o[(o.cohort == c) & (o.score == "P2") & (o.n == 400)], c)
add(k[k.n == 232], "GSE81538, Ki-67")

# ---- legends: renumber nothing (no citations)
refs = [f"{i + 1}. {REF[kk]}" for i, kk in enumerate(order)]
unused = [kk for kk in OLDKEYS if kk not in order]
print("references", len(refs), "unused", unused)

def wc(s): return len(re.findall(r"\S+", s))
main_words = sum(wc(x) for t, x in body if t == "p")
print("abstract words", wc(C.ABSTRACT), "main text words", main_words, "title chars", len(C.TITLE))
json.dump(dict(title=C.TITLE, running=C.RUNNING, abstract=C.ABSTRACT, keywords=C.KEYWORDS, body=body, ack=C.ACK,
               statements=C.STATEMENTS, refs=refs, legends=C.LEGENDS, tables={"1": T1, "2": T2, "3": T3, "4": T4},
               ttitles=C.TABLE_TITLES, tnotes=C.TABLE_NOTES, counts=dict(abstract=wc(C.ABSTRACT), main=main_words,
               refs=len(refs))), open("/home/claude/work/ms/ms.json", "w"), indent=1)
