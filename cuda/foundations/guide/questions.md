# Further notes

[Guide](../README.md) · [CUDA and software](05-cuda-and-software.md)

Short clarifications to revisit as needed. Expand a topic for the explanation.

<details>
<summary>CUDA as software</summary>

CUDA is NVIDIA's software platform and programming model. A compatible NVIDIA GPU is the hardware that executes its device kernels in the normal CUDA setup.

</details>

<details>
<summary>Host code and GPU kernels</summary>

The CPU runs the host part of a CUDA application. Its GPU kernels do not automatically execute on the CPU when a GPU is absent. A separately written CPU implementation can calculate the same mathematical result using CPU instructions. That is what this guide's CPU labs do.

</details>

<details>
<summary>GPU compatibility</summary>

CUDA targets compatible NVIDIA GPUs. Apple's GPU computing stack includes Metal; having an Apple GPU is not the same as having a CUDA-capable NVIDIA GPU.

</details>

<details>
<summary>From graphics to general computation</summary>

Graphics involves large amounts of arithmetic over geometry and image data. Similar hardware resources can also serve other numerical work. The name does not restrict all its calculations to visible pictures.

</details>

<details>
<summary>The same arithmetic on different processors</summary>

Adding arrays, multiplying matrices, and adjusting pixel values are mathematical operations, not intrinsically GPU-only operations. The execution approach, supported formats, numerical details, and speed can differ.

</details>

<details>
<summary>GPU performance and overhead</summary>

A GPU needs suitable parallel work. Submission, data movement, dependencies, memory access, and workload size affect total time. A CPU can finish small or poorly parallelized work sooner.

</details>

<details>
<summary>Integrated GPUs</summary>

An Apple Silicon chip includes GPU hardware. A separate graphics card is one physical arrangement, not a requirement for a GPU to exist.

</details>

<details>
<summary>Unified memory</summary>

CPU and GPU remain different execution resources. Sharing a physical memory pool also does not guarantee that one processor has finished producing data before the other reads it.

</details>

<details>
<summary>Python and device execution</summary>

Python code can request library operations on a GPU, then retrieve results for printing. You must inspect the chosen device and verify the operation's execution path. Ordinary Python lists and the first two experiments here use CPU execution.

</details>

<details>
<summary>Starting with the foundations</summary>

The six foundation sections introduce the hardware through small arithmetic examples. The CUDA programming guide then develops bits, instructions, C++, threads, and memory in more detail.

</details>

<details>
<summary>A complete execution path</summary>

Adding two tensors through the Apple GPU path in PyTorch involves these steps:

1. The CPU executes the host program that makes the request.
2. The program selects a compatible Apple GPU path, such as PyTorch's MPS backend.
3. That path executes the supported addition on the Apple GPU.
4. The result is made available to the CPU for validation or printing.
5. This can be GPU computing without being NVIDIA CUDA execution.

On a compatible NVIDIA GPU, the CUDA backend supplies the corresponding device implementation.

</details>
