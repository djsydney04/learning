"""Regenerate the guide's static PNG diagrams: python scripts/render_diagrams.py.

Requires matplotlib and numpy. No network, browser, or JavaScript is needed.
The attention figure computes its displayed values, rather than hand-copying them.
"""

from pathlib import Path
import os
import tempfile

# Keep font-cache writes out of the source tree and support restricted environments.
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "transformer-guide-matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PAPER = "#f7f5ef"
INK = "#25272b"
MUTED = "#61656c"
LINE = "#b9bec7"
BLUE = "#2454c6"
PALE = "#e3eafa"
WHITE = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 14,
    "text.color": INK,
    "axes.facecolor": PAPER,
    "figure.facecolor": PAPER,
    "savefig.facecolor": PAPER,
})


def canvas(title, subtitle, height=8):
    fig, ax = plt.subplots(figsize=(14, height), dpi=170)
    fig.subplots_adjust(left=.035, right=.965, bottom=.045, top=.95)
    ax.set(xlim=(0, 100), ylim=(0, 100))
    ax.axis("off")
    ax.text(0, 99, title, fontsize=24, weight="bold", va="top")
    ax.text(0, 92, subtitle, fontsize=13.5, color=MUTED, va="top")
    return fig, ax


def text(ax, x, y, label, size=14, color=INK, ha="center", **kwargs):
    return ax.text(x, y, label, fontsize=size, color=color, ha=ha,
                   va="center", linespacing=1.4, **kwargs)


def box(ax, x, y, w, h, label, fill=WHITE, color=LINE, size=14, weight=None):
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h, facecolor=fill,
                           edgecolor=color, linewidth=1.5))
    text(ax, x, y, label, size=size, weight=weight)


def arrow(ax, start, end, color=BLUE, label=None, label_offset=(0, 3), curve=0):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>",
        mutation_scale=17, linewidth=1.65, color=color,
        connectionstyle=f"arc3,rad={curve}", shrinkA=0, shrinkB=0))
    if label:
        mid=((start[0]+end[0])/2+label_offset[0],
             (start[1]+end[1])/2+label_offset[1])
        text(ax, *mid, label, size=12, color=MUTED)


def path(ax, points, color=BLUE, final_arrow=True):
    for start, end in zip(points[:-2], points[1:-1]):
        ax.plot([start[0],end[0]], [start[1],end[1]], color=color, linewidth=1.65)
    if final_arrow:
        arrow(ax, points[-2], points[-1], color=color)
    else:
        ax.plot(*zip(*points[-2:]), color=color, linewidth=1.65)


def finish(fig, name):
    ASSETS.mkdir(exist_ok=True)
    fig.savefig(ASSETS / name, dpi=170)
    plt.close(fig)
    print(name)


def overview():
    fig, ax = canvas("A small transformer, from text to predictions",
        "One decoder-only model. Each position predicts the next character.", 9)
    ys=[81, 67, 48, 26, 11]
    box(ax, 35, ys[0], 47, 10, 'Text → character IDs\n"cat!" → [2, 1, 3, 0]', size=15)
    box(ax, 35, ys[1], 47, 10, 'Token embedding + position embedding', fill=PALE, size=14)
    box(ax, 35, ys[2], 60, 21,
        'Decoder block\nLayerNorm → causal attention → add block input\nLayerNorm → feed-forward → add updated input',
        fill=WHITE, color=BLUE, size=13.5)
    box(ax, 35, ys[3], 47, 10, 'Final LayerNorm → vocabulary Linear', size=14)
    box(ax, 35, ys[4], 47, 10, 'Logits: one score per possible next character', fill=PALE, size=13.5)
    for a,b,ha,hb in [(81,67,10,10),(67,48,10,21),(48,26,21,10),(26,11,10,10)]:
        arrow(ax,(35,a-ha/2),(35,b+hb/2))
    text(ax, 72, 81, '[B, T]\ninteger addresses',ha='left',size=14)
    text(ax, 72, 67, '[B, T, C]\none vector per position',ha='left',size=14)
    text(ax, 72, 48, 'Repeat N blocks\nShape stays [B, T, C]\nResidual paths preserve input',ha='left',size=13.5)
    text(ax, 72, 26, 'C features → V scores',ha='left',size=14)
    text(ax, 72, 11, '[B, T, V]\nTrain: cross-entropy\nGenerate: softmax → sample',ha='left',size=13)
    finish(fig, "01-transformer-overview.png")


