"""
s04_figures.py  Manuscript figures, 300 dpi, legends inside plot area, no titles in figures.
Palette validated with dataviz validator (all checks pass, light mode):
  STABLE_A #7B5EA7  DISCORDANT #C27C0E  STABLE_B #A63D40
Redundant encoding (line style / marker shape) so every figure reads in greyscale.
"""
import time, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.duration.survfunc import SurvfuncRight
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
T0=time.time()
def log(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
R="/home/claude/work/results"; F="/home/claude/work/figures"
C_A,C_D,C_B="#7B5EA7","#C27C0E","#A63D40"; INK="#2B2B2B"; MUTED="#6B6B6B"; GRID="#E4E1DE"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.edgecolor":MUTED,
    "axes.labelcolor":INK,"xtick.color":MUTED,"ytick.color":MUTED,"axes.linewidth":0.8,
    "axes.spines.top":False,"axes.spines.right":False,"legend.frameon":False,"savefig.dpi":600})
STAMP="2026-10-14_1520"

def panel_letter(ax,s): ax.text(-0.12,1.02,s,transform=ax.transAxes,fontsize=11,fontweight="bold",color=INK,va="bottom")

# ---------------- Figure 1: agreement with PAM50 across the grid ----------------
a3=pd.read_csv(f"{R}/A3_agreement.csv"); grid=a3[a3.pct>0]; opt=a3[a3.pct==-1]
fig,axs=plt.subplots(1,2,figsize=(7.2,3.0),sharey=True)
for ax,(c,let) in zip(axs,[("TCGA","A"),("METABRIC","B")]):
    for s,col,ls,lab in [("P2",C_B,"-","18-gene proliferation score"),("P1",C_A,"--","MKI67 alone")]:
        g=grid[(grid.cohort==c)&(grid.score==s)]
        ax.plot(g.pct,g.kappa,color=col,ls=ls,lw=2,label=lab)
        o=opt[(opt.cohort==c)&(opt.score==s)].iloc[0]
        ax.axvspan(o.ci_lo,o.ci_hi,color=col,alpha=0.10,lw=0)
        ax.plot([o.opt_pct],[o.kappa],marker="o" if s=="P2" else "s",ms=7,color=col,mec="white",mew=1.5,zorder=5)
        ax.annotate(f"{int(o.opt_pct)}th",(o.opt_pct,o.kappa),xytext=(0,7 if s=="P2" else -15),textcoords="offset points",
                    ha="center",fontsize=7.5,color=INK)
    ax.set_xlabel("Cut-off (percentile within ER+/HER2− stratum)")
    ax.set_xlim(5,95); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True)
    ax.text(0.02,0.96,c,transform=ax.transAxes,fontsize=8.5,color=INK,va="top",fontweight="bold")
    panel_letter(ax,let)
axs[0].set_ylabel("Cohen κ versus PAM50")
axs[1].legend(loc="lower center",fontsize=7.5)
fig.tight_layout(); fig.savefig(f"{F}/{STAMP}_Fig1_agreement_sweep.png"); plt.close(fig); log("Fig 1 written")

if False:
 # ---------------- Figure 2 withdrawn (Error Log 1), whole cohort vs inside zone ----------------
    D=pd.read_csv(f"{R}/D_discordant_zone.csv")
    rows=[]
    for c in ["METABRIC","TCGA"]:
        for s,lab in [("P2","18-gene score"),("P1","MKI67")]:
            w=D[(D.cohort==c)&(D.score==s)&(D.test=="D3b_continuous_whole_cohort")].iloc[0]
            z=D[(D.cohort==c)&(D.score==s)&(D.test=="D3_continuous_in_zone")].iloc[0]
            rows.append((f"{c}, {lab}",w,z))
    fig,ax=plt.subplots(figsize=(6.0,3.4))
    ax.axvspan(0.67,1.50,color=GRID,alpha=0.7,lw=0,label="Equivalence margin (0.67–1.50)")
    ax.axvline(1,color=MUTED,lw=0.8)
    y=np.arange(len(rows))[::-1]*1.0
    for yi,(lab,w,z) in zip(y,rows):
        ax.plot([w.lo,w.hi],[yi+0.17]*2,color=C_B,lw=2); ax.plot(w.hr,yi+0.17,"o",color=C_B,ms=7,mec="white",mew=1.2)
        ax.plot([z.lo,z.hi],[yi-0.17]*2,color=C_D,lw=2,ls="--"); ax.plot(z.hr,yi-0.17,"s",color=C_D,ms=7,mec="white",mew=1.2)
        ax.text(3.6,yi+0.17,f"{w.hr:.2f} ({w.lo:.2f}–{w.hi:.2f})",va="center",fontsize=7,color=INK)
        ax.text(3.6,yi-0.17,f"{z.hr:.2f} ({z.lo:.2f}–{z.hi:.2f})",va="center",fontsize=7,color=INK)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],color=INK)
    ax.set_xscale("log"); ax.set_xticks([0.5,0.75,1,1.5,2,3]); ax.set_xticklabels(["0.5","0.75","1","1.5","2","3"])
    ax.set_xlim(0.45,3.4); ax.set_ylim(-0.7,y.max()+1.9)
    from matplotlib.ticker import NullFormatter; ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Hazard ratio per standard deviation of proliferation score")
    ax.plot([],[],"o-",color=C_B,lw=2,label="Whole ER+/HER2− cohort")
    ax.plot([],[],"s--",color=C_D,lw=2,label="Inside the discordant zone only")
    ax.legend(loc="upper left",fontsize=7,ncol=1)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y",length=0)
    fig.tight_layout(); fig.subplots_adjust(right=0.80)
    fig.savefig(f"{F}/{STAMP}_Fig2_forest_whole_vs_zone.png"); plt.close(fig); log("Fig 2 written")
    
