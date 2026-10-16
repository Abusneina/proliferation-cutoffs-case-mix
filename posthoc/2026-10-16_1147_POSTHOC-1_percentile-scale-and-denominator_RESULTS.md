# Post hoc check 1: denominator of the percentile and scale of the resampling slope
Recorded 2026-10-16 11:47 (Africa/Tripoli; time read from the system clock). Prompted by an external review (items 3 and 4). Script: ph1_scale_check.py (seed 20261016). Not pre-specified.

## Q1. Denominator
The observed kappa-optimal cut-offs (74, 59, 71) are percentiles of the whole ER+/HER2- stratum, which includes non-luminal tumors, while 100 minus the luminal B share (73.9, 61.1, 70.5) uses the luminal set. On a consistent scale (percentile of the luminal set), the P2 optima are 74.5, 59.2 and 73.3 against 73.9, 61.1 and 70.5: within 3 points. On the stratum scale with a stratum denominator they are 74, 59, 71 against 77.7, 69.2, 74.3.

## Q2. Scale of the resampling slope (Amendment 6 design, 200 resamples per share)
| Cohort | Score | Slope, percentile of luminal set | Slope a fixed cut-off would show | Slope in score units (luminal A quantile) | Kappa optimum, luminal A quantile, share 15% to 45% |
|---|---|---|---|---|---|
| TCGA-BRCA | P2 | 0.96 | 0.65 | 0.20 | 91.7 to 86.2 |
| TCGA-BRCA | P1 | 0.91 | 0.53 | 0.34 | 90.6 to 79.8 |
| METABRIC | P2 | 1.11 | 0.67 | 0.37 | 94.5 to 84.4 |
| METABRIC | P1 | 1.02 | 0.44 | 0.57 | 94.4 to 76.5 |
| SCAN-B | P2 | 0.96 | 0.70 | 0.22 | 95.6 to 88.1 |
| SCAN-B | P1 | 0.91 | 0.62 | 0.23 | 94.7 to 85.7 |

Reading: a cut-off that does not move at all changes its percentile when the case mix changes, by F_A(c) minus F_B(c) per point of share (0.44 to 0.70 here). Most of the near-one slope on the percentile scale comes from this. The kappa-optimal cut-off does also move in score units, as theory predicts (luminal A quantile slopes 0.20 to 0.57), but by less. Under within-class resampling the Youden cut-off is fixed by construction.

## Ki-67 (Amendment 7, existing output A7_resampling.csv)
The kappa-optimal consensus Ki-67 threshold stayed at 15% for imposed shares of 25% to 45% and rose only at 15% to 20%; its percentile moved from 69 to 50 because the threshold's percentile shifts with case mix. The registered C1 slope (0.62) therefore reflects mostly the scale, not movement of the threshold.
