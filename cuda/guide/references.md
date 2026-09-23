# Primary references and the next layer

[Guide](../README.md)

The lessons, examples, and diagrams are written for this repository. Official references were consulted while preparing this section in September 2026. NVIDIA's current documentation URLs can advance to newer toolkit releases; use the documentation matching your installed toolkit when checking precise compatibility and tool options. No toolkit version is presumed installed on this Mac.

## References for this guide

| Read alongside | Primary source | Purpose |
| --- | --- | --- |
| Setup | [CUDA installation for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) | Supported systems, toolkit installation, and host compiler constraints. |
| Setup | [CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) | Windows driver and WSL-specific setup. |
| Setup | [CUDA compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/) | Separate GPU, driver, and toolkit compatibility questions. |
| macOS boundary | [CUDA 10.2 release notes](https://docs.nvidia.com/cuda/archive/10.2/cuda-toolkit-release-notes/) | Historical end of macOS CUDA development/execution support. |
| Host/device, threads | [CUDA programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html) | The vocabulary and execution hierarchy. |
| First kernel | [Introduction to CUDA C++](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html) | Allocations, copies, launches, runtime interaction. |
| Indexing and cooperation | [Writing SIMT kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html) | Thread coordinates, shared memory, kernel behavior. |
| Memory and timing | [CUDA best practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) | Access patterns, measurement, and optimization reasoning. |
| Synchronization | [CUDA C++ memory model](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/cuda-cpp-memory-model.html) | Formal scopes and memory-ordering rules. |
| Streams | [Asynchronous execution](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html) | Stream ordering, events, and host/device completion. |
| Correctness tools | [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html) | What each checker detects and its limitations. |
| Application profiling | [Nsight Systems user guide](https://docs.nvidia.com/nsight-systems/UserGuide/index.html) | Timelines, copies, launch gaps, and overlap. |
| Kernel profiling | [Nsight Compute CLI](https://docs.nvidia.com/nsight-compute/NsightComputeCli/index.html) | Kernel metrics and profiler invocation. |
| Exponentials and precision | [CUDA Math API](https://docs.nvidia.com/cuda/cuda-math-api/cuda_math_api/group__CUDA__MATH__SINGLE.html) | Device float math operations such as `expf`. |

## Continue after E06

| Next subject | Why it follows | Primary starting point |
| --- | --- | --- |
| Warp collectives | Replace some shared-memory communication once lane participation is proven. | [CUDA programming guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html). |
| Parallel primitives | Compare your reduction with tuned sum, scan, and sorting implementations. | [NVIDIA CCCL / CUB](https://nvidia.github.io/cccl/unstable/cub/index.html) (development documentation; match APIs to your installed release). |
| Library matrix multiplication | Understand layout, precision, and a production baseline before custom optimization. | [cuBLAS documentation](https://docs.nvidia.com/cuda/cublas/). |
| Register tiling and Tensor Cores | Reuse more data per thread and learn hardware-supported matrix operations. | [NVIDIA CUTLASS](https://docs.nvidia.com/cutlass/latest/overview.html). |
| CUDA Graphs | Reduce repeated workflow submission overhead where measurements justify it. | [CUDA programming guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html). |
| Multiple GPUs | Separate per-device ownership from communication and collective operations. | [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/). |
| Full attention | Connect reductions and matrix products to query/key/value computations. | [Local transformer attention lesson](../../transformer/guide/05-attention.md). |

The CUDA section is a foundation in explicit CUDA C++ kernels. It does not claim exhaustive coverage of every GPU architecture or advanced CUDA feature. The next step is to extend one operation, measure it, and explain the result using the model you have built.
