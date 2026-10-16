# Amendment 10: post hoc exploratory rerun with the complete ER field
Recorded 2026-10-15 21:01 UTC+2. Version 2, 21:09 UTC+2 (times read from the clock), replaces the 21:01 version posted on OSF. Corrections: (1) the P2 gap below the target was stated as 9 to 13 points; the values are 9.4 (GSE25066) and 6.6 (SMC 2018). (2) The slope ranges now use the registered-run values for SMC 2018, whose eligibility is identical in both runs: kappa slopes 1.00 to 1.19, Youden slopes -0.02 to 0.04. Author: Abdelmuhsen M. Abusneina.

## Status
POST HOC and EXPLORATORY. Run at 21:00 UTC+2, after the registered result (NOT TESTED, underpowered) and after Error Log 4 were known. It has no confirmatory weight and does not change the registered verdict.

## What changed from the frozen script
One line: ER positivity from the field `er_status_ihc` = P (present for all 508 samples) instead of `er_status_ihc_esr1_for indeterminate` = P (present for 310). Everything else is identical, including the probe rule, the scores, the criteria and the random seed. Script: code/s24_amendment10_exploratory_ER-all508.py (diff against the frozen s23 shows only that line, the header, the output label and the verdict wording). Log: A10_EXPLORATORY-ER-all508_run.log. Results: A10_results_EXPLORATORY-ER-all508.csv.

## GSE25066 (289 ER-positive, HER2-negative; 147 luminal A, 71 luminal B; luminal B share 32.6%; target 67.4)
| Score | Kappa-optimal percentile | Within 5 of target | Kappa slope (0.7 to 1.3) | Youden slope (-0.3 to 0.3) | Youden LumA quantile (95% CI) | Peak kappa |
|---|---|---|---|---|---|---|
| P2 (15 genes) | 58 | no (9.4 below) | 1.19 | -0.01 | 79 (66 to 93) | 0.64 |
| P3 | 64 | yes | 1.00 | 0.00 | 76 (65 to 95) | 0.64 |
| P1 | 59 | no | 0.69 | 0.09 | 77 (36 to 86) | 0.34 |
| P4 | 59 | no | 0.99 | 0.01 | 86 (73 to 93) | 0.65 |
Both subtypes now exceed the minimum of 60. Applying the Amendment 10 rule would give "not all criteria met": P3 meets all three; P2 meets both resampling criteria and misses the observed-optimum criterion. Spearman P3 vs P2: 0.95.

SMC 2018 is unaffected by the change (same eligibility); results as in the registered run, small differences in slopes reflect the random stream.

## Reading
- Within-cohort dependence on case mix replicated in both independent cohorts for P2 and P3: the kappa optimum moved about one point per point of luminal B share (slopes 1.00 to 1.19, using the registered-run values for SMC 2018), and the Youden boundary on the luminal A scale did not move (slopes -0.02 to 0.04).
- The observed kappa optimum sat close to 100 minus the luminal B share in the four original cohorts, but 7 to 9 points below it for P2 in GSE25066 (58 against 67.4, 9.4 points) and SMC 2018 (44 against 50.6, 6.6 points); in the registered run on the smaller GSE25066 set the gap was 11.0 points (60 against 71.0). The level of the optimum therefore depends on more than case mix in these cohorts (biopsy material, platform, a different PAM50 implementation, or chance with 41 to 71 luminal B tumors), while its movement with case mix held.
- The manuscript should say this plainly: the resampling mechanism transferred to two independent cohorts; the approximate equality "optimum = 100 minus share" did not hold for the 18-gene score in either.
