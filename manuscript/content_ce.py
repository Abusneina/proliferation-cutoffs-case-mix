# Revised manuscript content for Cancer Epidemiology (revision after Amendment 12).
# [@key] tokens are numbered in order of first citation by build_ce.py (body first, then tables in order).
TITLE = ("Case mix and agreement-optimized proliferation cut-offs for luminal A versus luminal B breast cancer: "
         "prevalence, spectrum and transfer")
RUNNING = "Case mix and proliferation cut-offs"

ABSTRACT = [
("Background", "Laboratories without multigene assays separate luminal A from luminal B breast cancer with a Ki-67 "
 "cut-off; cut-offs derived against PAM50 range from 13% to 25%. Many studies choose the value that best reproduces "
 "PAM50, which depends on the luminal B share of the series. This study measured how far case mix moves derived cut-offs, "
 "compared the shift with sampling variation, and tested reweighting to target prevalence."),
("Methods", "In estrogen receptor-positive, HER2-negative tumors from TCGA-BRCA (n = 573), METABRIC (n = 1,397) and "
 "SCAN-B (n = 2,425), cut-offs for an 18-gene RNA proliferation score were derived against PAM50 by six criteria, in "
 "sets resampled within subtype to luminal B shares of 15% to 65% and between clinical subgroups, under registered "
 "amendments. A binormal model predicted the shifts. Ki-67 was examined in GSE81538 "
 "(232 luminal tumors)."),
("Results", "With subtype distributions fixed, the kappa optimum fell by 0.36 to 0.39 luminal A quantile "
 "points (percentiles of luminal A) per point of luminal B share, within 0.09 of the model. In sets "
 "of 400 tumors, case mix explained 54% to 65% of the variance of kappa-derived cut-offs over shares of 25% to 65%, "
 "and 28% to 40% over 35% to 55%. Cut-offs derived at 25% and 65% luminal B relabeled 16% to 18% of patients. "
 "Weighting to the true target share cut transfer error from 6.3-10.6 to 3.2-3.9 points but failed its registered "
 "test between tumor-size subgroups, whose score distributions also differed. On Ki-67 the registered test was not "
 "met; the model predicted kappa-optimal thresholds of 20% and 15% at 25% and 65% luminal B."),
("Conclusions", "Agreement-optimized proliferation cut-offs carry the prevalence of their derivation series "
 "predictably, and tumor spectrum adds to it; reweighting removes only the prevalence part. Derivation studies "
 "should report the criterion, the luminal B share and the cut-off as a luminal A quantile."),
]
KEYWORDS = "Ki-67; PAM50; Breast neoplasms; Cut-off; Case mix"

HIGHLIGHTS = [
"Agreement-optimized cut-offs fall as the derivation set's luminal B share rises",
"A binormal model predicted the shift within 0.09 luminal A quantile points",
"Cut-offs derived at 25% and 65% luminal B relabeled 16% to 18% of patients",
"Reweighting to target prevalence helped only when tumor spectrum was held fixed",
"Report criterion, luminal B share and cut-off as a luminal A quantile",
]

