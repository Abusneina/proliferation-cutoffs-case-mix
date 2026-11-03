# Manuscript content for Modern Pathology. [@key] tokens are numbered in order of first citation by build.py.
TITLE = ("Case mix of the derivation series shifts Ki-67 cut-offs for luminal A versus luminal B breast cancer: "
         "a predictive model and a correction")
RUNNING = "Case mix shifts Ki-67 cut-offs"

ABSTRACT = (
"Laboratories without multigene assays separate luminal A from luminal B breast cancer with a Ki-67 cut-off, and "
"published cut-offs range from 13% to 25%. Most derivation studies choose the value that best reproduces PAM50, a "
"criterion that depends on the luminal B share of the series. We measured how far case mix moves such cut-offs and "
"whether the shift can be predicted and corrected. In estrogen receptor-"
"positive, HER2-negative tumors from TCGA-BRCA (n = 573), METABRIC (n = 1,397) and SCAN-B (n = 2,425), cut-offs for an "
"18-gene proliferation score were derived against PAM50 by six criteria in derivation sets resampled to luminal B "
"shares of 15% to 65%, under registered protocols. Pathologist-scored Ki-67 was examined in GSE81538 (232 luminal "
"tumors). The kappa-optimal cut-off fell by 0.36 to 0.39 luminal A quantile points per point of luminal B share, and "
"a binormal model predicted this slope within 0.09 (registered criterion met). In derivation sets of 400 tumors, case "
"mix accounted for 54% to 65% of the variance of kappa-derived cut-offs and 85% to 87% for proportion matching, "
"against less than 1% for the Youden index. Cut-offs derived at 25% and at 65% luminal B gave different labels to 16% "
"to 18% of patients. Reweighting the derivation set to the luminal B share of the target population reduced transfer "
"error from 6.3-10.6 to 3.2-3.9 quantile points. For pathologist-scored Ki-67, the kappa optimum stayed at 15%, "
"whereas the minimum-misclassification optimum fell from 25% to 10% as the share rose from 15% to 65%. "
"Agreement-optimized proliferation cut-offs carry the case mix of the series that derived them, predictably and "
"correctably. Derivation studies should report the criterion and the luminal B share, and laboratories should not "
"adopt a threshold derived in a series whose case mix differs from their own.")

KEYWORDS = "Ki-67; PAM50; luminal breast cancer; cut-off; case mix; prevalence"

