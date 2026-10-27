#!/usr/bin/env python3
"""Show simultaneous register updates with an ideal, discrete two-stage model.

This Python model does not run SystemVerilog or model setup/hold, clock skew,
metastability, propagation delay, or simulator event scheduling.
"""


class Pipeline:
    """Two registers share an enable; stage 2 samples the old stage 1."""

    def __init__(self):
        self.reset()

    def reset(self):
        """An explicit reset event clears both stored values."""
        self.stage1 = 0
        self.stage2 = 0

    def tick(self, input_value, enable=True):
        """Apply one rising edge and return (stage1, stage2) after the edge."""
        if not 0 <= input_value <= 255:
            raise ValueError("input must fit in eight unsigned bits")
        if enable:
            old_stage1 = self.stage1
            self.stage1 = input_value
            self.stage2 = old_stage1
        return self.stage1, self.stage2


def main():
    print("Ideal clock-edge model; this does not simulate RTL or physical timing.\n")
    print("At an enabled edge: stage1 takes input; stage2 takes OLD stage1.")
    model = Pipeline()
    print("event       input enable | stage1 stage2 (after event)")
    print("reset          -      -  |      0      0")
    for number, (value, enable) in enumerate(((5, True), (9, True), (7, False), (4, True)), 1):
        first, second = model.tick(value, enable)
        print(f"rise {number:<5} {value:5} {int(enable):6}  | {first:6} {second:6}")
    model.reset()
    print("reset event    -      -  |      0      0")
    print("\nChanging an input between edges does not itself update these registers.")
    print("A disabled edge holds BOTH registers, so the pipeline pauses together.")
    print("Reset is an explicit model event, not an analog reset circuit.")


if __name__ == "__main__":
    main()
