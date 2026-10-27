"""Draw the primer's circuit foundations with explicit values and signal paths."""

from diagram_style import (
    canvas, text, box, arrow, wire, footer, save,
    INK, MUTED, BLUE, GREEN, ORANGE, PURPLE, GRAY,
)
from matplotlib.patches import Rectangle


def signals_and_bits():
    fig, ax = canvas("A bit is a meaning assigned to a voltage",
                     "Voltage is continuous. A digital input recognizes valid low and high ranges.")
    x0, y0, w, h = .95, 2.0, 6.1, 3.25
    ax.add_patch(Rectangle((x0, y0), w, .3*h, fc="#edf3fc", ec="none"))
    ax.add_patch(Rectangle((x0, y0+.3*h), w, .4*h, fc="#fff3e4", ec="none"))
    ax.add_patch(Rectangle((x0, y0+.7*h), w, .3*h, fc="#eaf6f0", ec="none"))
    for v, title, col in ((.15,"valid LOW\nlogic 0",BLUE),
                           (.50,"undefined\ninput range",ORANGE),
                           (.85,"valid HIGH\nlogic 1",GREEN)):
        text(ax,5.9,y0+v*h,title,size=11,color=col)
    arrow(ax,(x0,y0),(x0,y0+h+.12),MUTED)
    arrow(ax,(x0,y0),(x0+w+.13,y0),MUTED)
    for v in (0,.3,.7,1):
        text(ax,x0-.12,y0+v*h,f"{v:.1f}",size=10,ha="right",color=MUTED)
    text(ax,.35,3.8,"Normalized voltage",size=10,rotation=90)
    text(ax,6.6,1.75,"time →",size=10,color=MUTED)
    xs=[x0+.25,x0+.8,x0+1.0,x0+1.8,x0+2.0,x0+2.7,x0+2.9,x0+3.6]
    levels=[.08,.08,.93,.93,.08,.08,.93,.93]
    ax.plot(xs,[y0+v*h for v in levels],color=INK,lw=2.5,zorder=4)
    text(ax,4.0,1.35,"A transition passes through intermediate voltages.",size=11)
    text(ax,4.0,.95,"The thresholds here are illustrative, not a device specification.",size=10,color=MUTED)

    text(ax,9.55,5.35,"Eight wires form a byte-wide bus",size=11,weight="bold")
    bits="00101101"
    for i,bit in enumerate(bits):
        y=4.95-i*.38
        text(ax,8.4,y,f"bit {7-i}",size=10,ha="right",color=MUTED)
        ax.plot([8.65,10.3],[y,y],color=BLUE if bit=="1" else GRAY,lw=3)
        text(ax,10.6,y,bit,size=13,mono=True,color=BLUE if bit=="1" else MUTED)
    box(ax,8.1,.9,3.1,.85,"00101101 = 45",kind="state",fontsize=13)
    footer(ax,"A bus carries a pattern. A register is what remembers a pattern between updates.")
    save(fig,"01-signals-and-bits.png")


def binary_and_overflow():
    fig,ax=canvas("Bit positions determine value; width limits the result",
                  "Eight bits have unsigned weights 128 through 1. The same adder can produce a ninth carry bit.")
    bits="00101101"
    text(ax,.5,5.15,"position",size=10,ha="left",color=MUTED)
    text(ax,.5,4.45,"bit",size=10,ha="left",color=MUTED)
    text(ax,.5,3.72,"weight",size=10,ha="left",color=MUTED)
    text(ax,.5,3.12,"contributes",size=10,ha="left",color=MUTED)
    for i,bit in enumerate(bits):
        x=2.0+i*1.15
        pos=7-i
        text(ax,x+.47,5.15,str(pos),size=11,color=MUTED)
        box(ax,x,4.05,.95,.8,bit,kind="state" if bit=="1" else "plain",fontsize=20)
        text(ax,x+.47,3.72,str(2**pos),size=12,mono=True)
        text(ax,x+.47,3.12,str((2**pos)*int(bit)),size=12,color=BLUE if bit=="1" else MUTED)
    text(ax,6.45,2.6,"32 + 8 + 4 + 1 = 45",size=16,color=BLUE,weight="bold")
    text(ax,.5,1.9,"250 + 10 = 260",size=14,weight="bold",ha="left")
    result="100000100"
    for i,bit in enumerate(result):
        x=3.45+i*.82
        box(ax,x,.95,.72,.7,bit,kind="control" if i==0 else "state",fontsize=17)
    text(ax,3.81,.65,"carry = 1",size=10,color=ORANGE)
    text(ax,7.5,.65,"keep these eight bits: 00000100 = 4",size=11,color=BLUE)
    footer(ax,"Discarding the carry gives 260 modulo 256 = 4. Signed overflow uses a different test.")
    save(fig,"02-binary-and-overflow.png")


