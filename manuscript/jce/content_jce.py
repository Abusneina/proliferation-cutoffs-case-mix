# Manuscript content for the Journal of Clinical Epidemiology. [@key] tokens are numbered by build.py.
TITLE = ("Case mix of the derivation series and Ki-67 cut-offs for luminal A versus luminal B breast cancer: "
         "a predictive model and a correction")
RUNNING = "Case mix and Ki-67 cut-offs"

ABSTRACT_SECTIONS = [
("Introduction", "Laboratories without multigene assays separate luminal A from luminal B breast cancer with a Ki-67 "
 "cut-off, and published cut-offs range from 13% to 25%. Most derivation studies choose the value that best reproduces "
 "PAM50, a criterion that depends on the prevalence of luminal B in the derivation series. We measured how far case mix "
 "moves such cut-offs, compared it with sampling variation, and tested whether the shift can be predicted and corrected."),
("Methods", "In estrogen receptor-positive, HER2-negative tumors from TCGA-BRCA (n = 573), METABRIC (n = 1,397) and "
 "SCAN-B (n = 2,425), cut-offs for an 18-gene proliferation score were derived against PAM50 by six criteria in "
 "derivation sets of 150 to 1,000 tumors resampled to luminal B shares of 15% to 65%, under a registered protocol. "
 "A binormal model fitted to each cohort predicted the shift. Pathologist-scored Ki-67 was examined in GSE81538 "
 "(232 luminal tumors)."),
("Results", "The kappa-optimal cut-off fell by 0.36 to 0.39 luminal A quantile points per point of luminal B share, "
 "and the binormal model predicted this slope within 0.09 (registered criterion met). In derivation sets of 400 tumors, "
 "case mix accounted for 54% to 65% of the variance of kappa-derived cut-offs and 85% to 87% for proportion matching, "
 "against less than 1% for the Youden index. Cut-offs derived at 25% and at 65% luminal B gave different labels to 16% "
 "to 18% of patients. Reweighting the derivation set to the luminal B share of the target population reduced transfer "
 "error from 6.3-10.6 to 3.2-3.9 quantile points. For pathologist-scored Ki-67, the kappa optimum stayed at 15%, "
 "whereas the minimum-misclassification optimum fell from 25% to 10% as the share rose from 15% to 65%."),
("Discussion", "Agreement-optimized cut-offs carry the case mix of the series that derived them, by an amount that can "
 "be predicted from the separation of the two groups and largely removed by reweighting. Derivation studies should "
 "report the criterion and the prevalence of the derivation set, and a threshold derived in a series with a different "
 "case mix should not be adopted without correction."),
]
ABSTRACT = " ".join(t for _, t in ABSTRACT_SECTIONS)

WHAT_IS_NEW = [
("Key findings", "Kappa-, accuracy- and proportion-based cut-offs for luminal B breast cancer move with the luminal B "
 "share of the derivation set, by an amount a binormal model predicts; at a few hundred tumors this explains more of "
 "their variation than sampling does, and it changes the label of about one patient in six."),
("What this adds to what is already known", "The prevalence dependence of agreement statistics is known; this study "
 "measures its size for a cut-off that guides chemotherapy, separates it from sampling variation, and shows that "
 "reweighting the derivation set to the target prevalence removes most of it."),
("What are the implications and what should change now", "Studies that derive a diagnostic cut-off against a "
 "reference standard should report the criterion and the prevalence of the derivation set, and users should prefer a "
 "threshold derived at a prevalence close to their own or reweight."),
]

KEYWORDS = "Ki-67; PAM50; Breast neoplasms; Cut-off; Case mix; Prevalence; Kappa"

