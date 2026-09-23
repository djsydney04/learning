# CUDA, from the very beginning

Start with what a computer does to two numbers. Build up to writing the GPU operations behind array processing and neural networks. No prior C++, parallel programming, or GPU knowledge is assumed. The arithmetic starts with addition; matrices and exponentials are introduced when needed.

**Begin with [setup and your first session](guide/00-start.md), then [bits, instructions, and operands](guide/01-computers.md).** This is a local Markdown course with source code and diagrams. Open a lesson in your editor's Markdown preview beside its lab.

![The CPU prepares data and launches a kernel; the GPU runs many copies of that kernel and returns results.](assets/01-host-device.png)

## Your first command

From the repository root:

```sh
cd cuda
make check-cpu
```

This compiles and runs four ordinary C++ labs on your CPU. It needs a C++17 compiler and Make, but no CUDA installation or Python packages. **You can start on this Apple Silicon Mac. CUDA kernels themselves require a compatible NVIDIA GPU and CUDA environment.** The [setup guide](guide/00-start.md) separates those two paths.

## The route

| Lesson | Start with this question | Build or investigate |
| --- | --- | --- |
| [0 · Start here](guide/00-start.md) | What do I install, and where do commands run? | Your first CPU lab; later, query a CUDA device. |
| [1 · Computers and numbers](guide/01-computers.md) | What are bits, instructions, operands, and memory? | Trace one addition from memory to result. |
| [2 · Enough C++](guide/02-cpp.md) | What do types, loops, arrays, and pointers mean? | A sequential vector-add program. |
| [3 · Why parallel work?](guide/03-parallelism.md) | Which operations can happen independently? | Decompose a loop; estimate when a GPU helps. |
| [4 · Your first kernel](guide/04-first-kernel.md) | How does the CPU ask the GPU to work? | Allocate, launch, synchronize, copy, check, free. |
| [5 · Threads, blocks, grids](guide/05-indexing.md) | Which thread owns each output? | Vector addition and grid-stride SAXPY; E01–E02. |
| [6 · What the GPU executes](guide/06-execution.md) | How do threads relate to warps, SMs, and registers? | Reason about scheduling, divergence, and occupancy. |
| [7 · Where the bytes go](guide/07-memory.md) | Why can moving data cost more than adding it? | Flatten matrices; count addresses; explain coalescing. |
| [8 · Working together safely](guide/08-synchronization.md) | When can one thread read another's result? | Trace races, barriers, atomics, and kernel boundaries. |
| [9 · Add many numbers](guide/09-reduction.md) | How can many inputs become one result? | A block reduction with tail handling; E03. |
| [10 · Matrix multiplication](guide/10-matmul.md) | How does reusing a tile reduce memory traffic? | Naive and tiled multiplication; E04–E05. |
| [11 · Measure and debug](guide/11-performance.md) | Is it correct, and what actually takes time? | Error checks, sanitizers, event timing, profiling. |
| [12 · Streams and overlap](guide/12-streams.md) | Can copies and kernels make progress together? | Two ordered pipelines using pinned host buffers. |
| [13 · Your CUDA project](guide/13-project.md) | Can I build a stable operation used in attention? | Row-wise softmax from scratch; E06; an evidence notebook. |

Use [the exercise map](guide/exercises.md) to find exactly what to implement, [hints](guide/hints.md) after attempting a solution, [the glossary](guide/glossary.md) for vocabulary, and [debugging](guide/debugging.md) when a command fails. [Primary references](guide/references.md) lead into deeper CUDA topics after this foundation.

## Two ways to practice

The **working labs** show a complete calculation. Predict the result, run it, change one thing, and explain the change. CPU labs model arithmetic and index ownership; they are not GPU emulators or performance measurements.

The **implementation workbench** in [exercises/kernels.cuh](exercises/kernels.cuh) has six intentionally empty kernels. Work through them in order. Complete [reference solutions](reference/kernels.cuh) are supplied separately. On an NVIDIA machine:

```sh
make check-gpu                          # Run the complete reference labs.
make student LAB=02_vector_add          # Check your E01 implementation.
make student LAB=05_matmul ARGS=naive    # Check E04 before attempting E05.
make student LAB=08_softmax             # Check the final project.
```

Student outputs start as NaN, a special “not a number” value. An unfinished kernel therefore fails visibly. A successful reference run does not mean your exercises are complete.

## What has been verified

The local CPU checks and documentation checks are recorded in [verification notes](examples/RESULTS.md). This Mac has no `nvcc` compiler or NVIDIA CUDA device, so GPU compilation, execution, sanitizer results, and performance remain unverified here. The GPU labs contain checks against CPU results and edge cases for you to run on compatible hardware; no GPU benchmark numbers are invented.
