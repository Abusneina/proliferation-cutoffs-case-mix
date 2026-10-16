# Full-text eligibility and first-pass extraction (16 candidates), version 2
Supersedes 2026-10-13_2156 version. Reviewer 1: AI-assisted first pass (Claude), after OSF registration
osf.io/pc9wm. Not blinded (cut-offs seen in abstracts; see SEARCH-LOG.txt). Every entry awaits Reviewer 2.
Strata: P = prevalence-dependent criterion; Y = Youden / closest to (0,1); U = ROC, criterion not stated.
Reference: R1 = PAM50 / intrinsic subtype; R2 = risk assay (RS, MammaPrint).

## Status summary (16 of 16 assessed; 2 on abstract or partial text only)
| PMID | Study | Decision | Ref | Stratum | Cut-off | Source read |
|---|---|---|---|---|---|---|
| 19436038 | Cheang 2009, JNCI | Include | R1 | P (verify) | 13.25 % | PMC full text |
| 28423537 | Fernandez-Martinez 2017, Oncotarget | Include | R1 | Y | 14 % | PMC full text |
| 36867282 | Dix-Peek 2023, BCRT | Include (flag) | R1 | P | 25 % | PMC full text |
| 37773555 | Lopez-Tarruella 2024, BCRT | Include | R1 | Y | 13 % | PMC full text |
| 31158261 | Ceccarelli 2019, PLoS One | Include | R2 | U | 25 % | PMC full text |
| 27595437 | Chen 2016, J Chin Med Assoc | Include (flag: two criteria) | R2 | see entry | 20 % (max LR+); 25 % (max concordance) | PDF |
| 24630985 | Tobin 2014, Mol Oncol | Provisional exclude (population) | R1, R2 | U | Parker: 13 % Uppsala, 10 % Stockholm | PDF |
| 23643806 | Ingoldsby 2013, Breast | Exclude from regression; descriptive | R2 (continuous RS) | - | 15 % (tree split) | PDF |
| 37847456 | Shim 2023, BCRT | Exclude E2 | R2 | - | fixed IKWG cut points, no optimum | PMC full text |
| 38951111 | Kim 2024, J Breast Cancer | Exclude E2 (provisional) | R2 | - | 20 % used, derivation not described | PMC full text |
| 41850212 | Golash 2026, Clin Breast Cancer | Exclude E2 (provisional) | R2 | - | concordance at fixed thresholds | Abstract + publisher preview only |
| 32565110 | Marazzi 2020, Clin Breast Cancer | Exclude | R2 | - | Youden applied to model probability, no Ki-67 cut-off | PDF |
| 30854118 | Gao 2019, J Cancer | Exclude E1 | - | - | X-tile against DFS | PMC full text |
| 24951027 | Maisonneuve 2014, Breast Cancer Res | Exclude (criterion 4, E1) | none | - | DDFS-based | PMC full text |
| 28825136 | Gandara-Cortes 2017, Virchows Arch | Exclude (criterion 4) | none | - | applies published thresholds; no genomic reference | PDF |
| 22782361 | Tamaki 2014, Breast Cancer | Exclude E1 (on abstract) | none | - | 20-25 % chosen on DFS | Abstract only; uploaded PDF was a different paper |

Included so far: 6 studies. P/R1 = 2 (Cheang, Dix-Peek). Y/R1 = 2. R2 = 2.
Feasibility (>= 8 in P/R1) is not met. Pooling R1 and R2 still gives fewer than 8 in any single stratum.
Under the registered rule the synthesis becomes descriptive unless reference-list and citation searching
adds eligible studies. That search is the next step and must be logged as part of the registered search.

## Entries added or changed in version 2

### 27595437 Chen 2016 (PDF)
- Reference: multigene assay, 21-gene (n = 30) and 70-gene (n = 41) pooled, n = 71 HER2- luminal (R2).
  Risk counts from Table 3 rows: low 42, intermediate 9, high 20 (RS 18-21 recoded low; RS 26 recoded high).
  Non-low share 29/71 = 40.8 %; high share 20/71 = 28.2 %.
- Section 3.4: Ki-67 values tested in the St Gallen luminal A definition against multigene low risk.
  20 % gave the maximum positive likelihood ratio (Table S5, supplement not obtained).
  25 % (the cohort median) gave the highest concordance (67.6 %) in separating low from high risk.