BODY = [
("h1", "Introduction"),
("p", "The distinction between luminal A and luminal B disease guides adjuvant chemotherapy in estrogen receptor "
"(ER)-positive, HER2-negative breast cancer. Where multigene assays are unavailable, it is made with an "
"immunohistochemical surrogate in which the Ki-67 labeling index separates the two groups [@goldhirsch2011; "
"@goldhirsch2013; @coates2015]. The threshold has never settled. Cheang and colleagues derived 13.25% against PAM50 "
"[@cheang2009], later definitions added progesterone receptor [@prat2013] or moved to 20% and above [@goldhirsch2013; "
"@coates2015], and the International Ki67 Working Group accepts only values of 5% or less and 30% or more [@nielsen2021]. "
"Studies that derive a local threshold against PAM50 report 13% to 25% [@fernandez2017; @lopez2024; @dixpeek2023], and "
"many laboratories, including ours, still decide with the surrogate alone [@abusneina2026]."),
("p", "The usual explanation for the spread is analytical: antibody, platform and counting method change the number a "
"laboratory reports [@dowsett2011; @polley2013]. A second explanation has received less attention. Most derivation "
"studies choose the cut-off that maximizes agreement with the reference, through kappa, accuracy or concordance, or the "
"value that reproduces the reference subtype proportions, and these criteria depend on prevalence [@feinstein1990; "
"@byrt1993; @leeflang2013]. The Youden index does not include prevalence directly [@youden1950], although it can vary "
"with spectrum [@brenner1997]. The principle is long established [@metz1978], but we found no study that has measured "
"its size for Ki-67 cut-offs derived against PAM50, compared it with sampling variation, or asked how much of the "
"published spread it explains."),
("p", "We studied the question in three public cohorts in which the proliferation measure and the PAM50 reference come "
"from the same RNA profile, so analytical variation is absent. We measured how far cut-offs derived by six criteria "
"move with the luminal B share of the derivation set, compared that movement with sampling variation at the sizes of "
"published studies, tested a binormal model of it, evaluated a reweighting correction, counted the patients whose "
"label changes, and repeated the analysis on pathologist-scored Ki-67."),

("h1", "Methods"),
("h2", "Design and registration"),
("p", "This was a retrospective analysis of public cohorts with a supporting review of published studies, reported "
"following REMARK [@remark2006] (checklist in Online Resource 2). Each analysis was specified in a dated, frozen "
"amendment to a protocol registered on the Open Science Framework (OSF) before it was run; analyses not specified in "
"advance are labeled post hoc. The question arose when the first two cohorts were inspected; the proliferation gene "
"list and Amendments 2 to 6 were posted after their analyses, and their timing rests on the author's file records, "
"whereas Amendments 7 to 10 were posted before theirs. Amendment 11, which specifies the comparison of criteria, the binormal "
"model and the relabelling analysis reported here, was written after all earlier results were known, then frozen with "
"its script and registered (osf.io/vhg4s) before it was run. Six error logs record mistakes and their handling. The "
"full sequence is given in Online Resource 1."),
("h2", "Cohorts and scores"),
("p", "TCGA-BRCA (RNA sequencing) [@hoadley2018] and METABRIC (microarray) [@curtis2012; @pereira2016] were obtained "
"from cBioPortal [@cerami2012], and SCAN-B from the Gene Expression Omnibus (GSE96058; RNA sequencing) "
"[@brueffer2018]. Each stratum comprised ER-positive, HER2-negative tumors with the PAM50 calls supplied with the data: "
"573, 1,397 and 2,425 patients, of whom 490, 1,105 and 2,116 were luminal A or B (Table 1). The primary score, P2, was "
"the mean standardized expression of the 18 PAM50 proliferation genes other than MKI67 [@parker2009]; P1 was MKI67 "
"alone. Genes were standardized within each cohort's stratum."),
("h2", "Derivation criteria and scale"),
("p", "Tumors above a cut-off were called luminal B-like. Six criteria for choosing the cut-off against PAM50 were "
"compared: maximum Cohen's kappa; minimum misclassification (maximum accuracy), the criterion of Cheang and colleagues "
"[@cheang2009]; proportion matching, the lowest cut-off calling no more tumors positive than the luminal B share; "
"maximum Youden index; maximum kappa after weighting luminal A and B equally, which equals the Youden index and served "
"as a code check; and maximum kappa after weighting the derivation set to the luminal B share of the target population. "
"Candidate cut-offs were the observed values between the 5th and 95th percentiles, and ties went to the lowest value. "
"Because a laboratory transfers the value of a cut-off rather than its percentile, cut-offs were expressed as quantiles "
"of the full-cohort luminal A distribution."),
("h2", "Resampling design and outcomes"),
("p", "For each cohort and score, derivation sets of 150, 400 and 1,000 tumors were drawn with replacement within "
"subtype at luminal B shares of 15% to 65% in steps of 10 points, 500 times per cell. The range covers published "
"derivation studies, whose shares lie between 27.6% and 62.8% and whose sizes range from 71 to 1,029 tumors (Table 3). "
"Sampling within subtype fixes each subtype's score distribution, so any movement is caused by case mix alone; the "
"Youden cut-off therefore cannot move except by sampling noise, and its stability is not evidence in itself. The "
"case-mix slope was the change in the median cut-off per point of luminal B share (n = 1,000). The variance of the "
"derived cut-off over shares of 25% to 65% was split into the variance of the means at each share (case mix) and the "
"mean variance within shares (sampling). Transfer error was the root-mean-square difference (RMSE) between the derived "
"cut-off and the same criterion applied to the full cohort, with the percentage of tumors labeled differently and the "
"kappa in the full cohort. Relabelling was the percentage of the stratum labeled differently by the median kappa "
"cut-offs derived at 25% and at 65% luminal B. An earlier registered analysis measured the movement on a percentile "
"scale that also moves when the share changes (Error Log 5): its registered slopes of 0.89 to 1.12 included 0.44 to "
"0.70 that a fixed cut-off would produce, and the score-unit analysis replaces it (Online Resource 4)."),
("h2", "Binormal model"),
("p", "A binormal receiver operating characteristic model [@metz1978] was fitted to each cohort by least squares of "
"probit(sensitivity) on probit(1 - specificity) over values between 0.05 and 0.95. The model gives the population "
"cut-off of each criterion at any luminal B share, and from it a predicted slope. Amendment 11 fixed one criterion: for "
"P2, the predicted slope had to lie within 0.10 quantile points per point of share of the resampled slope for both "
"kappa and accuracy in all three cohorts. Under equal variances the accuracy-optimal cut-off is c = d/2 + ln[(1 - p)/p]/d, "
"where d is the separation in luminal A standard deviations and p the luminal B share."),
("h2", "Additional analyses"),
("p", "Patients between the kappa-optimal P2 cut-offs of TCGA-BRCA and METABRIC (59th and 74th percentiles) formed a "
"discordant group whose outcome was compared with stable groups in Cox models, with equivalence bounds of 0.67 to 1.50 "
"fixed in advance; endpoints were the progression-free interval in TCGA-BRCA, disease-specific survival in "
"METABRIC and overall survival in SCAN-B, with adjustment for age and stage (age, tumor size and nodal group in "
"SCAN-B). GSE81538 provided 232 PAM50 luminal tumors with "
"Ki-67 scored centrally by three pathologists [@brueffer2018]; Amendment 7 (osf.io/p5hb7) tested the mechanism on "
"consensus Ki-67, and Amendment 11 repeated the comparison of criteria with derivation sets of 150 and 232 tumors. A "
"score sharing no gene with PAM50 (P3; meta-PCNA genes [@venet2011] without PAM50 genes) and two further cohorts "
"(GSE25066 [@hatzis2011]; SMC 2018 [@kan2018]) were examined under Amendments 8 and 10. Published studies that derived "
"a Ki-67 cut-off against a multigene assay were sought under a registered protocol [@osfprotocol], screened by two "
"reviewers, and coded by criterion (Online Resource 3). Analyses used Python; all data were public and de-identified."),

("h1", "Results"),
("h2", "Agreement-optimal cut-offs"),
("p", "Luminal B made up 26.1%, 38.9% and 29.5% of luminal tumors in TCGA-BRCA, METABRIC and SCAN-B. The kappa-optimal "
"P2 cut-off lay at the 74th, 59th and 71st percentiles of the stratum (Fig. 1), with peak kappa 0.654, 0.666 and 0.724. "
"Within luminal tumors the optima were the 74.5th, 59.2nd and 73.3rd percentiles, within three points of 100 minus the "
"luminal B share (73.9, 61.1 and 70.5): the kappa optimum called about the luminal B share positive."),
("h2", "Movement with case mix and the binormal model"),
("p", "As the luminal B share of the derivation set rose from 15% to 65%, the kappa-optimal P2 cut-off fell by 0.39, "
"0.38 and 0.36 luminal A quantile points per point of share in TCGA-BRCA, METABRIC and SCAN-B (Table 2; Fig. 4a), and "
"the accuracy-optimal cut-off by 0.41 to 0.47. Proportion matching fell by 0.28 to 0.32. The Youden cut-off and kappa "
"weighted to the target share did not move (slopes -0.01 to 0.03), as the design requires. The movement was steeper "
"above a share of 45% than below it (0.44 to 0.51 against 0.24 to 0.39 for kappa; post hoc). The binormal model "
"predicted the slopes closely: for P2 the difference was at most 0.089 for kappa and 0.057 for accuracy, so the "
"registered criterion was met in all three cohorts. MKI67, which separates the subtypes less well, moved more (kappa "
"0.33 to 0.54), and the model again followed it (largest difference 0.13). The gene-disjoint score P3 met its "
"registered criteria, and in the two further cohorts the kappa optimum moved by 0.26 to 0.53 points per point of share "
"(exploratory; Online Resource 4)."),
("h2", "Case mix against sampling variation"),
("p", "In derivation sets of 400 tumors with luminal B shares spread over 25% to 65%, case mix accounted for 62%, 54% and "
"65% of the variance of the kappa-derived cut-off (Table 4; Fig. 4b). The share was 42% to 44% for sets of 150 tumors "
"and 69% to 78% for sets of 1,000, because sampling variation shrinks as sets grow while the case-mix component does "
"not. Proportion matching was the most exposed criterion (85% to 87% at 400 tumors), followed by accuracy (74% to 77%). "
"For the Youden index and for target-weighted kappa, case mix accounted for less than 1%."),
("h2", "Transfer and a correction"),
("p", "A kappa cut-off derived at 400 tumors landed on average 6.3 to 10.6 quantile points from the cut-off the same "
"criterion gave in the full cohort, and labeled 5.3% to 8.7% of luminal tumors differently (Table 4; Fig. 4c). The "
"Youden cut-off transferred with less error (4.5 to 5.4 points; 3.3% to 4.6% of tumors), but its mean kappa against "
"PAM50 was higher only in METABRIC (0.651 against 0.644) and lower in TCGA-BRCA (0.598 against 0.608) and SCAN-B "
"(0.676 against 0.682), because these cohorts have fewer than 50% luminal B tumors. Target-weighted kappa gave the "
"smallest transfer error (3.2 to 3.9 points; 2.3% to 3.4% of tumors) and the highest mean kappa (0.643, 0.655 and "
"0.716), within 0.013 of the best attainable in each cohort."),
("h2", "Patients whose label depends on the cut-off"),
("p", "The kappa cut-offs derived at 25% and at 65% luminal B gave different labels to 101 of 573 patients in TCGA-BRCA "
"(17.6%), 227 of 1,397 in METABRIC (16.3%) and 404 of 2,425 in SCAN-B (16.7%); 30.0% of the 404 SCAN-B patients had "
"received chemotherapy. The discordant group between the two observed optima held 15% of each cohort. Its outcomes "
"were intermediate (Fig. 2): stable luminal A-like patients had lower risk in METABRIC (hazard ratio 0.66, 95% CI 0.50 "
"to 0.86), and equivalence with stable luminal B-like patients was not shown."),
("h2", "Pathologist-scored Ki-67"),
("p", "In GSE81538 (147 luminal A and 85 luminal B tumors), kappa, accuracy and the Youden index all chose a consensus "
"Ki-67 cut-off of 15% (kappa 0.530). The registered test of Amendment 7 was not met: the kappa-optimal percentile moved "
"by 0.62 points per point of share against a minimum of 0.70, and the median kappa threshold stayed at 15% at every "
"share (Fig. 3). Ki-67 here is recorded in 5-point steps, and simulations showed that the coarse, tied scores account "
"for the shortfall. The comparison of criteria showed that the result depends on the criterion (Fig. 4d; Table 4). The "
"minimum-misclassification threshold was 25% at shares of 15% and 25%, 15% at 35% to 55% and 10% at 65%, with case mix "
"accounting for 64% of its variance; proportion matching moved from 25% to 15%."),
("h2", "Published cut-offs"),
("p", "Seven studies met the review criteria and one was provisionally eligible (Table 3). Among studies against PAM50, "
"case mix ranged from 27.6% [@holm2021] to 62.8% luminal B [@dixpeek2023] and optima from 13% to 25%. Too few used a "
"prevalence-dependent criterion for the registered regression. In the one study that reported two criteria on the "
"same tumors, maximum concordance chose 25% and the prevalence-free positive likelihood ratio chose 20% [@chen2016], "
"and several studies justified a threshold by the subtype proportions it produced [@dixpeek2023; @maisonneuve2014; "
"@lundgren2019]."),

("h1", "Discussion"),
("p", "A cut-off chosen to reproduce a reference standard carries the case mix of the series in which it was chosen. "
"Here the kappa-optimal proliferation cut-off fell by about 0.4 luminal A quantile points for each point of luminal B "
"share, a binormal model predicted this within 0.09, and once a derivation set reached a few hundred tumors case mix "
"explained more of the variation in derived cut-offs than sampling did. Cut-offs derived at the two ends of the "
"published range of case mix labeled about one patient in six differently, and reweighting the derivation set to the "
"target prevalence removed most of the transfer error."),
("p", "That agreement statistics depend on prevalence is old [@feinstein1990; @byrt1993; @metz1978]. What this study "
"adds is the size of the effect for a decision that guides chemotherapy, its separation from sampling variation, and a "
"practical correction. The size is predictable: under a binormal model the accuracy-optimal cut-off depends only on "
"the separation of the groups and the prevalence, and the kappa and proportion-matching cut-offs behave similarly. A "
"study that reports its criterion, its prevalence and the separation of its score can therefore be placed on a common "
"scale. The same reasoning applies to any cut-off derived by maximizing agreement with a reference standard."),
("p", "The effect also explains part of the disagreement among published Ki-67 thresholds. The minimum-misclassification "
"rule used by Cheang and colleagues [@cheang2009] moved most on pathologist-scored Ki-67, from 25% to 10%, a range that "
"covers every published threshold. Proportion matching, used to justify several thresholds [@dixpeek2023; "
"@maisonneuve2014; @lundgren2019], and Swedish guidance that recalibrates cut-offs so that one third of cases are "
"Ki-67-high [@brueffer2018] fix the proportion called positive and so move with case mix by design. Analytical "
"variation between laboratories [@dowsett2011; @polley2013] was absent here only because score and reference came from "
"the same profile; case mix adds to it."),
("p", "The choice of criterion involves a trade-off. The Youden cut-off is free of prevalence and transferred with less "
"error, but it maximizes agreement only at a prevalence of 50%, and its sampling variation was larger in two of the "
"three cohorts, as expected for empirical Youden estimates [@fluss2005]. Target-weighted kappa keeps the agreement "
"criterion and removes its dependence on the derivation series, at the cost of needing an estimate of the target "
"prevalence, which can come from a population-based series of the same region."),
("p", "On pathologist-scored Ki-67 the kappa optimum did not move. With scores in 5-point steps, a shift of about 2 "
"points for a 10-point difference in luminal B share, as the RNA cohorts imply, cannot appear; a definitive test needs "
"continuous Ki-67 scores paired with PAM50 calls, and we found no public cohort of that kind."),
("p", "The study has limitations. The question arose after the first optima were inspected, and Amendment 11 was written "
"with earlier results known; its registration protects its own analyses, not the choice to run them. Resampling within "
"subtype holds each subtype's score distribution fixed, whereas real series also differ in spectrum [@brenner1997], so "
"the measured component is the part caused by prevalence alone. The registered test in the further cohorts was not done "
"because of a specification error, the endpoints differed between cohorts, treatment was not modeled, and too few "
"published studies qualified for the registered regression. The literature search preceded registration, and the "
"first pass of screening and extraction was assisted by a language model, with a second person checking the values."),
("p", "Three practical rules follow. A derivation study should report its criterion, the prevalence of its derivation "
"set and the cut-off as a quantile of the reference-negative distribution [@remark2006]. A user choosing between "
"published thresholds should prefer one derived at a prevalence close to its own, or reweight. A threshold intended to "
"transfer should be derived with a prevalence-robust or target-weighted criterion and validated outside the derivation "
"set, because optimal cut-offs chosen in the same data are unstable [@altman1994]. In conclusion, agreement-optimized "
"cut-offs for luminal A versus luminal B breast cancer shift with the case mix of the derivation series, predictably and "
"correctably, and reporting the criterion and the case mix with any threshold would show when it is unlikely to "
"transfer."),
]

