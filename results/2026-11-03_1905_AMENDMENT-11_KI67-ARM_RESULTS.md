# Amendment 11, conditional Ki-67 arm (GSE81538): results record

Recorded: 2026-11-03 19:05 UTC+2 (time read from the system clock). Run 19:05 with code/s28_amendment11_ki67_arm.py (hash in Error Log 6),
importing s27 unchanged. Identity check passed (256 eligible; 147 luminal A; 85 luminal B; share 36.6%).
Registered run log A11_run.log verified unchanged after the run (SHA-256 check).

Full-set optima (232 luminal tumors): kappa, accuracy and Youden all choose Ki-67 > 15% (kappa 0.530);
proportion matching chooses > 20% (kappa 0.358).

Median derived threshold (n = 232) by imposed luminal B share 15/25/35/45/55/65%:
- kappa (K):                15/15/15/15/15/15%   case-mix slope 0.00 q_A points per point
- minimum misclassification: 25/25/15/15/15/10%  slope 0.64
- proportion matching:       25/20/20/20/15/15%  slope 0.37
- Youden:                    15% throughout

O2 (shares 25-65%), fraction of threshold variance due to case mix: K 0.18 (n = 150) and 0.17 (n = 232);
accuracy 0.58 and 0.64; proportion matching 0.60 and 0.65; Youden and target-weighted kappa <= 0.003.
O3 (n = 232): RMSE against the same rule's full-set optimum, q_A points: K 5.3, accuracy 10.5, proportion matching 7.3,
Youden 4.5, target-weighted kappa 2.1; luminal tumors labelled differently: 1.6%, 7.6%, 6.7%, 1.1%, 0.2%.

Reading: with Ki-67 recorded in 5-point steps, the kappa optimum stayed at 15%, in line with Amendment 7. The
minimum-misclassification rule (the criterion of Cheang et al. 2009) moved from 25% to 10% across shares of 15% to 65%,
and proportion matching from 25% to 15%.
