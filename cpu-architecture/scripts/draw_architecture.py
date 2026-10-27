"""Draw six precise architecture illustrations for the CPU primer.

Run with a Python environment containing Matplotlib. All numbers are
teaching examples or values from the local Tiny8 instruction contract.
"""

from matplotlib.patches import Rectangle

from diagram_style import (
    canvas, text, box, arrow, wire, footer, save, KINDS,
    INK, MUTED, BLUE, GREEN, ORANGE, PURPLE, GRAY,
)


def cell(ax, x, y, w, h, value, kind="plain", size=11):
    fill, edge = KINDS[kind]
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill,
                           edgecolor=edge, linewidth=1.1, zorder=2))
    text(ax, x+w/2, y+h/2, value, size=size, mono=True)


def memory_bus():
    fig, ax = canvas("An address selects data; it is not the data",
                     "Tiny8 has separate address, write-data, read-data, and write-enable signals.")
    box(ax, .5, 2.0, 2.25, 3.2, "CPU", kind="state")
    text(ax, 1.625, 4.25, "One requester", size=11, color=BLUE)
    text(ax, 1.625, 2.65, "A = 09", size=14, mono=True)
    box(ax, 8.05, 1.65, 3.4, 3.8, "", kind="memory")
    text(ax, 9.75, 5.08, "256-byte RAM", size=13, weight="bold", color=PURPLE)
    text(ax, 8.85, 4.59, "Address", size=11, weight="bold")
    text(ax, 10.45, 4.59, "Contents", size=11, weight="bold")
    for index, (address, value) in enumerate((("00", "01"), ("01", "05"),
                                               ("…", "…"), ("80", "09"),
                                               ("…", "…"), ("FF", "00"))):
        yy = 4.1-index*.38
        if address == "80":
            ax.add_patch(Rectangle((8.25, yy-.17), 2.95, .35,
                                   facecolor="#fff0d5", edgecolor=ORANGE, lw=1.1,
                                   zorder=3))
        text(ax, 8.85, yy, address, size=12, mono=True)
        text(ax, 10.45, yy, value, size=12, mono=True)
    for yy, label, direction, color in (
        (4.65, "address = 80  [8 bits]", "out", BLUE),
        (3.85, "write data = 09  [8 bits]", "out", ORANGE),
        (3.05, "write enable = 1  [1 bit]", "out", ORANGE),
        (2.25, "read data = RAM[80]  [8 bits]", "in", PURPLE),
    ):
        ends = ((2.75, yy), (8.05, yy)) if direction == "out" else ((8.05, yy), (2.75, yy))
        arrow(ax, *ends, color=color)
        text(ax, 5.4, yy+.2, label, size=11, color=color)
    text(ax, 6, 1.13, "At a write edge with enable = 1: RAM[80] stores 09.",
         size=13, weight="bold")
    text(ax, 6, .71, "A read follows the selected address after access delay; a CPU register captures it separately.", size=11)
    footer(ax, "All values above are hexadecimal. Address 80 selects one byte; it does not mean that byte contains 80.")
    save(fig, "07-memory-and-bus.png")


def tiny8_datapath():
    fig, ax = canvas("Tiny8 reuses its parts across instruction steps",
                     "Blue: stored registers. Green: combinational logic. Purple: memory. Orange: control.")
    text(ax, .5, 5.5, "FETCH / OPERAND: select a program byte, then capture it", size=12,
         ha="left", weight="bold")
    box(ax, .5, 4.1, 1.4, 1.0, "PC", kind="state", sub="next byte")
    box(ax, 2.55, 4.1, 1.6, 1.0, "Address mux", sub="select PC", fontsize=11)
    box(ax, 4.85, 4.1, 1.6, 1.0, "RAM", kind="memory", sub="read byte")
    box(ax, 7.35, 4.55, 1.45, .65, "IR", kind="state")
    box(ax, 7.35, 3.5, 1.45, .65, "operand", kind="state", fontsize=11)
    box(ax, 9.65, 4.1, 1.85, 1.0, "Control", kind="control",
        sub="state + decode", fontsize=12)
    arrow(ax, (1.9,4.6),(2.55,4.6),color=BLUE)
    arrow(ax, (4.15,4.6),(4.85,4.6),color=GREEN)
    wire(ax, [(6.45,4.6),(6.85,4.6),(6.85,4.875),(7.35,4.875)],color=PURPLE)
    wire(ax, [(6.85,4.6),(6.85,3.825),(7.35,3.825)],color=PURPLE)
    arrow(ax, (8.8,4.875),(9.65,4.875),color=BLUE)
    text(ax, 6.82, 5.31, "FETCH", size=9.8, color=BLUE)
    text(ax, 6.5, 3.5, "OPERAND", size=9.8, color=BLUE)
    text(ax, 9.95, 3.59, "Enables choose which\nregister captures the byte.", size=10.5)
    text(ax, .5, 2.98, "EXECUTE an ADD: compute continuously; store only at the enabled edge", size=12,
         ha="left", weight="bold")
    box(ax, .7, 1.45, 1.7, .95, "A before edge", kind="state", sub="5", fontsize=11)
    box(ax, 3.15, 1.45, 1.7, .95, "operand", kind="state", sub="4", fontsize=11)
    box(ax, 6.1, 1.45, 1.65, .95, "ALU: ADD", sub="result wire = 9", fontsize=11)
    box(ax, 9.35, 1.45, 1.95, .95, "A after edge", kind="state", sub="9", fontsize=11)
    wire(ax, [(2.4,1.925),(2.75,1.925),(2.75,2.62),(6.925,2.62),(6.925,2.4)],color=BLUE)
    arrow(ax, (4.85,1.925),(6.1,1.925),color=BLUE)
    arrow(ax, (7.75,1.925),(9.35,1.925),color=GREEN)
    text(ax, 8.55, 2.23, "capture", size=10.5, color=GREEN)
    text(ax, 6, .88, "The two A boxes show the same register before and after one edge, not two physical registers.", size=11)
    footer(ax, "Simplified transfer views: load-input muxes, store-data wiring, Z updates, and jump paths are omitted here.")
    save(fig, "08-tiny8-datapath.png")


