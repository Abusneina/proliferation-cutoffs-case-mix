# Citation searching, round 1 (supplementary search, after registration osf.io/pc9wm)
Date: 2026-10-13 ~22:30 UTC+2. Source: Europe PMC via PubCrawl connector. Reviewer: AI first pass.

## Queries
1. CITES:19436038_MED AND (PAM50 OR Prosigna OR "intrinsic subtype" OR nCounter) AND ("Ki-67" OR Ki67)
   AND (ABSTRACT:"cut-off" OR ABSTRACT:cutoff OR ABSTRACT:threshold OR ABSTRACT:"cut point")  -> 23 records
2. (CITES:28423537_MED OR CITES:37773555_MED OR CITES:36867282_MED) AND ("Ki-67" OR Ki67)  -> 26 records
Limitation: Europe PMC citation links are incomplete for non-OA citing papers. Backward searching of
reference lists (all six included papers) has not been done yet.

## Records not already in the 183 PubMed set, screened on title/abstract
| PMID | Study | Decision | Reason |
|---|---|---|---|
| 31786414 | Noske 2020, Breast (EndoPredict vs Ki-67, n = 307) | Forward to full text | Reports Ki-67 > 25 % as the region overlapping EP high risk; check whether a cut-off was derived and whether EndoPredict falls within R2 as registered |
| 35681597 | Kjällquist 2022, Cancers (Prosigna, n = 360) | Exclude | Ki-67 compared across risk groups; no cut-off derivation |
| 37761848 | Dank 2023, Genes (PAM50, n = 42) | Exclude | IHC/FISH vs PAM50 concordance; no Ki-67 cut-off derivation |
Noske 2020 full text (PMC7375593) read: include provisionally, R2, stratum U.
- n = 307 ER+/HER2- with prospective EndoPredict. EPscore low 140, high 167 (high share 54.4 %).
  EPclin low 203, high 104 (high share 33.9 %).
- ROC of Ki-67 against dichotomized EPscore: AUC 0.797, reported cut-off 20 % (sens 68 %, spec 80 %).
  Against EPclin: AUC 0.745, cut-off 20 % (sens 67 %, spec 78 %). Selection rule not named -> U.
- Survival-derived optima (18 % OS, 24 % DFS) are E1 and are not extracted.
- Assay: MIB1 (Dako), BenchMark XT, IKWG scoring, single pathologist blinded to EP.
- Protocol v1.0 defines R2 as "a multigene risk assay dichotomized into low and high risk, such as the
  21-gene recurrence score"; EndoPredict therefore qualifies as R2 without any amendment.
All other records from both queries were either already in the 183 set or not about a Ki-67 cut-off.

## Records already in the 183 set that this search re-surfaced
31422497 Viale 2019 (Ki-67 30-9 and luminal A/B differentiation) and 38384489 Ziegler 2024 (Prosigna vs
Ki-67) were excluded at title/abstract as E2. Both full texts were then read (PMC6797656, PMC10878706):
- Viale 2019: no genomic reference; applies the Maisonneuve 14 %/20 % definition and tests it on DDFS.
  Exclusion confirmed (criterion 4). Descriptive note: authors justify the definition by the ~59 %
  luminal A-like share matching Cheang 2009.
- Ziegler 2024: n = 55 premenopausal, Prosigna; fixed Ki-67 groups (< 10, 10-24, >= 25 %); no optimum
  derived. Exclusion E2 confirmed.
