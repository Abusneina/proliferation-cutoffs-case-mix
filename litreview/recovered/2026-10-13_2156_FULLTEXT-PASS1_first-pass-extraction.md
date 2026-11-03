[Recovered on 2026-11-03 from the text of Online Resource 3 as submitted to Breast Cancer (BRCA-D-26-01218); the original file was not archived in the repository. Line breaks follow the submitted PDF.]

# Full-text eligibility and first-pass extraction (16 candidates)
Reviewer 1: AI-assisted first pass (Claude), 2026-10-13, after OSF registration osf.io/pc9wm.
Not blinded: the reviewer had seen cut-off values in abstracts (see SEARCH-LOG.txt). Every entry awaits
Reviewer 2 (human), who performs Pass 1 (design classification) from masked methods sections.
Strata: P = prevalence-dependent criterion; Y = Youden / closest to (0,1); U = ROC, criterion not stated.
Reference: R1 = PAM50 / intrinsic subtype; R2 = risk assay (RS, MammaPrint).
## Status summary
| PMID | Study | Decision | Ref | Stratum | Cut-off |
|---|---|---|---|---|---|
| 19436038 | Cheang 2009, JNCI | Include | R1 | P (verify) | 13.25 % |
| 28423537 | Fernandez-Martinez 2017, Oncotarget | Include | R1 | Y | 14 % |
| 36867282 | Dix-Peek 2023, BCRT | Include (flag) | R1 | P | 25 % |
| 37773555 | Lopez-Tarruella 2024, BCRT | Include | R1 | Y | 13 % |
| 31158261 | Ceccarelli 2019, PLoS One | Include | R2 | U | 25 % |
| 24630985 | Tobin 2014, Mol Oncol | Pending: PMC record has no body text; PDF needed | R1 and R2 | ? | 8-28 % range
(abstract) |
| 37847456 | Shim 2023, BCRT | Exclude E2 | R2 | - | fixed IKWG cut points tested, no optimum derived |
| 38951111 | Kim 2024, J Breast Cancer | Exclude E2 (provisional) | R2 | - | Ki-67 > 20 used; derivation not described
in text; check Table 3 |
| 30854118 | Gao 2019, J Cancer | Exclude E1 | - | - | X-tile against DFS; IHC 14 % adopted from literature |
| 24951027 | Maisonneuve 2014, Breast Cancer Res | Exclude (criterion 4 and E1) | none | - | outcome-based (DDFS); no
genomic reference |
| 41850212 | Golash 2026, Clin Breast Cancer | Pending: PDF needed | | | |
| 32565110 | Marazzi 2020, Clin Breast Cancer | Pending: PDF needed | | | |
| 27595437 | Chen 2016, J Chin Med Assoc | Pending: PDF needed | | | |
| 28825136 | Gandara-Cortes 2017, Virchows Arch | Pending: PDF needed | | | |
| 22782361 | Tamaki 2012, Breast Cancer | Pending: PDF needed | | | |
| 23643806 | Ingoldsby 2013, Breast | Pending: PDF needed | | | |
Counts so far: P/R1 = 2; Y/R1 = 2; U/R2 = 1. Feasibility threshold (8 in P/R1) cannot be met from this
set even if every pending paper qualifies (7 pending; at most 4 of them plausibly R1). The protocol's
fallback (pool R1 and R2, then descriptive only if still < 8) is the likely route. Reference-list
hand-searching is therefore essential before the feasibility decision is taken.
## Entries
### 19436038 Cheang 2009 (PMC2684553)
- Reference: PAM50 by qRT-PCR (R1). Training set 144 HR+/HER2- tumors: 84 LumA, 60 LumB (LumB share 41.7 %).
- Criterion: "ROC method, by minimizing the sum of the observed false-positive and false-negative errors",
with bootstrapping. Minimizing total misclassification is maximizing accuracy, which depends on
prevalence. Classified P. Reviewer 2 to confirm.
- Optimum 13.25 % (sensitivity 72 %, specificity 77 %). Same optimum in 127 unambiguous tumors.
- Assay: SP6 clone, 0.6 mm TMA cores, visual scoring by two pathologists.
### 28423537 Fernandez-Martinez 2017 (PMC5400635)
- Reference: Prosigna PAM50 (R1). n = 517 ER+/HER2- node-negative.
- PAM50: LumA 56.9 %, LumB 40.8 %, HER2E 1.2 %, basal 1.2 %.
- Criterion: Youden index on ROC. Classified Y.
- Comparison is LumA vs non-LumA (non-LumA share 43.1 %); LumB among luminal 41.8 %.
Flag: which share enters the regression must be fixed by the protocol rule, not by the reviewer.
- Optimum 14 %; AUC 0.79. Clones: 30-9 (GEICAM), MIB1 (CBM-Rome), local (VHIO). IKWG scoring.
### 36867282 Dix-Peek 2023 (PMC10147771)
- Reference: Prosigna PAM50 on nCounter SPRINT (R1). n = 378 Black South African women, all subtypes.
- PAM50: LumA 19.3 % (73), LumB 32.5 % (123), HER2E 23.5 % (89), basal 24.6 % (93).
LumB share among PAM50 luminal = 123/196 = 62.8 %.
- Criterion: maximum Cohen's kappa across a pre-set grid of five cut-offs (10, 15, 20, 25, 30 %).
Classified P.
- Optimum 25 % (kappa 0.128); worst 10 % (kappa 0.079). Authors also note 25 % brings IHC A/B proportions
closest to PAM50 proportions, an explicit prevalence-matching argument.
- Assay: 30-9 (Ventana), Benchmark XT, visual estimation, multiple scorers, single laboratory.
- Flags for Reviewer 2: (a) kappa appears to be computed on a four-class IHC scheme over the full cohort,
not on LumA vs LumB within ER+/HER2-; (b) a five-point grid may not meet the "derived optimum"
criterion as worded in the protocol; (c) HR+/HER2+ tumors sit in Clin-B. Decide eligibility jointly.
### 37773555 Lopez-Tarruella 2024 (PMC10771357)
- Reference: Prosigna PAM50, central laboratory (R1). n = 1,029 PAM50-luminal of 1,049 HR+/HER2(eight countries; mostly node-negative).
- PAM50 among 1,049: LumA 65 %, LumB 33 %, non-luminal 1.9 %. LumB share among luminal about 33.6 %
(exact count to be taken from Table 2).
- Criterion: ROC, cut-off maximizing Youden's J. Classified Y.
- Optimum 13 %; AUC 0.766 (95 % CI 0.736-0.796).
- Assay: Ki-67 from local laboratories; clone and scoring method not centralized.
### 31158261 Ceccarelli 2019 (PMC6546245)
- Reference: Oncotype DX RS (R2). n = 156 HR+/HER2- pT1-2 pN0-1, single institution.
- Positive class: RS High vs Low/Intermediate. High = 5.2 % (traditional) or 9.0 % (TAILORx).
Flag: paper does not state which classification the ROC used; it reports 25 % separates High in both.
- Criterion: "ROC Plot Analysis ... most informative value", no rule named. Classified U.
- Optimum 25 %.
- Assay: Benchmark Ultra, image cytometry (Image Pro Plus) on whole invasive front, >= 5,000 cells.
Clone not stated in the text.
### 24630985 Tobin 2014 (PMC5528643)



- PMC returned no body text. Abstract: ROC-optimized Ki-67 cut-offs 8-28 % against GGI, 70-gene,
p53 signature, RS, and Sorlie, Hu and Parker subtypes, in two cohorts (n = 253 and 159).
- Potentially several R1 and R2 entries from one paper. PDF required.
### 37847456 Shim 2023 (PMC10787679)
- Exclude E2. Tested IKWG cut points (<= 5 %, >= 30 %) and 10 % / 20 % against RS >= 26; no optimum derived.
### 38951111 Kim 2024 (PMC11221207)
- Provisional exclude E2. Ki-67 > 20 entered a logistic score; text does not describe how 20 was chosen.
Reviewer 2 to check Table 3 and supplement before final decision.
### 30854118 Gao 2019 (PMC6400683)
- Exclude E1. Optimum (RT-PCR Ki-67 5.68) derived by X-tile against DFS; IHC 14 % adopted.
### 24951027 Maisonneuve 2014 (PMC4095689)
- Exclude: no genomic reference (criterion 4); 20 % threshold chosen on DDFS. Keep for the descriptive
discussion: authors justify the definition partly by matching the ~50 % LumA share seen in
gene-expression series.
