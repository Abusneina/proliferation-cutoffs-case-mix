"""SCAN-B panels for Online Resource 4 (sweep and Kaplan-Meier), 600 dpi, no titles in figures."""
import time, warnings, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from statsmodels.duration.survfunc import SurvfuncRight
warnings.filterwarnings("ignore"); T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}",flush=True)
R="/home/claude/work/results"; F="/home/claude/work/figures"
C_A,C_D,C_B="#7B5EA7","#C27C0E","#A63D40"; INK="#2B2B2B"; MUTED="#6B6B6B"; GRID="#E4E1DE"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.edgecolor":MUTED,"axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,
 "axes.spines.top":False,"axes.spines.right":False,"legend.frameon":False,"savefig.dpi":600})
d=pd.read_csv(f"{R}/cohort_scanb.csv",low_memory=False); sr=pd.read_csv(f"{R}/SCANB_results.csv",header=None,low_memory=False)
def kappa(a,b):
    po=(a==b).mean(); pe=a.mean()*b.mean()+(1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe)
m=d.PAM50.isin(["LumA","LumB"]).values; y=(d.PAM50.values[m]=="LumB").astype(int); rng=np.random.default_rng(0)
grid=np.arange(5,96); out={}
fig,ax=plt.subplots(figsize=(3.8,3.0))
for s,col,ls,lab,mk in [("P2",C_B,"-","18-gene proliferation score","o"),("P1",C_A,"--","MKI67 alone","s")]:
    full=d[s].values; x=full[m]; cuts=np.percentile(full,grid)
    ks=np.array([kappa((x>c).astype(int),y) for c in cuts]); i=int(np.argmax(ks)); log(f"SCAN-B {s}: optimum {grid[i]}th, kappa {ks[i]:.3f}")
    row=sr[(sr.iloc[:,0]=="A3")&(sr.iloc[:,1]==s)&(sr.iloc[:,2]=="opt")].iloc[0]; lo,hi=float(row.iloc[4]),float(row.iloc[5])
    assert int(float(row.iloc[3]))==int(grid[i]); log(f"  CI from registered run {lo:.0f} to {hi:.0f}")
    ax.plot(grid,ks,color=col,ls=ls,lw=2,label=lab); ax.axvspan(lo,hi,color=col,alpha=0.10,lw=0)
    ax.plot([grid[i]],[ks[i]],marker=mk,ms=7,color=col,mec="white",mew=1.5,zorder=5)
    ax.annotate(f"{grid[i]}th",(grid[i],ks[i]),xytext=(0,7 if s=="P2" else -15),textcoords="offset points",ha="center",fontsize=7.5,color=INK)
ax.set_xlabel("Cut-off (percentile within ER+/HER2− stratum)"); ax.set_ylabel("Cohen κ versus PAM50"); ax.set_xlim(5,95)
ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True); ax.legend(loc="lower center",fontsize=7)
fig.tight_layout(); fig.savefig(f"{F}/2026-10-14_1520_FigS_SCANB_agreement_sweep.png"); plt.close(fig)
# KM
v=d.P2.values; tl,th=np.nanpercentile(v,59),np.nanpercentile(v,74)
g=np.where(v<=tl,"A",np.where(v<=th,"D","B")); dd=d[d.TIME.notna()&(d.TIME>=0)].copy(); g=g[d.TIME.notna()&(d.TIME>=0)]
tmax=84; ticks=np.arange(0,tmax+1,21)
fig,ax=plt.subplots(figsize=(3.8,3.5)); risk={}
for key,col,ls,lab in [("A",C_A,"-","Stable luminal A-like"),("D",C_D,"--","Discordant"),("B",C_B,"-.","Stable luminal B-like")]:
    sub=dd[g==key]; sf=SurvfuncRight(sub.TIME.values,sub.EVENT.values)
    ax.step(np.r_[0,sf.surv_times],np.r_[1,sf.surv_prob],where="post",color=col,ls=ls,lw=2,label=f"{lab} (n={len(sub)})")
    risk[key]=[int((sub.TIME>=t).sum()) for t in ticks]
ax.set_xlim(0,tmax); ax.set_ylim(0.7,1.005); ax.set_xticks(ticks); ax.set_xlabel("Months"); ax.set_ylabel("Overall survival")
ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True); ax.legend(loc="lower left",fontsize=7)
for k,(key,col) in enumerate([("A",C_A),("D",C_D),("B",C_B)]):
    for t,n in zip(ticks,risk[key]): ax.text(t,-0.27-0.065*k,str(n),transform=ax.get_xaxis_transform(),ha="center",fontsize=6.5,color=col)
ax.text(-0.02,-0.27+0.065,"At risk",transform=ax.transAxes,ha="right",fontsize=6.5,color=MUTED)
fig.tight_layout(); fig.subplots_adjust(bottom=0.34); fig.savefig(f"{F}/2026-10-14_1520_FigS_SCANB_KM.png"); plt.close(fig); log("done")