def gates_and_mux():
    fig,ax=canvas("Gates compute rules; a mux chooses a source",
                  "The upper row shows logical blocks with one example each, rather than transistor-level schematics.")
    examples=[("AND","1 and 1","1"),("OR","1 or 1","1"),
              ("XOR","1 xor 1","0"),("NOT","not 1","0")]
    for i,(name,inputs,out) in enumerate(examples):
        x=.5+i*2.9
        text(ax,x+1.1,5.25,inputs,size=11,color=MUTED)
        arrow(ax,(x+1.1,5.0),(x+1.1,4.75))
        box(ax,x,3.95,2.2,.8,name,fontsize=14)
        arrow(ax,(x+1.1,3.95),(x+1.1,3.65))
        text(ax,x+1.1,3.4,f"output {out}",size=12,color=GREEN)
    ax.plot([.5,11.5],[2.95,2.95],color=GRAY,lw=1)
    box(ax,.7,1.95,2.45,.6,"a = 0011",kind="state",fontsize=12)
    box(ax,.7,.95,2.45,.6,"b = 1010",kind="state",fontsize=12)
    box(ax,5.0,1.1,2.0,1.35,"MUX",sub="select one input",fontsize=15)
    wire(ax,[(3.15,2.25),(4.2,2.25),(5.0,2.1)],color=MUTED)
    wire(ax,[(3.15,1.25),(4.2,1.25),(5.0,1.45)],color=BLUE)
    text(ax,4.25,2.5,"s = 0 path",size=10,color=MUTED)
    text(ax,4.2,.95,"s = 1 path",size=10,color=BLUE)
    text(ax,6,2.75,"s = 1",size=11,color=ORANGE,weight="bold")
    arrow(ax,(6,2.6),(6,2.45),color=ORANGE)
    arrow(ax,(7.0,1.78),(8.45,1.78),color=BLUE)
    box(ax,8.45,1.36,2.8,.84,"y = 1010",kind="state",fontsize=14)
    footer(ax,"For known select s: y = s ? b : a. The other input still exists, but it is not selected.")
    save(fig,"03-gates-and-mux.png")


def adder_and_alu():
    fig,ax=canvas("An adder passes carries; an ALU selects a result",
                  "Top: four full adders compute 0111 + 0001 = 1000. Carries flow from low bit to high bit.")
    for i in range(4):
        x=1.3+i*2.55
        a=1 if i<3 else 0
        b=1 if i==0 else 0
        text(ax,x+.65,5.2,f"a{i}={a}   b{i}={b}",size=11,mono=True)
        arrow(ax,(x+.65,4.98),(x+.65,4.7))
        box(ax,x,3.75,1.3,.95,f"FA {i}",fontsize=13)
        arrow(ax,(x+.65,3.75),(x+.65,3.43),color=BLUE)
        text(ax,x+.65,3.18,f"sum{i}={1 if i==3 else 0}",size=12,mono=True,color=BLUE)
        if i<3:
            arrow(ax,(x+1.3,4.22),(x+2.55,4.22),color=ORANGE)
            text(ax,x+1.92,4.5,"carry 1",size=10,color=ORANGE)
    text(ax,.55,4.22,"0",size=12,color=ORANGE)
    arrow(ax,(.72,4.22),(1.3,4.22),color=ORANGE)
    arrow(ax,(10.25,4.22),(11.15,4.22),color=ORANGE)
    text(ax,11.2,4.55,"carry 0",size=10,color=ORANGE)
    text(ax,6,2.72,"Read sum bits from high to low: sum3 sum2 sum1 sum0 = 1000",size=11,color=BLUE)
    ax.plot([.5,11.5],[2.4,2.4],color=GRAY,lw=1)
    box(ax,.5,.75,2.2,1.1,"a and b",kind="state",sub="operand buses",fontsize=13)
    arrow(ax,(2.7,1.3),(3.45,1.3))
    box(ax,3.45,.65,3.25,1.35,"ADD / SUB / AND / OR",sub="candidate calculations",fontsize=11)
    arrow(ax,(6.7,1.3),(7.45,1.3))
    box(ax,7.45,.75,1.5,1.1,"select",kind="control",fontsize=12)
    text(ax,8.2,2.18,"ALU op",size=11,color=ORANGE)
    arrow(ax,(8.2,2.02),(8.2,1.85),color=ORANGE)
    arrow(ax,(8.95,1.3),(9.6,1.3))
    box(ax,9.6,.75,1.9,1.1,"result",kind="logic",fontsize=13)
    footer(ax,"The ALU output is combinational. A destination register decides when to store that output.")
    save(fig,"04-adder-and-alu.png")


