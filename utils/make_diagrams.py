"""Draw the PNG diagrams used by verilong/cpu/intro.md.

Needs matplotlib. From the repo root:
    python3 -m venv /tmp/tiny8-diagrams
    /tmp/tiny8-diagrams/bin/pip install matplotlib
    /tmp/tiny8-diagrams/bin/python utils/make_diagrams.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

OUT = Path(__file__).resolve().parents[1] / "verilong" / "cpu" / "docs" / "img"

INK = "#1f2933"
MUTED = "#616e7c"
WIRE = "#3e4c59"
FAINT = "#c3cad3"

# (fill, edge). The same colour always means the same kind of hardware.
REG = ("#e3efff", "#2f6fb3")
COMB = ("#e5f5e9", "#2f8f4e")
CTRL = ("#fff0dc", "#c26a00")
MEM = ("#f0e8ff", "#6f47b5")
SOFT = ("#f3f5f7", "#9aa5b1")
HOT = ("#fff4c2", "#c98a00")
WHITE = ("#ffffff", MEM[1])

SANS = "DejaVu Sans"
MONO = "DejaVu Sans Mono"
ARROW = "-|>,head_length=0.55,head_width=0.3"
HEAD = 0.1

plt.rcParams.update({"font.family": SANS, "font.size": 11, "text.color": INK})


def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=150, facecolor="white", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", OUT / name)


def box(ax, x, y, w, h, colors, lw=1.8, r=0.08, z=1):
    fc, ec = colors
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def label(ax, x, y, s, size=11, color=INK, weight="normal", ha="center", va="center",
          family=SANS, style="normal", rotation=0, z=5):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight, ha=ha, va=va, family=family,
            style=style, rotation=rotation, linespacing=1.35, zorder=z)


def stack(ax, cx, cy, items, gap=0.05):
    heights = [(s.count("\n") + 1) * size * 1.4 / 72 for s, size, _ in items]
    y = cy + (sum(heights) + gap * (len(items) - 1)) / 2
    for (s, size, kw), h in zip(items, heights):
        label(ax, cx, y - h / 2, s, size=size, **kw)
        y -= h + gap


def block(ax, x, y, w, h, colors, title, sub=None, code=None, title_size=12.5):
    box(ax, x, y, w, h, colors)
    items = [(title, title_size, {"weight": "bold"})]
    if sub:
        items.append((sub, 9.5, {"color": MUTED}))
    if code:
        items.append((code, 9.5, {"family": MONO, "color": colors[1]}))
    stack(ax, x + w / 2, y + h / 2, items)


def wire(ax, pts, color=WIRE, lw=1.7, head=True, dashed=False, z=2):
    pts = list(pts)
    line = pts
    if head:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        line = pts[:-1] + [(x2 - ux * HEAD, y2 - uy * HEAD)]
    xs, ys = zip(*line)
    ax.plot(xs, ys, color=color, lw=lw, ls=(0, (4, 2.5)) if dashed else "-",
            solid_capstyle="butt", dash_capstyle="butt", solid_joinstyle="miter", zorder=z)
    if head:
        ax.add_patch(FancyArrowPatch((x2 - ux * 0.02, y2 - uy * 0.02), (x2, y2), arrowstyle=ARROW,
                                     mutation_scale=14, color=color, lw=0, shrinkA=0, shrinkB=0,
                                     zorder=z))


def curve(ax, p1, p2, rad, color=WIRE, lw=1.8, style=ARROW):
    ax.add_patch(FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}", arrowstyle=style,
                                 mutation_scale=14, color=color, lw=lw, shrinkA=0, shrinkB=0,
                                 zorder=2))


def dot(ax, x, y, color=WIRE):
    ax.plot([x], [y], "o", ms=5, color=color, zorder=4)


def bridge(ax, x, y, under_is_horizontal):
    # Break the lower wire at a crossing so the other one reads as passing over it.
    if under_is_horizontal:
        ax.plot([x - 0.09, x + 0.09], [y, y], color="white", lw=5, zorder=2.5)
    else:
        ax.plot([x, x], [y - 0.09, y + 0.09], color="white", lw=5, zorder=2.5)


def mux(ax, x, y, w, h, inset):
    ax.add_patch(Polygon([(x, y), (x + w, y + inset), (x + w, y + h - inset), (x, y + h)],
                         closed=True, fc=COMB[0], ec=COMB[1], lw=1.8, zorder=1))
    label(ax, x + w / 2, y + h / 2, "mux", size=8.5, color=COMB[1])


def clock_mark(ax, x, y, color, s=0.12):
    ax.add_patch(Polygon([(x, y - s), (x + s * 1.3, y), (x, y + s)], closed=True, fill=False,
                         ec=color, lw=1.4, zorder=3))


def tag(ax, x, y, s, ha="left"):
    label(ax, x, y, s, size=8.5, color=CTRL[1], weight="bold", ha=ha)


def bus_segment(ax, x0, x1, yc, amp, text, fill="white", d=0.07):
    pts = [(x0, yc), (x0 + d, yc + amp), (x1 - d, yc + amp), (x1, yc), (x1 - d, yc - amp),
           (x0 + d, yc - amp)]
    ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=WIRE, lw=1.5, zorder=2))
    label(ax, (x0 + x1) / 2, yc, text, family=MONO, size=11)


def layers():
    fig, ax = canvas(10.4, 6.45)
    rows = [
        ("Software", "Programs people write: C, Python, apps", "a = a + 4", "compiled into"),
        ("Instruction set (ISA)", "The contract: which bytes mean which operation",
         "ADD #4  =  02 04", "carried out by"),
        ("Microarchitecture (RTL)", "The hardware that makes those bytes do something",
         None, "synthesized into"),
        ("Logic gates and flip-flops", "AND, OR, NOT, and 1-bit memory cells", "AND  OR  DFF",
         "built from"),
        ("Transistors", "Tiny on/off switches etched into silicon", "on / off", None),
    ]
    x, w, h, gap, top = 1.0, 6.2, 0.86, 0.34, 6.05
    for i, (name, desc, example, link) in enumerate(rows):
        y = top - h - i * (h + gap)
        here = example is None
        box(ax, x, y, w, h, HOT if here else SOFT, lw=2.6 if here else 1.6)
        label(ax, x + 0.25, y + h * 0.66, name, size=12.5, weight="bold", ha="left")
        label(ax, x + 0.25, y + h * 0.3, desc, size=10, color=MUTED, ha="left")
        if here:
            label(ax, x + w + 0.35, y + h * 0.66, "SystemVerilog", family=MONO, size=11.5,
                  weight="bold", ha="left")
            label(ax, x + w + 0.35, y + h * 0.3, "\u2190 you are here", size=11, weight="bold",
                  color=HOT[1], ha="left")
        else:
            label(ax, x + w + 0.35, y + h / 2, example, family=MONO, size=11, ha="left")
        if link:
            label(ax, x + w / 2, y - gap / 2, "\u2193  " + link, size=9.5, color=MUTED,
                  style="italic")
    curve(ax, (0.5, 0.55), (0.5, 5.9), 0, color=FAINT, lw=1.6,
          style="<|-|>,head_length=0.55,head_width=0.3")
    label(ax, 0.5, 6.15, "abstract", size=9.5, color=MUTED)
    label(ax, 0.5, 0.3, "physical", size=9.5, color=MUTED)
    save(fig, "01_layers.png")


def computer():
    fig, ax = canvas(10.3, 5.5)
    box(ax, 0.3, 0.35, 5.7, 4.85, SOFT, r=0.14)
    label(ax, 0.55, 4.92, "CPU", size=14, weight="bold", ha="left")
    block(ax, 0.6, 2.95, 2.3, 1.55, CTRL, "Control unit", "decides what happens\non each clock")
    block(ax, 3.55, 2.95, 2.15, 1.55, REG, "Registers", "tiny, fast storage", "PC  IR  A")
    block(ax, 2.0, 0.65, 2.5, 1.45, COMB, "ALU", "does the math", "+  \u2212  AND  OR")

    wire(ax, [(2.9, 3.95), (3.55, 3.95)], color=CTRL[1], dashed=True)
    label(ax, 3.22, 4.12, "load", size=8.5, color=CTRL[1], weight="bold")
    wire(ax, [(3.55, 3.4), (2.9, 3.4)])
    label(ax, 3.22, 3.23, "opcode", size=8.5, color=MUTED)
    wire(ax, [(2.45, 2.95), (2.45, 2.1)], color=CTRL[1], dashed=True)
    label(ax, 2.35, 2.52, "which op", size=8.5, color=CTRL[1], weight="bold", ha="right")
    wire(ax, [(4.0, 2.95), (4.0, 2.1)])
    label(ax, 3.9, 2.52, "inputs", size=8.5, color=MUTED, ha="right")
    wire(ax, [(4.5, 1.35), (5.1, 1.35), (5.1, 2.95)])
    label(ax, 5.2, 2.2, "result", size=8.5, color=MUTED, ha="left")

    box(ax, 7.3, 0.65, 2.7, 3.95, MEM)
    label(ax, 8.65, 4.25, "Memory", size=13, weight="bold")
    box(ax, 7.55, 2.45, 2.2, 1.45, WHITE, lw=1.2)
    stack(ax, 8.65, 3.175, [("program", 11, {"weight": "bold", "color": MEM[1]}),
                            ("instructions", 9.5, {"color": MUTED})])
    box(ax, 7.55, 0.9, 2.2, 1.35, WHITE, lw=1.2)
    stack(ax, 8.65, 1.575, [("data", 11, {"weight": "bold", "color": MEM[1]}),
                            ("numbers you store", 9.5, {"color": MUTED})])

    wire(ax, [(6.0, 3.75), (7.3, 3.75)])
    label(ax, 6.65, 3.92, "address", size=9.5, color=MUTED)
    curve(ax, (6.0, 2.75), (7.3, 2.75), 0, lw=1.7, style="<|-|>,head_length=0.55,head_width=0.3")
    label(ax, 6.65, 2.92, "data", size=9.5, color=MUTED)
    wire(ax, [(6.0, 1.75), (7.3, 1.75)], color=CTRL[1], dashed=True)
    label(ax, 6.65, 1.92, "write?", size=9.5, color=CTRL[1], weight="bold")
    save(fig, "02_computer.png")


def cycle():
    fig, ax = canvas(9.6, 5.8)
    steps = {
        "FETCH": ((4.8, 4.55), "read the byte at PC,\nthen PC = PC + 1"),
        "DECODE": ((7.9, 1.3), "what does this\nopcode mean?"),
        "EXECUTE": ((1.7, 1.3), "do it: math, load,\nstore, or jump"),
    }
    w, h = 3.0, 1.35
    for name, ((cx, cy), sub) in steps.items():
        box(ax, cx - w / 2, cy - h / 2, w, h, CTRL)
        stack(ax, cx, cy, [(name, 14, {"weight": "bold"}), (sub, 10.5, {"color": MUTED})])
    curve(ax, (6.3, 4.55), (7.9, 1.975), -0.3)
    curve(ax, (6.4, 1.3), (3.2, 1.3), -0.3)
    curve(ax, (1.7, 1.975), (3.3, 4.55), -0.3)
    label(ax, 4.8, 2.4, "repeat until HLT", size=11, color=MUTED, style="italic")
    save(fig, "04_fetch_decode_execute.png")


def comb_vs_seq():
    fig, ax = canvas(11.0, 6.9)

    box(ax, 0.3, 3.55, 5.1, 3.1, SOFT, r=0.12)
    label(ax, 0.55, 6.3, "Combinational", size=13.5, weight="bold", ha="left")
    label(ax, 0.55, 5.95, "always_comb  /  assign", size=10, family=MONO, color=COMB[1], ha="left")
    box(ax, 1.9, 4.4, 1.6, 1.0, COMB)
    label(ax, 2.7, 4.9, "a + b", family=MONO, size=13, weight="bold")
    label(ax, 0.9, 5.15, "a", family=MONO, size=11)
    wire(ax, [(1.1, 5.15), (1.9, 5.15)])
    label(ax, 0.9, 4.65, "b", family=MONO, size=11)
    wire(ax, [(1.1, 4.65), (1.9, 4.65)])
    wire(ax, [(3.5, 4.9), (4.3, 4.9)])
    label(ax, 4.4, 4.9, "result", family=MONO, size=10, ha="left")
    label(ax, 2.85, 3.95, "No memory and no clock.\nChange a or b and result changes right away.",
          size=10, color=MUTED)

    box(ax, 5.7, 3.55, 5.0, 3.1, SOFT, r=0.12)
    label(ax, 5.95, 6.3, "Sequential", size=13.5, weight="bold", ha="left")
    label(ax, 5.95, 5.95, "always_ff @(posedge clk)", size=10, family=MONO, color=REG[1],
          ha="left")
    box(ax, 7.6, 4.35, 1.3, 1.1, REG)
    label(ax, 8.25, 4.9, "acc", family=MONO, size=12, weight="bold")
    label(ax, 7.74, 5.15, "D", size=9, color=MUTED)
    label(ax, 8.76, 4.9, "Q", size=9, color=MUTED)
    clock_mark(ax, 7.6, 4.62, REG[1])
    label(ax, 5.95, 5.15, "alu_result", family=MONO, size=10, ha="left")
    wire(ax, [(6.85, 5.15), (7.6, 5.15)])
    label(ax, 5.95, 4.62, "clk", family=MONO, size=10, ha="left")
    wire(ax, [(6.4, 4.62), (7.6, 4.62)], head=False)
    wire(ax, [(8.9, 4.9), (9.6, 4.9)])
    label(ax, 9.7, 4.9, "stored\nvalue", size=9.5, color=MUTED, ha="left")
    label(ax, 8.2, 3.95, "Holds its value. Takes a new one only\non the rising edge of clk.",
          size=10, color=MUTED)

    box(ax, 0.3, 0.3, 10.4, 2.95, SOFT, r=0.12)
    label(ax, 0.55, 2.9, "pc <= pc + 1", family=MONO, size=12.5, weight="bold", ha="left")
    label(ax, 2.0, 2.9, "is this circuit, not a line of code that runs later", size=11,
          color=MUTED, ha="left")
    box(ax, 3.2, 1.0, 1.4, 1.0, REG)
    label(ax, 3.9, 1.5, "PC", size=13, weight="bold")
    label(ax, 3.33, 1.75, "D", size=9, color=MUTED)
    label(ax, 4.47, 1.5, "Q", size=9, color=MUTED)
    clock_mark(ax, 3.2, 1.25, REG[1])
    wire(ax, [(4.6, 1.5), (6.2, 1.5)])
    label(ax, 5.4, 1.63, "pc", family=MONO, size=9, color=MUTED)
    box(ax, 6.2, 1.15, 1.0, 0.7, COMB)
    label(ax, 6.7, 1.5, "+1", family=MONO, size=13, weight="bold")
    wire(ax, [(7.2, 1.5), (7.8, 1.5), (7.8, 2.45), (2.7, 2.45), (2.7, 1.75), (3.2, 1.75)])
    label(ax, 5.25, 2.57, "pc + 1", family=MONO, size=9, color=MUTED)
    label(ax, 1.95, 1.25, "clk", family=MONO, size=10, ha="right")
    wire(ax, [(2.05, 1.25), (3.2, 1.25)], head=False)
    label(ax, 3.9, 0.62, "register: only changes\non the clock edge", size=9.5, color=REG[1])
    label(ax, 6.7, 0.7, "combinational:\nalways adding", size=9.5, color=COMB[1])
    label(ax, 9.25, 1.55, "Every rising edge\nof clk, PC becomes\npc + 1.", size=10, color=MUTED)
    save(fig, "05_comb_vs_seq.png")


def clock():
    fig, ax = canvas(10.6, 4.6)

    def X(t):
        return 2.3 + t * 0.78

    for t in (1, 3, 5, 7, 9):
        ax.plot([X(t)] * 2, [0.9, 3.95], color=FAINT, ls=(0, (3, 3)), lw=1.2, zorder=0)
    label(ax, X(1) - 0.05, 4.2, "\u2191 rising edge: every always_ff register copies its input",
          size=10, color=MUTED, ha="left")

    lo, hi = 3.33, 3.77
    pts = [(X(0), lo)]
    for k in range(5):
        pts += [(X(2 * k + 1), lo), (X(2 * k + 1), hi), (X(2 * k + 2), hi), (X(2 * k + 2), lo)]
    ax.plot(*zip(*pts), color=WIRE, lw=2, zorder=2)

    label(ax, 0.3, 3.55, "clk", family=MONO, size=11, weight="bold", ha="left")
    label(ax, 0.3, 2.52, "alu_result", family=MONO, size=11, ha="left")
    label(ax, 0.3, 2.22, "always_comb", family=MONO, size=9, color=COMB[1], ha="left")
    label(ax, 0.3, 1.37, "acc", family=MONO, size=11, ha="left")
    label(ax, 0.3, 1.07, "always_ff", family=MONO, size=9, color=REG[1], ha="left")

    for t0, t1, v in [(0, 1.7, "5"), (1.7, 2.5, "9"), (2.5, 5.6, "4"), (5.6, 10, "6")]:
        bus_segment(ax, X(t0), X(t1), 2.4, 0.24, v, fill=HOT[0] if v == "9" else "white")
    for t0, t1, v in [(0, 1, "0"), (1, 3, "5"), (3, 7, "4"), (7, 10, "6")]:
        bus_segment(ax, X(t0), X(t1), 1.25, 0.24, v, fill=REG[0])
    for t in (1, 3, 5, 7, 9):
        wire(ax, [(X(t), 2.16), (X(t), 1.52)], color=REG[1], lw=1.3)

    label(ax, X(5), 0.5, "9 only existed between two rising edges, so acc never stored it.",
          size=10, color=MUTED, style="italic")
    save(fig, "06_clock.png")


def encoding():
    fig, ax = canvas(8.0, 6.85)
    rows = [
        ("0x00", "01", "opcode: LDA #imm", CTRL),
        ("0x01", "nn", "operand: a constant", REG),
        ("0x02", "02", "opcode: ADD #imm", CTRL),
        ("0x03", "nn", "operand: a constant", REG),
        ("0x04", "06", "opcode: STA addr", CTRL),
        ("0x05", "80", "operand: an address", REG),
        ("0x06", "0A", "opcode: HLT", CTRL),
        None,
        ("0x80", "??", "data", MEM),
        None,
    ]
    top, rh = 6.3, 0.52

    def yc(i):
        return top - (i + 1) * rh + rh / 2

    label(ax, 1.2, 6.55, "address", size=9.5, color=MUTED)
    label(ax, 2.05, 6.55, "byte", size=9.5, color=MUTED)
    label(ax, 2.85, 6.55, "what the CPU treats it as", size=9.5, color=MUTED, ha="left")
    label(ax, 5.6, 6.55, "instruction", size=9.5, color=MUTED, ha="left")

    for i, row in enumerate(rows):
        if row is None:
            label(ax, 2.05, yc(i), "\u22ee", size=15, color=MUTED)
            continue
        addr, byte, meaning, colors = row
        label(ax, 1.45, yc(i), addr, family=MONO, size=10.5, color=MUTED, ha="right")
        box(ax, 1.6, yc(i) - rh / 2 + 0.03, 0.9, rh - 0.06, colors, lw=1.5, r=0.05)
        label(ax, 2.05, yc(i), byte, family=MONO, size=12, weight="bold")
        label(ax, 2.85, yc(i), meaning, size=10.5, ha="left")

    for first, last, asm in [(0, 1, "LDA #nn"), (2, 3, "ADD #nn"), (4, 5, "STA $80"),
                             (6, 6, "HLT")]:
        y1 = yc(first) + rh / 2 - 0.06
        y2 = yc(last) - rh / 2 + 0.06
        ax.plot([5.3, 5.4, 5.4, 5.3], [y1, y1, y2, y2], color=WIRE, lw=1.4)
        label(ax, 5.6, (y1 + y2) / 2, asm, family=MONO, size=11.5, weight="bold", ha="left")

    label(ax, 0.3, yc(0), "PC", size=11, weight="bold", ha="left")
    wire(ax, [(0.62, yc(0)), (0.95, yc(0))])

    curve(ax, (4.5, yc(5)), (3.45, yc(8)), -0.45, color=MEM[1], lw=1.5)
    label(ax, 4.75, 2.4, "an address is a number\nthat points at another byte", size=9.5,
          color=MEM[1], ha="left")

    label(ax, 0.3, 0.45, "256 bytes total (0x00\u20130xFF). Program and data share the same memory.",
          size=10, color=MUTED, ha="left")
    save(fig, "03_instruction_encoding.png")


def datapath():
    fig, ax = canvas(13.8, 9.0)

    block(ax, 0.4, 7.6, 13.0, 1.0, CTRL, "Control FSM",
          "each clock: pick the next state, then drive the orange control signals", "cpu.sv")

    block(ax, 0.4, 5.45, 1.4, 0.8, REG, "PC", code="pc.sv")
    mux(ax, 2.4, 5.1, 0.6, 1.0, 0.25)
    box(ax, 4.2, 4.8, 2.4, 2.0, MEM)
    stack(ax, 5.4, 6.1, [("Memory", 12.5, {"weight": "bold"}),
                         ("256 \u00d7 8 bits", 9.5, {"color": MUTED}),
                         ("memory.sv", 9.5, {"family": MONO, "color": MEM[1]})])
    label(ax, 4.28, 5.6, "addr", size=8.5, color=MUTED, ha="left")
    label(ax, 6.52, 5.6, "rdata", size=8.5, color=MUTED, ha="right")
    label(ax, 5.0, 4.95, "wdata", size=8.5, color=MUTED)
    block(ax, 8.2, 5.2, 1.4, 0.8, REG, "IR")
    block(ax, 10.2, 5.1, 2.4, 1.0, COMB, "Decoder", code="decoder.sv")

    wire(ax, [(1.8, 5.85), (2.4, 5.85)])
    label(ax, 2.1, 5.98, "pc", family=MONO, size=8.5, color=MUTED)
    wire(ax, [(3.0, 5.6), (4.2, 5.6)])
    wire(ax, [(6.6, 5.6), (8.2, 5.6)])
    label(ax, 7.05, 5.73, "rdata", family=MONO, size=8.5, color=MUTED)
    dot(ax, 7.55, 5.6)
    wire(ax, [(9.6, 5.6), (10.2, 5.6)])
    label(ax, 9.9, 5.73, "opcode", size=8, color=MUTED)
    wire(ax, [(11.4, 6.1), (11.4, 7.6)])
    label(ax, 11.5, 6.85, "flags", size=9, color=MUTED, ha="left")

    wire(ax, [(1.1, 7.6), (1.1, 6.25)], color=CTRL[1], dashed=True)
    tag(ax, 1.2, 6.55, "inc / load")
    wire(ax, [(2.7, 7.6), (2.7, 5.98)], color=CTRL[1], dashed=True)
    tag(ax, 2.8, 6.55, "sel")
    wire(ax, [(5.4, 7.6), (5.4, 6.8)], color=CTRL[1], dashed=True)
    tag(ax, 5.5, 7.2, "we (write)")
    wire(ax, [(8.9, 7.6), (8.9, 6.0)], color=CTRL[1], dashed=True)
    tag(ax, 9.0, 6.55, "load")

    block(ax, 2.6, 2.2, 1.4, 0.8, REG, "operand")
    tag(ax, 4.08, 3.1, "load")
    block(ax, 5.2, 2.0, 1.8, 1.2, COMB, "ALU", "op from decoder", "alu.sv")
    mux(ax, 8.0, 1.95, 0.6, 1.3, 0.3)
    tag(ax, 8.3, 3.42, "sel", ha="center")
    block(ax, 9.4, 2.2, 1.4, 0.8, REG, "A", "accumulator")
    tag(ax, 10.35, 3.12, "load")
    box(ax, 9.6, 0.9, 1.0, 0.6, COMB)
    label(ax, 10.1, 1.2, "== 0 ?", family=MONO, size=10, weight="bold")
    block(ax, 11.2, 0.9, 1.0, 0.6, REG, "Z")
    tag(ax, 11.7, 1.65, "load", ha="center")

    wire(ax, [(7.55, 5.6), (7.55, 3.0), (8.0, 3.0)])
    wire(ax, [(7.55, 4.3), (3.3, 4.3), (3.3, 3.0)])
    dot(ax, 7.55, 4.3)

    wire(ax, [(3.3, 2.2), (3.3, 1.3), (1.1, 1.3), (1.1, 5.45)])
    wire(ax, [(2.0, 1.3), (2.0, 5.35), (2.4, 5.35)])
    wire(ax, [(3.3, 1.3), (7.75, 1.3), (7.75, 2.2), (8.0, 2.2)])
    wire(ax, [(6.1, 1.3), (6.1, 2.0)])
    for x in (2.0, 3.3, 6.1):
        dot(ax, x, 1.3)
    label(ax, 4.3, 1.43, "operand", family=MONO, size=8.5, color=MUTED, ha="left")
    label(ax, 1.2, 3.3, "jump\ntarget", size=8, color=MUTED, ha="left")

    wire(ax, [(7.0, 2.6), (8.0, 2.6)])
    label(ax, 7.03, 2.73, "result", size=8, color=MUTED, ha="left")
    wire(ax, [(8.6, 2.6), (9.4, 2.6)])
    dot(ax, 9.0, 2.6)
    wire(ax, [(9.0, 2.6), (9.0, 1.2), (9.6, 1.2)])
    wire(ax, [(10.6, 1.2), (11.2, 1.2)])
    wire(ax, [(12.2, 1.2), (13.1, 1.2), (13.1, 7.6)])
    label(ax, 13.28, 4.4, "zero flag, used by JZ", size=8.5, color=MUTED, rotation=90)

    bridge(ax, 5.0, 4.3, under_is_horizontal=True)
    bridge(ax, 7.55, 3.75, under_is_horizontal=False)
    wire(ax, [(10.1, 3.0), (10.1, 3.75), (5.0, 3.75), (5.0, 4.8)], z=3)
    wire(ax, [(6.1, 3.75), (6.1, 3.2)], z=3)
    dot(ax, 6.1, 3.75)
    label(ax, 9.3, 3.88, "A", family=MONO, size=9, weight="bold", color=MUTED)

    lx, ly = 0.4, 0.3
    for colors, text, width in [(REG, "register  (always_ff)", 2.35),
                                (COMB, "combinational  (always_comb)", 3.0),
                                (MEM, "memory", 1.2)]:
        box(ax, lx, ly - 0.11, 0.3, 0.22, colors, lw=1.4, r=0.03)
        label(ax, lx + 0.42, ly, text, size=9.5, ha="left")
        lx += 0.42 + width
    wire(ax, [(lx, ly), (lx + 0.45, ly)], color=CTRL[1], dashed=True, head=False)
    label(ax, lx + 0.57, ly, "control signal from the FSM", size=9.5, color=CTRL[1], ha="left")
    save(fig, "07_tiny8_datapath.png")


def fsm():
    fig, ax = canvas(12.8, 7.4)
    w, h = 2.5, 1.0
    states = {
        "FETCH": ((1.6, 4.0), "ir \u2190 mem[pc]\npc \u2190 pc + 1", MONO),
        "DECODE": ((4.9, 4.0), "look at the opcode", SANS),
        "OPERAND": ((8.0, 5.55), "operand \u2190 mem[pc]\npc \u2190 pc + 1", MONO),
        "EXECUTE": ((11.0, 4.0), "ALU, store, or jump", SANS),
        "HALT": ((4.9, 1.5), "stay here", SANS),
        "LOAD": ((11.0, 1.5), "A \u2190 mem[operand]", MONO),
    }
    for name, ((cx, cy), sub, family) in states.items():
        box(ax, cx - w / 2, cy - h / 2, w, h, SOFT if name == "HALT" else CTRL)
        stack(ax, cx, cy, [(name, 12.5, {"weight": "bold"}),
                           (sub, 9.5, {"family": family, "color": MUTED})])

    wire(ax, [(2.85, 4.0), (3.65, 4.0)])
    wire(ax, [(6.15, 4.3), (6.75, 5.4)])
    label(ax, 6.3, 5.0, "needs an\noperand", size=9, color=MUTED, style="italic", ha="right")
    wire(ax, [(6.15, 3.8), (9.75, 3.8)])
    label(ax, 7.95, 3.6, "NOP (no operand)", size=9, color=MUTED, style="italic")
    wire(ax, [(9.25, 5.4), (10.4, 4.5)])
    curve(ax, (11.7, 4.5), (1.6, 4.5), 0.5)
    label(ax, 6.65, 7.2, "instruction done: fetch the next one", size=9.5, color=MUTED,
          style="italic")
    wire(ax, [(11.0, 3.5), (11.0, 2.0)])
    label(ax, 11.1, 2.75, "LDA addr", size=9, color=MUTED, style="italic", ha="left")
    wire(ax, [(11.0, 1.0), (11.0, 0.35), (1.6, 0.35), (1.6, 3.5)])
    wire(ax, [(4.9, 3.5), (4.9, 2.0)])
    label(ax, 5.0, 2.75, "HLT", size=9, color=MUTED, style="italic", ha="left")
    curve(ax, (6.15, 1.75), (6.15, 1.25), -1.8)
    label(ax, 6.75, 1.5, "forever", size=9, color=MUTED, style="italic", ha="left")
    save(fig, "08_tiny8_fsm.png")


def timeline():
    fig, ax = canvas(13.0, 6.2)
    states = ["FETCH", "DECODE", "OPERAND", "EXECUTE"]
    x0, cw, pad = 2.5, 2.5, 0.07
    xe = x0 + cw * len(states)

    label(ax, 0.3, 5.85, "One ADD #nn instruction, sitting at addresses n and n + 1", size=12.5,
          weight="bold", ha="left")

    lo, hi = 4.75, 5.15
    pts = [(x0 - 0.35, lo)]
    for i in range(len(states)):
        xa = x0 + i * cw
        pts += [(xa, lo), (xa, hi), (xa + cw / 2, hi), (xa + cw / 2, lo)]
    pts += [(xe, lo), (xe, hi), (xe + 0.3, hi)]
    ax.plot(*zip(*pts), color=WIRE, lw=2)
    label(ax, 0.3, 4.95, "clk", family=MONO, size=11, weight="bold", ha="left")
    for k in range(len(states) + 1):
        xk = x0 + k * cw
        ax.plot([xk, xk], [1.0, lo], color=FAINT, lw=1.1, ls=(0, (3, 3)), zorder=0)

    rows = [
        ("state", 3.85, 0.6, None),
        ("address bus", 3.1, 0.55, ["PC = n", "not used", "PC = n + 1", "not used"]),
        ("memory outputs", 2.35, 0.55, ["02  (ADD)", "\u2014", "nn", "\u2014"]),
        ("stored at the\nrising edge", 1.05, 1.1,
         ["IR \u2190 02\nPC \u2190 n + 1", "nothing\n(decoder: needs operand)",
          "operand \u2190 nn\nPC \u2190 n + 2", "A \u2190 A + nn\nZ \u2190 (result == 0)"]),
    ]
    for name, y, h, cells in rows:
        label(ax, 0.3, y + h / 2, name, size=10.5, ha="left")
        for i in range(len(states)):
            xa = x0 + i * cw + pad
            if cells is None:
                box(ax, xa, y, cw - 2 * pad, h, CTRL)
                label(ax, xa + cw / 2 - pad, y + h / 2, states[i], size=12, weight="bold")
                continue
            text = cells[i]
            quiet = text in ("not used", "\u2014") or text.startswith("nothing")
            if name == "memory outputs":
                colors = MEM
            elif name.startswith("stored"):
                colors = SOFT if quiet else REG
            else:
                colors = SOFT
            box(ax, xa, y, cw - 2 * pad, h, colors, lw=1.3)
            label(ax, xa + cw / 2 - pad, y + h / 2, text, size=9.5 if quiet else 10,
                  family=SANS if quiet else MONO, color=MUTED if quiet else INK)

    label(ax, 0.3, 0.45,
          "The bottom row happens at the rising edge that ends each column.\n"
          "After EXECUTE the FSM goes back to FETCH, and PC already points at the next "
          "instruction (n + 2).",
          size=10, color=MUTED, ha="left")
    save(fig, "09_one_instruction.png")


def add_program():
    """The three bytes used by walkthrough.md."""
    fig, ax = canvas(10.6, 4.15)
    label(ax, 0.35, 3.85, "The whole program is three bytes", size=14, weight="bold", ha="left")
    rows = [
        ("0", "02", "opcode", "ADD", "Do an add. This names the operation."),
        ("1", "04", "operand", "4", "The number to add. Not an operation."),
        ("2", "0A", "opcode", "HLT", "Halt: stop. This byte stands alone."),
    ]
    y0, rh = 2.85, 0.78
    for i, (addr, byte, kind, name, plain) in enumerate(rows):
        y = y0 - i * rh
        colors = HOT if i == 0 else (REG if i == 1 else CTRL)
        label(ax, 0.85, y, addr, family=MONO, size=13, color=MUTED)
        box(ax, 1.35, y - 0.28, 1.15, 0.56, colors, lw=1.8, r=0.06)
        label(ax, 1.92, y, byte, family=MONO, size=16, weight="bold")
        label(ax, 2.75, y, kind, size=11, color=MUTED, ha="left")
        label(ax, 4.15, y, name, family=MONO, size=14, weight="bold", ha="left")
        label(ax, 5.55, y, plain, size=11, ha="left")
    label(ax, 0.85, 3.35, "address", size=9.5, color=MUTED)
    label(ax, 1.92, 3.35, "byte", size=9.5, color=MUTED)
    curve(ax, (0.28, 2.85), (1.28, 2.85), 0, color=CTRL[1], lw=1.6)
    label(ax, 0.35, 3.12, "PC", size=11, weight="bold", color=CTRL[1], ha="left")
    label(ax, 0.35, 0.28, "PC is 0, so the next byte to read is the 02.", size=11, color=MUTED, ha="left")
    save(fig, "10_add_program.png")


def add_snapshots():
    """Register values at four moments of the walkthrough's ADD."""
    fig, ax = canvas(11.4, 6.35)
    label(ax, 0.3, 6.05, "Same add, four moments", size=14, weight="bold", ha="left")
    cols = [
        ("Before any rise",
         [("FETCH", CTRL), ("0", REG), ("00", SOFT), ("00", SOFT), ("0", SOFT)],
         "Memory is already\nshowing 02. IR has\nnot copied it."),
        ("After rise 1\nFETCH",
         [("DECODE", CTRL), ("1", HOT), ("02", HOT), ("00", SOFT), ("0", SOFT)],
         "IR holds the opcode.\nDecoder already says\n\"needs a second byte.\""),
        ("After rise 3\nOPERAND",
         [("EXECUTE", CTRL), ("2", REG), ("02", REG), ("04", HOT), ("0", SOFT)],
         "ALU result wire is\nalready 4. A has not\ncopied it yet."),
        ("After rise 4\nEXECUTE",
         [("FETCH", CTRL), ("2", REG), ("02", REG), ("04", REG), ("4", HOT)],
         "A copied the 4 on\nthe rise. Next byte\nto read is 0A, halt."),
    ]
    names = ["state", "PC", "IR", "operand", "A"]
    x0, cw = 0.35, 2.75
    for i, (title, cells, note) in enumerate(cols):
        x = x0 + i * cw
        label(ax, x + 1.15, 5.35, title, size=11, weight="bold")
        for j, ((text, colors), name) in enumerate(zip(cells, names)):
            y = 4.35 - j * 0.72
            label(ax, x, y, name, size=9, color=MUTED, ha="left")
            box(ax, x + 0.95, y - 0.24, 1.35, 0.48, colors, lw=1.5, r=0.05)
            label(ax, x + 1.62, y, text, family=MONO, size=12, weight="bold")
        label(ax, x + 1.15, 0.7, note, size=9, color=MUTED)
    save(fig, "11_add_snapshots.png")


if __name__ == "__main__":
    layers()
    computer()
    encoding()
    cycle()
    comb_vs_seq()
    clock()
    datapath()
    fsm()
    timeline()
    add_program()
    add_snapshots()
