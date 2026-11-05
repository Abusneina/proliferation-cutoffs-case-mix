// Cover letter and highlights for the Journal of Clinical Epidemiology (A4).
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, ImageRun, LevelFormat } = require("docx");
const [outLetter, outHi, mainWords] = process.argv.slice(2);
const FONT = "Times New Roman", SZ = 22;
const P = (t, o = {}) => new Paragraph({ spacing: { after: 110, line: 264 }, ...o,
  children: (Array.isArray(t) ? t : [t]).map(x => typeof x === "string" ? new TextRun({ text: x, font: FONT, size: SZ }) : x) });
const B = (t) => new TextRun({ text: t, font: FONT, size: SZ, bold: true });
const I = (t) => new TextRun({ text: t, font: FONT, size: SZ, italics: true });
const tight = { spacing: { after: 0, line: 264 } };
const sig = fs.readFileSync("/mnt/user-data/attachments/a7b57c6a-e976-5695-9c98-df16e019d7c0/acf6bd14-image.png");
const letter = [
  P([B("Abdelmuhsen M. Abusneina")], tight),
  P("Department of Molecular Diagnostics, Faculty of Biomedical Sciences", tight),
  P("University of Benghazi, Fourth Ring Road, Benghazi, Libya", tight),
  P("abdelmuhsen.abusneina@uob.edu.ly | +218 91 420 0539 | ORCID 0000-0001-9909-5588"),
  P("November 5, 2026"),
  P("The Editors", tight), P([I("Journal of Clinical Epidemiology")]),
  P([B("Re: Submission of an Original Research article")], tight),
  P([I("Case mix of the derivation series and Ki-67 cut-offs for luminal A versus luminal B breast cancer: a predictive model and a correction")]),
  P("Dear Editors,"),
  P(["I submit the enclosed Original Research article for consideration in the ", I("Journal of Clinical Epidemiology"), ". The work has not been published and is not under consideration elsewhere."]),
  P("Many diagnostic cut-offs are chosen to maximize agreement with a reference standard, through kappa, accuracy or matched proportions, and these criteria depend on the prevalence of the target condition in the derivation series. The principle is well known, but its size, its share of the variation in derived cut-offs, and a practical correction have rarely been measured for a cut-off that changes treatment. The manuscript does this for the Ki-67 cut-off that separates luminal A from luminal B breast cancer and guides adjuvant chemotherapy, where published values range from 13% to 25%."),
  P("In three public cohorts (4,395 tumors) in which the score and the PAM50 reference come from the same RNA profile, cut-offs derived by six criteria in resampled derivation sets moved by 0.36 to 0.39 luminal A quantile points per point of luminal B share. A binormal model predicted the shift within 0.09, meeting a registered criterion. At 400 tumors, case mix explained 54% to 65% of the variance of kappa-derived cut-offs, more than sampling did; cut-offs derived at the two ends of the published range of case mix relabeled 16% to 18% of patients; and reweighting the derivation set to the target prevalence reduced transfer error from 6.3-10.6 to 3.2-3.9 quantile points. On pathologist-scored Ki-67, the minimum-misclassification optimum moved from 25% to 10%."),
  P("The contribution is methodological: it quantifies a known source of bias in cut-off derivation, separates it from sampling variation, offers a predictive model and a correction, and ends with reporting rules that apply to any cut-off derived against a reference standard. The protocol and every amendment were registered on the Open Science Framework before the analyses they specify were run (most recently osf.io/vhg4s), and the code and records are archived at https://doi.org/10.5281/zenodo.23926714."),
  P(`The main text has ${mainWords} words, excluding the abstract and references. Reporting follows the REMARK guideline, and the completed checklist is provided as Online Resource 2. No preprint has been posted.`),
  P("Thank you for considering this manuscript."),
  P("Sincerely,", { spacing: { after: 60 } }),
  new Paragraph({ children: [new ImageRun({ type: "png", data: sig, transformation: { width: 130, height: 73 } })] }),
  P([B("Abdelmuhsen M. Abusneina, PhD")], tight),
  P("Associate Professor of Molecular Oncology and Cancer Metabolism", tight),
  P("Faculty of Biomedical Sciences, University of Benghazi, Libya", tight),
];
const page = { size: { width: 11906, height: 16838 }, margin: { top: 900, bottom: 850, left: 1300, right: 1300 } };
const H = fs.readFileSync("/home/claude/work/ms/highlights.txt", "utf8").trim().split("\n");
const hi = new Document({ numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: "left", style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] }] },
  sections: [{ properties: { page }, children: [P([B("Highlights")]), ...H.map(h => new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: h, font: FONT, size: 24 })] }))] }] });
const doc = new Document({ sections: [{ properties: { page }, children: letter }] });
Packer.toBuffer(doc).then(b => fs.writeFileSync(outLetter, b));
Packer.toBuffer(hi).then(b => { fs.writeFileSync(outHi, b); console.log("written"); });
