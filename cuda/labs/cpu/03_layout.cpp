#include "math.hpp"
#include <set>

int main() {
    const int rows = 3, cols = 5;
    std::vector<int> flat(rows * cols);
    for (int row = 0; row < rows; ++row)
        for (int col = 0; col < cols; ++col) {
            int offset = row * cols + col;
            flat[offset] = 10 * row + col;
            require(offset / cols == row && offset % cols == col, "Flattening failed");
        }
    require(flat[2 * cols + 4] == 24, "Last matrix entry was wrong");
    for (int stride : {1, 2, 8}) {
        std::set<int> sectors;
        for (int lane = 0; lane < 32; ++lane) sectors.insert((lane * stride * 4) / 32);
        std::cout << "03 Layout: 32 lanes, float stride " << stride
                  << ": " << sectors.size() << " distinct 32-byte sectors\n";
        require(sectors.size() == static_cast<std::size_t>(4 * stride), "Sector model failed");
    }
    std::cout << "These are aligned address counts, not measured memory transactions.\n";
    auto result = matmul_cpu({1, 2, 3, 4}, {2, 0, 1, 0, 3, 1}, 2, 2, 3);
    require(result == std::vector<double>({2, 6, 3, 6, 12, 7}), "Hand matrix product failed");
    std::cout << "PASS: rectangular layout and hand-worked matrix product\n";
}
