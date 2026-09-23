# GPU foundations: verification

[Foundations](../README.md) · [CUDA guide verification](../../examples/RESULTS.md)

The two foundation experiments were run on the local CPU using Python 3.14. They require no third-party packages:

```sh
python3 cuda/foundations/experiments/01_pixels.py
python3 cuda/foundations/experiments/02_work.py
```

The pixel example produced `[20,80]` and `[140,255]` for an increase of 20. Its checks also verified clamping when darkening and preservation of the original input. The work-assignment model produced eight rounds for one worker and two for four; ownership checks passed for zero, one, and partial-round input sizes.

These are CPU arithmetic models, not parallel GPU execution, CUDA emulation, or performance measurements. The examples print this distinction explicitly.

The local macOS graphics query identified **Apple M3 Pro**, vendor Apple. This verifies the GPU model, not CUDA execution. The CUDA guide's NVIDIA compilation and runtime checks remain unverified on this machine.

The four foundation diagrams can be regenerated from the repository root using the existing Matplotlib environment:

```sh
MPLCONFIGDIR=/tmp/cuda-matplotlib transformer/.venv/bin/python cuda/foundations/scripts/render_figures.py
```

The renderer reuses the CUDA guide's drawing helpers. Reading the PNGs requires no Python packages. Run `python3 cuda/scripts/check_docs.py` from the repository root to check local links and code fences throughout the combined CUDA guide.

All four diagrams were rendered and visually inspected. After integration under `cuda/foundations/`, both experiments passed at their new paths, and the combined documentation check passed for 33 Markdown files, 176 local links, and closed code fences. `git diff --check` also passed.
