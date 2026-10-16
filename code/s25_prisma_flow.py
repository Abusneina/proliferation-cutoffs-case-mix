import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import sys
out=sys.argv[1]
M='#7B1E3A'; G='#444444'; LG='#F3EEEC'
fig,ax=plt.subplots(figsize=(8.3,9.6)); ax.set_xlim(0,100); ax.set_ylim(0,116); ax.axis('off')
def box(x,y,w,h,lines,fc='white',ec=G,fs=8.0,boldfirst=True):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=0.8',fc=fc,ec=ec,lw=1.1))
    n=len(lines); step=h/(n+0.6)
    for i,t in enumerate(lines):
        ax.text(x+w/2,y+h-step*(i+0.8),t,ha='center',va='center',fontsize=fs,fontweight='bold' if (i==0 and boldfirst) else 'normal')
def arr(x,y1,y2):
    ax.annotate('',xy=(x,y2),xytext=(x,y1),arrowprops=dict(arrowstyle='-|>',color=G,lw=1.1,shrinkA=0,shrinkB=0))
for y,h,t in [(86,30,'Identification'),(54,29,'Screening'),(21,30,'Eligibility'),(0.5,17,'Included')]:
    ax.add_patch(FancyBboxPatch((0.4,y),4.6,h,boxstyle='round,pad=0.1',fc=M,ec=M))
    ax.text(2.7,y+h/2,t,rotation=90,ha='center',va='center',color='white',fontsize=9,fontweight='bold')
LX,RX,W=8,54,43
# left: databases
box(LX,88,W,26,['Database search',  'PubMed: query A 178 and query B 32 records','Duplicates removed: 27','Unique records: 183','Europe PMC (not in MEDLINE): 0 additional'],LG)
box(LX,60,W,20,['Records screened on title and abstract (n = 183)','Excluded: 167','(2 of these, Viale 2019 and Ziegler 2024, were','re-surfaced by citation searching and read in full;','exclusion confirmed)'],fs=7.5)
box(LX,25,W,28,['Reports assessed in full text (n = 16)','Excluded: 10','No multigene reference: 2','Cut-off from outcome only: 2','Fixed or adopted cut-off, none derived: 3','No Ki-67 cut-off derived: 1','No computable luminal B or high-risk share: 1','Population criterion not met: 1'],fs=7.6)
box(LX,4,W,14,['Included from database search (n = 6)','Cheang 2009; Fernandez-Martinez 2017;','Dix-Peek 2023; Lopez-Tarruella 2024;','Chen 2016; Ceccarelli 2019'],LG,M,fs=7.6)
arr(LX+W/2,88,80.6); arr(LX+W/2,60,53.6); arr(LX+W/2,25,18.6)
# right: citation
box(RX,88,W,26,['Citation searching','Forward, round 1: 49 records','Backward: 194 unique records (237 links)','Forward, round 2: 36 records','Total retrieved: 279'],LG)
box(RX,60,W,20,['Excluded without full text (n = 275)','Off-topic, already assessed, or excluded','on abstract (round 2 backward: 87 off-topic,','6 already assessed, 98 excluded on abstract;','other rounds not tallied separately)'],fs=7.5)
box(RX,25,W,28,['Reports assessed in full text (n = 4)','Noske 2020','Holm 2021','Lundgren 2019','Thakur 2018','Excluded: 2 (Lundgren 2019, Thakur 2018;','no cut-off derived against a reference)'],fs=7.6)
box(RX,4,W,14,['Included from citation searching (n = 2)','Noske 2020','Holm 2021 (provisional)'],LG,M,fs=7.6)
arr(RX+W/2,88,80.6); arr(RX+W/2,60,53.6); arr(RX+W/2,25,18.6)
fig.savefig(out,dpi=300,facecolor='white',bbox_inches='tight')