# (heading level, text) or ("p", text)
BODY = [
("h1", "Introduction"),
("p", "The distinction between luminal A and luminal B disease guides the use of adjuvant chemotherapy in estrogen "
"receptor (ER)-positive, HER2-negative breast cancer. Where multigene assays are unavailable or unaffordable, the "
"distinction is made with an immunohistochemical surrogate in which the Ki-67 labeling index separates the two groups "
"[@goldhirsch2011; @goldhirsch2013; @coates2015]. The threshold has never settled. Cheang and colleagues derived 13.25% "
"against PAM50 [@cheang2009], a later definition added a progesterone receptor criterion [@prat2013], the St Gallen panels "
"moved from 14% to 20% and then to a range of 20% to 29% [@goldhirsch2011; @goldhirsch2013; @coates2015], and the "
"International Ki67 Working Group now accepts only values of 5% or less and 30% or more for prognosis in early disease "
"[@nielsen2021]. Studies that derive a local threshold against PAM50 continue to report values from 13% to 25% "
"[@fernandez2017; @lopez2024; @dixpeek2023]. Laboratories in many regions, including ours, still make this decision with "
"the surrogate alone [@abusneina2026]."),
("p", "The usual explanation for the spread is analytical. Antibody, staining platform, field selection and counting "
"method all change the number a laboratory reports, and agreement between experienced laboratories is only moderate "
"[@dowsett2011; @polley2013]. A second explanation has received less attention. Most derivation studies choose the "
"cut-off that maximizes agreement with the genomic reference, through kappa, accuracy or concordance, or the value that "
"reproduces the reference subtype proportions. These criteria depend on prevalence [@feinstein1990; @byrt1993; "
"@leeflang2013]. The Youden index is computed from sensitivity and specificity alone, so prevalence does not enter it "
"directly [@youden1950], although both can still vary with the spectrum of the population [@brenner1997]. The "
"principle is long established [@feinstein1990; @byrt1993; @metz1978]. We found no study that has measured its size "
"for Ki-67 cut-offs derived against PAM50, compared it with ordinary sampling variation, or asked how much of the "
"published spread it can explain."),
("p", "We studied the question where analytical variation can be set aside: in three public cohorts, the proliferation "
"measure and the PAM50 reference come from the same RNA profile. The aims were to measure how far agreement-optimal "
"cut-offs move with the luminal B share of the derivation series; to compare that movement with sampling variation at "
"the sizes of published derivation studies and test whether a binormal model predicts it; to compare derivation "
"criteria for how well a cut-off transfers to another population, including a reweighting correction; to count the "
"patients whose label changes; to repeat the analysis on pathologist-scored Ki-67; and to look for the effect in "
"published derivation studies."),

("h1", "Materials and Methods"),
("h2", "Design and registration"),
("p", "This was a retrospective analysis of six public breast cancer cohorts and a supporting analysis of published "
"studies. Each analysis was specified in a dated, frozen amendment to a protocol registered on the Open Science "
"Framework (OSF) before it was run, and analyses that were not specified in advance are labeled post hoc. The question "
"arose when the first two cohorts were inspected, so the earliest amendments were written after those optima were "
"known; the proliferation gene list and Amendments 2 to 6 were posted on OSF after their analyses, and their timing "
"rests on the author's file records. Amendments 7 to 10 were posted before their analyses. Amendment 11, which "
"specifies the resampling comparison of derivation criteria, the binormal model and the relabelling analysis, was "
"written after all earlier results were known, frozen with its analysis script and registered (osf.io/vhg4s) before "
"it was run. Six error logs record mistakes in specification or execution and how each was handled. The sequence of "
"frozen documents, what was known when each was frozen, and the error logs are given in Online Resource 1. Reporting "
"follows the REMARK recommendations [@remark2006] (checklist, Online Resource 2)."),
("h2", "Cohorts and proliferation scores"),
("p", "TCGA-BRCA (PanCancer Atlas, RNA sequencing) [@hoadley2018] and METABRIC (Illumina HT-12 microarray) [@curtis2012; "
"@pereira2016] were obtained from cBioPortal [@cerami2012], and SCAN-B from the Gene Expression Omnibus (GSE96058; RNA "
"sequencing; 136 technical replicates excluded) [@brueffer2018]. Each analysis stratum comprised ER-positive, "
"HER2-negative tumors (definitions in Online Resource 1). PAM50 calls were those supplied with each dataset. The strata "
"comprised 573, 1,397 and 2,425 patients, of whom 490, 1,105 and 2,116 were PAM50 luminal A or B (Table 1). Two scores "
"were defined in advance. P1 was MKI67 expression alone. P2, the 18-gene score, was the mean standardized expression "
"of the 18 PAM50 proliferation genes other than MKI67 [@parker2009], so the two scores share no gene. Expression was "
"used on a log2 scale, and every gene was standardized within the stratum of its own cohort."),
("h2", "Derivation criteria and scale"),
("p", "Tumors with a score above a cut-off were called luminal B-like. Six criteria for choosing the cut-off against "
"PAM50 among luminal A and B tumors were compared: maximum Cohen's kappa; minimum misclassification (maximum "
"accuracy), the criterion used by Cheang and colleagues [@cheang2009]; proportion matching, the lowest cut-off that "
"calls no more tumors positive than the luminal B share of the series; maximum Youden index; maximum kappa after "
"weighting luminal A and B tumors equally, which is algebraically identical to the Youden index and served as a check "
"of the code; and maximum kappa after weighting the derivation set to the luminal B share of the target population. "
"Candidate cut-offs were the observed values between the 5th and 95th percentiles of the derivation set, and ties went "
"to the lowest value. A laboratory transfers the value of a cut-off, not its percentile, so each cut-off was expressed "
"in score units as a quantile of the full-cohort PAM50 luminal A distribution (luminal A quantile)."),
("h2", "Case-mix resampling"),
("p", "For each cohort and score, derivation sets of 150, 400 and 1,000 tumors were drawn with replacement within "
"subtype at imposed luminal B shares of 15%, 25%, 35%, 45%, 55% and 65%, 500 times per cell (Amendment 11). The range "
"covers the published derivation studies, whose luminal B shares lie between 27.6% and 62.8% (Table 3), and their "
"sizes, which range from 71 to 1,029 tumors. Sampling within subtype keeps the score distribution of each subtype "
"fixed, so any movement of a cut-off is caused by case mix alone; for the same reason the Youden cut-off cannot move "
"except by sampling noise, and its stability under this design is not evidence in itself. Four quantities were "
"computed. The case-mix slope was the change in the median cut-off, in luminal A quantile points, per point of "
"luminal B share (n = 1,000). The variance of the derived cut-off over shares of 25% to 65% was split into the "
"variance of the means at each share (case mix) and the mean variance within shares (sampling). Transfer error was "
"the root-mean-square difference between the derived cut-off and the same criterion applied to the full cohort, with "
"the percentage of luminal tumors labeled differently and the kappa against PAM50 in the full cohort. Relabelling was "
"the percentage of the whole ER-positive, HER2-negative stratum whose label differs between the median kappa-optimal "
"cut-offs derived at 25% and at 65% luminal B (n = 1,000)."),
("p", "An earlier amendment (Amendment 6) measured the same movement as the slope of the kappa-optimal percentile within "
"the resampled luminal set. On that scale a cut-off that does not move also changes its percentile when the share "
"changes, so the registered slopes mixed a scale component with real movement (Error Log 5). They are reported for "
"completeness, and the score-unit analysis above replaces them."),
("h2", "Binormal model"),
("p", "A binormal receiver operating characteristic model [@metz1978] was fitted to each cohort by least squares of "
"probit(sensitivity) on probit(1 - specificity) over values of both between 0.05 and 0.95. On the latent scale, "
"luminal A scores are standard normal and luminal B scores normal with mean a/b and standard deviation 1/b. The model "
"gives the population cut-off of each criterion at any luminal B share, and from it a predicted case-mix slope. "
"Amendment 11 fixed one criterion in advance: for P2, the predicted slope had to lie within 0.10 luminal A quantile "
"points per point of share of the resampled slope for both the kappa and the accuracy criteria in all three cohorts. "
"Under equal variances the accuracy-optimal cut-off has the closed form c = d/2 + ln[(1 - p)/p]/d, where d is the "
"separation in luminal A standard deviations and p the luminal B share, so its slope depends only on d and p."),
("h2", "Patients whose label depends on the cut-off"),
("p", "Before any outcome comparison, a discordant group was defined from the kappa-optimal P2 cut-offs of TCGA-BRCA and "
"METABRIC, the 59th and 74th percentiles. Patients at or below the 59th percentile were stable luminal A-like, those "
"above the 74th stable luminal B-like, and those between discordant; the same percentiles were carried into SCAN-B. "
"The endpoints were the progression-free interval in TCGA-BRCA [@liu2018], disease-specific survival in METABRIC and "
"overall survival in SCAN-B. Cox models with the discordant group as reference were adjusted for age and stage, or for "
"age, tumor size and nodal group in SCAN-B; grade entered only a sensitivity model. Equivalence required the 95% "
"confidence interval (CI) to lie within 0.67 to 1.50, fixed in advance. Estimates were pooled with fixed-effect and "
"DerSimonian-Laird models [@dersimonian1986]. Treatment was recorded only as received or not and was not modeled."),
("h2", "Pathologist-scored Ki-67"),
("p", "GSE81538 holds 405 SCAN-B tumors that do not overlap GSE96058, with PAM50 calls and Ki-67 stained centrally and "
"scored by three pathologists [@brueffer2018]. Eligible tumors had an ER consensus score of 1 to 3 and HER2 not "
"amplified; 232 of 256 were PAM50 luminal A or B. Amendment 7 (osf.io/p5hb7), registered before any value was "
"examined, tested the mechanism on consensus Ki-67 with slope criteria on the percentile scale. Amendment 11 repeated "
"the resampling comparison of derivation criteria on consensus Ki-67 with derivation sets of 150 and 232 tumors. The "
"series matrix used for this arm had no recorded checksum from the first download, so its identity was confirmed by "
"reproducing the Amendment 7 counts before the arm was run (Error Log 6)."),
("h2", "A score sharing no gene with PAM50, and independent cohorts"),
("p", "Amendment 8 (osf.io/su2hg) added P3, the median standardized expression of the meta-PCNA genes, the 1% of genes "
"most correlated with PCNA across normal tissues [@venet2011], without the 11 that belong to PAM50 (120 genes); "
"secondary scores used the same genes or the hallmark G2M set [@liberzon2015] without its PAM50 genes. Amendment 10 "
"(osf.io/db7a8) applied the same criteria to GSE25066, pretreatment biopsies on Affymetrix arrays [@hatzis2011], and to "
"SMC 2018, Korean tumors with RNA sequencing [@kan2018]."),
("h2", "Published derivation studies"),
("p", "Under a protocol registered on OSF [@osfprotocol], published studies were sought to ask whether the luminal B "
"share of a study population predicts the Ki-67 cut-off it reports as optimal. The database search was run before "
"registration, a deviation recorded in Online Resource 3. Two reviewers screened titles, abstracts and full texts "
"independently, and a third checked the extracted values. Eligible studies derived a Ki-67 cut-off within the study in "
"hormone receptor-positive, HER2-negative or luminal tumors against a multigene subtype assay or risk assay. Criteria "
"were coded as prevalence-dependent, Youden-type or unstated, and a formal regression required at least eight "
"prevalence-dependent studies against a subtype assay."),
("h2", "Software, sex and data"),
("p", "Analyses used Python (pandas, NumPy, SciPy, statsmodels, scikit-learn and matplotlib). Sex was recorded as female "
"for all patients in the TCGA-BRCA and METABRIC strata; SCAN-B and GSE81538 deposit no sex field, and the analysis "
"could not examine sex as a factor. All data were public and de-identified."),

("h1", "Results"),
("h2", "Cohorts and agreement-optimal cut-offs"),
("p", "The three strata included 4,395 patients (Table 1). Luminal B made up 26.1%, 38.9% and 29.5% of PAM50 luminal "
"tumors in TCGA-BRCA, METABRIC and SCAN-B. The kappa-optimal P2 cut-off lay at the 74th percentile of the stratum in "
"TCGA-BRCA (95% CI 64th to 79th), the 59th in METABRIC (54th to 67th) and the 71st in SCAN-B (68th to 74th) (Fig. 1a, "
"b). P2 agreed with PAM50 better than MKI67 alone in every cohort (peak kappa 0.654, 0.666 and 0.724 against 0.551, "
"0.446 and 0.609). Within luminal tumors the P2 optima were the 74.5th, 59.2nd and 73.3rd percentiles, within three "
"points of 100 minus the luminal B share (73.9, 61.1 and 70.5): the kappa optimum called about the luminal B share "
"positive. In score units the optima lay at the 91st, 85th and 94th luminal A quantiles, and the Youden cut-off at "
"the 82nd, 84th and 85th (Fig. 1e)."),
("h2", "Movement with case mix and the binormal model"),
("p", "As the luminal B share of the derivation set rose from 15% to 65%, the kappa-optimal P2 cut-off fell by 0.39, "
"0.38 and 0.36 luminal A quantile points per point of share in TCGA-BRCA, METABRIC and SCAN-B (Table 2; Fig. 4a), and "
"the accuracy-optimal cut-off by 0.41 to 0.47. Proportion matching fell by 0.28 to 0.32. The Youden cut-off and kappa "
"weighted to the target share did not move (slopes -0.01 to 0.03), as the design requires. The movement was steeper "
"above a share of 45% than below it (0.44 to 0.51 against 0.24 to 0.39 for kappa; post hoc), in line with the model. "
"The binormal model predicted the slopes closely: for P2 the difference was at most 0.089 for kappa and 0.057 for "
"accuracy, so the registered criterion was met in all three cohorts. For MKI67 the slopes were larger (kappa 0.33 to "
"0.54; accuracy 0.52 to 0.78), because MKI67 separates the subtypes less well, and the model again followed them "
"(largest difference 0.13). The registered percentile-scale slopes of Amendment 6 were 0.89 to 1.12, of which a "
"fixed cut-off would have produced 0.44 to 0.70 (Error Log 5)."),
("p", "With every PAM50 gene removed, P3 met the registered criteria of Amendment 8 in each cohort, with kappa-optimal "
"percentiles of 74, 59 and 68 against 73.9, 61.1 and 70.5, and it correlated closely with P2 (Spearman 0.95 to 0.97). "
"In the independent cohorts the registered test of Amendment 10 was not done, because the specified ER field covered "
"only 310 of 508 samples in GSE25066 (Error Log 4); in exploratory analyses of GSE25066 (71 luminal B tumors) and SMC "
"2018 (41), the kappa optimum moved by 0.26 to 0.53 luminal A quantile points per point of share (Online Resource 4)."),
("h2", "Case mix against sampling variation"),
("p", "In derivation sets of 400 tumors with luminal B shares spread over 25% to 65%, case mix accounted for 62%, 54% and "
"65% of the variance of the kappa-derived P2 cut-off in TCGA-BRCA, METABRIC and SCAN-B (Table 4; Fig. 4b). The share "
"was 42% to 44% for sets of 150 tumors and 69% to 78% for sets of 1,000, because sampling variation shrinks as sets "
"grow while the case-mix component does not. Proportion matching was the most exposed criterion (85% to 87% at 400 "
"tumors), followed by accuracy (74% to 77%). For the Youden index and for kappa weighted to the target share, case mix "
"accounted for less than 1%."),
("h2", "Transfer to another population and a correction"),
("p", "A kappa cut-off derived at 400 tumors landed on average 6.3 to 10.6 luminal A quantile points from the cut-off the "
"same criterion gave in the full cohort, and labeled 5.3% to 8.7% of luminal tumors differently (Table 4; Fig. 4c). The "
"Youden cut-off transferred with less error (4.5 to 5.4 points; 3.3% to 4.6% of tumors), but its mean kappa against "
"PAM50 was higher only in METABRIC (0.651 against 0.644) and lower in TCGA-BRCA (0.598 against 0.608) and SCAN-B "
"(0.676 against 0.682), because these cohorts have fewer than 50% luminal B tumors. Kappa weighted to the luminal B share of the target population "
"gave the smallest transfer error (3.2 to 3.9 points; 2.3% to 3.4% of tumors) and the highest mean kappa (0.643, 0.655 "
"and 0.716), within 0.013 of the best kappa attainable in each cohort. The 50:50-weighted kappa selected the same "
"cut-off as the Youden index in 99.5% of derivations, as expected."),
("h2", "Patients whose label depends on the cut-off"),
("p", "The median kappa cut-offs derived at 25% and at 65% luminal B gave different labels to 101 of 573 patients in "
"TCGA-BRCA (17.6%), 227 of 1,397 in METABRIC (16.3%) and 404 of 2,425 in SCAN-B (16.7%); 30.0% of the 404 SCAN-B "
"patients had received chemotherapy. The two observed kappa optima of TCGA-BRCA and METABRIC left 15% of each cohort in "
"the discordant group (86, 210 and 363 patients). Stable luminal A-like patients had lower risk than discordant "
"patients in METABRIC (hazard ratio 0.66, 95% CI 0.50 to 0.86); in SCAN-B the estimate was 0.77 (0.53 to 1.14) (Fig. "
"2). Stable luminal B-like patients had hazard ratios of 1.23 (0.92 to 1.63) and 1.20 (0.80 to 1.81) against "
"discordant patients, so equivalence was not shown. Pooled over the three cohorts with overall survival, the hazard "
"ratios were 1.08 (0.90 to 1.30) for stable luminal B-like and 0.77 (0.65 to 0.91) for stable luminal A-like patients. "
"Discordant tumors lie between the two optima by construction, so intermediate outcomes are expected. In SCAN-B, "
"chemotherapy was recorded for 16.6%, 33.9% and 52.3% of stable luminal A-like, discordant and stable luminal B-like "
"patients."),
("h2", "Pathologist-scored Ki-67"),
("p", "GSE81538 had 232 PAM50 luminal tumors (147 luminal A, 85 luminal B; share 36.6%). Kappa, accuracy and the Youden "
"index all chose a consensus Ki-67 cut-off of 15% in the full set (kappa 0.530). In the registered test of Amendment 7, "
"the kappa-optimal percentile moved by 0.62 points per point of share, below the registered minimum of 0.70, so the "
"mechanism was not confirmed on immunohistochemistry; the median kappa threshold stayed at 15% at every imposed share "
"(Fig. 3). Ki-67 in this series is recorded in steps of 5 points and is heavily tied, and simulations showed that the "
"coarse, tied scores account for the shortfall (Online Resource 4)."),
("p", "The comparison of criteria in Amendment 11 showed that the result depends on the criterion (Fig. 4d; Table 4). "
"The kappa-derived threshold stayed at 15% at every share, and case mix accounted for 17% of its variance. The "
"minimum-misclassification threshold, the criterion of Cheang and colleagues, was 25% at shares of 15% and 25%, 15% at "
"35% to 55% and 10% at 65%, and case mix accounted for 64% of its variance; proportion matching moved from 25% to 15% "
"(65%). The Youden threshold stayed at 15%."),
("h2", "Published cut-offs"),
("p", "Of 183 records, 16 were read in full and citation searching added two (Online Resource 3). Seven studies met the "
"criteria [@cheang2009; @fernandez2017; @lopez2024; @dixpeek2023; @chen2016; @ceccarelli2019; @noske2020] and one was "
"provisionally eligible [@holm2021] (Table 3). Two studies against PAM50 used a prevalence-dependent criterion "
"[@cheang2009; @dixpeek2023], three with the provisional study, below the registered threshold of eight, so the evidence "
"is summarized descriptively. Among studies against PAM50, case mix ranged from 27.6% [@holm2021] to 62.8% luminal B "
"[@dixpeek2023] and optima from 13% to 25%. In the one study that reported two criteria on the same 71 tumors, maximum "
"concordance chose 25% and the prevalence-free maximum positive likelihood ratio chose 20% [@chen2016]. Several studies "
"justified a threshold by the subtype proportions it produced [@dixpeek2023; @maisonneuve2014; @lundgren2019]."),

("h1", "Discussion"),
("p", "A proliferation cut-off chosen to reproduce PAM50 carries the case mix of the series in which it was chosen. "
"Across three cohorts and two platforms, the kappa-optimal cut-off fell by about 0.4 luminal A quantile points for each "
"point of luminal B share, and a binormal model fitted to the separation of the two subtypes predicted this slope "
"within 0.09. Over the range of case mix seen in published derivation studies, case mix explained more of the "
"variation in kappa-derived cut-offs than sampling did once a derivation set reached a few hundred tumors, and "
"cut-offs derived at the two ends of that range gave different labels to about one patient in six. Reweighting the "
"derivation set to the luminal B share of the target population removed most of the transfer error."),
("p", "The principle that agreement statistics depend on prevalence is old [@feinstein1990; @byrt1993; @metz1978]. What "
"this study adds is its size and its practical form for the luminal A versus B decision. Two features make the size "
"predictable. Under a binormal model the accuracy-optimal cut-off depends only on the separation of the subtypes and "
"the luminal B share, and the kappa and proportion-matching cut-offs follow a similar pattern; and the Youden boundary "
"lay about one luminal A standard deviation above the luminal A mean on both RNA sequencing and microarrays. A study that reports its criterion, its luminal B share and the separation of its "
"score can therefore be placed on a common scale, and a laboratory can estimate how far a published threshold would "
"move in its own population."),
("p", "The effect also explains some of the disagreement among published thresholds. The minimum-misclassification rule "
"used by Cheang and colleagues [@cheang2009] is the criterion that moved most on pathologist-scored Ki-67: from 25% to "
"10% as the luminal B share rose from 15% to 65%, a range that covers every published threshold. Proportion matching, "
"which several studies used to justify a threshold [@dixpeek2023; @maisonneuve2014; @lundgren2019], moved from 25% to "
"15%. Swedish quality assurance guidance, as reported by Brueffer and colleagues, asks each laboratory to recalibrate "
"its cut-off every year so that one third of consecutive cases are Ki-67-high [@brueffer2018]; a threshold set in this "
"way fixes the proportion called positive and therefore its percentile, and moves with case mix by design. Analytical "
"variation between laboratories is large [@dowsett2011; @polley2013] and was absent here only because score and "
"reference came from the same RNA profile, so case mix adds to the analytical explanations without replacing them."),
("p", "The choice of criterion involves a trade-off. The Youden cut-off does not depend on prevalence, and it transferred "
"with less error than the kappa cut-off, but it maximizes agreement only at a luminal B share of 50%, and in these "
"cohorts, with 26% to 39% luminal B, its agreement with PAM50 was no better than that of a transferred kappa cut-off. "
"Its sampling variation was also larger in two of the three cohorts, as is usual for empirical Youden estimates [@fluss2005]. Weighting the "
"derivation set to the target luminal B share keeps the agreement criterion and removes its dependence on the "
"derivation series. It requires an estimate of the luminal B share in the population where the threshold will be "
"used, which a laboratory without PAM50 does not have directly but can take from a population-based series of the same "
"region, from a regional derivation study, or from the published cohort that best matches its own."),
("p", "On pathologist-scored Ki-67, the kappa optimum did not move, and the registered test of Amendment 7 was not met. "
"Ki-67 in GSE81538 is recorded in steps of 5 points, so the kappa curve has few candidate thresholds and a shift of a "
"few points cannot appear; the minimum-misclassification optimum, which moves more steeply, did move. The arithmetic "
"of the RNA cohorts suggests that a 10-point difference in luminal B share would move an agreement-optimal Ki-67 "
"threshold by about 2 points, which is below the resolution of this series. A definitive test needs continuous "
"Ki-67 scores, from digital image analysis or from several laboratories, paired with PAM50 calls; we found no public "
"cohort of that kind."),
("p", "About one patient in seven lay between the two observed kappa optima, so their label depended on where the cut-off "
"had been tuned. Their outcomes were intermediate, and in SCAN-B they received chemotherapy twice as often as stable "
"luminal A-like patients, which may have narrowed the contrast. These are the patients for whom a borrowed threshold "
"decides the label, and the group overlaps the intermediate range that the International Ki67 Working Group declined "
"to classify [@nielsen2021]."),
("p", "The study has limitations. The question arose after the first optima were inspected, the timing of the gene list "
"and Amendments 2 to 6 rests on the author's records, and Amendment 11 was written with all earlier results known; its "
"registration protects its own analyses, not the choice to run them. The registered slope criteria of Amendments 6 to "
"10 used a scale that includes a fixed-cut-off component (Error Log 5). Resampling within subtype holds each subtype's "
"score distribution fixed, whereas real derivation series also differ in spectrum, grade and stage [@brenner1997], so "
"the case-mix component measured here is the part caused by the luminal B share alone. In the independent cohorts the "
"registered test was not done because of a specification error, and the exploratory results rest on 41 to 71 "
"luminal B tumors. The endpoints differed between cohorts and treatment was not modeled. Too few published studies "
"qualified for a formal regression, the literature search preceded registration, and the first pass of screening and "
"extraction was assisted by a language model, with a second person checking the values."),
("p", "Three practical rules follow. First, a derivation study should report its criterion, the luminal B share of its "
"derivation set and the cut-off as a quantile of its luminal A distribution, in line with reporting guidelines that "
"ask for the spectrum of the study population [@remark2006]. Second, a laboratory choosing between published "
"thresholds should prefer one derived in a series with a luminal B share close to its own, or reweight. Third, a "
"threshold intended to transfer should be derived with a prevalence-robust or target-weighted criterion and validated "
"outside the derivation set, because optimal cut-offs chosen in the same data are unstable and overstate effects "
"[@altman1994]."),
("p", "In conclusion, agreement-optimized proliferation cut-offs for luminal A versus luminal B breast cancer shift with "
"the luminal B share of the series that derived them, by an amount that a binormal model predicts from the separation "
"of the two subtypes, and reweighting to the target population removes most of the shift. Reporting the derivation "
"criterion and the case mix with any proposed threshold would make published values comparable and show when a "
"threshold is unlikely to transfer."),
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
 "available at https://github.com/Abusneina/proliferation-cutoffs-case-mix. The literature protocol is registered at "
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
