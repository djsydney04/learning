# When a command or kernel fails

[Guide](../README.md) · [Setup](00-start.md) · [Measurement](11-performance.md)

Start with the first actionable error in the output. A long compiler message often ends with consequences of an earlier missing header or syntax error.

| Symptom | What to check |
| --- | --- |
| `No rule to make target` | Run `pwd`; commands assume the `cuda/` folder. Use the exact lab name from the exercise map. |
| `c++` or `make` missing | Install the host development tools for your operating system. The CPU path does not need CUDA. |
| `nvcc not found` | You need a CUDA development toolkit on a supported NVIDIA machine. `make check-cpu` remains available locally. |
| `nvidia-smi` works, `nvcc` does not | Driver visibility and compiler installation are separate. Check the toolkit's documented PATH setup. |
| CUDA syntax rejected by `c++` | Build `.cu` files with the Makefile's GPU targets or `nvcc`, not the host-only compiler command. |
| Unsupported host compiler | Match toolkit and compiler versions using the installation guide; do not begin by bypassing compatibility checks. |
| No CUDA-capable device / insufficient driver | Check GPU visibility, driver/toolkit compatibility, and whether your shell or container actually has GPU access. |
| No kernel image / invalid device function | Check GPU compute capability against compiled targets and toolkit support. Rebuild with appropriate architecture flags. |
| Invalid launch configuration | Check nonzero grid, total and per-axis block limits, dynamic shared-memory bytes, and kernel requirements. |
| Illegal memory access | Check element count versus byte count, pointer location, flat strides, and every tail guard; run memcheck. |
| Output stays NaN | An exercise may still be empty; otherwise a thread missed its store or produced a non-finite result. Trace ownership. |
| Results vary across runs | Investigate missing ordering, conflicting writers, uninitialized reads, and floating-point operation order. |
| Partial blocks fail | Check rounded-up grid size and the bounds check. Cooperative kernels need neutral padding and uniform barrier participation. |
| Hang or synchronization report | Examine barriers under divergent conditions and cross-block spin waits. Use synccheck; reduce the input. |
| Student matrix E04 passes but default command fails | Default tests both naive and tiled. Use `ARGS=naive` until E05 is implemented. |
| New compiler flags seem ignored | Make tracks file timestamps, not flag history. Use `make -B` with the intended target and flags. |
| Kernel timing looks impossibly small | Check asynchronous submission, event placement, repeats, cache reuse, and whether useful outputs were verified. |

## Reduce the failure to one output

For a matrix mismatch at offset `i`, calculate `row = i / N` and `col = i % N`. Find the thread assigned to that row and column. List the K A/B input pairs it should multiply. Then check whether shared tiles represent exactly those pairs.

For a reduction mismatch, inspect the block partial before inspecting the final total. Write down the block's input range, tail zeros, and each halving stage. The reference lab already compares each partial separately for this reason.

For softmax, inspect one row's maximum and denominator. Test one-column and all-equal rows first. Then add the 1000-shift test. A row summing to one is necessary but not sufficient; an incorrectly permuted or uniform output could satisfy that condition and still be wrong.

## Keep diagnostic and performance runs separate

`CUDA_LAUNCH_BLOCKING=1`, device `printf`, debug compilation, and sanitizers can all change timing. Use them to find bugs, then repeat normal validated runs for measurements. Device printing from many threads also has limited buffering and nondeterministic order; it is a poor substitute for copying a small structured output back to the host.

If a kernel corrupts device execution state, restart the executable after fixing it. Record the exact error and command in [your notebook](experiments.md), including whether it came from compilation, launch, synchronization, copying, or numerical validation.