# ---------------- Figure 3: Kaplan-Meier, three groups ----------------
CUTS={"P2":(59,74)}
def groups(d,s):
    v=d[s].values; tl,th=np.nanpercentile(v,CUTS[s][0]),np.nanpercentile(v,CUTS[s][1])
    return np.where(v<=tl,"STABLE_A",np.where(v<=th,"DISCORDANT","STABLE_B"))
fig,axs=plt.subplots(1,2,figsize=(7.2,3.4))
for ax,(c,f,ylab,let,tmax) in zip(axs,[("METABRIC","cohort_metabric.csv","Disease-specific survival","A",240),
                                       ("TCGA","cohort_tcga.csv","Progression-free interval","B",120)]):
    d=pd.read_csv(f"{R}/{f}",low_memory=False); d=d[d.TIME.notna()&(d.TIME>=0)]
    g=groups(d,"P2")
    ticks=np.arange(0,tmax+1,tmax//4)
    risk={}
    for key,col,ls,lab in [("STABLE_A",C_A,"-","Stable luminal A-like"),("DISCORDANT",C_D,"--","Discordant zone"),
                            ("STABLE_B",C_B,"-.","Stable luminal B-like")]:
        sub=d[g==key]; sf=SurvfuncRight(sub.TIME.values,sub.EVENT.values)
        t=np.r_[0,sf.surv_times]; s_=np.r_[1,sf.surv_prob]
        ax.step(t,s_,where="post",color=col,ls=ls,lw=2,label=f"{lab} (n={len(sub)})")
        risk[key]=[int((sub.TIME>=tt).sum()) for tt in ticks]
    ax.set_xlim(0,tmax); ax.set_ylim(0.4 if c=="METABRIC" else 0.3,1.01); ax.set_xticks(ticks)
    ax.set_xlabel("Months"); ax.set_ylabel(ylab); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True)
    ax.legend(loc="lower left",fontsize=7)
    ax.text(0.98,0.97,c,transform=ax.transAxes,ha="right",va="top",fontsize=8.5,fontweight="bold",color=INK)
    for k,(key,col) in enumerate([("STABLE_A",C_A),("DISCORDANT",C_D),("STABLE_B",C_B)]):
        for tt,n in zip(ticks,risk[key]):
            ax.text(tt,-0.30-0.065*k,str(n),transform=ax.get_xaxis_transform(),ha="center",fontsize=6.5,color=col)
    ax.text(-0.02,-0.30+0.065,"At risk",transform=ax.transAxes,ha="right",fontsize=6.5,color=MUTED)
    panel_letter(ax,let)
fig.tight_layout(); fig.subplots_adjust(bottom=0.36,wspace=0.32)
fig.savefig(f"{F}/{STAMP}_Fig3_KM_three_groups.png"); plt.close(fig); log("Fig 3 written")

# ---------------- Figure S1: descriptive gradient by twentieth (post hoc, labelled) ----------------
d=pd.read_csv(f"{R}/cohort_metabric.csv",low_memory=False); d=d[d.TIME.notna()&(d.TIME>=0)]
q=pd.qcut(d["P2"],20,labels=False)
X=pd.get_dummies(q,prefix="q",drop_first=True).astype(float); X["age"]=d["AGE_N"].values
ok=X.notna().all(axis=1).values
m=PHReg(d.TIME.values[ok],X.values[ok],status=d.EVENT.values[ok]).fit(disp=False)
k=X.shape[1]-1; hr=np.r_[1,np.exp(m.params[:k])]; ci=np.exp(m.conf_int()[:k])
lo=np.r_[1,ci[:,0]]; hi=np.r_[1,ci[:,1]]
mid=np.arange(20)*5+2.5
fig,ax=plt.subplots(figsize=(5.6,3.2))
ax.axvspan(59,74,color=C_D,alpha=0.14,lw=0,label="Discordant zone (59th–74th)")
ax.axhline(1,color=MUTED,lw=0.8)
ax.vlines(mid,lo,hi,color=INK,lw=1.2)
ax.plot(mid,hr,"o",color=C_B,ms=6,mec="white",mew=1.2,label="HR vs lowest twentieth (95% CI)")
ax.set_yscale("log"); ax.set_yticks([0.5,1,2,4]); ax.set_yticklabels(["0.5","1","2","4"])
ax.set_xlim(0,100); ax.set_xlabel("18-gene proliferation score, percentile (METABRIC)")
ax.set_ylabel("Disease-specific hazard ratio"); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True)
ax.legend(loc="upper left",fontsize=7)
fig.tight_layout(); fig.savefig(f"{F}/{STAMP}_FigS1_gradient_by_twentieth_POSTHOC.png"); plt.close(fig)
pd.DataFrame({"twentieth":np.arange(1,21),"mid_pct":mid,"HR":hr,"lo":lo,"hi":hi}).to_csv(f"{R}/S1_gradient_twentieths_POSTHOC.csv",index=False)
log("Fig S1 written (post hoc, descriptive)")
