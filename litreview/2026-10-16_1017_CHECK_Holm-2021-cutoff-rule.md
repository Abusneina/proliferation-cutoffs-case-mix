# Check: Holm et al. 2021 (JNCI Cancer Spectr, pkaa087), rule for the "free" Ki-67 cut-off
Source: pkaa087_supplementary_data.pdf (supplied by Adam, 16 Oct 2026), Supplementary Methods, manuscript lines 80 to 89, printed pages 8 to 9 (PDF pages 2 to 3).

Verbatim: "The StGallen additionally noted that local experience may be best to define locally useful cut-offs for Ki-67, consequently, a third cutoff tailored to each dataset was defined. Using the R package caret modeling framework, we obtained the optimal cutoff (hereafter denoted "free") for Ki-67 by including it as a tuning parameter in cross-validation. We used a grid search of 10 equidistant values ranging from 5 to 50 percent for evaluation against true PAM50 in a 10-fold, 10 times repeated cross-validation."

- The optimization metric is not stated. caret's default selection metric for classification models is accuracy.
- The sentence given by the checker for Q3 ("Cut-offs for the Prolif surrogate were tailored to each dataset to maximize the agreement with PAM50 intrinsic subtype classification", "p. 4") does not appear in the supplement (text search: 0 matches).
