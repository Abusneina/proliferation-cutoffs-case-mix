// Build the manuscript .docx from ms.json (A4, Times New Roman 12, double spacing, line numbers, tables landscape).
const fs = require("fs");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType,
        PageBreak, Footer, PageNumber, LineNumberRestartFormat, PageOrientation, BorderStyle, ShadingType } = D;
const m = JSON.parse(fs.readFileSync("/home/claude/work/ms/ms_jce.json", "utf8"));
const out = process.argv[2];
const FONT = "Times New Roman";
const P = (text, opts = {}) => new Paragraph({ spacing: { line: 480, after: 0 }, ...opts,
  children: Array.isArray(text) ? text : [new TextRun({ text, font: FONT, size: 24 })] });
const B = (t) => new TextRun({ text: t, font: FONT, size: 24, bold: true });
const T = (t) => new TextRun({ text: t, font: FONT, size: 24 });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: FONT, size: 24, bold: true })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, font: FONT, size: 24, italics: true })] });

const front = [
  P([B(m.title)]), P(""),
  
  P("Abdelmuhsen M. Abusneina"),
  P("Department of Molecular Diagnostics, Faculty of Biomedical Sciences, University of Benghazi, Fourth Ring Road, Benghazi, Libya"), P(""),
  P([B("Corresponding author: "), T("Abdelmuhsen M. Abusneina, PhD, Department of Molecular Diagnostics, Faculty of Biomedical Sciences, University of Benghazi, Fourth Ring Road, Benghazi, Libya. E-mail: abdelmuhsen.abusneina@uob.edu.ly. Telephone: +218914200539. ORCID: 0000-0001-9909-5588")]), P(""),
  P([B("Article type: "), T("Research Article")]),
  P([B("Word counts: "), T(`abstract ${m.counts.abstract}; main text ${m.counts.main.toLocaleString("en-US")}; references ${m.counts.refs}; tables 4; figures 4.`)]),
  new Paragraph({ children: [new PageBreak()] }),
  H1("Abstract"), ...m.abstract_sections.map(([h, x]) => P([B(h + ": "), T(x)])), P(""), P([B("Keywords: "), T(m.keywords)]), P(""),
  H1("What is new?"), ...m.what_is_new.map(([h, x]) => P([B(h + ": "), T(x)])),
  new Paragraph({ children: [new PageBreak()] }),
];
const body = [];
for (const [t, x] of m.body) body.push(t === "h1" ? H1(x) : t === "h2" ? H2(x) : P(x, { indent: { firstLine: 567 } }));
body.push(H1("Acknowledgments"), P(m.ack));
for (const [h, x] of m.statements) body.push(H1(h), P(x));
body.push(new Paragraph({ children: [new PageBreak()] }), H1("References"));
for (const r of m.refs) body.push(P(r));
body.push(new Paragraph({ children: [new PageBreak()] }), H1("Figure legends"));
for (const [f, x] of m.legends) body.push(P([B(f + " "), T(x)]), P(""));

// tables (landscape section)
const LAND_W = 16838 - 2 * 1134; // A4 landscape width minus margins (DXA)
const thin = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
function makeTable(rows, headerRows) {
  const ncol = rows[0].length; const w = Math.floor(LAND_W / ncol); const widths = Array(ncol).fill(w);
  return new Table({ width: { size: w * ncol, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({ tableHeader: i < headerRows, children: r.map(c => new TableCell({
      width: { size: w, type: WidthType.DXA },
      borders: { top: i === 0 ? thin : none, bottom: (i === headerRows - 1 || i === rows.length - 1) ? thin : none, left: none, right: none },
      margins: { top: 40, bottom: 40, left: 60, right: 60 },
      children: [new Paragraph({ suppressLineNumbers: true, children: [new TextRun({ text: c, font: FONT, size: 18, bold: i < headerRows })] })] })) })) });
}
const tables = [];
const hdr = { "1": 1, "2": 2, "3": 1, "4": 1 };
for (const k of ["1", "2", "3", "4"]) {
  tables.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: m.ttitles[k], font: FONT, size: 22, bold: true })] }));
  tables.push(makeTable(m.tables[k].filter(r => r.some(c => c.trim() !== "")), hdr[k]));
  tables.push(new Paragraph({ spacing: { before: 120, after: 0 }, children: [new TextRun({ text: m.tnotes[k], font: FONT, size: 18 })] }));
  if (k !== "4") tables.push(new Paragraph({ children: [new PageBreak()] }));
}
const footer = new Footer({ children: [new Paragraph({ suppressLineNumbers: true, alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })] })] });
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true }, paragraph: { spacing: { before: 240, after: 120, line: 480 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, italics: true }, paragraph: { spacing: { before: 120, after: 0, line: 480 }, keepNext: true, outlineLevel: 1 } }] },
  sections: [
    { properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
        lineNumbers: { countBy: 1, restart: LineNumberRestartFormat.CONTINUOUS } },
      footers: { default: footer }, children: [...front, ...body] },
    { properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
        margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, footers: { default: footer }, children: tables },
  ] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("written", out); });
