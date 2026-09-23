"""Render the GPU foundations using the CUDA guide's shared drawing helpers.

From repository root, with the existing Matplotlib environment:
MPLCONFIGDIR=/tmp/cuda-matplotlib transformer/.venv/bin/python cuda/foundations/scripts/render_figures.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "scripts"))
from render_diagrams import (  # noqa: E402
    canvas, label, box, arrow, plt, BLUE, PALE_BLUE, GREEN, PALE_GREEN,
    ORANGE, PALE_ORANGE, GRAY, PALE_GRAY, MUTED,
)


def save(fig, name):
    out = ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / name, dpi=150, facecolor="white")
    plt.close(fig)
    print(name)


def computer():
    fig, ax = canvas("Instructions, processors, and stored values", "A program supplies instructions. Processors execute them. Memory holds working values.")
    box(ax, .3, 2.1, 2.5, 1.2, "Storage\nSaved file", GRAY, PALE_GRAY)
    box(ax, 4.05, 1.6, 3.2, 2.2, "Working memory\nInput and result values", ORANGE, PALE_ORANGE)
    box(ax, 8.65, 3.5, 3, 1, "CPU\nRuns host program", BLUE, PALE_BLUE)
    box(ax, 8.65, 1.3, 3, 1, "GPU\nRuns requested GPU work", GREEN, PALE_GREEN, 11)
    arrow(ax, (2.8, 2.7), (4.05, 2.7))
    label(ax, 3.4, 3.08, "load file", 9)
    arrow(ax, (7.25, 3.5), (8.65, 4))
    arrow(ax, (8.65, 3.55), (7.25, 3.1))
    arrow(ax, (7.25, 2.25), (8.65, 1.85))
    arrow(ax, (8.65, 1.45), (7.25, 1.85))
    arrow(ax, (10.15, 3.5), (10.15, 2.3))
    label(ax, 10.4, 2.9, "request", 9.5, ha="left")
    label(ax, 6, .7, "CPU and GPU are hardware. Your program is software.", 13)
    label(ax, 6, .25, "Connections are conceptual; separate and unified memory arrangements are explained later.", 10, MUTED)
    save(fig, "01-computer.png")


def parallel_work():
    fig, ax = canvas("Eight independent jobs", "An imagined worker completes one job per slot. These are assumptions, not benchmark results.", 6.4)
    label(ax, .3, 4.78, "One worker: eight time slots", 13, BLUE, ha="left", weight="bold")
    for i in range(8):
        box(ax, .4 + i * 1.4, 3.8, 1.2, .65, f"job {i+1}")
        label(ax, 1 + i * 1.4, 3.56, f"slot {i+1}", 9, MUTED)
    label(ax, .3, 2.9, "Four workers: two time slots", 13, GREEN, ha="left", weight="bold")
    for worker in range(4):
        x = 2 + worker * 2.4
        label(ax, x + .9, 2.4, f"worker {worker+1}", 10, GREEN)
        for slot in range(2):
            box(ax, x, 1.45 - slot * .8, 1.8, .6, f"job {slot*4+worker+1}", GREEN, PALE_GREEN)
    label(ax, .8, 1.75, "slot 1", 10)
    label(ax, .8, .95, "slot 2", 10)
    label(ax, 6, .23, "Real CPUs also execute parallel work. This is not a CPU-versus-GPU core-count diagram.", 10, MUTED)
    save(fig, "02-parallel-work.png")


def software():
    fig, ax = canvas("The same calculation can have different implementations", "Example request: add [1, 2, 3] to [10, 20, 30]. Hardware and software are different layers.", 6.2)
    rows = [(.3, "CPU implementation", "CPU", BLUE, PALE_BLUE),
            (4.25, "CUDA kernel", "Compatible NVIDIA GPU", GREEN, PALE_GREEN),
            (8.2, "Metal compute implementation", "Apple GPU", ORANGE, PALE_ORANGE)]
    for x, code, hardware, edge, fill in rows:
        box(ax, x, 3.1, 3.5, 1, code, edge, fill, 11)
        arrow(ax, (x + 1.75, 3.1), (x + 1.75, 2.35), edge)
        box(ax, x, 1.4, 3.5, .95, hardware, edge, fill, 11)
    label(ax, .35, 4.45, "SOFTWARE: code and programming system", 10, MUTED, ha="left")
    label(ax, .35, 1.06, "HARDWARE: the processor executing the arithmetic", 10, MUTED, ha="left")
    label(ax, 6, .62, "This guide teaches the CUDA path. The CPU runs its host program and launches the GPU kernel.", 10.5)
    label(ax, 6, .2, "Missing NVIDIA hardware does not automatically redirect a CUDA kernel to the CPU.", 10.5, GREEN)
    save(fig, "03-software-paths.png")


def memory():
    fig, ax = canvas("Two ways CPU and GPU can access working data", "A shared physical memory pool does not make CPU and GPU the same processor.", 6.4)
    label(ax, 3, 4.97, "Separate memory pools", 13, BLUE, weight="bold")
    label(ax, 9.1, 4.97, "Unified physical memory", 13, GREEN, weight="bold")
    box(ax, .35, 3.4, 2.25, .85, "CPU")
    box(ax, 3.3, 3.4, 2.25, .85, "GPU", GREEN, PALE_GREEN)
    box(ax, .35, 1.65, 2.25, 1, "System RAM", ORANGE, PALE_ORANGE)
    box(ax, 3.3, 1.65, 2.25, 1, "GPU memory", ORANGE, PALE_ORANGE)
    arrow(ax, (1.48, 3.4), (1.48, 2.65))
    arrow(ax, (4.43, 3.4), (4.43, 2.65))
    arrow(ax, (2.6, 2.3), (3.3, 2.3))
    arrow(ax, (3.3, 1.98), (2.6, 1.98))
    label(ax, 2.95, 1.1, "Software arranges needed transfers", 10.5, BLUE)
    box(ax, 6.65, 3.4, 2.25, .85, "CPU")
    box(ax, 9.6, 3.4, 2.05, .85, "GPU", GREEN, PALE_GREEN)
    box(ax, 6.65, 1.65, 5, 1, "Memory accessible to CPU and GPU", ORANGE, PALE_ORANGE, 11)
    arrow(ax, (7.78, 3.4), (7.78, 2.65))
    arrow(ax, (10.63, 3.4), (10.63, 2.65))
    label(ax, 9.15, 1.1, "Apple Silicon uses a unified architecture", 10.5, GREEN)
    label(ax, 6, .43, "Both arrangements still require valid access and correct ordering: is the result ready to read?", 11)
    save(fig, "04-memory.png")


if __name__ == "__main__":
    computer()
    parallel_work()
    software()
    memory()
