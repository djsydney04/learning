# 2. Enough C++ to understand a kernel

[← Computers](01-computers.md) · [Next: parallelism →](03-parallelism.md)

**Build today:** add two lists of numbers on the CPU. Open [01_cpu.cpp](../labs/cpu/01_cpu.cpp). We use a small C++ subset; you do not need to learn the whole language first.

## Read a program from its entry point

```cpp
#include <iostream>

int main() {
    int count = 5;
    float scale = 2.0f;
    std::cout << count << " values, scale " << scale << '\n';
    return 0;
}
```

`#include` makes declarations from a header available. `main` is where this host program begins. Curly braces group statements. Most statements end with `;`. `int count = 5` creates an integer variable and initializes it to five. `float scale = 2.0f` creates a floating-point variable; the suffix `f` makes the literal a `float` rather than a `double`.

`std::cout` writes output. Here, `<<` sends values to that output stream. `\n` is a newline. `return 0` reports successful completion to the operating system; reaching the end of `main` also returns zero. An error reported by our checks causes the program to fail instead.

## Expressions, conditions, and loops

```cpp
int i = 0;
i = i + 1;            // Assignment changes i.
bool inside = i < 5;  // Comparison produces true or false.
if (inside) {
    std::cout << i << '\n';
}
for (int j = 0; j < 5; ++j) {
    std::cout << j << '\n';
}
```

The loop initializes `j` once, checks `j < 5` before each iteration, executes the body, then increments `j` using `++j`. It prints 0, 1, 2, 3, 4. The value 5 fails the condition, so the body does not execute for it.

`=` assigns; `==` compares equality. `&&` means logical “and.” `%` gives the remainder for these nonnegative integer examples. `5 / 2` is integer division and produces 2. `5.0f / 2.0f` produces 2.5. These details matter when calculating block counts and array offsets.

## Arrays and ownership

```cpp
#include <vector>

std::vector<float> a{1, 2, 3, 4, 5};
std::vector<float> b{10, 20, 30, 40, 50};
std::vector<float> c(a.size());
for (std::size_t i = 0; i < a.size(); ++i) {
    c[i] = a[i] + b[i];
}
```

`std::vector<float>` owns a contiguous sequence of floats in CPU-accessible memory. “Contiguous” means consecutive elements occupy consecutive element-sized regions. `a.size()` is the number of elements, not bytes. `a[0]` is the first and `a[4]` the fifth. `a[5]` is outside this array. C++ `operator[]` does not automatically protect you from this error.

`std::size_t` is an unsigned integer type used for sizes. Unsigned arithmetic cannot represent negative values; subtracting from zero wraps. Our test-data generator converts a small index to signed `int` before subtracting an offset. For simplicity, the CUDA labs use small positive shapes fitting in `int`; production code needs explicit size and overflow checks for larger tensors.

## Pointers: a value that identifies a location

```cpp
float* p = a.data();
float first = *p;
float third = *(p + 2);
p[1] = 20.0f;
```

In a declaration, `float*` means “pointer to float.” `a.data()` supplies the address of the first element. In an expression, `*p` means “access the float at the address in `p`,” called **dereferencing**. `p + 2` advances by two floats, not two bytes. `p[2]` and `*(p + 2)` access the same element.

`&a[2]` asks for the address of element 2. A pointer does not carry an array length. When passing a pointer to a function, we commonly pass the length separately. A `nullptr` pointer points to no object and must not be dereferenced.

The vector owns its allocation and releases it when the vector goes out of scope. `p` only refers to that allocation. If the vector is destroyed or reallocates, `p` may no longer be valid. Copying a pointer copies an address, not all the data at that address. This is especially important when CPU and GPU memory differ.

## Functions give an operation a name

```cpp
float add(float left, float right) {
    return left + right;
}

void add_arrays(const float* a, const float* b, float* c, int n) {
    for (int i = 0; i < n; ++i) c[i] = add(a[i], b[i]);
}
```

The first function returns a float. The second returns no value, written `void`; it writes into the output allocation through `c`. `const float* a` prevents writing the pointed-to floats through `a`. The pointer itself is still a value supplied to the function.

`add_arrays(a.data(), b.data(), c.data(), 5)` passes three addresses and a length. The function assumes the caller supplied enough valid elements. Later we will keep the same arithmetic but assign iterations to GPU threads.

## Supporting code you will see

The labs use [math.hpp](../include/math.hpp) for shared checks. `require(condition, message)` fails with a message if the condition is false. `check_values` compares every output with a CPU result, rejects non-finite values, and reports the first mismatching index. `auto` asks the compiler to infer a variable's type from its initializer; it does not remove static type checking.

You will later see a `DeviceBuffer` struct. A **struct** groups fields and functions. Its constructor allocates memory; its destructor releases it when its scope ends. Copying it is disabled to prevent two owners from freeing the same allocation. This ownership technique is called RAII. We first show explicit CUDA calls so this helper does not hide what allocation and copying mean.

## Run, modify, explain

```sh
make build/cpu/01_cpu
./build/cpu/01_cpu
```

Change one input value and the corresponding expected answer. Then write a loop that computes `c[i] = 2 * a[i] + b[i]`. Finally write a function that computes the sum of all five entries of `a`.

**Checkpoint:** explain why `float* p` differs from `float value`, why the loop uses `<` rather than `<=`, and why an address alone cannot tell you how many elements are valid.