BODY = [
("h1", "Introduction"),
("p", "The distinction between luminal A and luminal B disease guides adjuvant chemotherapy in estrogen receptor "
 "(ER)-positive, HER2-negative breast cancer. Where multigene assays are unavailable, it is made with an "
 "immunohistochemical surrogate in which the Ki-67 labeling index separates the two groups [@goldhirsch2011; "
 "@goldhirsch2013; @coates2015]. The threshold has never settled. Cheang and colleagues derived 13.25% against PAM50 "
 "[@cheang2009], later definitions added progesterone receptor [@prat2013] or moved to 20% and above [@goldhirsch2013; "
 "@coates2015], and the International Ki67 Working Group accepts only values of 5% or less and 30% or more "
 "[@nielsen2021]. Studies that derive a local threshold against PAM50 report 13% to 25% [@fernandez2017; @lopez2024; "
 "@dixpeek2023], and many laboratories, including those in the author's region, still decide with the surrogate alone [@abusneina2026]."),
("p", "The usual explanation for the spread is analytical: antibody, platform and counting method change the number a "
 "laboratory reports [@dowsett2011; @polley2013]. A second explanation concerns the derivation criterion. Many "
 "derivation studies choose the cut-off that maximizes agreement with the reference, through kappa, accuracy or "
 "concordance, or the value that reproduces the reference subtype proportions, and these criteria depend on "
 "prevalence [@feinstein1990; @byrt1993; @leeflang2013]. The Youden index does not include prevalence directly "
 "[@youden1950], although it can vary with spectrum [@brenner1997]. The principle is long established [@metz1978]. "
 "What is missing for this decision is its size, its weight against sampling variation at the sizes of published "
 "studies, and whether a simple reweighting removes it when populations differ in more than prevalence. PAM50 is "
 "itself an imperfect reference, so every cut-off studied here is optimal only relative to the calls it is compared "
 "with."),
("p", "These questions were studied in three public cohorts in which the proliferation measure and the PAM50 reference "
 "come from the same RNA profile, so analytical variation is absent by construction. The study measured how far "
 "cut-offs derived by six criteria move with the luminal B share of the derivation set, compared that movement with sampling "
 "variation, tested a binormal model of it, evaluated reweighting within cohorts and between natural clinical "
 "subgroups, counted the patients whose label changes, and repeated the analysis on pathologist-scored Ki-67."),

("h1", "Materials and methods"),
("h2", "Design and registration"),
("p", "This was a retrospective analysis of public cohorts with a supporting review of published studies, reported "
 "following REMARK [@remark2006] (Online Resource 2). The question arose when the first two cohorts were inspected, so "
 "the first comparison of optima is post hoc. The proliferation gene list and Amendments 2 to 6 were posted after "
 "their analyses, and their timing rests on the author's file records. Amendments 7 to 12 were registered on the Open "
 "Science Framework before their analyses were run; Amendments 11 (osf.io/vhg4s) and 12 (osf.io/ezmdn) were written "
 "with all earlier results known, and Amendment 12 after critiques of an earlier version of this manuscript. Analyses "
 "not specified in advance are labeled post hoc. Error logs and the full sequence are in Online Resource 1."),
("h2", "Cohorts and scores"),
("p", "TCGA-BRCA (RNA sequencing) [@hoadley2018] and METABRIC (microarray) [@curtis2012; @pereira2016] were obtained "
 "from cBioPortal [@cerami2012], and SCAN-B from the Gene Expression Omnibus (GSE96058; RNA sequencing; 136 technical "
 "replicates excluded) [@brueffer2018]. Each stratum comprised ER-positive, HER2-negative tumors with the PAM50 calls "
 "supplied with the data: 573, 1,397 and 2,425 patients, of whom 490, 1,105 and 2,116 were luminal A or B (Table 1; "
 "characteristics in Online Resource 4). The primary score, P2, was the mean standardized expression of the 18 PAM50 "
 "proliferation genes other than MKI67 [@parker2009]; P1 was MKI67 alone. Genes were standardized within each "
 "cohort's stratum."),
("h2", "Derivation criteria and scale"),
("p", "Tumors above a cut-off were called luminal B-like. Six criteria for choosing the cut-off against PAM50 were "
 "compared (Table 2), three of which depend on prevalence: maximum Cohen's kappa, minimum misclassification (maximum "
 "accuracy), the criterion of Cheang and colleagues [@cheang2009], and proportion matching. Candidate cut-offs were the "
 "observed values between the 5th and 95th percentiles, and ties went to the lowest value. A laboratory transfers the "
 "value of a cut-off, not its percentile, so cut-offs were expressed as luminal A quantiles: the percentage of the "
 "full-cohort luminal A distribution at or below the cut-off. An earlier registered analysis used percentiles of the "
 "resampled set, a scale that moves even for a fixed cut-off (Error Log 5); it is reported in Online Resource 4."),
("h2", "Resampling within cohorts"),
("p", "For each cohort and score, derivation sets of 150, 400 and 1,000 tumors were drawn with replacement within "
 "subtype at luminal B shares of 15% to 65% in steps of 10 points, 500 times per cell. The range covers published "
 "derivation studies (27.6% to 62.8% luminal B; 71 to 1,029 tumors). Sampling within subtype holds each "
 "subtype's score distribution fixed, so any movement is caused by prevalence alone, and the Youden cut-off can move "
 "only by sampling noise. The case-mix slope was the change in the median cut-off per point of luminal B share "
 "(n = 1,000). Over shares of 25% to 65%, the variance of the derived cut-off was split into the variance of the "
 "means at each share (case mix, B) and the mean variance within shares (sampling, W); the case-mix share was "
 "B/(B + W), also computed over narrower ranges. Transfer error was the root-mean-square difference (RMSE) between the "
 "derived cut-off and the same criterion applied to the full cohort. Relabeling was the percentage of the stratum "
 "labeled differently by the median kappa cut-offs derived at 25% and at 65% luminal B. TCGA-BRCA has 128 luminal B "
 "tumors, so its sets of 1,000 at shares of 45% or more repeat tumors heavily."),
("h2", "Transfer between natural subgroups"),
("p", "Under Amendment 12, luminal tumors of SCAN-B were split by tumor size (20 mm or less against more), nodal status "
 "and age (below 50 years against older). Cut-offs were derived in one subgroup, from the whole subgroup and from 500 "
 "bootstrap sets of up to 400 tumors with their natural case mix, and applied to the other, in both directions. "
 "Error was measured against the kappa optimum of the target subgroup. Kappa weighted to the target's luminal B share "
 "was compared with plain kappa; a second version used the share of all SCAN-B luminal tumors, standing in for a "
 "regional estimate. The registered criterion required lower error than plain kappa in both directions of the split "
 "with the largest difference in luminal B share. Within cohorts, the same weighting was also run with the target "
 "share misspecified by 5 to 15 points."),
("h2", "Binormal model"),
("p", "A binormal receiver operating characteristic model [@metz1978] was fitted to each cohort by least squares of "
 "probit(sensitivity) on probit(1 - specificity) over values between 0.05 and 0.95. It gives the population cut-off of "
 "each criterion at any luminal B share and hence a predicted slope. Amendment 11 required the predicted slope for P2 "
 "to lie within 0.10 of the resampled slope for kappa and accuracy in all three cohorts. Under equal variances the "
 "accuracy-optimal cut-off is c = d/2 + ln[(1 - p)/p]/d, where d is the separation in luminal A standard deviations "
 "and p the luminal B share. Fit was described by R2 and by the bootstrap interval of the variance ratio b."),
("h2", "Pathologist-scored Ki-67 and other analyses"),
("p", "GSE81538 provided 232 PAM50 luminal tumors with Ki-67 scored centrally by three pathologists "
 "[@brueffer2018]. Amendment 7 (osf.io/p5hb7) tested the mechanism on consensus Ki-67, Amendment 11 repeated the "
 "comparison of criteria in sets of 150 and 232 tumors, and Amendment 12 added the binormal prediction in Ki-67 "
 "percentage points and the near-optimal region of each criterion (thresholds within 0.01 of the maximum). A score "
 "sharing no gene with PAM50 (P3; meta-PCNA genes [@venet2011] without PAM50 genes), two further cohorts (GSE25066 "
 "[@hatzis2011]; SMC 2018 [@kan2018]) and an outcome comparison of patients between the two observed optima are "
 "reported in Online Resource 4. Published studies that derived a Ki-67 cut-off against a multigene assay were "
 "sought under a registered protocol [@osfprotocol]; the author screened with a language model, a second reviewer "
 "screened independently, and a third person checked extracted values (Online Resource 3). Analyses used Python. "
 "Before the Amendment 12 run, every deposited table was regenerated from the public data with the archived release "
 "and reproduced exactly; this rerun was done in the author's workspace, not by an independent analyst."),

("h1", "Results"),
("h2", "Agreement-optimal cut-offs"),
("p", "Luminal B made up 26.1%, 38.9% and 29.5% of luminal tumors in TCGA-BRCA, METABRIC and SCAN-B. The kappa-optimal "
 "P2 cut-off lay at the 74th, 59th and 71st percentiles of the stratum (Fig. 1), with peak kappa 0.654, 0.666 and "
 "0.724. Within luminal tumors the optima were the 74.5th, 59.2nd and 73.3rd percentiles, within three points of 100 "
 "minus the luminal B share (73.9, 61.1 and 70.5): the kappa optimum called about the luminal B share positive."),
("h2", "Movement with prevalence and the binormal model"),
("p", "As the luminal B share of the derivation set rose from 15% to 65%, the kappa-optimal P2 cut-off fell by 0.39, "
 "0.38 and 0.36 luminal A quantile points per point of share (Table 3; Fig. 2a), and the accuracy-optimal cut-off by "
 "0.41 to 0.47. Proportion matching, which fixes the share called positive and is therefore the definitional "
 "reference, fell by 0.28 to 0.32; kappa and accuracy moved further. The Youden cut-off and target-weighted kappa did "
 "not move (slopes -0.01 to 0.02), as the design requires. The movement was steeper above 45% luminal B (0.44 to 0.51 "
 "against 0.24 to 0.39 for kappa; post hoc). The binormal model fitted closely (R2 0.977 to 0.997; variance ratio "
 "intervals included 1 in all cohorts) and predicted the slopes within 0.089 for kappa and 0.057 for accuracy, meeting "
 "the registered criterion. MKI67 moved more (kappa 0.33 to 0.54) and the model again followed it (largest difference "
 "0.13), although in METABRIC its variance ratio was 0.76 (95% interval 0.65 to 0.88). The gene-disjoint score P3 met "
 "its registered criteria, and in the two further cohorts the kappa optimum moved by 0.26 to 0.53 points per point of "
 "share (exploratory)."),
("h2", "Case mix against sampling variation"),
("p", "In sets of 400 tumors, case mix accounted for 62%, 54% and 65% of the variance of the kappa-derived cut-off over "
 "luminal B shares of 25% to 65% (Table 4; Fig. 2b), and for 33%, 28% and 40% over 35% to 55%. Over the wide range the "
 "share was 42% to 44% for sets of 150 and 69% to 78% for sets of 1,000, because sampling variation shrinks as sets "
 "grow. Proportion matching was most exposed (85% to 87%), followed by accuracy (74% to 77%); for the Youden index and "
 "target-weighted kappa, case mix accounted for less than 1%."),
("h2", "Transfer and relabeling within cohorts"),
("p", "A kappa cut-off derived at 400 tumors landed on average 6.3 to 10.6 quantile points from the full-cohort kappa "
 "cut-off and labeled 5.3% to 8.7% of luminal tumors differently (Table 4; Fig. 2c). The Youden cut-off transferred "
 "with less error (4.5 to 5.4 points), and its mean kappa against PAM50 was higher than that of derived kappa "
 "cut-offs in METABRIC (0.651 against 0.644) and lower in TCGA-BRCA (0.598 against 0.608) and SCAN-B (0.676 against "
 "0.682). Kappa weighted to the true target share gave the smallest error (3.2 to 3.9 points) and a mean kappa within "
 "0.013 of the best attainable, and it stayed better than plain kappa when the target share was misstated by up to 10 "
 "points in either direction. The kappa cut-offs derived at 25% and 65% luminal B labeled differently 101 of 573 "
 "patients in TCGA-BRCA (17.6%), 227 of 1,397 in METABRIC (16.2%) and 404 of 2,425 in SCAN-B (16.7%)."),
("h2", "Transfer between natural subgroups"),
("p", "The tumor-size split gave the largest difference in case mix: 23.7% luminal B among 1,460 tumors of 20 mm or "
 "less and 42.3% among 648 larger tumors (Table 5; Fig. 3a). From small to large tumors, plain kappa landed 4.8 "
 "quantile points from the target optimum and target-weighted kappa 11.7 (7.0 with the regional share); from large to "
 "small tumors, the errors were 3.0 against 1.4 (1.3). The registered criterion was therefore not met. Within each "
 "subtype the score was higher in large tumors (mean difference 0.14 standardized units for luminal A and 0.09 for "
 "luminal B; post hoc). Accuracy "
 "transferred with 2.8 to 3.1 points and the Youden cut-off with 5.9 to 14.2. The nodal and age splits differed by "
 "7.6 and 3.9 points in luminal B share, and the pattern was mixed."),
("h2", "Pathologist-scored Ki-67"),
("p", "The registered test was not met. In GSE81538 (147 luminal A and 85 luminal B tumors), kappa, accuracy and the "
 "Youden index all chose a consensus Ki-67 cut-off of 15% (kappa 0.530). Under Amendment 7 the kappa-optimal "
 "percentile moved by 0.62 points per point of share against a minimum of 0.70, and the median kappa threshold stayed "
 "at 15% at every share (Fig. 4). That test used the percentile scale later found to include a fixed-cut-off component "
 "(a threshold fixed at 15% would show 0.56). Consensus Ki-67 took 12 distinct values in 5-point steps. The "
 "minimum-misclassification threshold was 25% at shares of 15% and 25%, 15% at 35% to 55% and 10% at 65%, with case "
 "mix accounting for 64% of its variance (Fig. 2d; Table 4). In the full set weighted to 25% and 65% luminal B, its "
 "near-optimal regions (30% to 35% and 10% to 15%) did not overlap. Proportion matching moved from 25% to 15%. The binormal model, fitted to five "
 "points (R2 0.90), predicted kappa-optimal thresholds of 20% and 15% at 25% and 65% luminal B (difference 5 points, "
 "95% interval 0 to 10) and accuracy-optimal thresholds of 25% and 10% (Fig. 3b)."),
("h2", "Published cut-offs"),
("p", "Seven studies met the review criteria and one was provisionally eligible (Table 6). Among studies against PAM50, "
 "luminal B made up 27.6% [@holm2021] to 62.8% [@dixpeek2023] and optima ranged from 13% to 25%. Too few used a "
 "prevalence-dependent criterion for the registered regression, so the review is descriptive. In the one study that "
 "reported two criteria on the same tumors, maximum concordance chose 25% and the prevalence-free positive likelihood "
 "ratio 20% [@chen2016], and several studies justified a threshold by the subtype proportions it produced "
 "[@dixpeek2023; @maisonneuve2014; @lundgren2019]."),

("h1", "Discussion"),
("p", "A cut-off chosen to reproduce a reference standard carries the prevalence of the series in which it was chosen. "
 "Here the kappa-optimal proliferation cut-off fell by about 0.4 luminal A quantile points for each point of luminal B "
 "share, a binormal model predicted this within 0.09, and in sets of a few hundred tumors case mix explained about a "
 "quarter to two thirds of the variation in derived cut-offs, depending on the range of case mix. Cut-offs derived at the "
 "two ends of the published range labeled about one patient in six differently."),
("p", "Part of this follows from definitions. A kappa optimum calls roughly the reference prevalence positive, and "
 "under a binormal model the accuracy optimum depends only on the separation of the groups and the prevalence. "
 "Proportion matching, which moves by definition, gives the reference slope, and kappa and accuracy moved further. "
 "What the data add is the size of the movement for a decision that guides chemotherapy, its weight against sampling "
 "variation, and the finding that the model predicts it, so a study that reports its criterion, prevalence and "
 "separation can be placed on a common scale [@feinstein1990; @byrt1993; @leeflang2013]."),
("p", "The natural-subgroup test shows the limit of that scale. Large tumors differed from small ones in the score "
 "distribution within each subtype as well as in prevalence, and reweighting for prevalence alone overshot in one "
 "direction while it helped in the other. Within-subtype resampling therefore measures the prevalence component only, "
 "and real transfer between laboratories adds spectrum [@brenner1997] and analytical variation [@dowsett2011; "
 "@polley2013]. The transfer errors and relabeling reported here are lower bounds for practice, and reweighting is not "
 "a correction for a threshold moved between populations."),
("p", "The effect still explains part of the spread of published Ki-67 thresholds. The minimum-misclassification "
 "criterion of Cheang and colleagues [@cheang2009] moved most on pathologist-scored Ki-67, and proportion matching, "
 "used to justify several thresholds [@dixpeek2023; @maisonneuve2014; @lundgren2019], moves by design, as does Swedish "
 "guidance that recalibrates cut-offs so that one third of cases are Ki-67-high [@brueffer2018]. For kappa, the "
 "model implies a shift of about 5 Ki-67 points across the published range of case mix, which scores recorded in "
 "5-point steps cannot show; the kappa optimum did not move in these data, and a definitive test needs continuous "
 "Ki-67 scores paired with PAM50 calls, and none was found in public data."),
("p", "The choice of criterion involves a trade-off. The Youden cut-off is free of prevalence and transferred with "
 "less error within cohorts, but it equals the accuracy-optimal cut-off only at 50% prevalence, and its empirical "
 "estimate is noisier [@fluss2005]. Between natural subgroups accuracy transferred best in most comparisons, although it "
 "moved most with prevalence. No criterion was best everywhere, so the derivation criterion and population matter as much as the "
 "number."),
("p", "The study has limitations. The first question arose after the optima were inspected, Amendments 2 to 6 were "
 "posted after their analyses, and Amendments 11 and 12 were written with earlier results known; registration "
 "protects their analyses, not the choice to run them. The work has a single author, and pre-registration does not "
 "remove the risk of unconscious choices in what was asked. PAM50 calls carry their own error and vary with platform, "
 "so agreement here is agreement with the calls supplied with each dataset. The registered test in the further cohorts "
 "was not done because of a specification error, the published studies were too few for the registered regression, "
 "the search preceded registration, and first-pass screening and extraction were assisted by a language model."),
("p", "Three practical rules follow. A derivation study should report its criterion, the luminal B share of its "
 "derivation set and the cut-off as a quantile of the reference-negative distribution [@remark2006]. A laboratory "
 "choosing between published thresholds should prefer one derived in a population close to its own in both "
 "prevalence and tumor spectrum. A threshold intended to transfer should be validated outside the derivation set, "
 "because optimal cut-offs chosen in the same data are unstable [@altman1994]. In conclusion, agreement-optimized "
 "proliferation cut-offs shift with the case mix of the derivation series, predictably for prevalence and less "
 "predictably for spectrum, and reporting the criterion and the case mix with any threshold would show when it is "
 "unlikely to transfer."),
]

