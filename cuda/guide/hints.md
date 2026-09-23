# Hints, one step at a time

[Guide](../README.md) · [Exercise map](exercises.md)

Open only the hint you need. First draw the inputs and expected output for a case smaller than one block.

<details>
<summary>E01: Which number identifies an element?</summary>

The block contributes `blockIdx.x * blockDim.x`, and the thread contributes `threadIdx.x`. Add them. Check the resulting index before reading either input or writing output. With `n=257` and 256 threads, block 1 has one useful writer.

</details>

<details>
<summary>E02: Why does my SAXPY work only for small inputs?</summary>

The checker launches only two 128-thread blocks. The total number of thread identities is 256. After processing its starting index, a thread advances by 256 until its index is outside the input. Advancing by `blockDim.x` alone makes different blocks overlap. Keep output separate from y as required by this exercise.

</details>

<details>
<summary>E03: How can threads outside the input still help?</summary>

They write zero into their shared slots and participate in every barrier. First fill all slots and synchronize. Halve the active range at each stage; threads in the lower half add the matching upper-half entries. Keep the barrier outside the `if (t < stride)`. Only thread zero writes the block partial. Do not have all blocks overwrite `partial[0]`.

</details>

<details>
<summary>E04: Why do square examples pass but rectangles fail?</summary>

A has K columns, B has N columns, and C has N columns. Their row strides are therefore K, N, and N. Keep `row`, `col`, and the reduction variable `inner` separate. Each output thread should loop over K and write once after finishing its sum. For row 1, column 2 in `[2,3] × [3,4]`, use A offsets 3,4,5 and B offsets 2,6,10.

</details>

<details>
<summary>E05: What do the two tile barriers protect?</summary>

The first protects consumers from reading before all producers load. The second protects slow consumers from the next iteration's writers. An out-of-range output thread still supplies a tile slot (possibly zero) and participates. Zero-fill independently for A and B using their respective bounds. Do not put an early output-bounds return at the top of this kernel.

</details>

<details>
<summary>E06: Why are very large scores failing?</summary>

Reduce the row maximum before exponentiating. Use `expf(x - maximum)`, not `expf(x)`. A lane with no assigned columns contributes negative infinity to the maximum and zero to the sum. Widths can exceed the number of threads: use a stride of `blockDim.x` within the row for all per-column phases.

</details>

<details>
<summary>E06: Why does scratch reuse still race?</summary>

Every thread must first copy the finished maximum from `scratch[0]` to a private variable. Then a block barrier ensures everyone has read it before any thread stores local sums into scratch. A barrier before the read makes the data ready; a barrier after the read makes reuse safe.

</details>

The complete [reference kernels](../reference/kernels.cuh) are intentionally readable. After consulting a solution, close it, rebuild the logic from your ownership and phase diagram, and explain every bounds check and barrier.