ACK = ("The author thanks the TCGA Research Network, the METABRIC consortium and the SCAN-B investigators for making their "
"data publicly available, and Soad M. Elwirfli and Raja A. Aljibali (Department of Forensic Sciences, Faculty of "
"Biomedical Sciences, University of Benghazi) for independent screening and for checking the values extracted from "
"published studies.")

STATEMENTS = [
("Author contributions", "Abdelmuhsen M. Abusneina conceived and designed the study, specified and verified all "
 "analyses, interpreted the results, and wrote and approved the manuscript."),
("Funding", "This research did not receive any specific grant from funding agencies in the public, commercial, or "
 "not-for-profit sectors."),
("Declarations of interest", "None."),
("Ethics approval and consent", "This study used only publicly available, de-identified data (TCGA-BRCA, METABRIC, "
 "SCAN-B, GSE81538, GSE25066 and SMC 2018). The original studies obtained ethics approval and informed consent; no new "
 "approval was required."),
("Data availability", "All cohort data are public: TCGA-BRCA PanCancer Atlas, METABRIC and SMC 2018 through cBioPortal "
 "(https://www.cbioportal.org), and SCAN-B and GSE25066 through the Gene Expression Omnibus (GSE96058, GSE81538 and "
 "GSE25066). The analysis code, frozen protocol documents, error logs, result tables and literature-review records are "
 "available at https://github.com/Abusneina/proliferation-cutoffs-case-mix (release v2.0) and archived at Zenodo "
 "(https://doi.org/10.5281/zenodo.23926714). The literature protocol is registered at "
 "https://osf.io/pc9wm, Amendment 7 at https://osf.io/p5hb7, Amendments 8 and 9 at https://osf.io/su2hg, Amendment 10 at "
 "https://osf.io/db7a8 and Amendment 11 at https://osf.io/vhg4s. All frozen documents, error logs and freeze records are "
 "posted at https://osf.io/cwkd9."),
("Declaration of generative AI and AI-assisted technologies in the manuscript preparation process",
 "During the preparation of this work the author used Claude (Anthropic) to write the analysis code, for the first "
 "pass of literature screening and extraction, and to draft and edit the text. After using this tool, the author "
 "specified every analysis in advance, reviewed every output and the text, edited the content as needed, and takes "
 "full responsibility for the content of the publication."),
]

