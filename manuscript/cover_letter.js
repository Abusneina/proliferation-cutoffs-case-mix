// Cover letter for Modern Pathology (A4, Times New Roman 12), with signature image.
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, ImageRun } = require("docx");
const out = process.argv[2];
const FONT = "Times New Roman";
const P = (t, o = {}) => new Paragraph({ spacing: { after: 110, line: 264 }, ...o,
  children: (Array.isArray(t) ? t : [t]).map(x => typeof x === "string" ? new TextRun({ text: x, font: FONT, size: 22 }) : x) });
const B = (t) => new TextRun({ text: t, font: FONT, size: 22, bold: true });
const I = (t) => new TextRun({ text: t, font: FONT, size: 22, italics: true });
const tight = { spacing: { after: 0, line: 276 } };
const sig = fs.readFileSync("/mnt/user-data/attachments/a7b57c6a-e976-5695-9c98-df16e019d7c0/acf6bd14-image.png");

const body = [
  P([B("Abdelmuhsen M. Abusneina")], tight),
  P("Department of Molecular Diagnostics, Faculty of Biomedical Sciences", tight),
  P("University of Benghazi, Fourth Ring Road, Benghazi, Libya", tight),
  P("abdelmuhsen.abusneina@uob.edu.ly | +218 91 420 0539 | ORCID 0000-0001-9909-5588"),
  P("November 3, 2026"),
  P("The Editor-in-Chief", tight),
  P([I("Modern Pathology")]),
  P([B("Re: Submission of a Research Article")], tight),
  P([I("Case mix of the derivation series and Ki-67 cut-offs for luminal A versus luminal B breast cancer: a predictive model and a correction")]),
  P("Dear Editor-in-Chief,"),
  P(["I submit the enclosed Research Article for consideration in ", I("Modern Pathology"), "."]),
  P("Where multigene assays are unavailable, the split between luminal A and luminal B breast cancer, and with it the use of adjuvant chemotherapy, rests on a Ki-67 cut-off. Published cut-offs derived against PAM50 range from 13% to 25%. Most were chosen to maximize agreement with PAM50, a criterion that depends on the luminal B share of the derivation series. The manuscript measures how far that share moves a cut-off, how much of the published variation it can explain, and how to correct for it."),
  P("In TCGA-BRCA, METABRIC and SCAN-B (4,395 estrogen receptor-positive, HER2-negative tumors), the proliferation score and the PAM50 reference come from the same RNA profile, which removes interlaboratory variation. Under a registered amendment, cut-offs were derived by six criteria in derivation sets resampled to luminal B shares of 15% to 65%. The kappa-optimal cut-off fell by 0.36 to 0.39 luminal A quantile points per point of luminal B share, and a binormal model fitted to the separation of the two subtypes predicted this within 0.09, meeting the registered criterion. In derivation sets of 400 tumors, case mix accounted for 54% to 65% of the variance of kappa-derived cut-offs and 85% to 87% for proportion matching. Cut-offs derived at 25% and at 65% luminal B gave different labels to 16% to 18% of patients. Reweighting the derivation set to the luminal B share of the target population reduced the transfer error from 6.3-10.6 to 3.2-3.9 quantile points."),
  P("On pathologist-scored Ki-67 (GSE81538), the kappa optimum stayed at 15%, and an earlier registered test of the mechanism was not met; the manuscript reports this and explains it by the 5-point steps in which Ki-67 was recorded. The minimum-misclassification rule, the criterion behind the original 13.25% cut-off, moved from 25% to 10% across the same range of case mix, which covers every published threshold."),
  P(["I believe the work fits the journal's scope in molecular classification and applied bioinformatics, and it bears directly on how pathology laboratories adopt and report a Ki-67 threshold. It ends with three reporting rules for derivation studies. Every analysis was specified in a dated, frozen amendment registered on the Open Science Framework before it was run, six documented errors and their handling are given in Online Resource 1, and the code and records are archived at Zenodo (https://doi.org/10.5281/zenodo.23926714)."]),
  P("This work has not been published and is not under consideration elsewhere. I am the sole author and have approved the submission. I have no competing interests to declare, and no funding was received. All cohort data are public. The use of a generative AI tool for code, literature screening and drafting is declared in the manuscript."),
  P("Thank you for considering this manuscript."),
  P("Sincerely,", { spacing: { after: 60 } }),
  new Paragraph({ children: [new ImageRun({ type: "png", data: sig, transformation: { width: 130, height: 73 } })] }),
  P([B("Abdelmuhsen M. Abusneina, PhD")], tight),
  P("Associate Professor of Molecular Oncology and Cancer Metabolism", tight),
  P("Faculty of Biomedical Sciences, University of Benghazi, Libya", tight),
];
const doc = new Document({ styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 850, bottom: 800, left: 1300, right: 1300 } } }, children: body }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("written", out); });
