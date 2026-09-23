#include "common.cuh"
#include "kernels.cuh"

int main() {
    for (int n : {1, 31, 32, 33, 255, 256, 257, 1003, 65537}) {
        auto a = pattern(n), b = pattern(n, 23);
        std::vector<float> expected(n), result(n, std::numeric_limits<float>::quiet_NaN());
        for (int i = 0; i < n; ++i) expected[i] = a[i] + b[i];
        float *da = nullptr, *db = nullptr, *dc = nullptr;
        std::size_t bytes = n * sizeof(float);
        CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&da), bytes));
        CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&db), bytes));
        CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&dc), bytes));
        CUDA_CHECK(cudaMemcpy(da, a.data(), bytes, cudaMemcpyHostToDevice));
        CUDA_CHECK(cudaMemcpy(db, b.data(), bytes, cudaMemcpyHostToDevice));
        CUDA_CHECK(cudaMemcpy(dc, result.data(), bytes, cudaMemcpyHostToDevice));
        const int threads = 256, blocks = (n + threads - 1) / threads;
        vector_add<<<blocks, threads>>>(da, db, dc, n);
        finish_kernel();
        CUDA_CHECK(cudaMemcpy(result.data(), dc, bytes, cudaMemcpyDeviceToHost));
        CUDA_CHECK(cudaFree(da));
        CUDA_CHECK(cudaFree(db));
        CUDA_CHECK(cudaFree(dc));
        check_values(result, expected);
    }
    std::cout << "PASS: vector addition at 9 boundary sizes\n";
}
