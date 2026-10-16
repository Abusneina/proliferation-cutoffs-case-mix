import csv,re,sys
KEY=re.compile(r"(cut-?off|cut off|cutpoint|cut-point|threshold|optimal|ROC|receiver|Youden|PAM50|intrinsic|concordan|agreement|kappa|κ|accura|Oncotype|recurrence score|MammaPrint|70-gene|21-gene|Prosigna|EndoPredict|luminal B|LumB)",re.I)
rows=list(csv.DictReader(open("records_183.csv")))
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for i,r in enumerate(rows[lo:hi],lo):
    if not r["title"]: continue
    sents=re.split(r"(?<=[.!?])\s+",r["abstract"])
    keep=[s for s in sents if KEY.search(s)]
    print(f"\n#{i} PMID {r['pmid']} ({r['year']}, {r['journal']}) [{r['types'][:40]}]\nT: {r['title']}")
    print("A: "+(" ".join(keep)[:520] if keep else "(no matching sentence) "+r["abstract"][:300]))
