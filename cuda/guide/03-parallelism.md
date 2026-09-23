# 3. Why do work in parallel?

[← C++](02-cpp.md) · [Next: first kernel →](04-first-kernel.md)

**Build today:** decide which parts of a calculation can happen independently. A GPU is useful when the problem supplies enough suitable work.

## Start with dependencies

In vector addition, `c[i] = a[i] + b[i]`, computing `c[3]` does not require `c[2]`. With separate output storage, each iteration reads its own inputs and writes its own output. All iterations could execute in any order and produce the same result.

Compare a recurrence:

```cpp
for (int i = 1; i < n; ++i) x[i] = x[i - 1] + 1;
```

Here iteration `i` requires the updated value from iteration `i-1`. Assigning one iteration to each thread without changing the algorithm creates a dependency problem. Sometimes mathematics gives a parallel alternative; merely launching more threads does not remove the dependency.

A sum also needs a different decomposition. The sequential loop updates one running total. A parallel reduction first forms independent partial sums and then combines them. We build that in [lesson 9](09-reduction.md).

## Latency and throughput

**Latency** is the time for one operation or request to complete. **Throughput** is the amount of work completed per unit time. A delivery taking 20 minutes has 20-minute latency. Ten independent deliveries finishing in those 20 minutes give higher total throughput than one, without making each journey instantaneous.

CPUs invest heavily in completing complex instruction streams efficiently, with caches, branch prediction, and other mechanisms. GPUs devote substantial resources to executing many threads and switching among ready work. Both have parallel execution capabilities; neither description means a CPU executes only one operation at a time or a GPU is universally faster.

CUDA exposes a way to describe many invocations of a **kernel**, a function executed on the GPU. Each invocation is a **thread** with its own identity and local state. You describe which data each thread owns.

## The cost of moving the problem

For a basic offload from separate host and device allocations:

```text
total time ≈ host preparation
           + host-to-device transfers
           + launch overhead
           + GPU execution
           + device-to-host transfer
           + host consumption
```

Suppose, purely as an invented arithmetic exercise, a CPU takes 10 microseconds, while transfers and launch take 25 microseconds and the GPU kernel takes 1 microsecond. The offload takes at least 26 microseconds before other costs. The 1-microsecond kernel does not make that application faster.

Keeping arrays on the GPU across many operations can amortize transfer costs. Combining compatible operations can avoid intermediate writes and launches. Whether either helps depends on the actual workload and hardware; we measure later.

## More workers do not remove serial work

If 80% of a program's original time can be accelerated and the other 20% is unchanged, making that 80% infinitely fast still leaves 20%:

```text
maximum speedup = 1 / 0.20 = 5
```

With parallel part speedup `s` and original parallel fraction `p`, ideal total speedup is `1 / ((1-p) + p/s)`, before added overhead. This is Amdahl's law. For `p=0.8`, `s=10`, speedup is about `3.57`, not ten. The fractions describe the original measured runtime, not lines of source code.

## Decompose a problem before coding

| Calculation | Natural output owner | What needs coordination? |
| --- | --- | --- |
| Vector addition | One thread per element | No cooperation for separate arrays. |
| Matrix multiplication | One thread per output entry initially | Shared tiles can reuse inputs later. |
| Sum | One group per partial sum | Combining partial results. |
| Row softmax | One block per row initially | Row maximum and denominator. |

For each problem, ask what a thread reads, what it writes, and whether another thread can access the same location at the same time. Ownership is the beginning of a correctness argument.

**Exercise:** compare `c[i] = a[i] + b[i]`, `a[i] = a[i] + 1`, and `a[i] = a[i-1]`. The first two can assign independent indices under the stated separate-element accesses. The last introduces cross-thread read/write dependencies.

**Checkpoint:** explain why a million independent additions can be a better GPU workload than five, and why the GPU still might lose if the arrays must be transferred for every tiny operation.
