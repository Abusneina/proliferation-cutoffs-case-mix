# Amendment 7 results: GSE81538 (run after OSF registration, 14 Oct 2026)
Script: code/s11_gse81538_amendment7.py (seed 0; ties resolved to the lowest cut-off; 200 resamples per share; 2,000 bootstraps).
Population: ER consensus 1-3, HER2 consensus 0: 256 tumors; PAM50 luminal 232 (LumA 147, LumB 85; LumB share 36.6%). Sensitivity ER 2-3: 254 and 232 (identical luminal set).

## Pre-specified predictions
| Test | Criterion | Result | Verdict |
|---|---|---|---|
| C1 K (consensus Ki-67), slope of median kappa-optimal percentile on 100 - share | 0.7 to 1.3 | 0.62 (ER 2-3: 0.61) | NOT MET |
| C2 K, slope of Youden LumA quantile | -0.3 to 0.3 | 0.00 (ER 2-3: -0.04) | Met |
| C3a P2, kappa-optimal percentile vs 100 - observed share | within 5 points | 65 vs 63.4 | Met |
| C3b P2, Youden LumA-quantile bootstrap 95% CI overlaps 82-85 | overlap | point 89, CI 73 to 97 | Met |
Decision rule: confirmed if C1 and C2 both hold for K. C1 failed, so the mechanism is NOT CONFIRMED on IHC Ki-67 by the registered rule.

## Descriptive (D1-D5)
Observed K (consensus): kappa-optimal K > 15% (percentile 54, kappa 0.530, bootstrap 95% CI 15 to 15); Youden K > 15% (LumA quantile 76, J 0.555, CI 10 to 15).
Imposed share 20% vs 45%: kappa-optimal threshold median 15 vs 15 (2.5-97.5%: 15-25 vs 15-15); Youden threshold 15 vs 15 (10-15 vs 10-15).
Kappa-optimal percentile by imposed share (15,20,25,30,35,40,45%): 69.0, 65.1, 62.1, 58.6, 56.0, 53.0, 50.0 (the percentile of a fixed 15% threshold moves; the threshold itself rarely does).
Single readings, slope C1 / C2: reading 1 0.95 / 0.02; reading 2 0.86 / -0.02; reading 3 1.26 / 0.05. Readings 1-3 each fall inside 0.7-1.3 (not the registered primary measure).
Agreement at own optimum: K 0.530; P1 0.464; P2 0.688. P2 kappa-optimal percentile 65 (CI 55-77); P1 61 (CI 43-81); P1 Youden LumA quantile 72 (CI 60-95).
Eligible group other PAM50 calls: Normal 15, Her2 7, Basal 2.

## Reading
Slope of 0.62 sits below the registered lower bound. The registered rule says report non-confirmation. The consensus Ki-67 is coarse (modal values 10, 15, 20), so the threshold stays at 15% across imposed shares of 25-45% and moves up only at low shares (upper bound 25-30% at 15-20% share). The Youden boundary is invariant (C2). The RNA proxy reproduces the pattern in a fourth cohort (C3).