def instruction_edges():
    fig, ax = canvas("From seven program bytes to fourteen clock edges",
                     "LDA #5 → ADD #4 → STA $80 → HLT. Register values below are shown AFTER each rising edge.")
    text(ax, .45, 5.34, "Memory\naddress", size=10.5, ha="left")
    text(ax, .45, 4.69, "Stored\nbyte", size=10.5, ha="left")
    memory_x = 2.1
    for index, value in enumerate(("01","05","02","04","06","80","0A")):
        xx=memory_x+index*1.24
        text(ax,xx+.52,5.44,f"{index:02X}",size=11,mono=True)
        cell(ax,xx,4.35,1.04,.7,value,"memory",size=14)
    for xx, title in ((3.24,"LDA #5"),(5.72,"ADD #4"),(8.2,"STA $80"),(10.42,"HLT")):
        text(ax,xx,4.02,title,size=11,weight="bold")
    x0=1.85
    width=.665
    text(ax,.45,3.35,"Rising edge",size=10.5,ha="left")
    text(ax,.45,2.71,"Step at edge",size=10.5,ha="left")
    text(ax,.45,1.97,"A afterward",size=10.5,ha="left")
    # Four states each for the load, add, store; FETCH+DECODE for halt.
    states=["F","D","O","E"]*3+["F","D"]
    a_values=[0,0,0,5,5,5,5,9,9,9,9,9,9,9]
    colors={"F":"memory","D":"control","O":"state","E":"logic"}
    for i,(state,value) in enumerate(zip(states,a_values)):
        xx=x0+i*width
        text(ax,xx+width/2,3.35,str(i+1),size=11,mono=True)
        cell(ax,xx,2.4,width,.6,state,colors[state],size=13)
        cell(ax,xx,1.65,width,.6,str(value),"state",size=12)
    for begin,count,label,color in ((0,4,"load 5",BLUE),(4,4,"add 4",GREEN),
                                     (8,4,"store 9",ORANGE),(12,2,"halt",PURPLE)):
        left=x0+begin*width
        right=left+count*width
        ax.plot([left+.04,right-.04],[1.43,1.43],color=color,lw=2.4)
        text(ax,(left+right)/2,1.15,label,size=11,color=color,weight="bold")
    text(ax,6,.7,"Edge 4: A = 5     •     Edge 8: A = 9     •     Edge 12: RAM[80] = 9     •     Edge 14: HALT",size=11.5)
    footer(ax,"F = FETCH, D = DECODE, O = OPERAND, E = EXECUTE. Reset is complete before edge 1; memory bytes are hexadecimal.")
    save(fig,"09-instruction-edges.png")


def pipeline_hazards():
    fig,ax=canvas("Pipelining overlaps instructions, not their dependencies",
                  "An ideal five-stage pipeline: each instruction takes five cycles, but completions can be one cycle apart.")
    x0=2.45
    w=1.17
    stage_kinds={"F":"memory","D":"control","E":"logic","M":"memory","W":"state"}
    for cycle in range(7):
        text(ax,x0+(cycle+.5)*w,5.42,str(cycle+1),size=11,mono=True)
    text(ax,1.2,5.42,"Cycle",size=11,weight="bold")
    for instruction in range(3):
        yy=4.5-instruction*.72
        text(ax,1.2,yy+.3,f"Instruction {instruction+1}",size=11)
        for cycle in range(7):
            stage_index=cycle-instruction
            stage="FDEMW"[stage_index] if 0<=stage_index<5 else ""
            cell(ax,x0+cycle*w,yy,w,.6,stage,stage_kinds.get(stage,"plain"),size=13)
    text(ax,6,2.68,"F fetch · D decode · E execute · M memory · W writeback",size=11,color=MUTED)
    text(ax,.5,2.16,"A dependent instruction has two possible situations:",size=12,ha="left",weight="bold")
    box(ax,.5,.92,2.3,.83,"Value is ready",kind="logic",fontsize=11)
    box(ax,4.0,.92,1.65,.83,"Consumer",kind="state",fontsize=11)
    arrow(ax,(2.8,1.33),(4.0,1.33),color=GREEN)
    text(ax,3.4,1.68,"forward",size=10.5,color=GREEN)
    box(ax,6.5,.92,2.45,.83,"Load not ready",kind="memory",fontsize=11)
    box(ax,10.0,.92,1.5,.83,"Wait",kind="control",fontsize=11)
    arrow(ax,(8.95,1.33),(10.0,1.33),color=ORANGE)
    text(ax,9.48,1.68,"stall",size=10.5,color=ORANGE)
    footer(ax,"Hypothetical processor, not Tiny8. The top schedule assumes independent instructions and no resource conflicts or stalls.")
    save(fig,"10-pipeline-and-hazards.png")


