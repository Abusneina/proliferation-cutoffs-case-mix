"""s06_scanb_clinical.py  Parse both GSE96058 series matrix files into one clinical table.
Characteristics are parsed by key, cell by cell, because GEO does not guarantee a fixed row
per key when fields are missing."""
import gzip, re, pandas as pd, numpy as np
from collections import Counter
U="/root/.claude/uploads/ec3ec192-a217-5587-af1a-bcdb9332ed30"
files=["6d1f02fa-GSE96058-GPL11154_series_matrix.txt.gz","34accb2c-GSE96058-GPL18573_series_matrix.txt.gz"]
frames=[]
for f in files:
    rec={}; titles=None; gsm=None
    for line in gzip.open(f"{U}/{f}","rt",encoding="utf-8",errors="replace"):
        if line.startswith("!Sample_title"): titles=[x.strip('"\n') for x in line.rstrip("\n").split("\t")[1:]]
        elif line.startswith("!Sample_geo_accession"): gsm=[x.strip('"\n') for x in line.rstrip("\n").split("\t")[1:]]
        elif line.startswith("!Sample_characteristics_ch1"):
            for i,cell in enumerate(line.rstrip("\n").split("\t")[1:]):
                cell=cell.strip('"')
                if ": " in cell:
                    k,v=cell.split(": ",1); rec.setdefault(i,{})[k.strip()]=v.strip()
    df=pd.DataFrame([rec.get(i,{}) for i in range(len(titles))]); df.insert(0,"title",titles); df.insert(1,"gsm",gsm)
    df["platform"]=f.split("-")[2].split("_")[0]; frames.append(df)
    print(f"{f}: {len(df)} samples")
c=pd.concat(frames,ignore_index=True)
c["is_repl"]=c["title"].str.contains("repl",case=False)
print("total:",len(c),"| replicate-titled:",int(c.is_repl.sum()))
print("example replicate titles:",c.loc[c.is_repl,"title"].head(4).tolist())
for k in ["er status","her2 status","pgr status","ki67 status","pam50 subtype","overall survival event","nhg","lymph node group","chemo treated","endocrine treated"]:
    print(f"\n{k}: {Counter(c.loc[~c.is_repl,k]).most_common(8)}")
c.to_csv("/home/claude/work/results/scanb_clinical_raw.csv",index=False)
