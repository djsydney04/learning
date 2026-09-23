# Sources and next steps

[Guide](../README.md)

The explanations, small examples, and diagrams are written for this repository. The platform distinctions were checked against these primary sources in September 2026. You do not need to read the full specifications before beginning the lessons.

| Source | Use it for |
| --- | --- |
| [NVIDIA CUDA programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html) | Host CPU, device GPU, kernels, and thread execution. |
| [NVIDIA CUDA 10.2 release notes](https://docs.nvidia.com/cuda/archive/10.2/cuda-toolkit-release-notes/) | Historical end of macOS CUDA development and execution support. |
| [Apple Metal overview](https://developer.apple.com/metal/) | Apple's graphics and compute programming interfaces. |
| [Apple M3 family](https://www.apple.com/newsroom/2023/10/apple-unveils-m3-m3-pro-and-m3-max-the-most-advanced-chips-for-a-personal-computer/) | CPU/GPU components and unified memory in Apple Silicon. |
| [PyTorch MPS backend](https://docs.pytorch.org/docs/stable/notes/mps.html) | Requesting supported operations on Apple's GPU path. |
| [PyTorch CUDA semantics](https://docs.pytorch.org/docs/stable/notes/cuda.html) | Devices and operations in the CUDA path. |

For this machine, the graphics model was read from the local system report, not inferred from a product recommendation. Actual experiment outcomes are in [verification notes](../examples/RESULTS.md).

Continue with [CUDA](../../README.md) to write kernels, [transformers](../../../transformer/README.md) to use arrays for a language model, or [the tiny CPU](../../../verilong/cpu/intro.md) to explore how hardware executes instructions.
