"""Fig 4: prevalence mechanism (Amendment 6). Cohorts in greyscale with marker shapes so the
three-group palette (purple/ochre/maroon) keeps one meaning across the paper."""
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R="/home/claude/work/results"; F="/home/claude/work/figures"
INK="#2B2B2B"; MUTED="#6B6B6B"; GRID="#E4E1DE"; REF="#A63D40"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.spines.top":False,"axes.spines.right":False,
  "axes.edgecolor":MUTED,"xtick.color":MUTED,"ytick.color":MUTED,"legend.frameon":False,"savefig.dpi":600})
STY={"TCGA":dict(color="#1F1F1F",marker="o",ls="-"),"METABRIC":dict(color="#6E6E6E",marker="s",ls="--"),
     "SCAN-B":dict(color="#A8A8A8",marker="^",ls="-.")}
e3=pd.read_csv(f"{R}/E3_prevalence_resampling.csv"); e1=pd.read_csv(f"{R}/E1_youden_scales.csv")
fig,axs=plt.subplots(1,3,figsize=(7.4,2.9),gridspec_kw={"width_ratios":[1,1,1.05]})
for ax,col,ylab,let in [(axs[0],"kappa_pct","κ-optimal cut-off (percentile)","A"),
                        (axs[1],"youden_q_lumA","Youden cut-off (quantile of luminal A)","B")]:
    for c,st in STY.items():
        g=e3[(e3.cohort==c)&(e3.score=="P2")]
        ax.plot(g.prev,g[col],lw=1.8,ms=5,mec="white",mew=0.8,label=c,**st)
    if col=="kappa_pct":
        xx=np.array([15,45]); ax.plot(xx,100-xx,color=REF,lw=1,ls=":",label="100 − luminal B share")
    ax.set_xlabel("Imposed luminal B share (%)"); ax.set_ylabel(ylab); ax.set_xticks([15,25,35,45])
    ax.set_ylim(50,100); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True)
    ax.text(-0.18,1.03,let,transform=ax.transAxes,fontsize=11,fontweight="bold")
axs[0].legend(loc="lower left",fontsize=6.6)
ax=axs[2]
y=0; labs=[]
for c,st in STY.items():
    r=e1[(e1.cohort==c)&(e1.score=="P2")].iloc[0]
    ax.plot([r.youden_q_lumA_lo,r.youden_q_lumA_hi],[y]*2,color=st["color"],lw=2)
    ax.plot(r.youden_q_lumA,y,marker=st["marker"],color=st["color"],ms=7,mec="white",mew=1)
    ax.plot([r.youden_pct_full_lo,r.youden_pct_full_hi],[y-0.32]*2,color=st["color"],lw=1.2,ls=":")
    ax.plot(r.youden_pct_full,y-0.32,marker=st["marker"],color=st["color"],ms=5,mfc="white",mew=1.2)
    labs.append((y-0.16,c)); y-=1
ax.set_yticks([l[0] for l in labs]); ax.set_yticklabels([l[1] for l in labs],color=INK); ax.tick_params(axis="y",length=0)
ax.spines["left"].set_visible(False); ax.set_xlim(45,100); ax.set_ylim(y+0.35,0.75)
ax.set_xlabel("Youden cut-off, 18-gene score"); ax.grid(axis="x",color=GRID,lw=0.6); ax.set_axisbelow(True)
ax.plot([],[],"o-",color=MUTED,lw=2,label="Quantile of luminal A")
ax.plot([],[],"o:",color=MUTED,mfc="white",lw=1.2,label="Percentile of whole stratum")
ax.legend(loc="upper left",fontsize=6.6,bbox_to_anchor=(0,1.02))
ax.text(-0.08,1.03,"C",transform=ax.transAxes,fontsize=11,fontweight="bold")
fig.tight_layout(); fig.savefig(f"{F}/2026-10-14_1520_Fig2_prevalence-mechanism.png"); print("ok")
