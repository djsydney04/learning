# Your CUDA experiment notebook

[Guide](../README.md) · [Measurement guide](11-performance.md)

Copy the entry below for each experiment. Leave GPU measurements blank until you actually run them. Label CPU arithmetic models separately from device execution.

## Experiment: __________________

Date:

Lesson and code file:

Question and prediction:

Hardware and software: operating system, CPU/GPU name, GPU compute capability, driver, toolkit, host compiler.

Build/run commands and flags:

Input: shape, layout, dtype, value pattern, allocation sizes.

Launch: block dimensions, grid dimensions, shared bytes, stream.

Ownership and synchronization: which thread writes which result; where data is published, consumed, and reused.

Correctness evidence: reference comparison, tested boundaries, error checks, sanitizer outcomes. Record failures as well as passes.

Timing scope: what starts and stops the clock; whether allocation, transfers, warmup, launch gaps, and validation are included.

| Variant | Repetitions / batches | Median time | Observed range | Correctness result |
| --- | --- | --- | --- | --- |
| Baseline | | | | |
| One change | | | | |

Observation:

Explanation, including what the evidence cannot establish:

Next experiment:

## Suggested experiments

1. Change the vector-add block size while preserving coverage.
2. Compare kernel-sequence timing with upload + kernel + download.
3. Trace aligned and shifted access addresses on the CPU, then use a profiler to investigate actual GPU traffic.
4. Compare naive and tiled matrix multiplication at matched square and rectangular sizes.
5. Compare softmax block sizes for short and long rows.
6. Inspect the stream timeline and identify any actual overlap; do not infer it from the presence of two streams.
