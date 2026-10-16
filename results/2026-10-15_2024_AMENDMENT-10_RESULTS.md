# Results of Amendment 10 (independent RNA cohort)
Recorded 2026-10-15 20:24 UTC+2. Author: Abdelmuhsen M. Abusneina.

## Governance
- Frozen 2026-10-15 19:38 UTC+2 with its analysis script (SHA-256 b0df341c...; freeze record verified OK before the run).
- Posted in osf.io/cwkd9 before the run (reported by the author at 20:22; exact time to be read from the OSF file list). Registration pending.
- Run started 2026-10-15 20:22:18 UTC+2. Log: A10_run.log. Results: A10_results.csv, A10_decision.json.

## Registered verdict, GSE25066
**NOT TESTED (underpowered).** The eligible stratum had 167 ER-positive, HER2-negative tumors: 93 luminal A and 38 luminal B (luminal B share 29.0%). The amendment requires at least 60 tumors in each luminal subtype. The small stratum results from an error in the ER field chosen (Error Log 4).

## Descriptive results (no confirmatory weight)
| Cohort | Score | Target | Kappa-optimal percentile | R1 (within 5) | Kappa slope (R2) | Youden slope (R3) | Youden LumA quantile (95% CI) | Peak kappa |
|---|---|---|---|---|---|---|---|---|
| GSE25066 (n = 167; 93 A, 38 B) | P2 (15 genes) | 71.0 | 60 | not met | 1.26 | 0.05 | 84 (74 to 98) | 0.70 |
| | P3 | 71.0 | 69 | met | 0.86 | -0.01 | 94 (67 to 98) | 0.73 |
| | P1 | 71.0 | 72 | met | 0.90 | -0.05 | 52 (39 to 92) | 0.38 |
| | P4 | 71.0 | 69 | met | 1.06 | -0.06 | 87 (69 to 98) | 0.69 |
| SMC 2018 (n = 90; 42 A, 41 B) | P2 (18 genes) | 50.6 | 44 | not met | 1.02 | 0.04 | 81 (74 to 100) | 0.71 |
| | P3 | 50.6 | 38 | not met | 1.17 | -0.02 | 71 (63 to 93) | 0.66 |
| | P1 | 50.6 | 50 | met | 0.91 | 0.05 | 81 (73 to 100) | 0.59 |
| | P4 | 50.6 | 38 | not met | 1.31 | 0.05 | 64 (56 to 93) | 0.54 |

Spearman correlation of P3 with P2 in GSE25066: 0.95.

## Reading
- The resampling criteria (R2 and R3) were met for P2 and P3 in both cohorts. Within each cohort, the kappa optimum moved with the imposed luminal B share (slopes 0.86 to 1.26) and the Youden boundary did not (slopes -0.02 to 0.05).
- The observed kappa optimum fell within 5 points of the target for P3 in GSE25066, and missed it for P2 in GSE25066 (60 against 71) and for P2 and P3 in SMC 2018 (44 and 38 against 50.6). With 38 to 42 luminal B tumors, single observed optima are imprecise.
- None of this is confirmatory. Limitation 4 remains open as a registered question.
