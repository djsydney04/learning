# 11. Correctness first, then measurement

[← Matrix multiplication](10-matmul.md) · [Next: streams →](12-streams.md)

**Build today:** a reliable way to distinguish a correct result, a memory-safe run, a kernel measurement, and an application improvement. These are different claims.

## A numerical comparison is the first gate

The lab hosts generate CPU expectations, launch the GPU calculation, and compare every output. Boundary sizes, rectangular matrices, large softmax offsets, and NaN-initialized outputs target specific failure modes. They are not a proof for every possible input.

When a test fails, identify the first differing index and compute it by hand. Check the owning thread, flat address, valid range, and every synchronization phase that produces the input. Keep an input small enough to trace. Increasing tolerance before understanding the error can conceal a real bug.

Use launch and completion checks:

```cpp
kernel<<<blocks, threads>>>(/* arguments */);
CUDA_CHECK(cudaGetLastError());
CUDA_CHECK(cudaDeviceSynchronize());
```

A failure reported during a later copy may originate in an earlier asynchronous kernel. `CUDA_LAUNCH_BLOCKING=1` can help localize errors during debugging. It changes scheduling and must not be used for normal performance conclusions.

## Memory and synchronization tools

On supported CUDA hardware with the tools installed:

```sh
make sanitize
```

The target builds and checks reference binaries. It runs `memcheck` on all of them, then `racecheck` and `synccheck` on cooperative kernels. To check a student binary, build it and name its path directly:

```sh
compute-sanitizer --error-exitcode 1 --tool memcheck ./build/student/05_matmul
compute-sanitizer --error-exitcode 1 --tool racecheck ./build/student/05_matmul
compute-sanitizer --error-exitcode 1 --tool synccheck ./build/student/05_matmul
```

`memcheck` targets invalid memory accesses; `racecheck` detects shared-memory access hazards; `synccheck` checks supported synchronization misuse. `initcheck` is useful for uninitialized memory reads under its supported modes. Racecheck is not a general detector for all global-memory races. Passing these tools adds evidence but does not prove an arbitrary algorithm correct. Consult the [Compute Sanitizer manual](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html) for exact supported checks.

## Why a CPU timer around a launch is misleading

```cpp
start_cpu_timer();
kernel<<<blocks, threads>>>(/* ... */);
stop_cpu_timer();
```

Without waiting, this can measure submission overhead while the GPU is still working. CUDA events can mark positions in a stream and measure elapsed device timeline between them:

```cpp
cudaEventRecord(start);
// Launch the repeated kernels in the same stream.
cudaEventRecord(stop);
cudaEventSynchronize(stop);
cudaEventElapsedTime(&milliseconds, start, stop);
```

This snippet omits the checks for readability; [06_timing.cu](../labs/gpu/06_timing.cu) checks every runtime call and validates the result. It warms up, records 100 repeated vector-add launches, and reports the elapsed time divided by 100. The interval can include gaps in the sequence caused by submission; treat it as the measured kernel sequence, not an isolated hardware instruction latency.

The same program separately uses a host clock around upload + launch + synchronization + download. Allocation, initial data generation, context warmup, and final CPU validation are excluded from that scope. State those exclusions when reporting it.

## Bytes, seconds, and bandwidth

Vector addition logically reads two float arrays and writes one. With N elements, that is `12*N` bytes. Effective bandwidth using milliseconds is:

```text
GB/s = logical_bytes / (milliseconds * 1,000,000)
```

For a made-up arithmetic example of 12,000,000 bytes in 0.1 ms, the result is 120 GB/s. This is not a measurement from the repository. Repeated arrays may fit in cache, so the logical byte count is not necessarily actual DRAM traffic. A bandwidth number exceeding a device's external-memory rate can signal cache reuse or a mistaken timing/counting scope, rather than a physical impossibility.

**Arithmetic intensity** is arithmetic operations per byte moved at the memory level under discussion. Vector addition has about one addition per 12 logical bytes. Matrix multiplication can reuse inputs for many operations. A rough roofline bound is `min(compute throughput, memory bandwidth * arithmetic intensity)`, with consistent units and memory level. It is a bottleneck model, not a promised speed.

## Choosing a profiler

| Investigate | Starting tool |
| --- | --- |
| Time spent copying, waiting, or launching. | Nsight Systems timeline. |
| Overlap between stream pipelines. | Nsight Systems timeline. |
| A kernel's memory and execution resource use. | Nsight Compute. |
| Limits on residency from registers or shared memory. | Compiler resource report and kernel metrics. |

Example commands, when those tools are installed and permitted:

```sh
nsys profile --trace=cuda -o build/streams ./build/gpu/07_streams
ncu --set basic ./build/gpu/06_timing
```

Profiling may add overhead, replay kernels, or require performance-counter permissions. Use ordinary runs for final elapsed-time comparisons and profiler runs to explain behavior. Follow [Nsight Systems](https://docs.nvidia.com/nsight-systems/UserGuide/index.html) and [Nsight Compute CLI](https://docs.nvidia.com/nsight-compute/NsightComputeCli/index.html) documentation for the installed versions.

## A useful experiment changes one thing

Record GPU, driver, toolkit, build flags, input size, layout, precision, block/grid sizes, number of repetitions, and timing scope. Run multiple batches and report spread, such as median and minimum/maximum across batches. Avoid calling a noisy one-off difference a speedup.

Try 128 versus 256 threads for vector addition. Recheck output, then time the same input and compare repeated runs. Predict what might change before looking at the result. Keep a hypothesis you can disprove, such as “this workload is too small for launch overhead to be negligible.”

<details>
<summary>Optional review</summary>

Explain how a fast event-timed kernel can coexist with a slower application, why warmup matters, and why a CPU check alone cannot detect every out-of-bounds GPU access.

</details>
