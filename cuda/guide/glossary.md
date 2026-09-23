# CUDA vocabulary in plain language

[Guide](../README.md)

| Term | Meaning here |
| --- | --- |
| Address | A value identifying a storage location. |
| Arithmetic intensity | Arithmetic operations per byte moved at a specified memory level. |
| Atomic | An operation whose specified update cannot be split by competing accesses at its documented scope. |
| Barrier | A point coordinating participating threads and the relevant memory ordering. |
| Bit / byte | A two-valued storage unit / eight bits. |
| Block | A group of kernel threads that can cooperate using block shared memory and barriers. |
| Broadcast | Serving the same value to multiple participating consumers. |
| Cache | Hardware-managed storage that retains data near execution units. |
| Coalescing | Combining a warp's compatible nearby memory accesses efficiently. |
| Compiler | Software translating source into executable instructions and related output. |
| Compute capability | NVIDIA's versioned description of a GPU's architectural feature set; distinct from toolkit version. |
| Constant operand | A fixed input value, such as literal `4` in `x + 4`. |
| Constant memory | A CUDA memory space with specific read-only device access and caching behavior; different from a literal or C++ `const`. |
| CUDA | NVIDIA's platform and programming model for GPU computing. |
| Device | The GPU side of this program. |
| Divergence | Threads within a warp following different control-flow paths. |
| Driver | System software connecting applications and the GPU. |
| Event | A CUDA marker for stream ordering, completion, and optionally timing. |
| Float32 | A 32-bit floating-point representation used for the numerical data here. |
| FLOP | One floating-point arithmetic operation under a stated counting convention. |
| Global memory | Device memory accessible through valid pointers across threads and launches. |
| Grid | All blocks in a kernel launch. |
| Grid-stride loop | A loop advancing each thread by the total number of threads in the launched 1D grid. |
| Host | The CPU side of this program. |
| Immediate | A constant operand encoded in a machine instruction. |
| Instruction | An encoded command a processor can execute. |
| Kernel | A function launched for execution across GPU threads. |
| Lane | A thread's numbered position within a warp. |
| Latency | Time from starting a request to completing it. |
| Launch | The host request to run a kernel with a grid, block, and optional stream/shared-memory configuration. |
| Local memory | Storage private to a thread logically, but backed by device memory rather than necessarily registers. |
| NaN | A floating-point “not a number” value; rejected by our output comparisons. |
| Occupancy | Resident warps as a fraction of an SM's maximum resident warps. |
| Operand | An input value used by an operation. |
| Pinned memory | Host memory held in place to support suitable device transfer behavior. |
| Pointer | A typed address value; it does not inherently store an allocation's length or ownership. |
| PTX | NVIDIA's intermediate virtual instruction representation used in CUDA compilation. |
| Race | Conflicting accesses without the required synchronization, producing invalid program behavior. |
| Reduction | Combining many values using an operation such as sum or maximum. |
| Register | Small, fast processor storage used for current execution state. |
| Row-major | Layout where adjacent columns of a row occupy adjacent elements. |
| Shared memory | Explicitly managed on-chip cooperation storage for a block in these labs. |
| SIMT | Single instruction, multiple threads: CUDA's thread-oriented execution model. |
| SM | Streaming multiprocessor: hardware that runs resident blocks and their warps. |
| Softmax | Turning scores into probabilities using exponentiation and row normalization. |
| Spill | Compiler placement of some thread state in local memory when it cannot remain in registers. |
| Stream | An ordered queue of CUDA operations. |
| Stride | A distance between successive elements/accesses; specify whether it is measured in elements or bytes. |
| Synchronization | Establishing required completion and ordering among work or memory accesses. |
| Tensor | An array organized by one or more axes (also including scalar arrays in common framework terminology). |
| Throughput | Work completed per unit time. |
| Tile | A subset of data processed cooperatively to expose reuse or local structure. |
| Toolkit | CUDA compiler, headers, libraries, and development tools. |
| Unified memory | Managed/system memory facilities under CUDA's supported access and coherence rules; not a promise of free transfers. |
| Warp | A group of 32 threads from one block. |
