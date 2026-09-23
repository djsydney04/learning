# 13. Build stable row-wise softmax

[← Streams](12-streams.md) · [Guide](../README.md) · [Further reading →](references.md)

**Build today:** turn a row of scores into probabilities using the pieces you have learned. This is E06, the final guided implementation. It connects CUDA to the [attention lesson](../../transformer/guide/05-attention.md).

## From scores to probabilities

Suppose three candidate next tokens have scores `[1,2,3]`. A larger score should receive more probability, while probabilities should be nonnegative and sum to one.

The exponential `exp(x)`, also written `e^x`, is positive and increases with x. Here `e` is a mathematical constant approximately 2.71828. **Softmax** exponentiates each score and divides by the row's total:

```text
p[i] = exp(x[i]) / sum_j exp(x[j])
```

For `[1,2,3]`, the result is approximately `[0.09003, 0.24473, 0.66524]`. A one-element row always gives `[1]`. If every score is equal, each of C entries gets `1/C`.

## Remove a common offset before exponentiating

Directly evaluating `exp(1002)` in float32 overflows. But adding a constant to every score should not change the probabilities: the same exponential factor appears in numerator and denominator and cancels.

Choose the row's maximum `m` and calculate:

```text
m = max_j x[j]
s = sum_j exp(x[j] - m)
p[i] = exp(x[i] - m) / s
```

For `[1000,1001,1002]`, the shifted values are `[-2,-1,0]`. Their exponentials are approximately `[0.13534,0.36788,1]`; the sum is 1.50322. Dividing gives the same three probabilities as `[1,2,3]`.

For finite inputs, the largest shifted value is zero and contributes one, so the denominator is positive. Very small contributions may underflow toward zero; that is different from overflowing the largest exponential. The project contract requires finite inputs, positive row/column counts, and contiguous float32 storage. NaN, infinity, and attention masks containing negative infinity are outside this starter contract.

## Map a row to a block

Launch one block per row. A row can have more columns than threads; use `col = threadIdx.x; col < cols; col += blockDim.x`. This distributes columns without requiring one thread per column.

The kernel has five conceptual phases:

1. Each thread finds a maximum over its assigned columns. A thread with none starts at negative infinity.
2. Reduce those local maxima across the block in shared memory.
3. Every thread reads the block maximum, then sums its assigned shifted exponentials.
4. Reduce those local sums across the block.
5. Every thread normalizes and writes its assigned outputs.

The shared-memory tree is the same pattern as [lesson 9](09-reduction.md), first with maximum and then addition. Use power-of-two block sizes and dynamic storage for one float per thread.

## A subtle reuse barrier

After the maximum reduction, every thread needs to read `scratch[0]` into its own `maximum` variable. Before any thread overwrites scratch for the sum phase, all threads must have performed that read:

```cpp
maximum = scratch[0];
__syncthreads();
// It is now safe to reuse scratch for the sum reduction.
```

The barrier at the end of the maximum reduction makes the maximum ready. This additional barrier prevents a fast thread from overwriting it while a slower thread has yet to read it. Distinguish **ready to read** from **finished being read**.

The reference recomputes exponentials during the final write instead of allocating a global intermediate array. That trades arithmetic for avoided storage and movement. Other implementations keep more values in registers or fuse softmax with neighboring operations. Compare those choices after the baseline is correct.

## Implement and validate

Fill `softmax_rows` in [exercises/kernels.cuh](../exercises/kernels.cuh). On an NVIDIA machine:

```sh
make student LAB=08_softmax
compute-sanitizer --error-exitcode 1 --tool memcheck ./build/student/08_softmax
compute-sanitizer --error-exitcode 1 --tool racecheck ./build/student/08_softmax
compute-sanitizer --error-exitcode 1 --tool synccheck ./build/student/08_softmax
```

The checker uses nine row widths, three block sizes, and four row patterns: ordinary values, values shifted by 1000, all-equal negative values, and one dominant score. It compares against a double-precision CPU calculation, checks finite probabilities in `[0,1]`, checks row sums, and checks invariance to the common shift. Width 1003 requires each thread to handle several columns; width 1 stresses mostly-empty thread assignments.

If you only have the Mac, trace the algorithm and run the CPU softmax example in `04_reduction`. That verifies the host mathematics, not your CUDA kernel.

## Make the project your own

After all six exercises pass, create your own `.cu` program that accepts a small matrix, allocates memory, launches softmax, checks output, and releases resources. Initially keep the input fixed so every result is explainable. Rebuilding the host setup proves that you understand more than the kernel body.

Then adapt the event-timing pattern from [06_timing.cu](../labs/gpu/06_timing.cu). Compare multiple row counts and widths and at least two valid block sizes. Validate after every change and record your timing scope. A row-per-block algorithm may have insufficient parallelism for very few rows and long rows; that is a specific limitation to investigate.

Your completion artifact is a short [experiment notebook](experiments.md) containing:

- A memory-and-thread diagram with ownership and barrier phases.
- Commands, environment, and exact correctness/sanitizer outcomes.
- Measurements from real GPU runs, with repeated-run variation.
- One failed hypothesis or optimization and your explanation.

## Beyond the foundation

You now have the pieces for row normalization, simple attention primitives, image filters, histograms, and scans. A scan differs from a reduction because it retains prefix results rather than only one aggregate. A histogram needs coordinated updates to shared bins. Layer normalization needs mean and variance with numerical care.

Production GPU software often starts with tuned libraries: cuBLAS/cuBLASLt for matrix operations, CUB for parallel primitives, and framework operators for tensor work. Further topics include warp collectives, register tiling, Tensor Cores, mixed precision, asynchronous shared-memory copies, CUDA Graphs, and multiple GPUs. These are a continuation path in [the references](references.md), not functionality claimed by this starter project.

<details>
<summary>Optional review</summary>

Explain your kernel from the bits stored in each input float to the ownership of each output probability. Name the data movement, arithmetic, synchronization, and evidence needed to claim it works and is fast for a particular workload.

</details>
