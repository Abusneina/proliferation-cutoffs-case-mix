# Agreement-optimized gene-expression proliferation cut-offs inherit the case mix of their derivation population

Code, frozen protocol documents, error logs, result tables and literature-review records for the manuscript:

> Abusneina AM. Agreement-optimized gene-expression proliferation cut-offs for luminal A versus luminal B breast cancer inherit the case mix of their derivation population: an analysis of six cohorts. Manuscript submitted to *Breast Cancer Research and Treatment*.

Author: Abdelmuhsen M. Abusneina, Department of Molecular Diagnostics, Faculty of Biomedical Sciences, University of Benghazi, Libya. ORCID [0000-0001-9909-5588](https://orcid.org/0000-0001-9909-5588). Contact: abdelmuhsen.abusneina@uob.edu.ly

## Registrations

| Document | Registration |
|---|---|
| Literature-review protocol v1.0 | https://osf.io/pc9wm |
| Amendment 7 (GSE81538, pathologist-scored Ki-67) | https://osf.io/p5hb7 |
| Amendments 8 and 9 (gene-disjoint score; overall survival) | https://osf.io/su2hg (DOI 10.17605/OSF.IO/SU2HG) |
| Amendment 10 (independent cohorts GSE25066 and SMC 2018) | https://osf.io/db7a8 (DOI 10.17605/OSF.IO/DB7A8) |
| All frozen documents, error logs and freeze records | https://osf.io/cwkd9 |

The timing of every frozen document, and what was known when each was frozen, is in Table 4 of the manuscript and in `protocol/`. The gene list and Amendments 2 to 6 were posted on OSF after their analyses; their timing rests on the author's file records (see Error Log 3).

## Repository layout

| Folder | Contents |
|---|---|
| `code/` | Analysis scripts, archived exactly as run (see "Paths" below) |
| `code/aux/` | Gene-symbol availability check and draft gene lists used for Amendment 8 |
| `protocol/` | Frozen gene list, Amendments 2 to 10 (drafts and frozen versions), freeze records with SHA-256 hashes, error logs 1 to 5, search log for independent cohorts, literature-review protocol |
| `results/` | Result tables (CSV, JSON), run logs and results records for each amendment |
| `posthoc/` | Post hoc analyses added after external review (Error Log 5), with their outputs |
| `litreview/` | Search logs, the 183 retrieved records, screening workbooks, decisions of both reviewers, full-text first-pass extraction, citation-search logs, protocol deviation 1, the stage 2 comparison and the check of the Holm et al. 2021 cut-off rule |
| `figures/` | Manuscript and supplementary figures (600 dpi) |
| `data/` | TCGA-BRCA clinical files as downloaded from cBioPortal (public) |

## Scripts, in run order

| Script | Analysis | Manuscript |
|---|---|---|
| `s00_raw_inflate.py` | Utility: recovers one entry from a split zip archive | Data handling |
| `s01_build_cohorts.py` | TCGA-BRCA and METABRIC cohorts; scores P1 (MKI67) and P2 (18-gene) | Methods: Cohorts, Proliferation scores |
| `s02_cutoff_sweep.py` | Cut-off sweep against PAM50 (A1 to A4) | Results: agreement-optimal cut-off |
| `s03_discordant_zone.py` | Amendment 2: discordant group and outcome contrasts | Results: patients whose label depends on the cut-off |
| `s04_figures.py`, `s05_fig2_corrected.py` | Early figures (300 dpi); s05 replaces a figure withdrawn under Error Log 1 | Superseded by s16 to s18 |
| `s06_scanb_clinical.py` | Parses GSE96058 series matrices into one clinical table | SCAN-B cohort |
| `s07_scanb_confirmatory.py` | SCAN-B cohort, sweep, outcomes (Amendments 3 to 5) | Results: SCAN-B |
| `s08_prevalence_mechanism.py` | Amendment 6: Youden scales and prevalence resampling (E1 to E3) | Results: movement with case mix; Table 2 |
| `s09_fig4_mechanism.py` | Early mechanism figure | Superseded |
| `s10_condense.py` | Literature screening helper: keyword condensation of records | Online Resource 3 |
| `s11_gse81538_amendment7.py` | Amendment 7: registered test in GSE81538 (C1 to C3) | Results: test with frozen predictions |
| `s12_exploratory_slope_vs_separation.py` | Exploratory: slope against separation for normal scores | Results: simulation (post hoc) |
| `s13_fig4.py`, `s14_jitter_robustness.py` | Exploratory: observed Ki-67 distributions at large N; random tie-breaking | Results: simulation (post hoc) |
| `s15_slope_ci.py` | Exploratory: patient-level bootstrap CI of the C1 slope | Results (post hoc) |
| `s16_figures_600dpi.py`, `s17_fig2_600dpi.py`, `s18_fig4_600dpi.py` | Final figures 1 to 4 at 600 dpi | Figures |
| `s19_scanb_supplement_figs.py` | SCAN-B supplementary panels | Online Resource 4 |
| `s20_online_resources.py` | Builds Online Resources 1 to 4 (PDF) | Online Resources |
| `s21_amendment8.py` | Amendment 8: gene-disjoint scores P3, P3m, P4 | Results: a score sharing no gene with PAM50 |
| `s22_amendment9.py` | Amendment 9: overall survival in all cohorts, pooled | Results: overall survival |
| `s23_amendment10.py` | Amendment 10, frozen script (SHA-256 b0df341cc4e829c7b7803f27095500894afee6eaf19eb914e1404aa413af3497) | Results: independent cohorts (registered test not done, Error Log 4) |
| `s24_amendment10_exploratory_ER-all508.py` | Post hoc exploratory rerun of s23 with the ER field recorded for all 508 samples (one-line change) | Results: independent cohorts (exploratory) |
| `posthoc/ph1_scale_check.py` | Post hoc (Error Log 5): observed optima as percentiles of the luminal set; resampling slope in score units and the slope of a fixed cut-off (P1, P2) | Results; Table 2; Online Resource 4, Table S22 |
| `posthoc/ph2_score_units_P3.py` | Post hoc (Error Log 5): the same for P3 and for GSE81538, using the Amendment 8 scoring functions unchanged | Results; Online Resource 4, Table S22 |
| `s25_prisma_flow.py` | PRISMA 2020 flow diagram for the literature component (Fig. S-L1); counts taken from the search and citation-search logs | Online Resource 3 |

Scripts marked exploratory or post hoc were not pre-specified and are labeled as such in the manuscript.

## Data sources (not redistributed)

| Cohort | Source | File (MD5) |
|---|---|---|
| TCGA-BRCA PanCancer Atlas | cBioPortal datahub, `brca_tcga_pan_can_atlas_2018` | `data_mrna_seq_v2_rsem.txt` (18d0267b0338b2d27ed023962bd88050) |
| METABRIC | cBioPortal datahub, `brca_metabric` | `data_mrna_illumina_microarray.txt` (a62c864b3f927cb965f0247d63fcf880) |
| SCAN-B | GEO GSE96058 | `GSE96058_gene_expression_3273_samples_and_136_replicates_transformed.csv.gz` (4362d1d9b5e80a6e1409cd7b9dc4a0ab), plus both series matrix files |
| GSE81538 | GEO GSE81538 | `GSE81538_gene_expression_405_transformed.csv.gz` (a51f0b2b60af070d43dacb7245b69294) and `GSE81538_series_matrix.txt.gz` |
| GSE25066 | GEO GSE25066; platform GPL96 | `GSE25066_series_matrix.txt.gz` (bb8ba628105514111aa818db5a3e3ac6); `GPL96.annot.gz` (a3c03c05e7b77d2305b84ba5e46181ec) |
| SMC 2018 | cBioPortal datahub, `brca_smc_2018` | `data_clinical_sample.txt`, `data_clinical_patient.txt`, `data_mrna_seq_tpm.txt` |

cBioPortal datahub files: `https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/<study>/<file>`. GEO files: `https://ftp.ncbi.nlm.nih.gov/geo/series/`.

## Paths

The scripts are archived exactly as they were run, so that the frozen scripts keep their recorded hashes. They read and write absolute paths from the original working environment: `/home/claude/work/{protocol,results,figures,code}` for the contents of this repository, and `/home/claude/raw/`, `/home/claude/dl/geo2/` and the upload folders for the downloaded data. To rerun, either recreate those paths (for example with symbolic links to this repository and to the downloaded files) or edit the path constants at the top of each script. File names expected in each location are given in the script headers.

## Software

Python 3 with NumPy, pandas, SciPy, statsmodels (Cox models, survival functions), scikit-learn (ROC curves), matplotlib (figures) and reportlab (Online Resources). Exact package versions were not recorded at run time. Scripts print progress throughout; run logs are in `results/`.

## Use of AI tools

Analysis code, first-pass literature screening and extraction, and text drafts were produced with a large language model (Claude, Anthropic). The author specified the analyses in advance and checked every output. A second reviewer screened the literature independently, and a second person checked the extracted values (details in `litreview/`).

## License

Code: MIT License (see `LICENSE`). Documents, tables and figures: CC BY 4.0.

## Citation

See `CITATION.cff`. Please cite the article once published.