def tensor_shapes():
    fig, ax = canvas("A tensor has named axes, not just a size",
        "x has shape [B=2, T=3, C=4]. Think: two tables, each with three rows and four columns.", 7.8)
    cellw, cellh=8,11
    for batch,x0 in [(0,10),(1,61)]:
        text(ax,x0+16,79,f'Batch {batch}: sequence "'+('cat' if batch==0 else 'dog')+'"',size=17,weight='bold')
        text(ax,x0+16,71,'C = 4 features →',size=13,color=MUTED)
        chars='cat' if batch==0 else 'dog'
        for row in range(3):
            y=59-row*cellh
            text(ax,x0-3,y,chars[row],size=16)
            for col in range(4):
                value=batch*12+row*4+col
                selected=(batch,row,col)==(1,2,3)
                box(ax,x0+col*cellw+cellw/2,y,cellw,cellh,str(value),
                    fill=BLUE if selected else WHITE,color=BLUE if selected else LINE,size=16)
                if selected:
                    ax.texts[-1].set_color(WHITE)
        text(ax,x0+16,20,'T = 3 positions ↓',size=14,color=MUTED)
    text(ax,50,7,'x[1, 2, 3] = 23     →     batch 1, position 2, feature 3',size=17,color=BLUE)
    text(ax,50,0,'The values are placeholders for practicing indexing; they are not learned character meanings.',size=12,color=MUTED)
    finish(fig,"02-tensor-shapes.png")


def training_loop():
    fig,ax=canvas("Training changes the numbers inside the model",
        "Repeat this loop on small batches. The targets are the input characters shifted one position forward.",8)
    nodes=[(16,70,'1. Clear old gradients\noptimizer.zero_grad()'),
           (50,70,'2. Forward pass\nlogits = model(inputs)'),
           (84,70,'3. Measure error\nFlatten batch + time\nlogits [B×T,V], targets [B×T]\ncross_entropy(logits, targets)'),
           (84,32,'4. Backward pass\nloss.backward()'),
           (50,32,'5. Update parameters\noptimizer.step()'),
           (16,32,'6. Get the next batch\ninputs and targets')]
    for idx,(x,y,label) in enumerate(nodes):
        box(ax,x,y,29,20,label,fill=PALE if idx in (1,4) else WHITE,size=13.3)
    arrow(ax,(30.5,70),(35.5,70)); arrow(ax,(64.5,70),(69.5,70))
    arrow(ax,(84,60),(84,42),label='use autograd',label_offset=(-12,0))
    arrow(ax,(69.5,32),(64.5,32)); arrow(ax,(35.5,32),(30.5,32))
    arrow(ax,(16,42),(16,60))
    text(ax,50,6,'Forward computes a prediction. Backward computes gradients. The optimizer changes parameters.',size=14,color=BLUE)
    finish(fig,'03-training-loop.png')


def embeddings():
    fig,ax=canvas("An embedding is a table lookup, followed by addition",
        "Hand-set vectors for one character position. Real embedding values are learned during training.",8.3)
    text(ax,19,81,'Token embedding table [V=4, C=3]',size=15,weight='bold')
    rows=[('0  !',[.0,.1,.2]),('1  a',[.3,.4,.5]),('2  c',[.6,.7,.8]),('3  t',[.9,1.0,1.1])]
    for i,(label,values) in enumerate(rows):
        y=68-i*9
        box(ax,6,y,9,9,label,fill=PALE if i==2 else WHITE,size=13)
        for j,value in enumerate(values):
            box(ax,17+j*9,y,9,9,f'{value:.1f}',fill=PALE if i==2 else WHITE,size=14)
    text(ax,19,25,'ID 2 selects row 2.\nIt does not multiply the vector by 2.',size=13.5,color=MUTED)
    box(ax,65,78,43,11,'Character "c" → token ID 2',fill=PALE,size=15)
    arrow(ax,(65,72.5),(65,55.5))
    arrow(ax,(39.5,50),(50,50))
    text(ax,79,60,'token vector',size=12,color=MUTED)
    box(ax,70,50,36,11,'[0.6, 0.7, 0.8]',size=17)
    text(ax,46,29,'+',size=25,color=BLUE)
    text(ax,70,39,'position 0 vector',size=12,color=MUTED)
    box(ax,70,29,36,11,'[0.1, 0.2, 0.3]',size=17)
    arrow(ax,(70,23.5),(70,15))
    box(ax,70,8,36,12,'x₀ = [0.7, 0.9, 1.1]',fill=PALE,color=BLUE,size=17)
    text(ax,19,7,'Whole batch:\nIDs [B,T] → vectors [B,T,C]',size=14,color=BLUE)
    finish(fig,'04-embeddings.png')


