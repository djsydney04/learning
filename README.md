# Learning, from the inside out

Read the local Markdown lessons beside the code. Each project starts with small experiments and builds toward something you can explain and implement yourself.

| Section | Start here | What you build |
| --- | --- | --- |
| CUDA | [CUDA from first principles](cuda/README.md) | Begin with what CPUs and GPUs are, then build kernels, reductions, matrix multiplication, and stable softmax. |
| Transformers | [Build a transformer](transformer/README.md) | A character-level language model in PyTorch. |
| Computer hardware | [Digital circuits and CPU foundations](cpu-architecture/README.md) | Start with bits, gates, registers, and memory, then build a processor in SystemVerilog. |

These paths connect: hardware executes instructions; CUDA distributes numerical work across a GPU; transformer operations give that work a purpose. Each section also works on its own.

The CUDA guide begins with [GPU foundations](cuda/foundations/README.md): what a GPU is, how it works with a CPU, and where CUDA fits. You can start those explanations and CPU examples on this Mac.

The hardware path begins with a [digital-circuits and architecture primer](cpu-architecture/README.md). It connects binary arithmetic, logic gates, clocked state, memory buses, and CPU instruction execution before introducing SystemVerilog. Worked examples and runnable models lead into the existing Tiny8 exercises.
