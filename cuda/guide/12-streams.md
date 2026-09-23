# 12. Streams, ordering, and possible overlap

[← Measurement](11-performance.md) · [Next: final project →](13-project.md)

**Build today:** two independent pipelines, each with upload → kernel → download. Open [07_streams.cu](../labs/gpu/07_streams.cu).

## A stream is an ordered queue

Within a CUDA stream, dependent operations occur in submission order. An upload followed by a kernel in that stream makes the uploaded input available to the kernel; a following download observes its completed output.

Two streams can make progress independently when dependencies, hardware resources, and the runtime allow it. They do not promise simultaneous execution or a particular speedup.

```text
stream 0: upload first half  -> kernel first half  -> download first half
stream 1: upload second half -> kernel second half -> download second half

host:     submit work ........ wait for both ........ inspect results
```

Those are logical dependencies. Only a recorded timeline can show which intervals actually overlap on a particular machine.

## Split the data without sharing output locations

The lab uses 100,003 elements, split into two uneven chunks. Each pipeline receives pointers advanced to its own offset and a chunk-local element count. The kernel computes indices relative to those pointers.

```cpp
saxpy<<<blocks, 256, 0, stream>>>(dx + offset, dy + offset,
                                 dout + offset, 2.0f, count);
```

The fourth launch parameter chooses a stream; the third is dynamic shared-memory bytes, zero here. Offsetting both the pointer and the kernel's logical index again would double-count the offset. Keeping chunk-local lengths prevents accessing the wrong half.

Each stream orders its own two uploads, SAXPY kernel, and download. No stream reads the other's output, and the two output regions are disjoint.

## Pinned host memory and lifetime

Ordinary CPU allocations can reside in pageable memory. The operating system may move their backing pages. **Pinned** host memory reserves pages for stable transfer access. CUDA's `cudaMallocHost` allocates pinned host buffers; `cudaFreeHost` releases them.

Pinned host memory is used here to support asynchronous transfers suitable for overlap. It is a limited system resource, so keep buffers reasonably sized and reuse them when useful. An `Async` API name alone does not guarantee every call returns immediately for every memory type and situation.

After queuing a copy, the host must not overwrite, read prematurely, or free the participating buffer while the transfer still uses it. The lab waits for both streams with `cudaStreamSynchronize` before validating output and freeing pinned buffers. Device buffers also remain alive through completion.

## Dependencies across streams

If stream B needs a result from stream A, “I submitted A first on the CPU” is insufficient. Record an event in A after the producing work, then make B wait for that event before consuming the result:

```cpp
cudaEventRecord(ready, stream_a);
cudaStreamWaitEvent(stream_b, ready, 0);
// Enqueue consumer in stream_b after the wait.
```

Create and destroy the event with checked runtime calls in a complete program. This establishes a device-side dependency without making the CPU wait for all GPU work.

Default-stream behavior has legacy and per-thread modes. The example explicitly creates nonblocking streams and does not rely on implicit default-stream synchronization. Its initialization finishes before those pipelines begin.

## Run and inspect

```sh
make build/gpu/07_streams
./build/gpu/07_streams
nsys profile --trace=cuda -o build/streams ./build/gpu/07_streams
```

The checker verifies the values after both streams complete. The profiler is how you investigate overlap. Small chunks, copy-engine limits, link bandwidth, or resource saturation can erase any gain. This lab makes no speedup claim.

<details>
<summary>Optional review</summary>

Draw the required order for one chunk, explain why host buffer lifetime matters, and add the dependency needed if a second kernel in another stream consumes the first kernel's output.

</details>

Reference: NVIDIA's [asynchronous execution guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html).