LEGENDS = [
("Fig. 1", "Agreement with PAM50 and dependence of the optimal cut-off on case mix. (a, b) Cohen's kappa between the "
 "proliferation-defined luminal B call and PAM50 across cut-offs in TCGA-BRCA (a) and METABRIC (b). Solid line, 18-gene "
 "proliferation score; dashed line, MKI67 alone. Markers show the kappa-optimal cut-off for each score and shaded bands "
 "its bootstrap 95% confidence interval. (c) Kappa-optimal cut-off for the 18-gene score, as a percentile of the "
 "resampled luminal set, under resampling to fixed luminal B shares within each cohort (registered scale of Amendment 6); "
 "dotted line, 100 minus the imposed share. On this scale a cut-off that does not move has slopes of 0.65 to 0.70 for "
 "this score (Error Log 5). (d) Youden-optimal cut-off, as a quantile of luminal A, under the same resampling, which "
 "keeps it fixed by design. (e) Youden-optimal cut-off with bootstrap 95% confidence intervals, as a quantile of luminal "
 "A (filled markers, solid lines) and as a percentile of the whole stratum (open markers, dotted lines). Two-column width."),
("Fig. 2", "Kaplan-Meier estimates by group defined on the 18-gene score: disease-specific survival in METABRIC (a), "
 "progression-free interval in TCGA-BRCA (b) and overall survival in SCAN-B (c). Stable luminal A-like, at or below the "
 "59th percentile (solid line); discordant, between the 59th and 74th percentiles (short dashes); stable luminal B-like, "
 "above the 74th percentile (dash-dot). Numbers at risk are shown beneath each panel. TCGA-BRCA had 12 events in the "
 "discordant group, so panel b is descriptive. Two-column width."),
("Fig. 3", "Registered test of the cut-off mechanism in GSE81538 (consensus Ki-67, 232 luminal tumors; Amendment 7). (a) "
 "Kappa-optimal percentile against 100 minus the imposed luminal B share for simulated continuous scores (circles), the "
 "observed Ki-67 distributions resampled at N = 40,000 (triangles), a threshold fixed at 15% (dashed; post hoc) and the "
 "registered test (diamonds); dotted line, slope 1. (b) Youden cut-off for consensus Ki-67, as a quantile of luminal A. "
 "(c) Kappa-optimal Ki-67 threshold; line, median of 200 resamples; band, 2.5th to 97.5th percentile; dotted line, 15%. "
 "Two-column width."),
("Fig. 4", "Case mix, sampling and transfer of derived cut-offs (Amendment 11). (a) Median kappa-optimal cut-off for the "
 "18-gene score, as a luminal A quantile, in derivation sets of 1,000 tumors resampled to each luminal B share; bands, "
 "10th to 90th percentile of 500 resamples; dotted lines, binormal model prediction for each cohort. (b) Share of the "
 "variance of the derived cut-off due to case mix, over luminal B shares of 25% to 65%, by criterion (derivation sets of "
 "400 tumors). (c) Transfer error: root-mean-square difference, in luminal A quantile points, between the cut-off derived "
 "at 400 tumors and the same criterion applied to the full cohort. (d) Pathologist-scored consensus Ki-67 in GSE81538: "
 "median derived threshold by imposed luminal B share for three criteria (derivation sets of 232 tumors); markers are "
 "offset horizontally where lines coincide. Cohorts are distinguished by color, marker and line style or hatching. "
 "Two-column width."),
]

