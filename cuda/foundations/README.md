# Part 1. GPU foundations for CUDA programming

[CUDA guide](../README.md) · [Continue to CUDA programming →](../guide/00-start.md)

An introduction to GPU hardware and the CPU's role in CUDA programs. It starts with basic arithmetic and introduces the hardware before the programming syntax.

A **CPU** and a **GPU** are physical processors: pieces of hardware that execute instructions. **CUDA** is NVIDIA's software platform for programming compatible NVIDIA GPUs. A GPU is not the same thing as CUDA, and many GPUs do not use CUDA.

## CPU and GPU roles

A CUDA application uses the CPU, while its CUDA kernels normally execute on an NVIDIA GPU. A kernel is the part of the program you ask the GPU to run. The CPU runs the main program, prepares the work, and requests the GPU calculation. NVIDIA calls these the **host** and **device** sides. See its [programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html).

For example, “add these two lists of numbers” can be implemented either as ordinary CPU code or as a CUDA kernel. The arithmetic is the same; the instructions and processor executing them differ. Standard CUDA does not automatically turn a kernel into a CPU implementation when no compatible GPU is present.

The existing command `make check-cpu` in the CUDA section runs separate **ordinary C++ CPU exercises**. It is there so you can learn immediately, not because it runs CUDA on a CPU.

![Hardware and software are different layers: a program can use CPU instructions, NVIDIA CUDA, or Apple's Metal path.](assets/03-software-paths.png)

## Your route

| Section | Topics | Example |
| --- | --- | --- |
| [1 · Computer parts](guide/01-computer.md) | Processors, RAM, storage, and graphics cards. | A picture moving from a saved file to a calculation. |
| [2 · Pixels and arithmetic](guide/02-pixels.md) | Image data and general GPU computation. | Brightening a tiny image represented as numbers. |
| [3 · Parallel work](guide/03-parallel-work.md) | Independent jobs, dependencies, and overhead. | Assigning jobs to four imagined workers. |
| [4 · Memory](guide/04-memory.md) | GPU memory, unified memory, and data movement. | One calculation with two memory arrangements. |
| [5 · CUDA and software](guide/05-cuda-and-software.md) | Host code, kernels, and programming systems. | The processor responsible for each step of a program. |
| [6 · Your machine](guide/06-your-machine.md) | Local CPU exercises and NVIDIA hardware requirements. | The path to your first real CUDA kernel. |

The diagrams are local PNGs. Read in your editor's Markdown preview. [Further notes](guide/questions.md) collect common distinctions; [references](guide/references.md) point to official explanations.

## A first session

Read [lesson 1](guide/01-computer.md), then [lesson 2](guide/02-pixels.md). Work the four brightness calculations by hand before running the optional experiment. From the repository root:

```sh
python3 cuda/foundations/experiments/01_pixels.py
```

This runs on the CPU and needs no extra Python packages. It prints a small image as numbers. Running it does not use the GPU. You can complete the lesson on paper if you have never used Python.

This workspace's hardware query identified an **Apple M3 Pro** GPU. That is a real GPU, using Apple's programming stack rather than NVIDIA CUDA. [Lesson 6](guide/06-your-machine.md) explains what that means for learning CUDA here. Actual execution checks and their limits are recorded in [verification notes](examples/RESULTS.md).

After the six lessons, continue to [Part 2: CUDA programming](../guide/00-start.md). The first CUDA task will then have a clear meaning: the CPU asks an NVIDIA GPU to write a number into memory.
