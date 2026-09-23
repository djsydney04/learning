# Verification notes

[Guide](../README.md)

Prepared September 2026. These notes distinguish checks performed locally from commands supplied for later use on NVIDIA hardware.

## Local CPU execution

Environment: macOS / Darwin arm64, Apple Clang 16.0.0, C++17. No CUDA compiler (`nvcc`) was found on this machine.

From `cuda/`, this command compiled and ran all four CPU labs successfully:

```sh
make check-cpu
```

The same four programs also passed a fresh build with compiler warnings treated as errors, AddressSanitizer, and UndefinedBehaviorSanitizer:

```sh
make -B check-cpu CXXFLAGS='-O1 -g -std=c++17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined -fno-omit-frame-pointer'
```

| Lab | Observed outcome |
| --- | --- |
| CPU arithmetic | `[11,22,33,44,55]`; array indexing and pointer arithmetic agree; integer and float division behave as explained. |
| Index ownership | Exact single ownership for 12 input sizes and 5 block sizes, including zero length; grid-stride ownership also passes. |
| Layout | Rectangular flattening; aligned address-region counts 4, 8, 32 for strides 1, 2, 8; hand matrix product matches. |
| Reduction and softmax math | Tree sum is 36; explicitly sequenced lost-update illustration gives 1; stable softmax matches known values, normalizes rows, and rejects NaN comparisons. |

These checks validate ordinary CPU code and mathematical/indexing examples. They do not simulate CUDA scheduling or establish GPU correctness or performance.

## Documentation and diagrams

The CUDA programming part contains 14 numbered lessons, six original local PNG diagrams, four CPU labs, nine CUDA programs, and six student kernel exercises with separate reference solutions. The opening [GPU foundations](../foundations/README.md) adds six introductory lessons, four diagrams, and two CPU arithmetic experiments before those programming lessons.

All six diagrams were rendered with Matplotlib 3.11.2 and visually inspected. To regenerate them using the existing environment, run from the repository root:

```sh
MPLCONFIGDIR=/tmp/cuda-matplotlib transformer/.venv/bin/python cuda/scripts/render_diagrams.py
```

Reading the PNGs and compiling the labs do not require Matplotlib. In a different checkout, any Python environment with Matplotlib can run that script.

From `cuda/`, check local Markdown links, nonempty linked assets, and closed code fences with:

```sh
python3 scripts/check_docs.py
```

This check does not fetch external websites or compile illustrative code snippets. Primary CUDA setup and API references were consulted separately while authoring the lessons.

Recorded result: **23 Markdown files, 122 local links, and all code fences passed** (including the repository's root index). All six linked PNGs exist and are nonempty. `git diff --check` also passed. The student matrix build command was inspected with Make's dry-run mode to confirm it selects student kernels and forwards `ARGS=naive`; this is not a CUDA compilation result.

After adding the foundations inside `cuda/`, the combined guide check passed for **33 Markdown files and 176 local links**, with closed code fences. The two new CPU experiments passed, and all four additional diagrams were rendered and visually inspected. These additions do not change the GPU validation limits below.

## GPU validation still to run

GPU compilation, CUDA runtime execution, Compute Sanitizer checks, profiler output, and performance measurements have **not** been verified on this Mac. The CUDA source has been reviewed, including tail guards, reduction identities, shared-memory reuse barriers, distinct stream output regions, and completion before crossing into nonblocking streams.

Running `make gpu` locally stopped at the intended prerequisite check: `nvcc not found. See guide/00-start.md; make check-cpu works without CUDA.`

On a compatible NVIDIA development machine, from `cuda/`:

```sh
make check-gpu
make sanitize
```

The GPU programs supply CPU reference comparisons and edge cases: vector and block boundaries, deliberately small grids, three reduction block sizes, rectangular matrix tails, uneven stream chunks, and softmax widths/patterns that expose overflow and missed columns. These are intended checks, not recorded GPU passes.

After implementing each exercise, use the commands in [the exercise map](../guide/exercises.md) and run sanitizers against `build/student/` binaries. Empty student kernels are intentional and should fail validation. Add actual GPU environment details and measured outcomes to [your experiment notebook](../guide/experiments.md); there are no GPU speedup claims in this guide.