def memory_hierarchy():
    fig,ax=canvas("Memory has layers because size and access cost compete",
                  "Registers hold working values. Caches retain memory lines. DRAM and persistent storage have different roles.")
    levels=[(4.72,1.95,"Registers","state"),
            (3.84,2.65,"L1 cache","memory"),
            (2.96,3.35,"L2 / last-level cache","memory"),
            (2.08,4.05,"DRAM: main memory","memory")]
    for yy,width,title,kind in levels:
        xx=2.75-width/2
        box(ax,xx,yy,width,.6,title,kind=kind,fontsize=11)
    for upper,lower in zip(levels,levels[1:]):
        arrow(ax,(2.75,upper[0]),(2.75,lower[0]+.6),color=PURPLE)
    box(ax,.5,.65,4.5,.65,"SSD: persistent file / block storage",kind="plain",fontsize=11)
    wire(ax,[(2.75,1.3),(2.75,2.08)],color=MUTED,dashed=True)
    text(ax,3.0,1.64,"OS-managed I/O\nor page transfer",size=9.5,color=MUTED,ha="left")
    text(ax,8.6,5.22,"A cache copies neighboring bytes together",size=12,weight="bold")
    text(ax,8.6,4.76,"Illustrative eight-byte line, addresses in decimal",size=10.5,color=MUTED)
    for i in range(8):
        cell(ax,6.05+i*.64,3.77,.64,.65,str(16+i),"memory",size=10.5)
    ax.plot([6.07,11.15],[3.55,3.55],color=PURPLE,lw=2)
    text(ax,8.6,3.26,"One line contains several nearby locations.",size=11,color=PURPLE)
    box(ax,6.05,2.11,5.1,.75,"Spatial locality: 16 → 17 → 18 → 19",kind="logic",fontsize=11)
    box(ax,6.05,1.05,5.1,.75,"Temporal locality: 16 → 16 → 16",kind="state",fontsize=11)
    footer(ax,"A CPU cache miss searches lower memory levels, not the SSD directly. Layouts and costs vary; no timings are implied.")
    save(fig,"11-memory-hierarchy.png")


def rtl_flow():
    fig,ax=canvas("Simulation checks behavior; implementation builds a circuit",
                  "The same supported RTL can feed separate verification and hardware-implementation flows.")
    box(ax,.5,3.15,2.1,1.1,"RTL source",kind="state",sub="modules + connections")
    box(ax,4.05,4.55,2.1,.95,"Simulator",kind="logic",sub="evaluate the model")
    box(ax,8.0,4.55,3.5,.95,"Waveforms + assertions",kind="plain",sub="observations and functional checks",fontsize=12)
    box(ax,4.05,3.15,2.1,.8,"Testbench",kind="control",fontsize=12)
    wire(ax,[(2.6,3.95),(3.2,3.95),(3.2,5.025),(4.05,5.025)],color=BLUE)
    arrow(ax,(5.1,3.95),(5.1,4.55),color=ORANGE)
    arrow(ax,(6.15,5.025),(8.0,5.025),color=GREEN)
    box(ax,4.05,1.9,2.1,.95,"Synthesis",kind="logic",sub="map supported RTL")
    box(ax,7.0,1.9,1.45,.95,"Netlist",kind="plain",fontsize=11.5)
    box(ax,9.2,1.9,2.3,.95,"Place + route\nTiming analysis",kind="control",fontsize=11)
    wire(ax,[(2.6,3.4),(3.2,3.4),(3.2,2.375),(4.05,2.375)],color=BLUE)
    arrow(ax,(6.15,2.375),(7.0,2.375),color=GREEN)
    arrow(ax,(8.45,2.375),(9.2,2.375),color=MUTED)
    box(ax,9.2,.65,2.3,.85,"Configure FPGA\nor fabricate ASIC",kind="memory",fontsize=11)
    arrow(ax,(10.35,1.9),(10.35,1.5),color=PURPLE)
    text(ax,6.3,.98,"Target technology + timing constraints\nguide physical implementation.",size=11,color=MUTED)
    footer(ax,"A passing simulation does not prove timing closure. Synthesis alone produces neither a routed FPGA bitstream nor a fabricated ASIC.")
    save(fig,"12-rtl-to-hardware.png")


def render_all():
    memory_bus()
    tiny8_datapath()
    instruction_edges()
    pipeline_hazards()
    memory_hierarchy()
    rtl_flow()


if __name__=="__main__":
    render_all()
