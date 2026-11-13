// Build the revised Cancer Epidemiology manuscript (.docx) from ms_ce.json.
// A4, Times New Roman 12, double spacing, continuous line numbers; tables in a landscape section with merged group cells.
const fs = require("fs");
const D = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType,
        PageBreak, Footer, PageNumber, LineNumberRestartFormat, PageOrientation, BorderStyle, VerticalAlign } = D;
const m = JSON.parse(fs.readFileSync(__dirname + "/ms_ce.json", "utf8"));
const out = process.argv[2];
const FONT = "Times New Roman";
const T = (t, o = {}) => new TextRun({ text: t, font: FONT, size: 24, ...o });
const P = (x, opts = {}) => new Paragraph({ spacing: { line: 480, after: 0 }, ...opts, children: Array.isArray(x) ? x : [T(x)] });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [T(t, { bold: true })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [T(t, { italics: true })] });
const PB = () => new Paragraph({ children: [new PageBreak()] });
const c = m.counts;

const front = [
  P([T(m.title, { bold: true })]), P(""),
  P([T("Running title: ", { bold: true }), T(m.running)]), P(""),
  P("Abdelmuhsen M. Abusneina"),
  P("Department of Molecular Diagnostics, Faculty of Biomedical Sciences, University of Benghazi, Fourth Ring Road, Benghazi, Libya"), P(""),
  P([T("Corresponding author: ", { bold: true }), T("Abdelmuhsen M. Abusneina, PhD, Department of Molecular Diagnostics, Faculty of Biomedical Sciences, University of Benghazi, Fourth Ring Road, Benghazi, Libya. E-mail: abdelmuhsen.abusneina@uob.edu.ly. Telephone: +218914200539. ORCID: 0000-0001-9909-5588")]), P(""),
  P([T("Article type: ", { bold: true }), T("Original Research Article")]),
  P([T("Word counts: ", { bold: true }), T(`abstract ${c.abstract}; main text ${c.main.toLocaleString("en-US")}; highlights ${c.highlights} words; references ${c.refs}; tables ${c.tables}; figures ${c.figures}.`)]),
  PB(), H1("Abstract"),
];
for (const [h, x] of m.abstract) front.push(P([T(h + ": ", { bold: true }), T(x)]));
front.push(P(""), P([T("Keywords: ", { bold: true }), T(m.keywords)]), PB());

const body = [];
for (const [t, x] of m.body) body.push(t === "h1" ? H1(x) : t === "h2" ? H2(x) : P(x, { indent: { firstLine: 567 } }));
body.push(H1("Acknowledgments"), P(m.ack));
for (const [h, x] of m.statements) body.push(H1(h), P(x));
body.push(PB(), H1("References"));
for (const r of m.refs) body.push(P(r));
body.push(PB(), H1("Figure legends"));
for (const [f, x] of m.legends) body.push(P([T(f + " ", { bold: true }), T(x)]), P(""));

// tables with vertical merging of repeated group labels and horizontal merging of repeated header cells
const LAND_W = 16838 - 2 * 1134;
const thin = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
function makeTable(rows, headerRows, mergeCols, widthsRel) {
  const ncol = rows[0].length;
  const rel = widthsRel || Array(ncol).fill(1); const sum = rel.reduce((a, b) => a + b, 0);
  const widths = rel.map(r => Math.floor(LAND_W * r / sum));
  const nrow = rows.length;
  const span = rows.map(r => r.map(() => 1));          // rowSpan for vertical merges (0 = covered)
  for (const j of mergeCols) {
    let i = headerRows;
    while (i < nrow) {
      let k = i; while (k + 1 < nrow && rows[k + 1][j] === rows[i][j] && rows[i][j] !== "" &&
                        mergeCols.slice(0, mergeCols.indexOf(j)).every(jj => span[k + 1][jj] === 0 || rows[k + 1][jj] === rows[i][jj])) k++;
      span[i][j] = k - i + 1; for (let q = i + 1; q <= k; q++) span[q][j] = 0; i = k + 1;
    }
  }
  const trows = [];
  for (let i = 0; i < nrow; i++) {
    const cells = []; let j = 0;
    while (j < ncol) {
      if (span[i][j] === 0) { j++; continue; }
      let cs = 1;
      if (i < headerRows) while (j + cs < ncol && rows[i][j + cs] === rows[i][j] && rows[i][j] !== "") cs++;
      const w = widths.slice(j, j + cs).reduce((a, b) => a + b, 0);
      const last = i + span[i][j] - 1;
      cells.push(new TableCell({ width: { size: w, type: WidthType.DXA }, columnSpan: cs, rowSpan: span[i][j],
        verticalAlign: VerticalAlign.TOP,
        borders: { top: i === 0 ? thin : none, bottom: (last === headerRows - 1 || last === nrow - 1) ? thin : none, left: none, right: none },
        margins: { top: 40, bottom: 40, left: 60, right: 60 },
        children: [new Paragraph({ suppressLineNumbers: true, alignment: cs > 1 ? AlignmentType.CENTER : AlignmentType.LEFT,
          children: [new TextRun({ text: rows[i][j], font: FONT, size: 18, bold: i < headerRows })] })] }));
      j += cs;
    }
    trows.push(new TableRow({ tableHeader: i < headerRows, cantSplit: true, children: cells }));
  }
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: trows });
}
const spec = { "1": [1, [0, 1, 2, 3, 4], null], "2": [1, [], [1.2, 3, 1.3, 1.6, 1.6]], "3": [2, [0], null],
               "4": [1, [0], [1.4, 1.6, 1, 1, 0.8, 0.9, 0.9, 1]], "5": [1, [0], [1, 3, 1, 1, 1.2, 1.2, 1]],
               "6": [1, [0], [1.3, 1.6, 1.2, 0.8, 1.1, 2.6, 0.9]] };
const tables = [];
for (const k of ["1", "2", "3", "4", "5", "6"]) {
  const [hr, mc, w] = spec[k];
  tables.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: m.ttitles[k], font: FONT, size: 22, bold: true })] }));
  tables.push(makeTable(m.tables[k].filter(r => r.some(x => x.trim() !== "")), hr, mc, w));
  tables.push(new Paragraph({ spacing: { before: 120, after: 0 }, children: [new TextRun({ text: m.tnotes[k], font: FONT, size: 18 })] }));
  if (k !== "6") tables.push(PB());
}
const footer = new Footer({ children: [new Paragraph({ suppressLineNumbers: true, alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })] })] });
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24, color: "000000" } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, color: "000000" }, paragraph: { spacing: { before: 240, after: 120, line: 480 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, italics: true, color: "000000" }, paragraph: { spacing: { before: 120, after: 0, line: 480 }, keepNext: true, outlineLevel: 1 } }] },
  sections: [
    { properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
        lineNumbers: { countBy: 1, restart: LineNumberRestartFormat.CONTINUOUS } }, footers: { default: footer }, children: [...front, ...body] },
    { properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
        margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, footers: { default: footer }, children: tables },
  ] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("written", out); });
