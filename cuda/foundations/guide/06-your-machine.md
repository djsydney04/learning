# 6. Your machine

[← CUDA and software](05-cuda-and-software.md) · [Further notes →](questions.md) · [Next: CUDA programming →](../../guide/00-start.md)

## This machine has an Apple GPU

The hardware query for this workspace identified **Apple M3 Pro** graphics. Its GPU is part of the Apple chip. You do have GPU hardware; it is not an NVIDIA GPU.

On a Mac, you can inspect graphics information through **System Information → Graphics/Displays**, or run:

```sh
system_profiler SPDisplaysDataType
```

Look for the chipset/model name. That is a hardware identification step. It does not prove that a particular programming environment can submit GPU calculations successfully.

Apple's [Metal](https://developer.apple.com/metal/) supports programming its GPU for graphics and computation. The ordinary NVIDIA CUDA labs in this repository do not run on the M3 Pro GPU. Installing CUDA software does not turn an Apple GPU into an NVIDIA GPU. Historical CUDA releases supporting some Intel Macs do not provide an Apple Silicon CUDA path; NVIDIA records the end of macOS support in its [CUDA 10.2 release notes](https://docs.nvidia.com/cuda/archive/10.2/cuda-toolkit-release-notes/).

The subject of this guide remains CUDA programming for NVIDIA GPUs. You can learn its foundations on this computer while keeping the hardware execution requirement clear.

## You can do the foundations now

From the repository root:

```sh
python3 cuda/foundations/experiments/01_pixels.py
python3 cuda/foundations/experiments/02_work.py
```

Both are ordinary CPU programs using Python's standard library. They teach image arithmetic and work ownership. They do not need CUDA, a GPU, or installed Python packages. You can also work the same examples on paper.

Then the CUDA programming part has four CPU C++ labs:

```sh
cd cuda
make check-cpu
```

The [setup guide](../../guide/00-start.md) explains the C++ tools. These labs are preparation for writing CUDA kernels. They are not running those kernels on a CPU.

## Your first real CUDA run

When you have access to a compatible NVIDIA development machine, copy or clone the repository there. Use the [setup guide](../../guide/00-start.md) to check its driver, toolkit, and compiler. In that machine's `cuda/` folder:

```sh
make build/gpu/00_device
./build/gpu/00_device
make build/gpu/01_first_kernel
./build/gpu/01_first_kernel
```

The device query asks CUDA which GPU it can see and prints its properties. It does not yet run your arithmetic kernel. The next program, [01_first_kernel.cu](../../labs/gpu/01_first_kernel.cu), does:

1. The CPU requests enough GPU memory for one integer.
2. The CPU launches a kernel with one GPU thread.
3. That thread writes the number 42 into the GPU allocation.
4. The CPU waits for completion and copies the result back.
5. The CPU checks that the number is 42 and frees the allocation.

A **thread** is one execution of the kernel with its own identity and state. The first program uses only one so you can understand the request and result before distributing work over many threads. The [first-kernel lesson](../../guide/04-first-kernel.md) explains every line of code.

These commands belong on the NVIDIA machine. On this Mac, the GPU build stops with a clear missing-tool message when `nvcc` is unavailable. Reading and editing the code are still useful; they do not establish that it has executed.

## What you need next

A university machine or another CUDA development machine you already have access to can provide the execution step. You can keep using this Mac to read and edit the source while CUDA compilation and execution happen elsewhere.

You do not need to buy a GPU to understand work ownership, memory, or bounds checks. Keep the distinction between **understanding an algorithm**, **running a CPU model**, and **testing the CUDA implementation** visible in your notes.

<details>
<summary>Optional review</summary>

Explain what the CPU will do, what the GPU will do, where the input and result live, and how the CPU knows the result is ready.

</details>

Continue to [CUDA programming](../../guide/00-start.md).
