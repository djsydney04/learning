# 2. A picture is also a collection of numbers

[← Computer parts](01-computer.md) · [Next: parallel work →](03-parallel-work.md)

## Start with four pixels

A **pixel** is one sample in a digital image's grid. In a simple grayscale image, one number represents a pixel's brightness. Suppose we use integers from 0 for black to 255 for white. This is one common 8-bit representation, not the only image format.

```text
Original 2 × 2 image:

  0    60
120   240
```

There are two rows and two columns, giving four pixels. Imagine the task “increase each stored brightness value by 20, stopping at 255.” It produces:

```text
 20    80
140   255
```

The last value is capped: 240 + 20 is 260, but this representation permits at most 255. This example modifies stored sample values; real image brightness and color processing can involve additional color-space rules.

## One rule, many independent inputs

To compute the first output, we need the first input and the constant 20. We do not need another output to finish first. The same is true for each pixel.

The operation has many independent instances:

```text
input 0   → add 20 and cap → output 20
input 60  → add 20 and cap → output 80
input 120 → add 20 and cap → output 140
input 240 → add 20 and cap → output 255
```

A CPU can calculate all four. A GPU can also perform this kind of operation, with work distributed across its execution resources. For four values, arranging GPU execution may cost more than the calculation. For a large image, the amount of independent work becomes much larger.

A 1920-by-1080 image has 2,073,600 pixels. Processing that many pixels repeatedly supplies a lot of arithmetic. Color images often represent each pixel using red, green, and blue components, supplying more values per pixel. Modern graphics also involves geometry, textures, depth, lighting, and other work; changing brightness is just our first accessible example.

## Why this connects to AI

A processor's arithmetic circuits operate on numbers. Those numbers can represent pixel colors, positions in a simulation, or the intermediate values of a neural network. Much neural-network computation involves arrays, matrix multiplication, and related operations with substantial parallel work.

That is why a GPU can calculate something that never becomes an image. **GPU computing** means using GPU hardware for computation, including work beyond drawing graphics. CUDA is one software platform for doing this on NVIDIA GPUs. Apple's Metal also supports both graphics and compute; see [Apple's overview](https://developer.apple.com/metal/).

The GPU does not become a different physical device when you switch from a game to a numerical program. Software asks it to perform different supported work.

## Run the arithmetic on your CPU

From the repository root:

```sh
python3 cuda/foundations/experiments/01_pixels.py
```

The [small program](../experiments/01_pixels.py) prints original and adjusted values. Its list of lists holds the rows. `for` repeats work over those rows and values, `min(255, value + 20)` chooses the smaller of 255 and the proposed output, and `print` displays text.

The program runs on the CPU. It demonstrates what the calculation means; it does not launch GPU work. Change the amount from 20 to 10, predict the four results, and rerun. Values leaving the range are clamped to 0 or 255 in the supplied function.

<details>
<summary>Optional review</summary>

Darken the original four pixels by 30, stopping at zero. Answer: `[0,30]` and `[90,210]`.

Explain why these four outputs could be calculated independently. Describe another collection of numbers to which the same rule could be applied.

</details>
