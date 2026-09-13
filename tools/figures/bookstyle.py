"""Shared drawing style. Typeface: ET Book (ETBembo). Monochrome, minimal rules."""
import os, glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

for f in glob.glob(os.path.expanduser('~/.fonts/et-book*.ttf')):
    try: font_manager.fontManager.addfont(f)
    except Exception: pass

INK='#111111'; MID='#8c8c8c'; LIGHT='#d6d6d6'; FAINT='#efefef'
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figures')
os.makedirs(OUT, exist_ok=True)

def setup(figsize=(7.2,4.2)):
    plt.rcParams.update({
        'font.family':'ETBembo','font.size':10,'axes.edgecolor':LIGHT,'axes.labelcolor':INK,
        'axes.labelsize':10,'axes.titlesize':12.5,'axes.titlelocation':'left','axes.titlepad':16,
        'text.color':INK,'xtick.color':MID,'ytick.color':MID,'xtick.labelsize':9.5,'ytick.labelsize':9.5,
        'axes.grid':True,'grid.color':FAINT,'grid.linewidth':0.9,'axes.axisbelow':True,
        'figure.dpi':300,'savefig.dpi':300,'axes.unicode_minus':False,
        'legend.frameon':False,'legend.fontsize':9.5,
        'mathtext.fontset':'custom','mathtext.rm':'ETBembo','mathtext.it':'ETBembo:italic','mathtext.bf':'ETBembo:bold','mathtext.cal':'ETBembo','mathtext.sf':'ETBembo','mathtext.tt':'ETBembo','mathtext.default':'regular'})
    fig,ax=plt.subplots(figsize=figsize)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(LIGHT); ax.spines['bottom'].set_color(LIGHT)
    ax.tick_params(length=0)
    return fig,ax

def save(fig,name,source=None,note=None):
    lines=[]
    if note: lines.append(note)
    if source: lines.append('Source: '+source)
    if lines: fig.text(0.005,-0.015,'\n'.join(lines),fontsize=8,color=MID,va='top')
    fig.tight_layout()
    for ext in ('png','svg'):
        fig.savefig(os.path.join(OUT,f'{name}.{ext}'),bbox_inches='tight',facecolor='white')
    plt.close(fig)
