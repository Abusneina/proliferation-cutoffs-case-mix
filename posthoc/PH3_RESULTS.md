# Post hoc analyses PH3 (28 October 2026; not registered)
Written after all registered results were known and after the BCRT decision on an earlier version. Code: posthoc/ph3a_independent_cohorts_and_pooled.py, posthoc/ph3b_ki67_ties_translation.py. Results: PH3a_independent_and_pooled.csv, PH3b_ki67_tie_rules.csv, PH3b_ki67_luminalA_quantiles.csv.

1. Score-unit slope (kappa optimum as luminal A quantile points per point of luminal B share, 200 resamples, 15% to 45%), P2 / P3: GSE25066 0.47 / 0.31; SMC 2018 0.26 / 0.53; GSE81538 0.29 / 0.43; TCGA-BRCA 0.22 / 0.40; METABRIC 0.36 / 0.42; SCAN-B 0.21 / 0.17.
2. Slope against the original luminal set (fixed reference), P2 / P3: GSE25066 0.59 / 0.36; SMC 2018 0.37 / 0.78; GSE81538 0.39 / 0.51; TCGA-BRCA 0.25 / 0.48; METABRIC 0.49 / 0.56; SCAN-B 0.25 / 0.21.
3. GSE81538 Ki-67 slope by tie rule (lowest, middle, highest): 0.61 inclusive and 0.59 mid-rank for all; threshold fixed at 15%: 0.56 inclusive, 0.52 mid-rank.
4. Luminal A (n = 147) Ki-67 quantiles: 60th 10; 70th and 75th 15; 80th to 89th 20; 90th to 94th 25; 95th 30. Used only as an illustrative translation, not confirmed for Ki-67.
Main-cohort P2 score-unit slopes in the manuscript (0.20 to 0.37) come from the earlier PH2 run; PH3a reproduced them within 0.02 (0.21 to 0.36).
