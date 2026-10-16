# Citation searching, round 2: backward search of the included studies' reference lists
Review: Ki-67 cut-off vs luminal B share (protocol v1.0, OSF osf.io/pc9wm). Supplementary search.
Run 2026-10-13, ~22:30 UTC+2. Reviewer: AI first pass (Claude). Every decision awaits a human Reviewer 2.

## Method
- Source papers (7): Cheang 2009 (19436038), Fernandez-Martinez 2017 (28423537), Dix-Peek 2023 (36867282),
  Lopez-Tarruella 2024 (37773555), Ceccarelli 2019 (31158261), Chen 2016 (27595437), Noske 2020 (31786414).
- Reference lists retrieved from Europe PMC citation links (query REFFED_BY:<pmid>_MED via the PubCrawl
  connector). The Europe PMC REST references endpoint was refused by the web proxy (rate limit) and was
  not retried. PMC full-text tools return article bodies without reference lists.
- Limitation: Europe PMC only lists references it could match to an indexed record. References it could
  not match (books, some non-indexed journals, conference abstracts) are not captured. Printed reference
  counts versus matched counts are given below so the shortfall is visible. A manual check of unmatched
  references against the printed lists remains to be done (Reviewer 2 task).
- Pre-screen filter: Ki67 OR "Ki-67" OR MIB1 OR "MIB-1" OR proliferation. Records without any of these
  terms cannot meet inclusion criterion 1 (Ki-67 IHC cut-off) and were excluded as off-topic.

## Retrieval per source paper
| Source | Printed references | Matched by Europe PMC |
|---|---|---|
| Cheang 2009 | not checked | 53 |
| Fernandez-Martinez 2017 | not checked | 26 |
| Dix-Peek 2023 | 53 | 47 |
| Lopez-Tarruella 2024 | 29 | 26 |
| Ceccarelli 2019 | 34 | 31 |
| Chen 2016 | ~28 (PDF) | 19 |
| Noske 2020 | 35 | 35 |
| Total | | 237 links |

## PRISMA counts
- Reference links: 237. Unique records after cross-list de-duplication: 194.
- Off-topic (no Ki-67 or proliferation term): 87 excluded.
- Ki-67/proliferation records: 107. Already screened in the 183 PubMed set or already assessed: 6
  (32590453, 23233704, 19436038, 31786414, 28423537, 24951027). Newly screened: 101.
- Excluded at title/abstract: 98, by reason
  - Guidelines, consensus statements, reviews, meta-analyses (St Gallen 2009-2021, IKWG 2011/2021, ASCO
    2016, AGO, IMPAKT, Luporsi, Yerushalmi, Petrelli, Stuart-Harris, de Azambuja, Denkert, Gyorffy,
    Schettini, Prat 2011, Viale 2012, Weigelt, Shiang): no primary derivation
  - Ki-67 survival or prognosis only (E1): Inwald 2013, Robertson 2018, Gudlaugsson 2012, Jonsdottir 2014,
    Domagala 1996, Clahsen 1999, Liu 2001, Goodson 2000, Trihia 2003, Viale 2008 and others
  - Neoadjuvant or presurgical (E5): Dowsett 2007, Ellis 2003, Ellis 2008, Nishimura 2010, Lips 2013
  - Fixed cut-offs tested, no optimum derived (E2): Patel 2022 (35947048), Sahebjam 2011 (21970880),
    Williams 2011 (21297447)
  - Correlation or concordance only, no Ki-67 cut-off derived: Niikura 2012 (22537114), Gluz 2016 PlanB
    (26926676), Hanna 2017 (28168058), Kim HK 2019 (30189722), Bastien 2012 (23035882; quartile cut-points
    on RT-qPCR, not IHC), Varga 2013, Ettl 2017, Sestak 2018, Buus 2021, Dowsett 2013, Bartlett 2016
  - Regression or nomogram models without a Ki-67 cut-off: Klein 2013, Orucevic 2017, Cuzick 2011,
    Barton 2012, Milburn 2013
  - Reproducibility, assay or image-analysis methods: Polley 2013, Polley 2015, Mengel 2002, Raap 2017,
    Tuominen 2010, Hsu 2003, Wong 2007, Nocito 2001, Keshgegian 1995
  - Other (epidemiology, genomics, HIV cohort, trials of other agents): remainder
- Forwarded to full text: 3 (Lundgren 2019, Holm 2021, Thakur 2018). All three are open access and
  were read in full.

## Full-text decisions
### 31432367 Lundgren 2019, Breast Cancer Res Treat (PMC6797629)
- SCAN-B, n = 2,063 ER+/HER2- PAM50-luminal tumors (RNA-seq nearest centroid). LumA 71 %, LumB 29 %.
- No Ki-67 optimum derived against PAM50. In an exploratory step the authors re-set the Ki-67 cut-offs
  to 16 % and 24 % so that the low/intermediate/high proportions matched those of Maisonneuve's series
  (34/24/42 %); agreement with PAM50 rose from 66 % to 73 %.
