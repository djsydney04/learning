"""Render the guide's original explanatory diagrams as local PNGs.

Needs matplotlib (only for regeneration, not for reading or running labs).
From repository root, the existing transformer environment can run:
    MPLCONFIGDIR=/tmp/cuda-matplotlib transformer/.venv/bin/python cuda/scripts/render_diagrams.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT = Path(__file__).resolve().parents[1] / "assets"
INK, MUTED = "#202d3a", "#586777"
BLUE, PALE_BLUE = "#2465ac", "#e8f1fb"
GREEN, PALE_GREEN = "#217254", "#e8f4ee"
ORANGE, PALE_ORANGE = "#a45a1c", "#fff0df"
GRAY, PALE_GRAY = "#9ba6af", "#f0f2f4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK})


def canvas(title, subtitle, height=6):
    fig, ax = plt.subplots(figsize=(12, height))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
    ax.set(xlim=(0, 12), ylim=(0, height))
    ax.axis("off")
    label(ax, 0.25, height - 0.4, title, 19, weight="bold", ha="left")
    label(ax, 0.25, height - 0.83, subtitle, 10.5, color=MUTED, ha="left")
    return fig, ax


def label(ax, x, y, value, size=11, color=INK, ha="center", weight="normal"):
    ax.text(x, y, value, fontsize=size, color=color, ha=ha, va="center",
            weight=weight, linespacing=1.4)


def box(ax, x, y, w, h, title="", edge=BLUE, fill=PALE_BLUE, size=12):
    ax.add_patch(Rectangle((x, y), w, h, linewidth=1.4, edgecolor=edge, facecolor=fill))
    if title:
        label(ax, x + w / 2, y + h / 2, title, size)


def arrow(ax, start, end, color=MUTED):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                                linewidth=1.4, color=color, shrinkA=2, shrinkB=2))


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=150, facecolor="white")
    plt.close(fig)
    print(name)


def host_device():
    fig, ax = canvas("One program, two places to execute", "Explicit allocations make ownership and data movement visible.")
    box(ax, .3, 1.25, 4, 3.3, edge=BLUE, fill="#fafcff")
    box(ax, 7.7, 1.25, 4, 3.3, edge=GREEN, fill="#fafffc")
    label(ax, 2.3, 4.18, "HOST · CPU", 14, BLUE, weight="bold")
    label(ax, 9.7, 4.18, "DEVICE · GPU", 14, GREEN, weight="bold")
    box(ax, .65, 2.85, 3.3, .8, "main() prepares and launches")
    box(ax, .65, 1.65, 3.3, .8, "Host array / result")
    box(ax, 8.05, 2.85, 3.3, .8, "Kernel threads execute", GREEN, PALE_GREEN)
    box(ax, 8.05, 1.65, 3.3, .8, "Device allocation", GREEN, PALE_GREEN)
    arrow(ax, (4.3, 3.3), (7.7, 3.3))
    label(ax, 6, 3.6, "launch kernel", 11)
    arrow(ax, (4.3, 2.4), (7.7, 2.4))
    label(ax, 6, 2.7, "copy inputs to device", 10)
    arrow(ax, (7.7, 1.65), (4.3, 1.65))
    label(ax, 6, 1.98, "copy results to host", 10)
    arrow(ax, (9.25, 2.45), (9.25, 2.85), GREEN)
    arrow(ax, (10.1, 2.85), (10.1, 2.45), GREEN)
    label(ax, 6, .62, "A pointer carries an address. A transfer moves the stored values.", 12)
    save(fig, "01-host-device.png")


def indexing():
    fig, ax = canvas("Every output has an owner", "n = 9 elements · 3 blocks · 4 threads per block")
    for block in range(3):
        y = 3.85 - 1.15 * block
        label(ax, 1.1, y + .35, f"block {block}", 13, weight="bold")
        for thread in range(4):
            i = block * 4 + thread
            valid = i < 9
            x = 2.3 + thread * 2.2
            box(ax, x, y, 1.95, .8, f"thread {thread}\ni = {i}",
                BLUE if valid else GRAY, PALE_BLUE if valid else PALE_GRAY, 11)
    label(ax, 6, .75, "i = blockIdx.x × blockDim.x + threadIdx.x", 14, BLUE)
    label(ax, 6, .3, "Indices 9, 10, 11 exist as threads, but skip the guarded array access.", 10.5, MUTED)
    save(fig, "02-indexing.png")


def execution():
    fig, ax = canvas("Logical work uses finite hardware", "Illustrative residency snapshot; block assignment is not fixed or ordered.", 6.8)
    for sm in range(2):
        x = .35 + sm * 6
        box(ax, x, 1.75, 5.3, 3.7, edge=GREEN, fill="#fafffc")
        label(ax, x + 2.65, 5.1, f"Streaming multiprocessor {sm}", 13, GREEN, weight="bold")
        box(ax, x + .3, 3.25, 4.7, 1.4, edge=BLUE, fill=PALE_BLUE)
        label(ax, x + 2.65, 4.33, f"Resident block (example: block {sm * 3})", 11, BLUE)
        for warp in range(2):
            box(ax, x + .55 + warp * 2.2, 3.48, 2, .5, f"warp {warp}: 32 lanes", BLUE, "white", 10)
        label(ax, x + 2.65, 2.87, "Each thread has its own register state", 10.5)
        box(ax, x + .5, 2, 4.3, .58, "Block shared memory", ORANGE, PALE_ORANGE, 11)
        arrow(ax, (x + 2.65, 1.7), (x + 2.65, 1.2))
    box(ax, .35, .5, 11.3, .7, "Device global memory · allocations shared through valid pointers", GRAY, PALE_GRAY)
    label(ax, 6, .15, "More blocks can wait for resources. Caches and execution units are omitted for clarity.", 9.5, MUTED)
    save(fig, "03-execution-memory.png")


def coalescing():
    fig, ax = canvas("Same requested bytes, different address patterns", "32 lanes × one 4-byte float · base aligned to 32 bytes · address model, not measured traffic")
    label(ax, .3, 4.5, "Consecutive elements: lane l reads x[l]", 13, BLUE, ha="left", weight="bold")
    x0, cw = .4, .35
    for sector in range(4):
        x = x0 + sector * 8 * cw
        box(ax, x, 3.35, 8 * cw - .08, .85, edge=BLUE, fill=PALE_BLUE)
        label(ax, x + 4 * cw - .04, 3.02, f"sector {sector}", 10, BLUE)
        for word in range(8):
            label(ax, x + (word + .5) * cw, 3.77, str(sector * 8 + word), 8.5)
    label(ax, 6, 2.55, "128 requested bytes touch 4 aligned 32-byte sectors", 12, BLUE)
    label(ax, .3, 1.97, "Stride-eight elements: lane l reads x[8*l]", 13, ORANGE, ha="left", weight="bold")
    for sector in range(32):
        x = x0 + sector * cw
        box(ax, x, 1, cw - .035, .55, edge=ORANGE, fill=PALE_ORANGE)
        label(ax, x + (cw - .035) / 2, 1.28, str(sector), 7.5)
    label(ax, 6, .62, "128 requested bytes touch 32 sectors; only one float is requested per sector", 11, ORANGE)
    label(ax, 6, .2, "Labels in the top row are element indices; labels in the bottom row are sector numbers.", 9.5, MUTED)
    save(fig, "04-coalescing.png")


def reduction():
    fig, ax = canvas("An eight-thread reduction, phase by phase", "Active entries are shown in blue. Every block thread reaches each barrier.", 6.5)
    rows = [([1, 2, 3, 4, 5, 6, 7, 8], "load", 8),
            ([6, 8, 10, 12], "stride 4", 4),
            ([16, 20], "stride 2", 2), ([36], "stride 1", 1)]
    for step, (values, title, active) in enumerate(rows):
        y = 4.65 - 1.12 * step
        label(ax, 1, y + .32, title, 12, weight="bold")
        for lane in range(8):
            x = 2.2 + lane * 1.13
            box(ax, x, y, .92, .65, str(values[lane]) if lane < active else "—",
                BLUE if lane < active else GRAY, PALE_BLUE if lane < active else PALE_GRAY)
        if step < 3:
            label(ax, 6.25, y - .23, "barrier → combine lower half with upper half", 9.5, MUTED)
    label(ax, 6, .57, "First stage: 1+5, 2+6, 3+7, 4+8. Last stage: 16+20 = 36.", 11)
    label(ax, 6, .2, "Seven additions; three dependency stages. No global cross-block barrier is implied.", 10, MUTED)
    save(fig, "05-reduction.png")


def matrix(ax, x, y, rows, cols, highlight, name, edge, fill):
    cell = .48
    for row in range(rows):
        for col in range(cols):
            active = highlight(row, col)
            box(ax, x + col * cell, y + (rows - row - 1) * cell, cell, cell,
                edge=edge if active else GRAY, fill=fill if active else "white")
    label(ax, x + cols * cell / 2, y - .35, name, 12, weight="bold")


def matmul():
    fig, ax = canvas("Reuse input tiles across an output tile", "Schematic tile size T = 2; the runnable kernel uses T = 16.", 6.2)
    matrix(ax, .7, 2.9, 4, 6, lambda r, c: r < 2 and 2 <= c < 4,
           "A [M, K]", BLUE, PALE_BLUE)
    matrix(ax, 4.9, 2.42, 6, 4, lambda r, c: 2 <= r < 4 and c < 2,
           "B [K, N]", GREEN, PALE_GREEN)
    matrix(ax, 8.55, 2.9, 4, 4, lambda r, c: r < 2 and c < 2,
           "C [M, N]", ORANGE, PALE_ORANGE)
    label(ax, 4.15, 3.9, "×", 23)
    label(ax, 7.75, 3.9, "→", 23)
    label(ax, 6, 1.65, "Move the highlighted K range across A and down B; accumulate into the same C tile.", 11)
    steps = ["Load A and B", "Block barrier", "Reuse for dot products", "Block barrier"]
    for i, step in enumerate(steps):
        x = .35 + i * 2.95
        box(ax, x, .65, 2.65, .6, step, GRAY, PALE_GRAY, 10)
        if i < 3:
            arrow(ax, (x + 2.65, .95), (x + 2.93, .95))
    label(ax, 6, .22, "Zero-fill incomplete input tiles. Guard the output store after all tile stages.", 10.5, MUTED)
    save(fig, "06-matmul.png")


if __name__ == "__main__":
    host_device()
    indexing()
    execution()
    coalescing()
    reduction()
    matmul()
