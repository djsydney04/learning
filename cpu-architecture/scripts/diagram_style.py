"""Shared visual vocabulary for the primer's original, code-drawn diagrams."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUT = Path(__file__).resolve().parents[1] / "assets"
INK = "#192b3a"
MUTED = "#607383"
BLUE = "#3269a8"
GREEN = "#25816e"
ORANGE = "#b96719"
PURPLE = "#7b55a7"
GRAY = "#dce4ea"
KINDS = {
    "state": ("#edf3fc", BLUE),
    "logic": ("#eaf6f0", GREEN),
    "control": ("#fff3e4", ORANGE),
    "memory": ("#f2edfa", PURPLE),
    "plain": ("#f5f7f9", MUTED),
}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "text.color": INK, "axes.unicode_minus": True})


def canvas(title, subtitle="", height=7):
    fig, ax = plt.subplots(figsize=(12, height))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set(xlim=(0, 12), ylim=(0, height))
    ax.axis("off")
    text(ax, .4, height-.45, title, size=19, ha="left", weight="bold")
    if subtitle:
        text(ax, .4, height-.94, subtitle, size=10.5, color=MUTED, ha="left")
    return fig, ax


def text(ax, x, y, value, size=11, color=INK, ha="center", va="center",
         weight="normal", mono=False, **kwargs):
    ax.text(x, y, value, fontsize=size, color=color, ha=ha, va=va,
            weight=weight, family="DejaVu Sans Mono" if mono else "DejaVu Sans",
            linespacing=1.35, zorder=5, **kwargs)


def box(ax, x, y, w, h, title, kind="logic", sub=None, fontsize=12):
    fill, edge = KINDS[kind]
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.10",
                                facecolor=fill, edgecolor=edge, linewidth=1.5,
                                zorder=2))
    text(ax,x+w/2,y+h/2+(.15 if sub else 0),title,size=fontsize,weight="bold")
    if sub:
        text(ax,x+w/2,y+h/2-.22,sub,size=9.5,color=MUTED)


def arrow(ax, start, end, color=INK, label=None, label_xy=None, bend=0):
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=13,
                                linewidth=1.5,color=color,shrinkA=0,shrinkB=0,
                                connectionstyle=f"arc3,rad={bend}",zorder=3))
    if label:
        pos=label_xy or ((start[0]+end[0])/2,(start[1]+end[1])/2+.18)
        text(ax,*pos,label,size=9.5,color=color)


def wire(ax, points, color=INK, head=True, dashed=False):
    xs,ys=zip(*points)
    ax.plot(xs,ys,color=color,lw=1.5,ls="--" if dashed else "-",zorder=1)
    if head:
        arrow(ax,points[-2],points[-1],color=color)


def footer(ax, value):
    text(ax,.4,.25,value,size=9.5,color=MUTED,ha="left")


def save(fig, name):
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/name
    fig.savefig(path,dpi=160,facecolor="white")
    plt.close(fig)
    print(path.name)
