# Amendment 11: results record

Recorded: 2026-11-03 18:57 UTC+2 (time read from the system clock). Author: Abdelmuhsen M. Abusneina.
Registration: osf.io/vhg4s (submitted 2026-11-03 18:55). Frozen 18:05; run 18:56 with script SHA-256 aa17d477… (checked).
Outputs: results/A11_*.csv, A11_derivations.csv.gz, A11_decision.json, A11_run.log. Scale: luminal A quantile (q_A).

## Registered criterion (O5)
Met. P2, kappa (K) and accuracy (ACC): |binormal model slope - resampled slope| = 0.045 and 0.006 (METABRIC),
0.089 and 0.057 (SCAN-B), 0.072 and 0.021 (TCGA-BRCA); all <= 0.10. (P1, not part of the criterion: largest
difference 0.129, TCGA-BRCA K.) Code check: BK = YJ in 99.53% of derivations.

## O1 case-mix slope, n = 1000, shares 15-65% (q_A points per point of luminal B share; sign: higher share, lower cut-off)
P2: K 0.39, 0.38, 0.36 (TCGA-BRCA, METABRIC, SCAN-B); ACC 0.47, 0.46, 0.41; PM 0.30, 0.32, 0.28; YJ, BK, SK -0.01 to 0.03.
P1: K 0.54, 0.47, 0.33; ACC 0.65, 0.78, 0.52; PM 0.43, 0.59, 0.36.

## O2 variance decomposition over shares 25-65%, P2, kappa rule (fraction of cut-off variance due to case mix)
n = 150: 0.42, 0.44, 0.42 (TCGA-BRCA, METABRIC, SCAN-B); n = 400: 0.62, 0.54, 0.65; n = 1000: 0.77, 0.69, 0.78.
Proportion matching: 0.72 to 0.94; accuracy: 0.61 to 0.86. Youden and target-weighted kappa: <= 0.013.

## O3 transfer to the full cohort, P2, n = 400 (RMSE in q_A points; % of luminal tumors labelled differently from the same rule's target optimum; mean kappa vs PAM50 | target-optimal kappa)
K:  10.6, 6.3, 10.6 | 8.6%, 5.3%, 8.7% | 0.608, 0.644, 0.682 (0.655, 0.668, 0.727)
YJ:  5.4, 4.5, 5.2 | 4.6%, 3.3%, 4.3% | 0.598, 0.651, 0.676 (0.609, 0.664, 0.683)
SK:  3.2, 3.9, 3.4 | 2.3%, 3.4%, 2.5% | 0.643, 0.655, 0.716
(order TCGA-BRCA, METABRIC, SCAN-B)

## O4 relabelling between kappa cut-offs derived at 25% and 65% luminal B (n = 1000, median thresholds), P2
TCGA-BRCA 101 of 573 ER+/HER2- patients (17.6%); METABRIC 227 of 1,397 (16.3%); SCAN-B 404 of 2,425 (16.7%),
of whom 30.0% received chemotherapy. P1: 24.1%, 16.8%, 10.0%.

## Ki-67 arm
Not run: GSE81538 file not supplied (GEO not reachable from the analysis environment).

## Note added after the run (descriptive, not registered)
The O1 kappa slope for P2 over 15-45% only is 0.28, 0.39, 0.24, close to the post hoc PH1 values (0.20, 0.37, 0.22),
which used 15-45% and an integer-percentile grid; between 45% and 65% it is 0.51, 0.44, 0.46. The movement is
steeper at higher shares, as the binormal model predicts.
