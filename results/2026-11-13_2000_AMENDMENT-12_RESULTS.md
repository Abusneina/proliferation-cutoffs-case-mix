# Amendment 12: results of the registered run

Registration: https://osf.io/ezmdn (registered 2026-11-13 19:54 UTC+2, public, no embargo; registered from osf.io/cwkd9).
Archived files checked against the freeze record: amendment text bf86e9c4..., script ef134636..., freeze record 07fa2c75..., reproduction record f3617dd7... (all match).
Run: 2026-11-13 19:58 UTC+2, `python3 -I code/s31_amendment12.py GSE81538_series_matrix.txt.gz`, script unchanged (SHA-256 ef134636...), seed 20261113. GSE81538 identity check passed (256 eligible; 147 luminal A; 85 luminal B). Log: results/A12_run.log.

## Verdicts under the rules fixed in the amendment

| Analysis | Rule fixed in advance | Result |
|---|---|---|
| N2 transfer between natural subgroups | SK better than K (RMSE against target K optimum) in both directions of the primary split | Primary split: tumor size 20 mm or less (luminal B 23.7%) versus over 20 mm (42.3%); gap 18.6 points. Not met for SK_oracle or SK_population |
| N3 misspecified target share | Largest abs(delta) with SK RMSE below K in all cohorts, both directions | 10 points |
| N4 Ki-67 prediction | Report if at least 3 points in the fitting window | 5 points (R^2 0.90); reported |
| N5 equal variance | b interval includes 1 | Adequate for P2 in all three cohorts and for P1 in TCGA-BRCA and SCAN-B; not adequate for P1 in METABRIC (b 0.76, 95% interval 0.65 to 0.88) |
| N8 Ki-67 accuracy optimum | Robust only if near-optimal regions at 25% and 65% do not overlap | 30% to 35% at 25% luminal B; 10% to 15% at 65%. No overlap: robust |

## N2 (18-gene score, RMSE in target luminal A quantile points against the target K optimum; derivation sets of up to 400, 500 samples)

| Split, direction | K | ACC | SK_oracle | SK_population | YJ |
|---|---|---|---|---|---|
| Size, small to large | 4.8 | 3.1 | 11.7 | 7.0 | 14.2 |
| Size, large to small | 3.0 | 2.8 | 1.4 | 1.3 | 5.9 |
| Nodes, negative to positive (26.8% to 34.4%) | 5.4 | 3.4 | 9.2 | 6.4 | 17.9 |
| Nodes, positive to negative | 2.1 | 2.0 | 2.0 | 2.0 | 4.5 |
| Age, under 50 to 50 or over (26.2% to 30.1%) | 2.0 | 2.0 | 2.0 | 2.0 | 3.2 |
| Age, 50 or over to under 50 | 7.8 | 5.2 | 5.5 | 7.3 | 18.0 |

Reweighting to the target share helped when deriving in the higher-share subgroup and hurt when deriving in the lower-share subgroup. Subgroups differ in the score distributions of each subtype as well as in prevalence.

## N3 (18-gene score, n = 400, shares 25% to 65%; RMSE against the full-cohort K optimum)

K: 10.7 (TCGA-BRCA), 6.6 (METABRIC), 10.7 (SCAN-B). SK with the true share: 3.1, 4.0, 3.4. SK stayed below K for misspecification up to 10 points either way in all cohorts; at -15 points it exceeded K in METABRIC (6.7 against 6.6).

## N4 (consensus Ki-67, binormal model, values in Ki-67 %)

| Rule | 25% luminal B | 65% luminal B | Difference (95% interval) |
|---|---|---|---|
| Kappa | 20 | 15 | 5 (0 to 10) |
| Accuracy | 25 | 10 | 15 (5 to 20) |
| Proportion matching | 20 | 15 | 5 (5 to 10) |
| Youden | 15 | 15 | 0 |

Values fall on the 5-point grid because the luminal A distribution used for conversion is recorded in 5-point steps (12 distinct values).

## N5 binormal fit (a, b, R^2)

18-gene: TCGA-BRCA 2.20, 1.23 (0.74 to 1.60), 0.981; METABRIC 1.95, 1.02 (0.83 to 1.25), 0.997; SCAN-B 2.19, 0.99 (0.84 to 1.17), 0.977. MKI67: 1.52, 0.97, 0.984; 0.99, 0.76, 0.993; 1.75, 1.01, 0.996. Equal-variance slopes match the free-b slopes within 0.02 for the 18-gene score.

## N7 case-mix share of variance (kappa rule; n = 400 for RNA, 232 for Ki-67)

| Range of imposed shares | TCGA-BRCA | METABRIC | SCAN-B | GSE81538 Ki-67 |
|---|---|---|---|---|
| 25% to 65% (registered) | 0.62 | 0.54 | 0.65 | 0.17 |
| 35% to 55% | 0.33 | 0.28 | 0.40 | 0.03 |
| 25% to 45% | 0.33 | 0.32 | 0.37 | 0.04 |
| 45% to 65% | 0.32 | 0.26 | 0.35 | 0.11 |

## N8 Ki-67 near-optimal region (population weights; within 0.01 of the maximum)

Accuracy: 30% to 35% at 15% and 25% luminal B; 15% at 35% to 55%; 10% to 15% at 65%. Kappa: 15% at every share.

## N9 cohort characteristics
In results/A12_N9_cohorts.csv.
