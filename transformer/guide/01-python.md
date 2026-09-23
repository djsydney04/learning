# 1. Enough Python to build a model

[← Start](00-start.md) · [Next: tensors →](02-tensors.md)

**Build today:** a small program that turns `"cat"` into numbers and back. No machine learning yet. This gives you the programming tools you will reuse in every layer.

Read a short section, predict its output on paper, run it, then change something. Getting a prediction wrong is useful: locate the exact line where your mental model differs from the program.

## A terminal is not Python

The **terminal** is a text interface for telling your computer to run programs. **Python** is one of those programs. A file ending in `.py` contains Python instructions. Your editor changes the file; Python executes it.

```text
EDITOR                         TERMINAL
Write and save scratch.py       python scratch.py
           │                         │
           └── file on disk ─────────┤
                                     ▼
                               Python executes lines
                                     │
                                     ▼
                               Printed output
```

First finish the environment setup in [Start](00-start.md). Run these commands in the terminal, from the project folder:

```bash
python --version
python -m labs.01_python
```

`-m labs.01_python` means “find the module named `01_python` inside the `labs` package and run it.” You do not type the `.py` suffix with `-m`. This first lab needs only Python; later labs need PyTorch installed in the selected environment.

If you type `python` by itself, you enter an interactive Python prompt, usually marked `>>>`. Type `exit()` to return to the terminal. Commands such as `cd`, `python -m ...`, and `pip install ...` belong in the terminal, not after `>>>`.

For the examples below, create `scratch.py` in the project folder, paste a Python code block into it, save, then run:

```bash
python scratch.py
```

When a later block uses an earlier variable, keep both blocks in the file in order. `print(...)` displays a value; otherwise a script may run successfully without showing anything.

## Names, values, and basic types

```python
message = "cat"          # str: text, called a string
count = 3                # int: an integer
learning_rate = 0.1      # float: a number with a fractional part
is_training = True      # bool: True or False

print(message)
print(count + 2)
print(count * 2)
print(count / 2)
print(type(message).__name__)
```

Expected output is `cat`, `5`, `6`, `1.5`, and `str`, on separate lines. `=` assigns a value to a name. It does not mean “check whether these things are equal”; that is `==`. A `#` starts a comment for the human reader. Quotes distinguish the text `"3"` from the number `3`.

Prediction: what does `"cat" * 2` produce? What about `3 ** 2`?

<details>
<summary>Check your prediction</summary>

`"catcat"` and `9`. The meaning of an operator depends on its inputs. `**` is exponentiation: `3 ** 2` means three squared.

</details>

## Lists, indices, and slices

A **list** stores a sequence of values. **Indexing** selects one value. Python starts counting positions at zero.

```python
ids = [1, 0, 2]
print(ids[0])       # 1: the value at position zero
print(ids[-1])      # 2: the final value
print(ids[:2])      # [1, 0]: positions before 2
print(ids[1:])      # [0, 2]: position 1 through the end
print(len(ids))     # 3: how many values
ids.append(3)      # Change the list by adding one value.
print(ids)         # [1, 0, 2, 3]
```

```text
positions:     0     1     2
             ┌─────┬─────┬─────┐
values:      │  1  │  0  │  2  │
             └─────┴─────┴─────┘
ids[0]       ──┘
ids[1:]            └─────────┘
```