def draw_matrix(ax, data, x0,y0,width,height, heat=False, selected=2, title=None):
    rows,cols=data.shape
    cw,ch=width/cols,height/rows
    if title:
        text(ax,x0+width/2,y0+height+11,title,size=16,weight='bold')
    text(ax,x0+width/2,y0+height+6,'key position (source) →',size=12,color=MUTED)
    for j in range(cols):
        text(ax,x0+(j+.5)*cw,y0+height+2,str(j),size=12,color=MUTED)
    for i in range(rows):
        text(ax,x0-4,y0+height-(i+.5)*ch,str(i),size=13,color=BLUE if i==selected else MUTED)
        for j in range(cols):
            value=data[i,j]
            face=WHITE
            foreground=INK
            if heat:
                face=plt.get_cmap('Blues')(.08+.75*value)
                if value>.85: foreground=WHITE
            elif not np.isfinite(value):face='#e9e8e2'
            box(ax,x0+(j+.5)*cw,y0+height-(i+.5)*ch,cw,ch,
                '−∞' if not np.isfinite(value) else f'{value:.3f}',fill=face,color=LINE,size=15)
            ax.texts[-1].set_color(foreground)
    ax.add_patch(Rectangle((x0,y0+height-(selected+1)*ch),width,ch,fill=False,edgecolor=BLUE,linewidth=2))


def attention():
    q=np.array([[1.,0.],[0.,1.],[1.,1.]])
    v=np.array([[10.,0.],[0.,8.],[4.,4.]])
    scores=q@q.T/np.sqrt(2)
    scores[np.triu_indices(3,1)]=-np.inf
    weights=np.exp(scores-np.max(scores,axis=-1,keepdims=True))
    weights/=weights.sum(axis=-1,keepdims=True)
    output=weights@v
    fig,ax=canvas('Attention: scores → weights → a mixture of values',
        'Three positions, one head, two features. Row = receiving query; column = supplying key.',9.4)
    text(ax,0,80,'Q = K = [[1, 0], [0, 1], [1, 1]]',ha='left',size=15)
    text(ax,53,80,'V = [[10, 0], [0, 8], [4, 4]]',ha='left',size=15)
    draw_matrix(ax,scores,7,35,35,27,title='1. QKᵀ / √2, then causal mask')
    draw_matrix(ax,weights,61,35,35,27,heat=True,title='2. Softmax along each row')
    text(ax,0,48,'query position',size=11,color=MUTED,rotation=90)
    text(ax,54,48,'query position',size=11,color=MUTED,rotation=90)
    arrow(ax,(45,49),(53,49))
    text(ax,24.5,29,'Future positions get −∞ before softmax.',size=12,color=MUTED)
    text(ax,78.5,29,'Masked weights = 0. Each row sums to 1.',size=12,color=MUTED)
    text(ax,0,19,'3. For query position 2, multiply each weight by its value vector:',ha='left',size=14,weight='bold')
    text(ax,50,10,
        f'{weights[2,0]:.3f} × [10, 0]  +  {weights[2,1]:.3f} × [0, 8]  +  {weights[2,2]:.3f} × [4, 4]  ≈  [{output[2,0]:.3f}, {output[2,1]:.3f}]',
        size=17,color=BLUE)
    text(ax,50,1,'Only shown numbers are rounded. The first query has one allowed key, so its output is exactly [10, 0].',size=12,color=MUTED)
    finish(fig,'05-attention.png')


