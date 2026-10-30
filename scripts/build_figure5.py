"""Generate portfolio figures from existing Figure 5 artifacts; never run Spectre or write into the source project."""
from pathlib import Path
import os,json,csv,re,hashlib,ast,shutil
os.environ.setdefault('MPLCONFIGDIR','/tmp/portfolio-mpl-cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
from matplotlib.patches import FancyBboxPatch,Circle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figure5';OUT.mkdir(parents=True,exist_ok=True)
SRC=Path('/Users/dani/Downloads/virtuoso-bridge-lite/artifacts/assignment_fig5')
v=json.loads((SRC/'validation.json').read_text())
net=(SRC/'assignment_fig5.scs').read_text()
topology={m[0]:tuple(m[1:5]) for m in re.findall(r'^(Q\d+) \((\w+) (\w+) (\w+) (\w+)\) (\w+)',net,re.M)}
# Recover a DC peak directly from stored PSF ASCII, independent of display CSV.
raw=SRC/'spectre_refined_20261016/assignment_fig5_refined.raw/refined.dc'
text=raw.read_text().split('VALUE\n',1)[1]
vectors={name:np.array([float(x) for x in re.findall(r'^"'+name+r'"\s+([\deE+.-]+)',text,re.M)]) for name in ['vinpbias','vout']}
x,y=vectors['vinpbias'],vectors['vout'];gradient=np.gradient(y,x,edge_order=2);center=x[np.argmax(abs(gradient))];mask=abs(x-center)<=5e-6
fit=Polynomial.fit(x[mask],y[mask],5);der=fit.deriv();roots=[float(r.real) for r in der.deriv().roots() if abs(r.imag)<1e-12 and x[mask][0]<r.real<x[mask][-1] and der(r.real)<0]
assert len(roots)==1
peak=roots[0];gain=float(der(peak));out=float(fit(peak))
assert abs(gain-v['maximum_signed_gain_V_per_V'])<1e-6
# Correct additive conductance stamps handle tied gate/drain terminals.
nodes=['vs','n3','n4','n7','n9','n10','vout','bias_n'];index={n:i for i,n in enumerate(nodes)}
A=np.zeros((8,8));rhs=np.zeros(8)
def add(row,col,value):
 if row not in index:return
 if col in index:A[index[row],index[col]]+=value
 elif col=='vinp':rhs[index[row]]+=value
for q,(d,g,s,b) in topology.items():
 for col,value in [(d,v[q+'_gds']),(g,v[q+'_gm']),(s,-(v[q+'_gds']+v[q+'_gm']+v[q+'_gmbs'])),(b,v[q+'_gmbs'])]:
  add(d,col,value);add(s,col,-value)
theory=float(np.linalg.solve(A,-rhs)[index['vout']])
metrics={'source_peak_gain_V_per_V':gain,'peak_input_V':peak,'peak_output_V':out,'gain_magnitude_dB':float(20*np.log10(abs(gain))),'archived_theoretical_gain_V_per_V':v['theoretical_full_small_signal_gain_V_per_V'],'recomputed_additive_nodal_gain_V_per_V':theory,'recomputed_theory_error_percent':abs(theory-gain)/abs(gain)*100,'fit_samples':int(mask.sum()),'raw_samples':len(x),'fit_method':v['fit_method'],'saturation_checks':v['saturation'],'source_op_errors':v['op_errors']}
(OUT/'verified-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
for name in ['transfer.csv','gain.csv','validation.json','assignment_fig5.scs']:
 shutil.copyfile(SRC/name,OUT/name)
with (OUT/'topology.csv').open('w',newline='') as h:
 w=csv.writer(h);w.writerow(['Device','Drain','Gate','Source','Bulk']);w.writerows((q,*nets) for q,nets in topology.items())
manifest={str(p.relative_to(SRC)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SRC/'transfer.csv',SRC/'gain.csv',SRC/'validation.json',SRC/'assignment_fig5.scs',raw]}
(OUT/'source-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Print calculations before graphics for review.
print(json.dumps(metrics,indent=2))
bg='#101b29';ink='#dce8f1';muted='#9cb0c3';teal='#87dec3';violet='#b5a3ed';grid='#2b3d4e'
plt.rcParams.update({'figure.facecolor':bg,'axes.facecolor':bg,'axes.edgecolor':grid,'axes.labelcolor':ink,'xtick.color':muted,'ytick.color':muted,'text.color':ink,'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','savefig.facecolor':bg})
def setup(ax,title,xlabel,ylabel):
 ax.set_title(title,loc='left',fontsize=15,pad=20,fontweight='bold');ax.set_xlabel(xlabel,labelpad=10);ax.set_ylabel(ylabel,labelpad=10);ax.grid(alpha=.55,color=grid);ax.set_axisbelow(True)
def save(fig,name):
 fig.savefig(OUT/(name+'.svg'),bbox_inches='tight');fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight');plt.close(fig)
t=np.genfromtxt(SRC/'transfer.csv',delimiter=',',names=True);g=np.genfromtxt(SRC/'gain.csv',delimiter=',',names=True)
fig,axes=plt.subplots(1,2,figsize=(13.2,4.8),layout='constrained')
axes[0].plot(t['vinp_V'],t['vout_V'],color=teal,lw=2);axes[0].scatter([peak],[out],color=violet,zorder=4,s=32);axes[0].set(xlim=(0,1.8),ylim=(-.03,1.83));setup(axes[0],'DC transfer · full input sweep','VINP (V) · VINN held at 0.9 V','VOUT (V)')
axes[0].annotate('Peak-gain operating point',xy=(peak,out),xytext=(.1,.6),arrowprops={'arrowstyle':'->','color':muted},fontsize=10,color=muted)
axes[1].plot((x-peak)*1e6,y,color=teal,lw=2);axes[1].scatter([0],[out],color=violet,zorder=4,s=30);axes[1].set_xlim(-30,30);setup(axes[1],'Transition detail · stored 20 nV sweep','VINP − peak input (µV)','VOUT (V)')
fig.suptitle('FIGURE 5 / SKY130 CMOS AMPLIFIER',x=.02,ha='left',fontsize=11,color=muted)
save(fig,'dc-transfer')
fig,ax=plt.subplots(figsize=(10.5,5.3),layout='constrained');near=abs(g['vinp_V']-peak)<=30e-6;ax.plot((g['vinp_V'][near]-peak)*1e6,g['gain_V_per_V'][near],color=violet,lw=2,label='Archived DC transfer derivative');xx=np.linspace(x[mask][0],x[mask][-1],300);ax.plot((xx-peak)*1e6,der(xx),color=teal,lw=2,label='Reproduced degree-5 fit derivative');ax.scatter([0],[gain],color=teal,zorder=5);ax.annotate(f'{gain:,.2f} V/V\nVINP = {peak:.9f} V',xy=(0,gain),xytext=(10,gain+18),color=ink,fontsize=11,arrowprops={'arrowstyle':'->','color':muted});setup(ax,'Local DC voltage gain · not a frequency response','VINP − peak input (µV)','dVOUT / dVINP (V/V)');ax.legend(facecolor=bg,edgecolor=grid,loc='upper left',fontsize=9);save(fig,'dc-gain')
fig,ax=plt.subplots(figsize=(10.5,5.1),layout='constrained');qs=list(topology);vds=np.array([abs(v[q+'_vds']) for q in qs]);sat=np.array([abs(v[q+'_vdsat']) for q in qs]);pos=np.arange(12);ax.bar(pos-.18,vds,width=.36,color=teal,label='|VDS|');ax.bar(pos+.18,sat,width=.36,color=violet,label='|VDSAT|');ax.set_xticks(pos,qs);setup(ax,'Operating-point headroom · all 12 devices pass archived test','Device','Voltage magnitude (V)');ax.legend(facecolor=bg,edgecolor=grid,fontsize=10);save(fig,'headroom')
# Clean named-net schematic: all 12 devices represented exactly by D/G/S/B labels.
fig,ax=plt.subplots(figsize=(16,11));ax.set(xlim=(0,16),ylim=(0,11));ax.axis('off');fig.subplots_adjust(left=.02,right=.98,top=.96,bottom=.03)
ax.text(.3,10.65,'ESE 5620 · FIGURE 5',fontsize=13,color=teal,weight='bold');ax.text(.3,10.15,'Differential CMOS amplifier with cascoded output',fontsize=22,weight='bold');ax.text(.3,9.72,'Net-labeled redraw from the archived Spectre deck · matching labels are electrically connected',fontsize=11,color=muted)
blocks=[(.2,3.1,'01 / REFERENCE'),(3.6,5.7,'02 / INPUT PAIR & LOADS'),(9.6,2.7,'03 / MIRROR PATH'),(12.6,3.2,'04 / OUTPUT CASCODES')]
for x0,w,title in blocks:
 ax.add_patch(FancyBboxPatch((x0,.75),w,8.55,boxstyle='round,pad=.08,rounding_size=.12',facecolor='#132231',edgecolor=grid,lw=1));ax.text(x0+.15,8.95,title,fontsize=10,color=muted,weight='bold')
def mos(q,cx,cy):
 d,g,s,b=topology[q];pmos=q in ['Q3','Q4','Q7','Q9','Q11'];color=violet if pmos else teal
 # Electrical symbol: gate left; PMOS source on top, NMOS drain on top.
 ax.plot([cx,cx],[cy-.28,cy+.28],color=color,lw=2);ax.plot([cx-.14,cx-.14],[cy-.3,cy+.3],color=color,lw=1.5)
 ax.plot([cx,cx+.32,cx+.32],[cy+.22,cy+.22,cy+.62],color=color,lw=1.5);ax.plot([cx,cx+.32,cx+.32],[cy-.22,cy-.22,cy-.62],color=color,lw=1.5)
 ax.plot([cx-.72,cx-.2],[cy,cy],color=color,lw=1.5)
 if pmos:ax.add_patch(Circle((cx-.20,cy),.055,edgecolor=color,facecolor=bg,lw=1.3))
 ax.text(cx+.52,cy+.1,q,fontsize=12,color=ink,weight='bold');ax.text(cx+.52,cy-.15,'PMOS' if pmos else 'NMOS',fontsize=8,color=muted)
 ax.text(cx+.32,cy+.72,('S: ' if pmos else 'D: ')+(s if pmos else d).upper(),ha='center',fontsize=8.5,color=color)
 ax.text(cx+.32,cy-.82,('D: ' if pmos else 'S: ')+(d if pmos else s).upper(),ha='center',fontsize=8.5,color=color)
 ax.text(cx-.73,cy+.14,'G: '+g.upper(),ha='left',fontsize=8,color=muted)
 ax.text(cx+.52,cy-.42,'B: '+b.upper(),fontsize=8,color=muted)
mos('Q6',1.35,3.1);ax.text(.5,7.7,'IREF = 200 nA',fontsize=13,color=ink);ax.text(.5,7.25,'VDD → BIAS_N',fontsize=11,color=teal);ax.text(.5,6.55,'Q6 is diode-connected.\nBIAS_N drives tail Q5.',fontsize=10,color=muted,linespacing=1.6)
for q,cx,cy in [('Q4',4.65,7.6),('Q3',7.35,7.6),('Q1',4.65,4.8),('Q2',7.35,4.8),('Q5',6,2.0),('Q7',10.65,7.6),('Q8',10.65,3.1),('Q9',13.75,7.7),('Q11',13.75,5.7),('Q12',13.75,3.7),('Q10',13.75,1.7)]:mos(q,cx,cy)
ax.text(9.95,5.5,'N3 → N7',fontsize=10,color=muted);ax.text(9.95,5.05,'Level translation',fontsize=9,color=muted)
ax.text(.3,.25,'VDD 1.8 V  |  VINN 0.9 V  |  VB1 0.650 V  |  VB2 0.51548 V  |  All MOS: W/L = 30 µm / 10 µm',fontsize=11,color=muted)
save(fig,'schematic')
