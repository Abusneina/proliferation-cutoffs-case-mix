# Search log: independent cohorts for limitations 1, 2 and 4
Recorded 2026-10-15 19:28 UTC+2 (time read from the system clock). Author: Abdelmuhsen M. Abusneina.

## What was looked at
Only series titles, metadata field names, the number of non-missing entries per field, label sets of categorical fields, the value format of the Ki-67 field in GSE21653, and platform gene coverage. No expression value, no cross-tabulation of any field against another, and no subtype count was read for any candidate cohort.

## Routes searched
- Web searches (3, extended mode) for public cohorts with Ki-67 IHC and PAM50 on the same tumors.
- Full-text pages of four candidate articles (data availability statements).
- GEO series matrix headers downloaded from ftp.ncbi.nlm.nih.gov for 25 series.
- cBioPortal API for brca_smc_2018 (clinical attributes and molecular profiles).
- GEO and ArrayExpress search services (eutils, ebi.ac.uk) are blocked from the working environment and were not used.

## Limitations 1 and 2: continuous Ki-67 IHC plus PAM50 on the same tumors
| Source | Ki-67 | PAM50 | Access | Verdict |
|---|---|---|---|---|
| Holm et al., JNCI Cancer Spectr 2021 (STO-3, n = 561; Clinseq, n = 237) | Continuous % | From expression | Not public ("cannot be shared publicly due to regulations under the Swedish law"); request to senior author after legal review | Data request candidate |
| Prat group pooled analysis (Front Oncol 2019; 8 studies, 1,416 HR+/HER2- tumors) | IKWG 2011 method | Yes | Held by investigators | Data request candidate (to be verified) |
| SCAN-B full cohort | Pathology Ki-67 | Yes | Data access request | Request already planned |
| Zito Marino et al., J Transl Med 2026 (Naples) | IHC, format unclear | Prosigna | No accession, no data statement | Not usable |
| Feeley et al., Mod Pathol 2014 (Toronto, n = 359 luminal) | Continuous % | No (IHC only) | No accession | Not usable |
| Sci Rep 2019 PCA-PAM50 (CBCP, TCGA, METABRIC) | Categorical (≥15%) or none | Yes | Not public or no IHC | Not usable |
| GSE21653 (Marseille, n = 266) | Field "ki67 ihc", about 5 distinct values (coarse or binary) | Older single-sample predictor labels | Public | Not usable for the IHC question |
| GSE96058, GSE202203 (SCAN-B) | Binary "ki67 status" | Yes | Public | Same initiative; not independent |
| GSE87411 (Z1031), GSE20181, GSE59515, GSE111563, GSE105777, GSE126870 (endocrine neoadjuvant) | No Ki-67 field in GEO | GSE126870 has PAM50 | Public | Ki-67 not deposited |
Conclusion: no public cohort with continuous Ki-67 IHC and PAM50 on the same tumors was found. Limitations 1 and 2 depend on data requests.

## Limitation 4: independent RNA cohort with PAM50 calls
| Source | Samples | Fields | Platform | Verdict |
|---|---|---|---|---|
| GSE25066 (Hatzis et al., JAMA 2011; MDACC, I-SPY, USO, LBJ/IN/GEI) | 508 pretreatment biopsies | pam50_class (LumA, LumB, Her2, Basal, Normal); ER IHC and ESR1 mRNA; HER2 status (P, N, I, NA); distant relapse-free survival | Affymetrix U133A (GPL96), MAS5 probe level | Primary candidate. MKI67 present; P2 15 of 18 genes (ANLN, NUF2, UBE2T absent); P3 120 of 120 |
| brca_smc_2018 (cBioPortal; Kan et al., Nat Commun 2018) | 168 with RNA-seq | PAM50_SUBTYPE; IHC_SUBTYPE; no Ki-67 | RNA-seq TPM | Secondary candidate (small) |
| GSE20194 (MAQC-II, MDACC) | 278 | ER, HER2; no PAM50 field | U133A | Not used: likely overlaps GSE25066 patients |
| GSE20685, GSE58644, GSE45255, GSE48390 | | No PAM50 field, or no ER/HER2 | | Not used |
Data-quality note: in GSE25066 the characteristic fields are not in the same order for every sample, so they must be parsed by field name.