TABLE_TITLES = {
1: "Table 1 Analysis cohorts and agreement of the proliferation-defined luminal B call with PAM50",
2: "Table 2 Case-mix slope of the derived cut-off by criterion: resampled and predicted by the binormal model",
3: "Table 3 Published studies that derived a Ki-67 cut-off against a multigene reference",
4: "Table 4 Case mix against sampling variation, and transfer of derived cut-offs to the full cohort",
}
TABLE_NOTES = {
1: ("ER+/HER2-, estrogen receptor-positive, HER2-negative; PFI, progression-free interval; DSS, disease-specific "
    "survival; OS, overall survival. Luminal B share is the PAM50 luminal B proportion among PAM50 luminal tumors. "
    "Cut-offs are percentiles of the ER+/HER2- stratum; confidence intervals are from 2,000 bootstrap resamples. The last "
    "column gives the optimum as a percentile of the PAM50 luminal tumors and as a quantile of the luminal A "
    "distribution. 18-gene, PAM50 proliferation genes with MKI67 excluded."),
2: ("Slope: change in the median derived cut-off, in luminal A quantile points, per point of luminal B share, over imposed "
    "shares of 15% to 65% (derivation sets of 1,000 tumors, 500 resamples per share; Amendment 11). Negative values mean "
    "the cut-off falls as the share rises. Model: slope of the population cut-off under a binormal model fitted to each "
    "cohort. Registered criterion: for the 18-gene score, |resampled - model| <= 0.10 for kappa and accuracy in all three "
    "cohorts (met). The Youden cut-off cannot move under within-subtype resampling; its model slope is zero."),
3: ("P, prevalence-dependent criterion; Y, Youden-type; U, criterion not stated; ROR, risk of recurrence; RS, recurrence "
    "score. a Luminal B among PAM50 luminal tumors; the reported comparison was luminal A against all other subtypes. "
    "b Prolif surrogate in the STO-3 and Clinseq cohorts. c All subtypes, of which 196 PAM50 luminal; kappa was computed "
    "across the full IHC classification. d Share not at low risk. e Tumors <= 2 cm and > 2 cm; share at intermediate or "
    "high ROR. f High risk under traditional or TAILORx categories."),
4: ("RNA cohorts: 18-gene score, derivation sets of 400 tumors. Ki-67: consensus Ki-67 in GSE81538, derivation sets of "
    "232 tumors. Case-mix share: fraction of the variance of the derived cut-off explained by the imposed luminal B share "
    "(25% to 65%). RMSE: root-mean-square difference, in luminal A quantile points, from the same criterion applied to the "
    "full set. Relabelled: mean percentage of luminal tumors in the full set labeled differently from that criterion's "
    "full-set cut-off. Kappa: mean kappa against PAM50 in the full set (the best attainable is in parentheses for the "
    "kappa row). Target-weighted kappa uses the luminal B share of the full set."),
}