def register_feedback():
    fig,ax=canvas("A counter is an incrementer feeding a register",
                  "The combinational logic computes a next value. Only a clock edge makes it the stored value.")
    box(ax,.65,3.15,2.2,1.2,"8-bit register",kind="state",sub="current count Q",fontsize=14)
    box(ax,4.5,3.15,2.3,1.2,"+ 1",sub="incrementer",fontsize=17)
    box(ax,8.5,3.15,2.25,1.2,"MUX",kind="control",sub="choose D",fontsize=16)
    arrow(ax,(2.85,3.75),(4.5,3.75),color=BLUE)
    text(ax,3.7,3.45,"Q = 5",size=12,color=BLUE)
    arrow(ax,(6.8,3.75),(8.5,3.75),color=GREEN)
    text(ax,7.65,4.05,"Q + 1 = 6",size=12,color=GREEN)
    wire(ax,[(3.5,3.75),(3.5,5.0),(9.6,5.0),(9.6,4.35)],color=BLUE)
    text(ax,6.4,5.25,"hold path: pass Q when enable = 0",size=11,color=BLUE)
    wire(ax,[(10.75,3.75),(11.3,3.75),(11.3,1.9),(.35,1.9),(.35,3.75),(.65,3.75)],color=ORANGE)
    text(ax,5.9,2.15,"D = enable ? (Q + 1) : Q",size=13,color=ORANGE,mono=True)
    text(ax,9.6,2.63,"enable",size=12,color=ORANGE)
    arrow(ax,(9.6,2.85),(9.6,3.15),color=ORANGE)
    text(ax,1.75,2.65,"clock ↑",size=12,color=BLUE)
    arrow(ax,(1.75,2.85),(1.75,3.15),color=BLUE)
    box(ax,1.0,.65,4.5,.65,"enable = 0 at edge: Q stays 5",kind="state",fontsize=12)
    box(ax,6.0,.65,4.95,.65,"enable = 1 at edge: Q becomes 6",kind="state",fontsize=12)
    footer(ax,"Between edges Q holds. After an update, the incrementer computes the following count; it does not store it.")
    save(fig,"05-register-feedback.png")


def clock_and_sampling():
    fig,ax=canvas("Registers sample on rising edges, then hold",
                  "An ideal two-stage pipeline: first <= input; second <= first. Reset has already set both stages to zero.",height=7.4)
    left,right=1.7,11.3
    scale=(right-left)/10
    xx=lambda t:left+t*scale
    edges=[2,5,8]
    for t in edges:
        ax.axvline(xx(t),ymin=.18,ymax=.76,color=ORANGE,lw=1.1,ls="--",zorder=0)
        text(ax,xx(t),5.85,f"rise {edges.index(t)+1}",size=10,color=ORANGE)
    text(ax,.45,5.2,"clock",size=12,ha="left",color=MUTED)
    clock_times=[0,2,2,3.5,3.5,5,5,6.5,6.5,8,8,9.5,9.5,10]
    clock_levels=[0,0,1,1,0,0,1,1,0,0,1,1,0,0]
    ax.plot([xx(t) for t in clock_times],[4.95+.5*v for v in clock_levels],color=INK,lw=2)
    for t in edges:
        arrow(ax,(xx(t),4.6),(xx(t),4.91),color=ORANGE)

    rows=[("input",3.9,[(0,1,0),(1,3,7),(3,4,13),(4,6.8,9),(6.8,10,4)],GREEN),
          ("first",2.75,[(0,2,0),(2,5,7),(5,8,9),(8,10,4)],BLUE),
          ("second",1.6,[(0,2,0),(2,5,0),(5,8,7),(8,10,9)],PURPLE)]
    for name,y,segments,color in rows:
        text(ax,.45,y,name,size=12,ha="left",color=color)
        for start,end,val in segments:
            ax.add_patch(Rectangle((xx(start),y-.28),(end-start)*scale,.56,
                                   facecolor="white",edgecolor=color,lw=1.5,zorder=2))
            text(ax,(xx(start)+xx(end))/2,y,str(val),size=13,color=color,mono=True)
    text(ax,xx(3.5),4.57,"not sampled",size=10,color=GREEN)
    arrow(ax,(xx(3.5),4.4),(xx(3.5),4.2),color=GREEN)
    arrow(ax,(xx(2)+.12,3.48),(xx(2)+.12,3.08),color=BLUE)
    arrow(ax,(xx(5)+.12,2.35),(xx(5)+.12,1.93),color=PURPLE)
    text(ax,4.6,.8,"At rise 2: first takes 9; second takes the old first value, 7.",size=12,ha="center")
    footer(ax,"Rows show ideal stored values after each edge. Physical clock-to-Q, setup, and hold timing are omitted.")
    save(fig,"06-clock-and-sampling.png")


def render_all():
    signals_and_bits()
    binary_and_overflow()
    gates_and_mux()
    adder_and_alu()
    register_feedback()
    clock_and_sampling()


if __name__ == "__main__":
    render_all()
