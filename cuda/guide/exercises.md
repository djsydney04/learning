# Your implementation workbench

[Guide](../README.md) · [Hints](hints.md) · [Reference implementation](../reference/kernels.cuh)

Edit [exercises/kernels.cuh](../exercises/kernels.cuh). The host setup and comparison code are supplied in [labs/gpu](../labs/gpu). Each kernel is intentionally empty. All arrays passed to these exercises are distinct contiguous float32 allocations. Sizes are positive, small enough for the integer indexing shown, and selected by the host checks.

| Exercise | Read first | Contract and success condition | Command on an NVIDIA machine |
| --- | --- | --- | --- |
| E01 · Vector add | [Indexing](05-indexing.md) | Each valid output gets `a[i]+b[i]`; final partial block is safe. | `make student LAB=02_vector_add` |
| E02 · Grid-stride SAXPY | [Indexing](05-indexing.md) | Cover inputs larger than the launched grid; `out[i]=alpha*x[i]+y[i]`. | `make student LAB=03_grid_stride` |
| E03 · Block sum | [Reduction](09-reduction.md) | Power-of-two 1D blocks; one shared float per thread; one output per block. | `make student LAB=04_reduce` |
| E04 · Matrix product | [Matrices](10-matmul.md) | `[M,K] × [K,N] → [M,N]`; use correct row-major strides and bounds. | `make student LAB=05_matmul ARGS=naive` |
| E05 · Tiled product | [Matrices](10-matmul.md) | Exactly 16×16 threads; shared input tiles; all threads reach both tile barriers. | `make student LAB=05_matmul ARGS=tiled` |
| E06 · Row softmax | [Project](13-project.md) | One block per row; finite inputs; power-of-two blocks; one shared float per thread; arbitrary tested positive widths. | `make student LAB=08_softmax` |

Dynamic shared-memory bytes are supplied by the host for E03 and E06. Do not allocate output storage inside the kernels. `make student` recompiles before running; it never silently substitutes reference code. NaN output indicates a missing write or another numerical failure and is deliberately rejected.

## A method for every exercise

1. Solve a tiny example on paper.
2. Write down which thread owns each output and which inputs it reads.
3. State the valid shape and launch configuration.
4. Implement only that exercise and run its checker.
5. Trace the first mismatch before changing tolerances.
6. Run memory and synchronization tools on the student binary as appropriate.

For example, after E03:

```sh
compute-sanitizer --error-exitcode 1 --tool memcheck ./build/student/04_reduce
compute-sanitizer --error-exitcode 1 --tool racecheck ./build/student/04_reduce
compute-sanitizer --error-exitcode 1 --tool synccheck ./build/student/04_reduce
```

You can run `make check-gpu` to examine working reference behavior first. It does not check student code. `make sanitize` also targets reference binaries; use the student paths above for your implementations.

## Written exercises available on any computer

| Problem | What your answer must show |
| --- | --- |
| Trace 1003 elements with 256-thread blocks. | Grid size, final valid thread, first invalid thread. |
| Trace identity 5 with a stride of 8 over 22 elements. | Indices 5, 13, 21, and the failed next condition. |
| Map a `[3,5]` matrix into memory. | Fifteen offsets and both coordinate-to-offset directions. |
| Reduce seven inputs using eight threads. | The zero-padding input and all three stages. |
| Multiply `[2,3] × [3,4]`. | Eight output owners and their three product terms. |
| Process `[1000,1001,1002]` with softmax. | Maximum, shifted inputs, exponentials, denominator, output. |
| Diagnose `if (i<n) { shared[t]=x[i]; __syncthreads(); }`. | Which threads take the branch in a partial block and a uniform-participation rewrite. |

## Second pass: remove the scaffolding

After E01–E06 pass, write a new host executable for your chosen kernel. Query the device, initialize inputs, allocate/copy, launch, check completion, compare output, and free memory. Then add explicit validation of user-supplied shapes and a documented policy for empty inputs. The provided beginner binaries have fixed inputs and are not general tensor APIs.

Extensions worth attempting after the baseline: keep a reduction entirely on the GPU using repeated passes; build a transpose and explain bank conflicts; add a numerically defined masked-softmax contract; implement a histogram and compare atomics with block partials. Each extension needs its own tests and performance evidence before claiming it works.
