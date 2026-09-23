// Run from cuda/: make check-cpu
#include "math.hpp"

float add(float left, float right) {
    return left + right;
}

int main() {
    std::vector<float> a{1, 2, 3, 4, 5};
    std::vector<float> b{10, 20, 30, 40, 50};
    std::vector<float> c(a.size());
    for (std::size_t i = 0; i < a.size(); ++i) c[i] = add(a[i], b[i]);

    float* pointer = a.data();
    std::cout << "01 CPU: ";
    for (float value : c) std::cout << value << ' ';
    std::cout << "\nOne float occupies " << sizeof(float) << " bytes here.\n";
    std::cout << "a[2] = " << a[2] << ", *(pointer + 2) = " << *(pointer + 2) << '\n';
    check_values(c, std::vector<float>{11, 22, 33, 44, 55});
    require(pointer + 2 == &a[2], "Pointer arithmetic disagrees with indexing");
    require(5 / 2 == 2 && close(5.0f / 2.0f, 2.5), "Division example failed");
    std::cout << "PASS: CPU arithmetic, indexing, and pointers\n";
}
