# 8. Make cooperation correct

[← Memory](07-memory.md) · [Next: reduction →](09-reduction.md)

**Investigate today:** when a thread may safely consume another thread's result. Predict a lost update in [04_reduction.cpp](../labs/cpu/04_reduction.cpp).

## A race begins with conflicting access

Suppose two threads execute `counter = counter + 1`. That source expression can involve reading, adding, and writing. Starting from zero, this interleaving loses an update:

```text
thread A reads 0
thread B reads 0
thread A computes 1 and stores 1
thread B computes 1 and stores 1
final value: 1, although two increments were requested
```

The CPU lab explicitly sequences those actions to demonstrate the arithmetic. It does not launch racy CPU threads. Actual unsynchronized conflicting accesses can have undefined behavior, so a real faulty program is not limited to this one illustrated outcome.

Separate output ownership avoids many races. If each vector-add thread writes one distinct output and reads only input data, no barrier is needed. Cooperation introduces additional requirements.

## A block barrier

`__syncthreads()` is a block-scoped barrier and establishes the corresponding memory visibility for participating threads. A common pattern is:

```cpp
shared[threadIdx.x] = some_value;
__syncthreads();
// Now consume values published by the block's threads.
```

The barrier says that producers must finish this phase before consumers proceed. A second barrier may be needed before the next phase overwrites storage that other threads still read.

In these lessons, keep barriers on a path reached by every block thread, including tail threads. The simplest safe tail policy is “supply an identity value and participate”:

```cpp
scratch[t] = i < n ? input[i] : 0.0f;
__syncthreads();
```

Avoid putting a barrier under `if (i < n)` in a partial block. Threads would not have a uniform participation pattern. Early return can also skip values needed by the algorithm. A bounds-based return is fine in the naive matrix kernel because it has no block barriers and no shared cooperative data.

## What a block barrier does not do

It does not synchronize other blocks. It does not wait for an unrelated CPU task. It does not automatically create a global phase boundary across a grid. Blocks must not assume all other blocks are simultaneously resident or will execute in a particular order.

For a basic multi-phase algorithm, use separate kernels in the same stream:

```text
kernel A writes all partial results
              ↓ same-stream ordering
kernel B consumes those results
```

The host need not synchronize between these two launches just to preserve their same-stream dependency. Specialized cooperative launches and clusters offer additional synchronization mechanisms under specific requirements; they are later topics, not assumptions built into ordinary launches.

## Atomic operations

An atomic update provides an indivisible operation on a particular location at its documented scope. `atomicAdd` can combine updates without the lost-update interleaving shown earlier.

It does not make every surrounding operation atomic, create a grid barrier, or by itself ensure a complete publication protocol for other data. Many threads contending for one address can limit throughput. Floating-point atomic sums may also accumulate in different orders across runs.

A reduction tree gives each block a structured way to combine values with fewer global updates. Atomics are useful tools, not a replacement for understanding ownership and ordering.

## Warp communication needs a contract too

`__syncwarp(mask)` and shuffle operations such as `__shfl_down_sync(mask, value, delta)` serve particular warp-level communication patterns. A mask names participating lanes; it must agree with the actual executing participants and the operation's rules. A full mask is not universally correct inside arbitrary divergent branches.

Our first reductions use whole-block shared memory and barriers so all intermediate values are inspectable. Only replace them with warp operations after proving participation, data dependencies, and the behavior of incomplete warps. `volatile` alone does not supply a synchronization protocol.

## Three different waits

| Operation | Scope in this course |
| --- | --- |
| `__syncthreads()` | Device threads coordinate inside one block. |
| `cudaStreamSynchronize(stream)` | Host waits for previously submitted work in one stream. |
| `cudaDeviceSynchronize()` | Host waits for previously requested device work. |

These are not interchangeable. Putting a host runtime call in place of a device barrier does not fix a kernel's race.

**Exercise:** a block loads a shared tile, synchronizes, reads the tile, and immediately overwrites it for the next loop iteration. Explain why fast threads could overwrite values before slow threads finish reading. Add a barrier between reading and replacement.

**Checkpoint:** distinguish avoiding a race by assigning distinct outputs, coordinating phases with a barrier, and combining conflicting updates atomically. Explain why none implies a free global barrier.

See NVIDIA's [synchronization guidance for kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html) and [CUDA C++ memory model](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cuda-cpp-memory-model.html) for formal rules.
