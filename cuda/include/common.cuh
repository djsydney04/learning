#pragma once
#include <cuda_runtime.h>
#include "math.hpp"
#include <cstdlib>

inline void cuda_check(cudaError_t status, const char* expression, const char* file, int line) {
    if (status != cudaSuccess) {
        std::cerr << file << ':' << line << ": " << expression << ": "
                  << cudaGetErrorString(status) << '\n';
        std::exit(EXIT_FAILURE);
    }
}
#define CUDA_CHECK(call) cuda_check((call), #call, __FILE__, __LINE__)

// The first two GPU labs use explicit allocation/free. Later labs use this
// owning object to keep the numerical code visible. See guide/04-first-kernel.md.
struct DeviceBuffer {
    float* data = nullptr;
    std::size_t count;
    explicit DeviceBuffer(std::size_t n) : count(n) {
        require(n > 0, "DeviceBuffer requires a positive element count");
        CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&data), n * sizeof(float)));
    }
    ~DeviceBuffer() { CUDA_CHECK(cudaFree(data)); }
    DeviceBuffer(const DeviceBuffer&) = delete;
    DeviceBuffer& operator=(const DeviceBuffer&) = delete;
    void upload(const std::vector<float>& host) {
        require(host.size() == count, "Upload size mismatch");
        CUDA_CHECK(cudaMemcpy(data, host.data(), count * sizeof(float), cudaMemcpyHostToDevice));
    }
    std::vector<float> download() const {
        std::vector<float> host(count);
        CUDA_CHECK(cudaMemcpy(host.data(), data, count * sizeof(float), cudaMemcpyDeviceToHost));
        return host;
    }
    void poison() { upload(std::vector<float>(count, std::numeric_limits<float>::quiet_NaN())); }
};

inline void finish_kernel() {
    CUDA_CHECK(cudaGetLastError());       // launch configuration errors
    CUDA_CHECK(cudaDeviceSynchronize()); // execution errors; wait for results
}