ACK = ("The author thanks the TCGA Research Network, the METABRIC consortium and the SCAN-B investigators for making "
       "their data publicly available, and Soad M. Elwirfli and Raja A. Aljibali (Department of Forensic Sciences, "
       "Faculty of Biomedical Sciences, University of Benghazi) for independent screening and for checking the values "
       "extracted from published studies.")

STATEMENTS = [
("Author contributions", "Abdelmuhsen M. Abusneina conceived and designed the study, specified and verified all analyses, "
 "interpreted the results, and wrote and approved the manuscript."),
("Funding", "This research did not receive any specific grant from funding agencies in the public, commercial, or "
 "not-for-profit sectors."),
("Declarations of interest", "None."),
("Ethics approval and consent", "This study used only publicly available, de-identified data (TCGA-BRCA, METABRIC, "
 "SCAN-B, GSE81538, GSE25066 and SMC 2018). The original studies obtained ethics approval and informed consent; no new "
 "approval was required."),
("Data availability", "All cohort data are public: TCGA-BRCA PanCancer Atlas, METABRIC and SMC 2018 through cBioPortal "
 "(https://www.cbioportal.org), and SCAN-B and GSE25066 through the Gene Expression Omnibus (GSE96058, GSE81538 and "
 "GSE25066). The analysis code, frozen protocol documents, error logs, result tables and literature-review records are "
 "at https://github.com/Abusneina/proliferation-cutoffs-case-mix and archived at Zenodo (DOI to be added for release "
 "v2.1). Registrations: literature protocol https://osf.io/pc9wm; Amendment 7 https://osf.io/p5hb7; Amendments 8 and 9 "
 "https://osf.io/su2hg; Amendment 10 https://osf.io/db7a8; Amendment 11 https://osf.io/vhg4s; Amendment 12 "
 "https://osf.io/ezmdn. All frozen documents, error logs and freeze records are at https://osf.io/cwkd9."),
("Declaration of generative AI and AI-assisted technologies in the manuscript preparation process",
 "During the preparation of this work the author used Claude (Anthropic) to write the analysis code, for the first "
 "pass of literature screening and extraction, and to draft and edit the text. The author specified every analysis "
 "before it was run; every number in the text and tables was traced to the output files of the archived scripts, "
 "and all deposited tables were regenerated from the public data with the archived release. A second person screened the "
 "literature independently and a third checked the extracted values. The author edited the content as needed and "
 "takes full responsibility for the content of the publication."),
]
