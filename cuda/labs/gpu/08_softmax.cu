#include "common.cuh"
#include "kernels.cuh"

int main() {
    const int rows = 4;
    for (int threads : {32, 128, 256}) {
        for (int cols : {1, 3, 31, 32, 33, 255, 256, 257, 1003}) {
            std::vector<float> x(rows * cols);
            for (int col = 0; col < cols; ++col) {
                float value = static_cast<float>(col % 17) - 8.0f;
                x[col] = value;
                x[cols + col] = value + 1000.0f; // shift invariance
                x[2 * cols + col] = -1000.0f;   // uniform row
                x[3 * cols + col] = col == cols / 2 ? 1000.0f : -1000.0f;
            }
            auto expected = softmax_cpu(x, rows, cols);
            DeviceBuffer dx(x.size()), dy(x.size());
            dx.upload(x); dy.poison();
            softmax_rows<<<rows, threads, threads * sizeof(float)>>>(dx.data, dy.data, cols);
            finish_kernel();
            auto y = dy.download();
            check_values(y, expected, 2e-6, 2e-5);
            for (int row = 0; row < rows; ++row) {
                double sum = 0;
                for (int col = 0; col < cols; ++col) {
                    float value = y[row * cols + col];
                    require(std::isfinite(value) && value >= 0 && value <= 1, "Invalid probability");
                    sum += value;
                }
                require(close(sum, 1, 2e-5, 2e-5), "Softmax row does not sum to one");
            }
            for (int col = 0; col < cols; ++col)
                require(close(y[col], y[cols + col], 2e-6, 2e-5), "Softmax shift invariance failed");
        }
    }
    std::cout << "PASS: stable softmax, 9 widths, 3 block sizes, and four input patterns\n";
}
