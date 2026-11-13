"""ph5_size_subgroup_score_means.py  POST HOC (13 Nov 2026, after the Amendment 12 run): mean and SD of the 18-gene
score (P2) by PAM50 luminal subtype and tumor-size subgroup in SCAN-B, to describe the spectrum difference between the
Amendment 12 primary-split subgroups. Descriptive only. Output: posthoc/PH5_size_subgroup_score_means.csv"""
import os, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "..", "results")
d = pd.read_csv(os.path.join(R, "cohort_scanb.csv")); d = d[d.PAM50.isin(["LumA", "LumB"]) & d.SIZE.notna()]
d["size_group"] = (d.SIZE > 20).map({False: "20 mm or less", True: "more than 20 mm"})
out = d.groupby(["PAM50", "size_group"]).P2.agg(["count", "mean", "std"]).round(3).reset_index()
out.to_csv(os.path.join(HERE, "PH5_size_subgroup_score_means.csv"), index=False); print(out.to_string(index=False))