- Classification problem: maximum LR+ is prevalence-independent but is neither Youden nor a P criterion.
  The protocol has no stratum for it. Proposed handling: record the 25 % (max concordance) result as the
  P entry; record the 20 % (LR+) result as a non-P entry; Reviewer 2 to confirm. Report as an amendment
  note if the coding rule has to be extended.
- Within-study contrast worth noting in the discussion: the prevalence-dependent criterion chose a higher
  cut-off (25 %) than the prevalence-independent one (20 %) in the same 71 tumors.
- Assay: MIB-1 (Dako), manual or ImmunoRatio, >= 3 HPF averaged, readers blind to assay result.

### 24630985 Tobin 2014 (PDF)
- Two cohorts, all breast cancers (ER+ and ER-), Affymetrix arrays: Uppsala n = 253, Stockholm n = 159.
- Ki-67 cut-off chosen by ROC as "best signature-reproducing"; the rule is not named in the main text
  (Supplementary methods not obtained). Coded U.
- Parker (PAM50) entries, read from Tables 1-3:
  - Uppsala: positive class LumB + HER2 vs others; cut-off >= 13 %; AUC 0.68; similarity 67 %.
    Positive share from Table 1 counts: 63/233 = 27.0 %.
  - Stockholm: positive class all except normal-like and LumA; cut-off >= 10 %; AUC 0.77; similarity 73 %.
    Positive share from Table 3 counts: 54/113 = 47.8 %.
- RS entries also exist (Uppsala low vs intermediate/high, >= 12 %; Stockholm low/intermediate vs high).
- Reason for provisional exclusion: unselected population including ER- tumors, and the positive class
  includes HER2-enriched (and basal in Stockholm). This is not luminal A vs B within ER+/HER2-.
  Reviewer 2 to decide against the protocol population criterion. Counts were read from table images
  and must be re-checked.

### 23643806 Ingoldsby 2013 (PDF)
- n = 52 TAILORx-enrolled ER+ node-negative (Ki-67 available in 48). Reference: Oncotype RS.
- Ki-67 15 % arose as a recursive-partitioning split predicting the continuous RS (p = 0.003).
  No dichotomized reference class, so no positive share exists. Not usable in the meta-regression.
  Keep for the descriptive table.
- Assay: MIB-1 (Dako), Benchmark XT, >= 300 cells including hot spots.

### 41850212 Golash 2026 (abstract and ScienceDirect preview only)
- n = 195 ER+/HER2-, East Cheshire. Correlation and concordance of Ki-67 with RS (51.8 % concordance).
  No derivation of an optimal Ki-67 cut-off is visible. Provisional exclude E2; confirm when the full
  methods section is available.

### 32565110 Marazzi 2020 (PDF)
- n = 407 internal, 183 external. Youden index was applied to the predicted probability of a logistic
  model for RS <= 25 or <= 20. Ki-67 entered as a continuous quantitative IHC variable. No Ki-67 cut-off.
  Exclude.

### 28825136 Gandara-Cortes 2017 (PDF)
- n = 521, standardized 4-IHC with image analysis. Applies published Ki-67/PR thresholds and compares
  resulting subtype proportions with published genomic series. No genomic assay on these tumors. Exclude
  (criterion 4). Descriptive note: another instance of judging thresholds by matching published subtype
  proportions.

### 22782361 Tamaki 2014 (abstract only)
- The uploaded PDF is Jain P et al., "Ki-67 labeling index as a predictor of response to neoadjuvant
  chemotherapy in breast cancer", Jpn J Clin Oncol 2019;49(4):329-338, doi 10.1093/jjco/hyz012.
  That paper is outside the candidate list (neoadjuvant, E5).
- Tamaki abstract: 408 IDC; 20-25 % suggested from DFS and OS comparisons. No genomic reference.
  Exclusion on criteria 4 and E1 is secure from the abstract; full text still preferred for the record.

## Entries unchanged from version 1
Cheang 2009, Fernandez-Martinez 2017, Dix-Peek 2023, Lopez-Tarruella 2024, Ceccarelli 2019, Shim 2023,
Kim 2024, Gao 2019, Maisonneuve 2014: see 2026-10-13_2156 version for full notes.