def multihead():
    fig,ax=canvas('Multiple heads: rearrange features, then restore their order',
        'Example: B=2, T=3, C=8, H=2, D=4. C = H × D. Apply the same rearrangement to Q, K, and V.',8.8)
    top=[(16,'Projected Q\n[2, 3, 8]'),(50,'Split features\n[2, 3, 2, 4]'),(84,'Move head axis\n[2, 2, 3, 4]')]
    for x,label in top:box(ax,x,74,28,14,label,fill=PALE,size=16)
    arrow(ax,(30,74),(36,74),label='reshape',label_offset=(0,12))
    arrow(ax,(64,74),(70,74),label='transpose(1, 2)',label_offset=(0,12))
    text(ax,16,62,'[B, T, C]',size=13,color=MUTED)
    text(ax,50,62,'[B, T, H, D]',size=13,color=MUTED)
    text(ax,84,62,'[B, H, T, D]',size=13,color=MUTED)
    box(ax,27,45,39,12,'Head 0: causal attention\nQ₀, K₀, V₀ → mixed₀ [B,T,D]',size=14)
    box(ax,73,45,39,12,'Head 1: causal attention\nQ₁, K₁, V₁ → mixed₁ [B,T,D]',size=14)
    path(ax,[(98,74),(99,74),(99,55),(27,55),(27,51)])
    arrow(ax,(73,55),(73,51))
    text(ax,50,35,'Independent attention per head',size=12,color=MUTED)
    bottom=[(16,'Mixed heads\n[2, 2, 3, 4]'),(50,'Restore position axis\n[2, 3, 2, 4]'),(84,'Join head features\n[2, 3, 8]')]
    for x,label in bottom:box(ax,x,18,28,14,label,fill=PALE,size=14)
    path(ax,[(27,39),(27,28),(16,28),(16,25)])
    path(ax,[(73,39),(73,28),(27,28)],final_arrow=False)
    arrow(ax,(30,18),(36,18),label='transpose',label_offset=(0,-12))
    arrow(ax,(64,18),(70,18),label='reshape',label_offset=(0,-12))
    text(ax,84,0,'Then apply the output Linear layer.',size=12,color=BLUE)
    finish(fig,'06-multihead.png')


def feature_strip(ax,x,y,n,width=16,highlight=False):
    w=width/n
    for index in range(n):
        box(ax,x-width/2+(index+.5)*w,y,w-0.3,6,'',
            fill=PALE if highlight else WHITE,color=BLUE if highlight else LINE)


def feedforward():
    fig,ax=canvas('Feed-forward: transform each position independently',
        'The same learned layers are reused at every position. Attention handles mixing between positions.',8)
    xs=[12,38,64,90]
    headings=['Input','Linear: C → 4C','GELU: 4C → 4C','Linear: 4C → C']
    for x,label in zip(xs,headings):text(ax,x,78,label,size=14,weight='bold')
    for row,y in enumerate([62,43,24]):
        text(ax,1,y+7,f'position {row}',ha='left',size=12,color=MUTED)
        for i,x in enumerate(xs):
            feature_strip(ax,x,y,2 if i in (0,3) else 8,highlight=row==1)
        for left,right in zip(xs[:-1],xs[1:]):arrow(ax,(left+8.4,y),(right-8.4,y),color=BLUE if row==1 else MUTED)
    text(ax,50,9,'Here C=2, so the hidden width is 8. All outputs return to two features.',size=14,color=BLUE)
    text(ax,50,0,'Changing position 1 changes only its own output in this sublayer. The weights stay shared.',size=12,color=MUTED)
    finish(fig,'07-feedforward.png')


def block():
    fig,ax=canvas('One transformer block: normalize the branch, keep the residual',
        'Pre-norm order. Every main-path tensor has shape [B, T, C].',10)
    # Main path is vertical; the two skip paths reconnect at their own add node.
    center=48
    text(ax,center,83,'input x',size=17,weight='bold')
    box(ax,center,71,32,9,'LayerNorm 1',size=16)
    box(ax,center,58,32,10,'Causal multi-head attention',fill=PALE,size=14)
    box(ax,center,37,32,9,'LayerNorm 2',size=16)
    box(ax,center,24,32,10,'Feed-forward',fill=PALE,size=16)
    for y in [46,12]:
        ax.add_patch(Circle((center,y),2.5,facecolor=WHITE,edgecolor=BLUE,linewidth=1.8))
        text(ax,center,y,'+',size=21,color=BLUE)
    arrow(ax,(center,80),(center,75.5))
    arrow(ax,(center,66.5),(center,63))
    arrow(ax,(center,53),(center,48.5))
    arrow(ax,(center,43.5),(center,41.5))
    arrow(ax,(center,32.5),(center,29))
    arrow(ax,(center,19),(center,14.5))
    arrow(ax,(center,9.5),(center,4))
    text(ax,center,0,'output y',size=17,weight='bold')
    path(ax,[(center,79),(18,79),(18,46),(45.5,46)])
    text(ax,15,62,'carry x\nunchanged',size=13,color=BLUE,ha='right')
    path(ax,[(center,43),(79,43),(79,12),(50.5,12)])
    text(ax,83,28,'carry updated h\nunchanged',size=13,color=BLUE,ha='left')
    text(ax,66,48,'h = x + attention(LN₁(x))',ha='left',size=12.5)
    text(ax,5,11,'y = h + FFN(LN₂(h))',ha='left',size=12.5)
    finish(fig,'08-block.png')


if __name__ == '__main__':
    for render in [overview,tensor_shapes,training_loop,embeddings,attention,multihead,feedforward,block]:
        render()
