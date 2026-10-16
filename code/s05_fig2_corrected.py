"""s05_fig2_corrected.py  Replaces the withdrawn Fig 2 (Error Log 1).
Panel A: pre-specified D1 group contrasts, DISCORDANT as reference.
Panel B: POST HOC piecewise-linear slopes (knot at lower zone edge), whole-cohort SD units."""
import numpy as np, pandas as pd, warnings
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
R="/home/claude/work/results"; F="/home/claude/work/figures"
C_A,C_D,C_B="#7B5EA7","#C27C0E","#A63D40"; INK="#2B2B2B"; MUTED="#6B6B6B"; GRID="#E4E1DE"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.spines.top":False,"axes.spines.right":False,
  "axes.edgecolor":MUTED,"xtick.color":MUTED,"ytick.color":MUTED,"legend.frameon":False,"savefig.dpi":300})
D=pd.read_csv(f"{R}/D_discordant_zone.csv")
KN={"P2":59,"P1":64}
pw=[]
for c,f in [("METABRIC","cohort_metabric.csv"),("TCGA","cohort_tcga.csv")]:
    d=pd.read_csv(f"{R}/{f}",low_memory=False); d=d[d.TIME.notna()&(d.TIME>=0)]
    for s in ["P2","P1"]:
        v=d[s].values; z=(v-np.nanmean(v))/np.nanstd(v,ddof=1); k=np.nanpercentile(z,KN[s])
        X=np.column_stack([z,np.maximum(z-k,0),d.AGE_N.values]); ok=~np.isnan(X).any(1)
        m=PHReg(d.TIME.values[ok],X[ok],status=d.EVENT.values[ok]).fit(disp=False)
        b=m.params; V=m.cov_params()
        below=(b[0],np.sqrt(V[0,0])); above=(b[0]+b[1],np.sqrt(V[0,0]+V[1,1]+2*V[0,1])); diff=(b[1],np.sqrt(V[1,1]))
        for lab,(e,se) in [("below",below),("above",above),("diff",diff)]:
            pw.append(dict(cohort=c,score=s,part=lab,hr=np.exp(e),lo=np.exp(e-1.96*se),hi=np.exp(e+1.96*se),
                           p=float(2*(1-__import__("scipy").stats.norm.cdf(abs(e/se))))))
pw=pd.DataFrame(pw); pw.to_csv(f"{R}/S2_piecewise_slopes_POSTHOC.csv",index=False)

fig,axs=plt.subplots(1,2,figsize=(7.4,3.6),gridspec_kw={"width_ratios":[1.15,1]})
labels=[]; y=0
ax=axs[0]
ax.axvspan(0.67,1.50,color=GRID,alpha=0.7,lw=0,label="Equivalence margin (0.67–1.50)"); ax.axvline(1,color=MUTED,lw=0.8)
for c in ["METABRIC","TCGA"]:
    for s,sl in [("P2","18-gene"),("P1","MKI67")]:
        a=D[(D.cohort==c)&(D.score==s)&(D.test=="D1_STABLE_A_vs_DISC")].iloc[0]
        b=D[(D.cohort==c)&(D.score==s)&(D.test=="D1_STABLE_B_vs_DISC")].iloc[0]
        ax.plot([a.lo,a.hi],[y+0.16]*2,color=C_A,lw=2); ax.plot(a.hr,y+0.16,"o",color=C_A,ms=6.5,mec="white",mew=1.2)
        ax.plot([b.lo,b.hi],[y-0.16]*2,color=C_B,lw=2,ls="-."); ax.plot(b.hr,y-0.16,"D",color=C_B,ms=6,mec="white",mew=1.2)
        labels.append((y,f"{c}, {sl}")); y-=1
ax.set_yticks([l[0] for l in labels]); ax.set_yticklabels([l[1] for l in labels],color=INK)
ax.set_xscale("log"); ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xticks([0.25,0.5,1,2]); ax.set_xticklabels(["0.25","0.5","1","2"]); ax.set_xlim(0.15,2.4); ax.set_ylim(y+0.4,1.9)
ax.plot([],[],"o-",color=C_A,lw=2,label="Stable luminal A-like vs discordant")
ax.plot([],[],"D-.",color=C_B,lw=2,label="Stable luminal B-like vs discordant")
ax.legend(loc="upper left",fontsize=6.8); ax.set_xlabel("Hazard ratio (discordant zone = reference)")
ax.spines["left"].set_visible(False); ax.tick_params(axis="y",length=0)
ax.text(-0.02,1.02,"A",transform=ax.transAxes,fontsize=11,fontweight="bold",ha="right")
ax=axs[1]; ax.axvline(1,color=MUTED,lw=0.8); y=0; labels=[]
for c in ["METABRIC","TCGA"]:
    for s,sl in [("P2","18-gene"),("P1","MKI67")]:
        for part,dy,col,mk,ls in [("below",0.16,C_A,"o","-"),("above",-0.16,C_B,"D","-.")]:
            r=pw[(pw.cohort==c)&(pw.score==s)&(pw.part==part)].iloc[0]
            ax.plot([r.lo,r.hi],[y+dy]*2,color=col,lw=2,ls=ls); ax.plot(r.hr,y+dy,mk,color=col,ms=6,mec="white",mew=1.2)
        labels.append((y,f"{c}, {sl}")); y-=1
ax.set_yticks([l[0] for l in labels]); ax.set_yticklabels([]); ax.tick_params(axis="y",length=0)
ax.set_xscale("log"); ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xticks([0.5,1,2,4]); ax.set_xticklabels(["0.5","1","2","4"]); ax.set_xlim(0.3,5); ax.set_ylim(y+0.4,1.9)
ax.plot([],[],"o-",color=C_A,lw=2,label="Slope below lower zone edge")
ax.plot([],[],"D-.",color=C_B,lw=2,label="Slope above lower zone edge")
ax.legend(loc="upper left",fontsize=6.8); ax.set_xlabel("Hazard ratio per whole-cohort SD (post hoc)")
ax.spines["left"].set_visible(False)
ax.text(-0.02,1.02,"B",transform=ax.transAxes,fontsize=11,fontweight="bold",ha="right")
fig.tight_layout(); fig.savefig(f"{F}/2026-10-13_1640_Fig2_group-contrasts_and_piecewise.png"); plt.close(fig)
print(pw.round(3).to_string(index=False))
