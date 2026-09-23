"""A CPU-only arithmetic example. No GPU, CUDA, or extra packages are used.

From the repository root: python3 cuda/foundations/experiments/01_pixels.py
"""


def brighten(image, amount):
    result = []
    for row in image:
        new_row = []
        for value in row:
            new_row.append(max(0, min(255, value + amount)))
        result.append(new_row)
    return result


def show(label, image):
    print(label)
    for row in image:
        print(row)


def main():
    image = [[0, 60], [120, 240]]
    amount = 20  # Change this and predict the output before rerunning.
    show("Original grayscale values:", image)
    show("Adjusted grayscale values:", brighten(image, amount))
    # Fixed known answers check the function independently of your experiment amount.
    assert brighten(image, 20) == [[20, 80], [140, 255]]
    assert brighten(image, -30) == [[0, 30], [90, 210]]
    assert image == [[0, 60], [120, 240]], "The original must remain unchanged"
    print("PASS: image arithmetic on the CPU. No GPU work was launched.")


if __name__ == "__main__":
    main()
