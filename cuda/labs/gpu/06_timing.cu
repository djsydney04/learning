#include "common.cuh"
#include "kernels.cuh"
#include <chrono>

int main() {
    const int n = 1 << 20, threads = 256, blocks = (n + threads - 1) / threads;
    const int repeats = 100;
    auto a = pattern(n), b = pattern(n, 23);
    DeviceBuffer da(n), db(n), dc(n);
    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));
    da.upload(a); db.upload(b); dc.poison();
    vector_add<<<blocks, threads>>>(da.data, db.data, dc.data, n);
    finish_kernel(); // Warm up context/kernel before either timing scope.

    CUDA_CHECK(cudaEventRecord(start));
    for (int repeat = 0; repeat < repeats; ++repeat)
        vector_add<<<blocks, threads>>>(da.data, db.data, dc.data, n);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));
    float total_ms = 0;
    CUDA_CHECK(cudaEventElapsedTime(&total_ms, start, stop));
    float ms = total_ms / repeats;
    require(ms > 0, "Timer resolution insufficient");

    auto begin = std::chrono::steady_clock::now();
    da.upload(a); db.upload(b);
    vector_add<<<blocks, threads>>>(da.data, db.data, dc.data, n);
    finish_kernel();
    auto result = dc.download();
    auto end = std::chrono::steady_clock::now();
    std::vector<float> expected(n);
    for (int i = 0; i < n; ++i) expected[i] = a[i] + b[i];
    check_values(result, expected);
    double transfer_and_kernel_ms = std::chrono::duration<double, std::milli>(end - begin).count();
    std::cout << "Kernel sequence mean: " << ms << " ms\n"
              << "Effective logical bandwidth: " << (3.0 * n * sizeof(float)) / (ms * 1e6) << " GB/s\n"
              << "One upload + kernel + download: " << transfer_and_kernel_ms << " ms\n"
              << "Allocation, initialization, and CPU validation excluded from these timings.\n"
              << "Repeated arrays may be cache-resident; logical bytes are not measured DRAM traffic.\n";
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
    std::cout << "PASS: timed outputs match CPU reference\n";
}