Strings also support indexing and slicing: `"cat"[0]` is `"c"`, and `"cat"[1:]` is `"at"`. A slice `start:stop` includes `start` and excludes `stop`. You will use adjacent slices to create next-character training examples. See the [Python introduction](https://docs.python.org/3/tutorial/introduction.html) for these syntax rules.

## Dictionaries connect labels to values

A **dictionary** looks up a value using a key. Here, the keys are characters and the values are arbitrary IDs:

```python
char_to_id = {"a": 0, "c": 1, "t": 2}
print(char_to_id["c"])  # 1
```

ID `2` does not mean `"t"` is twice as important as `"c"`. IDs name entries in a table, like seat numbers. Their numeric distances are not a measure of meaning.

## Loops and conditions

A **loop** repeats a block. Python uses indentation, usually four spaces, to mark the block.

```python
message = "cat"
char_to_id = {"a": 0, "c": 1, "t": 2}
ids = []
for character in message:
    token_id = char_to_id[character]
    ids.append(token_id)
print(ids)  # [1, 0, 2]

for position, token_id in enumerate(ids):
    print(position, token_id)

if len(ids) == 3:
    print("We have three tokens.")
else:
    print("We have a different number of tokens.")
```

`enumerate` supplies the position and the value together. The comma in `position, token_id` unpacks that pair into two names. The three loop iterations print `0 1`, `1 0`, and `2 2`. `if` runs a block only when its condition is true.

You will also see `for step in range(5):`. `range(5)` supplies `0, 1, 2, 3, 4`; it is useful when you want to repeat an operation five times.

A **list comprehension** is a compact spelling of the earlier loop:

```python
ids = [char_to_id[character] for character in message]
```

Read it as “for each character in message, collect its ID.” The longer loop is equally valid. Use it when you want to inspect intermediate values.

## Functions name a reusable calculation

```python
def encode(text, char_to_id):
    ids = []
    for character in text:
        ids.append(char_to_id[character])
    return ids

mapping = {"a": 0, "c": 1, "t": 2}
encoded = encode("cat", mapping)
print(encoded)  # [1, 0, 2]
```

`def` defines a function. `text` and `char_to_id` are **parameters**: names for inputs. `"cat"` and `mapping` are the **arguments** supplied by this call. `return` sends a result back to the caller. A function that only prints something does not return that printed value; without an explicit return value, its result is `None`.

Think of a neural-network layer as a function with extra stored, adjustable numbers:

```text
ordinary function:      inputs ── calculation ── output

learned layer:          inputs ── calculation ── output
                                     ▲
                            stored weights and biases
```

## Classes keep data and behavior together

A **class** is a recipe for making an object. An **object** is one instance of that recipe. An **attribute** is something stored on the object. A **method** is a function attached to the class.

```python
class Vocabulary:
    def __init__(self, text):
        self.characters = sorted(set(text))
        self.char_to_id = {}
        for index, character in enumerate(self.characters):
            self.char_to_id[character] = index

    def encode(self, text):
        return [self.char_to_id[character] for character in text]

    def decode(self, ids):
        return "".join(self.characters[token_id] for token_id in ids)

vocabulary = Vocabulary("cat")
print(vocabulary.characters)            # ['a', 'c', 't']
print(vocabulary.encode("cat"))         # [1, 0, 2]
print(vocabulary.decode([1, 0, 2]))      # cat
```

Read this one line at a time:

- `__init__` runs while a new instance is initialized. `Vocabulary("cat")` supplies its `text` input.
- `self` names this particular object inside its methods. `self.characters` keeps data for later calls.
- `set(text)` removes duplicates; `sorted(...)` arranges the remaining characters consistently.
- `vocabulary.encode("cat")` calls `encode`, passing `vocabulary` as `self` automatically.
- `"".join(...)` glues a sequence of strings together with no separator. The expression inside generates each decoded character.

You do not need to master object-oriented design first. For this project, remember: create layers in `__init__`, then use them in `forward`.

## Imports and the PyTorch class pattern

`import` makes code from another module available. `import torch` allows `torch.tensor(...)`. `from torch import nn` allows `nn.Linear(...)` as a shorter spelling of `torch.nn.Linear(...)`.

Here is a preview; [chapter 3](03-learning.md) explains the computation:

```python
import torch
from torch import nn

class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2, 1)

    def forward(self, x):
        return self.linear(x)

model = TinyModel()
x = torch.tensor([[1.0, 2.0]])
print(model(x).shape)  # torch.Size([1, 1])
```

`TinyModel(nn.Module)` means this class inherits PyTorch's model behavior. `super().__init__()` initializes that parent behavior before layers are assigned. Layers stored as attributes are registered as submodules, so `model.parameters()` can find their adjustable values. Define the calculation in `forward`; call the object with `model(x)`, so PyTorch's normal module-call machinery runs. See [the Module API](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html).

The output number in this preview can change between runs because the layer starts with random weights. Its shape should always be `[1, 1]`.

## Reading a few extra pieces of lab syntax

The labs use short printing and checking expressions. These do not add new model behavior:

```python
step = 3
loss = 0.123456
print(f"step {step}: loss = {loss:.4f}")  # step 3: loss = 0.1235
assert step == 3
```

An **f-string** starts with `f` before the quote. Expressions inside `{...}` are inserted into the text. `:.4f` displays a floating-point value with four digits after the decimal point; it changes the display, not the stored number. `assert` checks that a condition is true and stops the program if it is false.

`if __name__ == "__main__":` at a file's end makes its demonstration run when you execute that file as a program, while allowing another file to import its functions without running the demo. You can use this pattern unchanged for now.

## Do the lab, then make it yours

Open [labs/01_python.py](../labs/01_python.py), read `main()`, and run:

```bash
python -m labs.01_python
```

The default vocabulary is `{'a': 0, 'c': 1, 't': 2}`; the IDs are `[1, 0, 2]`. Every lab ends with assertions. `assert condition` stops with an `AssertionError` when the condition is false. It turns “I think this works” into a precise check.

1. Change `MESSAGE` to `"taco"`. Predict the sorted vocabulary and IDs before running.
2. Write `count_character(text, wanted)` using a loop and an `if`.
3. Write a check that encoding then decoding `"tact"` returns `"tact"` with a vocabulary built from `"cat"`.
4. Try encoding `"dog"` with that vocabulary. Read the last line of the error. Explain why this should fail.

<details>
<summary>Solutions</summary>

1. Characters: `['a', 'c', 'o', 't']`. IDs: `[3, 0, 1, 2]`.
2. One possible function:

   ```python
   def count_character(text, wanted):
       count = 0
       for character in text:
           if character == wanted:
               count += 1  # Same as count = count + 1.
       return count

   assert count_character("banana", "a") == 3
   ```

3. `assert vocabulary.decode(vocabulary.encode("tact")) == "tact"`.
4. `KeyError: 'd'`: the dictionary has no entry for `d`. A character outside the known vocabulary cannot be encoded by this tiny tokenizer.

</details>

## Before you continue

You are ready when you can create and run a `.py` file, explain the difference between an ID and an index, write a loop inside a function, and explain what `self.linear` stores. If classes still feel unfamiliar, keep this chapter open beside the later model code. You can learn the pattern through repeated use.

[Next: arranging numbers into tensors →](02-tensors.md)
