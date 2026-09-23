#pragma once
// CPU reference calculations and comparisons; no CUDA headers required.
#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

inline void require(bool condition, const std::string& message) {
    if (!condition) throw std::runtime_error(message);
}

inline bool close(double got, double expected, double atol = 1e-5, double rtol = 1e-5) {
    return std::isfinite(got) && std::isfinite(expected) &&
           std::abs(got - expected) <= atol + rtol * std::abs(expected);
}

template <class T>
void check_values(const std::vector<float>& got, const std::vector<T>& expected,
                  double atol = 1e-5, double rtol = 1e-5) {
    require(got.size() == expected.size(), "Output size mismatch");
    for (std::size_t i = 0; i < got.size(); ++i) {
        if (!close(got[i], expected[i], atol, rtol)) {
            throw std::runtime_error("Mismatch at index " + std::to_string(i) +
                ": got " + std::to_string(got[i]) + ", expected " + std::to_string(expected[i]));
        }
    }
}

inline std::vector<float> pattern(std::size_t n, int period = 17) {
    std::vector<float> values(n);
    for (std::size_t i = 0; i < n; ++i) {
        // Convert before subtracting: size_t is unsigned.
        values[i] = static_cast<float>(static_cast<int>(i % period) - period / 2) * 0.25f;
    }
    return values;
}

inline std::vector<double> matmul_cpu(const std::vector<float>& a,
                                    const std::vector<float>& b, int m, int k, int n) {
    require(m > 0 && k > 0 && n > 0, "Matrix sizes must be positive");
    require(a.size() == static_cast<std::size_t>(m) * k &&
            b.size() == static_cast<std::size_t>(k) * n, "Matrix input size mismatch");
    std::vector<double> c(static_cast<std::size_t>(m) * n, 0.0);
    for (int row = 0; row < m; ++row)
        for (int col = 0; col < n; ++col)
            for (int inner = 0; inner < k; ++inner)
                c[row * n + col] += static_cast<double>(a[row * k + inner]) * b[inner * n + col];
    return c;
}

inline std::vector<double> softmax_cpu(const std::vector<float>& x, int rows, int cols) {
    require(rows > 0 && cols > 0 && x.size() == static_cast<std::size_t>(rows) * cols,
            "Softmax expects a nonempty rectangular array");
    std::vector<double> y(x.size());
    for (int row = 0; row < rows; ++row) {
        double maximum = -std::numeric_limits<double>::infinity();
        for (int col = 0; col < cols; ++col) {
            require(std::isfinite(x[row * cols + col]), "Softmax inputs must be finite");
            maximum = std::max(maximum, static_cast<double>(x[row * cols + col]));
        }
        double total = 0.0;
        for (int col = 0; col < cols; ++col) {
            y[row * cols + col] = std::exp(static_cast<double>(x[row * cols + col]) - maximum);
            total += y[row * cols + col];
        }
        for (int col = 0; col < cols; ++col) y[row * cols + col] /= total;
    }
    return y;
}
