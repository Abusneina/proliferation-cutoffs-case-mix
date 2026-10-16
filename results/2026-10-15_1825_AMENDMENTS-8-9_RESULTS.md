# Results of Amendments 8 and 9
Recorded 2026-10-15 18:25 UTC+2. Author: Abdelmuhsen M. Abusneina.

## Governance
- Amendment 8 frozen 2026-10-14 16:41; Amendment 9 frozen 2026-10-14 16:51 (UTC+2).
- Both posted on OSF (osf.io/cwkd9, OSF Storage) on 2026-10-15 at 18:13, as shown in the OSF file list.
- SHA-256 of all four frozen files re-checked against the freeze records before the run: all OK.
- Runs: s22_amendment9.py and s21_amendment8.py, mode "run", started after the posting. Logs: A9_run.log, A8_run.log.
- Reproduction check: P1 and P2, rerun through the Amendment 8 code, give the registered kappa-optimal percentiles in every cohort (P2: 74, 59, 71, 65; P1: 77, 64, 66, 61).

## Amendment 8: gene-disjoint proliferation score

Registered verdict for P3 (meta-PCNA minus PAM50 genes, median of 119 or 120 genes): **CONFIRMED FOR A GENE-DISJOINT SCORE**. G1, G2 and G3 held in all three cohorts; the supporting test G4 also held.

| Cohort | 100 minus LumB share | P3 kappa-optimal percentile (95% CI) | G1 (within 5) | Resampling slope, kappa (G2: 0.7 to 1.3) | Resampling slope, Youden on LumA scale (G3: -0.3 to 0.3) | Youden boundary, LumA quantile (95% CI) |
|---|---|---|---|---|---|---|
| TCGA-BRCA | 73.9 | 74 (63 to 81) | met | 1.06 | -0.00 | 82 (73 to 92) |
| METABRIC | 61.1 | 59 (55 to 64) | met | 1.13 | -0.01 | 82 (78 to 87) |
| SCAN-B | 70.5 | 68 (66 to 73) | met | 0.89 | 0.00 | 85 (83 to 91) |
| GSE81538 (G4) | 63.4 | 64 (53 to 79) | met | 1.05 | 0.02 | 86 (67 to 97) |

Secondary scores (H3), same rules: P3m (mean aggregation) and P4 (Hallmark G2M minus PAM50, median of 186 or 187 genes) also met G1 to G3 in all three cohorts, and G4. TCGA-BRCA P4 had a kappa slope of 0.73, close to the lower bound of 0.70.

H1, peak kappa with PAM50 (95% CI):

| Score | TCGA-BRCA | METABRIC | SCAN-B | GSE81538 |
|---|---|---|---|---|
| P1 (MKI67) | 0.55 (0.48 to 0.64) | 0.45 (0.40 to 0.51) | 0.61 (0.57 to 0.65) | 0.46 (0.39 to 0.60) |
| P2 (18 PAM50 genes) | 0.65 (0.58 to 0.73) | 0.67 (0.63 to 0.71) | 0.72 (0.70 to 0.76) | 0.69 (0.60 to 0.79) |
| P3 (gene-disjoint, median) | 0.62 (0.56 to 0.71) | 0.66 (0.62 to 0.71) | 0.69 (0.66 to 0.73) | 0.62 (0.54 to 0.73) |
| P3m (gene-disjoint, mean) | 0.59 (0.52 to 0.68) | 0.66 (0.62 to 0.70) | 0.67 (0.64 to 0.71) | 0.63 (0.54 to 0.74) |
| P4 (Hallmark G2M, disjoint) | 0.66 (0.59 to 0.74) | 0.63 (0.59 to 0.68) | 0.60 (0.57 to 0.64) | 0.52 (0.44 to 0.65) |

Removing every PAM50 gene lowered peak kappa by 0.00 to 0.07 (P3 against P2).

H2, Spearman correlation with P2: P3 0.95 to 0.97 in the ER-positive, HER2-negative strata; 0.91 to 0.96 within luminal A; 0.86 to 0.92 within luminal B. P4: 0.86 to 0.95.

Reading, as limited in advance: the pattern does not depend on genes shared with PAM50. The shared biology remains. P3 measures the same proliferation axis as P2 almost perfectly (rho about 0.96), so this analysis removes gene overlap as an explanation without making the score independent of the biology that drives the PAM50 luminal A/B split.

## Amendment 9: overall survival in all three cohorts (secondary endpoint)

Primary pooled set, P2, fixed effect (random effects identical; I-squared 0%):
- STABLE_B vs DISCORDANT: HR 1.08 (95% CI 0.90 to 1.30), inside [0.67, 1.50]. Registered verdict: **B-like supported on a common endpoint**. METABRIC + SCAN-B: 1.07 (0.88 to 1.28), same verdict.
- STABLE_A vs DISCORDANT: HR 0.77 (0.65 to 0.91). Registered reading: **discordant group has worse overall survival than stable luminal A-like**.
- P1 gives the same verdicts: STABLE_B 1.04 (0.85 to 1.26); STABLE_A 0.81 (0.68 to 0.97).

Per cohort, P2 (overall survival; deaths in the comparison):

| Cohort | STABLE_A vs DISC | STABLE_B vs DISC | Continuous score inside the zone, HR per SD | Rule R1 (zone empty) | Trend per step |
|---|---|---|---|---|---|
| TCGA-BRCA | 0.88 (0.38 to 2.05); 35 | 1.50 (0.62 to 3.59); 26 | 1.70 (0.78 to 3.71); 7 deaths | not met (imprecise) | 1.35 (1.00 to 1.82) |
| METABRIC | 0.76 (0.63 to 0.92); 573 | 1.03 (0.84 to 1.27); 382 | 1.04 (0.88 to 1.22); 144 deaths | met | 1.18 (1.09 to 1.27) |
| SCAN-B | 0.77 (0.53 to 1.14); 136 (registered C1) | 1.20 (0.80 to 1.81); 103 (registered C1) | 0.96 (0.70 to 1.32); 36 deaths | met | 1.27 (1.08 to 1.48) |

BH-adjusted p-values within cohort are in A9_overall_survival.csv.

Comparison with the registered mixed-endpoint pool (Amendment 4, P2, fixed effect): STABLE_B vs DISC was 1.22 (0.96 to 1.54) for METABRIC + SCAN-B ("inconclusive") and 1.17 (0.94 to 1.46) for all three cohorts. STABLE_A vs DISC was 0.69 (0.55 to 0.87) and 0.67 (0.54 to 0.83).

Cautions for reporting:
1. Overall survival includes deaths from other causes, and METABRIC carries most of the weight (811 deaths, many non-cancer). This dilution pulls hazard ratios toward 1. It weakens the STABLE_A contrast, as stated in advance, and for the same reason it makes an equivalence verdict on STABLE_B easier to reach. The "B-like supported" verdict must be reported with this caveat and must not replace the registered primary results.
2. The METABRIC overall-survival result is not independent of its known disease-specific result.
3. The in-zone test (R1) is met in METABRIC and SCAN-B for P2. For P1 it is met in METABRIC only; SCAN-B P1 is imprecise (1.09, 0.76 to 1.57). TCGA-BRCA has 6 to 7 deaths in the zone.