- Decision: exclude (cut-offs derived by matching an external distribution, not against the study's own
  reference). Descriptive table: a further instance of proportion matching. Also noted: only 47 % of
  Ki-67 >= 20 % tumors were LumB, and the authors question whether 20 % is too low.
- Relevance to the main paper: same cohort source as our SCAN-B arm (GSE96058). Cite in the Discussion.

### 33442660 Holm 2021, JNCI Cancer Spectrum (PMC7791620)
- Two Swedish cohorts with PAM50: STO-3 (n = 561, microarray, central IHC, whole-slide Ki-67) and
  Clinseq (n = 237, RNA-seq, clinical hotspot Ki-67).
- For the St Gallen and Prolif surrogates, a "free" Ki-67 cut-off was tailored to each dataset with the
  R caret package. Free cut-offs: Prolif 20 % (STO-3) and 40 % (Clinseq); St Gallen 45 % (STO-3) and 40 %
  (Clinseq). The optimization rule is in the supplement (not obtained); caret's default for
  classification is accuracy, which would place it in stratum P. Coding must wait for the supplement.
- Population includes all subtypes; the free cut-off optimizes a multi-class surrogate, and LumB shares
  among luminal tumors are in Table 2 (not in the retrieved text).
- Decision: include provisionally (R1, stratum P pending supplement), with the same flag as Dix-Peek
  (multi-class target, full cohort). Supplement and Table 2 needed. Two entries (one per cohort).

### 29304138 Thakur 2018, PLoS One (PMC5755729)
- n = 328 HR+/HER2- with Oncotype DX; automated hotspot Ki-67. No Ki-67 cut-off derived; a random-forest
  model predicts RS group. "97 % of high-risk patients had Ki-67 > 20 %" is descriptive. Exclude E2.

## Additional entries found in already-included papers
- Fernandez-Martinez 2017 also derived Youden-optimal Ki-67 cut-offs against Prosigna ROR-low vs
  ROR-intermediate/high: 12 % (tumors <= 2 cm) and 15 % (> 2 cm); AUC 0.76 and 0.72. These are Y/R2
  entries (ROR dichotomized). Add to extraction.

## Updated stratum count (AI first pass)
| Stratum | Studies |
|---|---|
| P / R1 | Cheang 2009; Dix-Peek 2023 (flag); Holm 2021 (provisional, 2 cohorts) |
| P / R2 | Chen 2016 (25 %, max concordance) |
| Y / R1 | Fernandez-Martinez 2017; Lopez-Tarruella 2024 |
| Y / R2 | Fernandez-Martinez 2017 (ROR entries) |
| U / R2 | Ceccarelli 2019; Noske 2020 |
| Other / R2 | Chen 2016 (20 %, max LR+) |

P/R1 = 3 studies at most (2 if Holm or Dix-Peek fails eligibility). Pooled R1 + R2 in stratum P = 4.
Both are below the registered threshold of 8. Under protocol v1.0 Section 5 the primary test is not run
and the review is reported as a descriptive systematic review with no inferential claim.

## Outstanding before the descriptive decision is final
1. Reviewer 2 screens this round independently.
2. Manual check of unmatched references (printed minus matched counts above), mainly Dix-Peek (6),
   Lopez-Tarruella (3), Ceccarelli (3), Chen (~9), plus Cheang and Fernandez-Martinez printed counts.
3. Holm 2021 supplement (optimization rule, Table 2 LumB shares).
4. Forward citation search for Ceccarelli 2019, Chen 2016 and Noske 2020 (round 1 covered the others).

## Addendum (2026-10-13 22:40): forward search for the remaining sources, and Chen unmatched references
- Forward search: (CITES:31158261_MED OR CITES:27595437_MED OR CITES:31786414_MED) -> 36 records.
  Already assessed: 2 (36867282, 38384489). Screened on abstract: Connolly 2026 (41488588; accuracy of
  St Gallen subtyping vs Oncotype/EndoPredict, no cut-off derived), Jank 2022 (34783927; fixed 10/20/30 %
  vs EndoPredict), Liu 2022 (34907993; BluePrint vs surrogate, no derivation), Li 2026 (41728598;
  survival, 20 % fixed), Macarron 2025 (39858055; nomogram threshold, not Ki-67). All excluded. The rest
  are off-topic (endometrial carcinoma, imaging, other markers). New includes: 0.
- Chen 2016 printed list: 25 references (PDF; 19 matched by Europe PMC, so 6 unmatched). All 25
  printed titles were read: guidelines (ASCO, NCCN web page, ASCO/CAP, St Gallen 2009-2015, IKWG),
  model papers (IHC4, Magee, IHC4+C), a health technology assessment, statistics (Harrell 1996),
  reproducibility and trial papers. None reports a Ki-67 cut-off derived against a genomic reference.
  New includes: 0.
- Remaining manual checks (Dix-Peek, Lopez-Tarruella, Ceccarelli, Cheang, Fernandez-Martinez printed
  lists) are left to Reviewer 2. On the evidence of the matched references, they are unlikely to add an
  eligible study.
