# 0. Start here

[Course](../README.md) · [Next: computers and numbers →](01-computers.md)

You will first run a program on the CPU, then learn why and how parts of a program move to the GPU. Take one lesson at a time. Before moving on, answer its checkpoint without looking at the code.

## A file, a terminal, and a compiler

A **source file** contains the program you write. A **compiler** translates that source into instructions the machine can execute. A **terminal** lets you type commands to run the compiler and the resulting program. These are three different things.

Open this repository in an editor. Open a terminal and run:

```sh
pwd
```

`pwd` prints the folder the terminal is currently working in. On this machine, enter the CUDA folder with:

```sh
cd /Users/djsydney/Downloads/learning/cuda
```

In another checkout, use its own path. All course commands after this assume the terminal is in `cuda/`. Do not type them into a Python prompt or a C++ source file. In shell examples, a line beginning with `#` is a comment.

## Start on your CPU

```sh
c++ --version
make --version
make check-cpu
```

`make` reads the [Makefile](../Makefile), compiles changed source files into `build/`, and runs the requested task. Its default target builds only the CPU labs. The first arithmetic result is:

```text
01 CPU: 11 22 33 44 55
```

There are four `PASS` lines, one per lab. Read the first now; the other labs preview later lessons. You can run just the first binary again:

```sh
./build/cpu/01_cpu
```

`./` means “look in this folder,” and `build/cpu/01_cpu` is the executable produced by the compiler. To see compilation without Make:

```sh
c++ -std=c++17 -O2 -Wall -Wextra -Iinclude labs/cpu/01_cpu.cpp -o build/first
./build/first
```

`-std=c++17` selects the language version; `-O2` enables optimization; the warning flags ask for useful diagnostics; `-Iinclude` adds a directory of supporting headers; `-o` names the output. `build/` already exists after `make check-cpu`.

If a compiler is missing on macOS, install Apple's Command Line Tools with `xcode-select --install`. On a Linux machine, use its distribution's C++ compiler and Make packages. Windows readers can use a Linux environment under WSL for these Make commands. Read [debugging](debugging.md) if the build fails.

## The hardware boundary

Apple's GPU uses Apple's graphics/compute stack; it does not execute these NVIDIA CUDA programs. Installing a Python library or changing a filename to `.cu` does not change that. Use the CPU labs and hand traces locally, then use a compatible NVIDIA machine for the `.cu` labs. Modern CUDA toolkit releases do not support macOS; see NVIDIA's [platform release notes](https://docs.nvidia.com/cuda/archive/12.6.3/cuda-toolkit-release-notes/index.html#deprecated-features).

A CUDA development environment has separate pieces:

| Piece | Its job | Check |
| --- | --- | --- |
| Compatible NVIDIA GPU | Executes device instructions | Device visible to the system. |
| NVIDIA driver | Lets the operating system and application communicate with the GPU | `nvidia-smi`. |
| CUDA toolkit | Supplies `nvcc`, headers, runtime development files, and tools | `nvcc --version`. |
| Supported host compiler | Compiles the CPU part of your CUDA C++ program | Compiler supported by your installed toolkit. |
| Your program | Launches kernels and checks their results | The device and kernel labs below. |

The “CUDA Version” shown by `nvidia-smi` indicates driver support, not proof that `nvcc` is installed. A framework can run prebuilt GPU operations while still lacking the toolkit required to compile your own `.cu` files.

## Continue on an NVIDIA machine

Use a university workstation, a machine you already have access to, or a GPU development environment. Copy or clone this repository there. The CPU lessons do not require you to rent anything.

Follow the installation instructions for that machine's exact operating system, GPU, and toolkit. NVIDIA maintains the [Linux installation guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) and [WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html). Under WSL, the Windows NVIDIA driver provides GPU support; follow the WSL-specific instructions instead of installing a Linux GPU display driver inside WSL.

Run these commands **on the GPU machine**:

```sh
nvidia-smi
nvcc --version
make build/gpu/00_device
./build/gpu/00_device
make build/gpu/01_first_kernel
./build/gpu/01_first_kernel
```

The device query prints the GPU's actual name, memory, warp size, and limits. The first kernel should print `PASS: first kernel wrote 42`. This checks actual execution, beyond detecting a device. Later, `make check-gpu` runs every reference lab.

If your compiler's default architecture does not match the GPU, set `CUDA_ARCH` to a target supported by **both** your GPU and toolkit. For example, `CUDA_ARCH=sm_80` is an example target for compute capability 8.0, not a setting to copy for every GPU. To rebuild already-created binaries with new flags, use `make -B gpu CUDA_ARCH=...` with the actual target substituted. Do not enter the literal `...`. Consult the [compatibility guide](https://docs.nvidia.com/deploy/cuda-compatibility/) when driver, toolkit, and GPU support differ.

## Your first study session

1. Read [computers and numbers](01-computers.md), especially operands and addresses.
2. Read [enough C++](02-cpp.md) beside [01_cpu.cpp](../labs/cpu/01_cpu.cpp).
3. Predict the five output values. Run the program.
4. Change `b`'s first value from `10` to `100`. Predict which check will fail, then update the expected result to `101` and rebuild.
5. Explain why all five additions could be done independently.

Keep notes in [the experiment notebook](experiments.md). Each session should produce a prediction, an observation, and an explanation. Sessions are units of progress, not deadlines. If you only have this Mac, complete the CPU labs and written exercises, then resume the real kernel checks when hardware is available.
