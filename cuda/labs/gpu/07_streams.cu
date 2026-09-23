#include "common.cuh"
#include "kernels.cuh"

int main() {
    const int n = 100003, chunk = (n + 1) / 2;
    const std::size_t bytes = n * sizeof(float);
    float *x = nullptr, *y = nullptr, *out = nullptr;
    CUDA_CHECK(cudaMallocHost(reinterpret_cast<void**>(&x), bytes));
    CUDA_CHECK(cudaMallocHost(reinterpret_cast<void**>(&y), bytes));
    CUDA_CHECK(cudaMallocHost(reinterpret_cast<void**>(&out), bytes));
    auto xv = pattern(n), yv = pattern(n, 23);
    for (int i = 0; i < n; ++i) { x[i] = xv[i]; y[i] = yv[i]; out[i] = NAN; }
    DeviceBuffer dx(n), dy(n), dout(n);
    dout.poison();
    // Pageable H2D copies may return after staging, before device DMA finishes.
    // Establish completion before launching work in independent streams.
    CUDA_CHECK(cudaDeviceSynchronize());
    cudaStream_t streams[2];
    for (auto& stream : streams) CUDA_CHECK(cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking));
    for (int part = 0; part < 2; ++part) {
        int offset = part * chunk, count = std::min(chunk, n - offset);
        auto stream = streams[part];
        std::size_t chunk_bytes = count * sizeof(float);
        CUDA_CHECK(cudaMemcpyAsync(dx.data + offset, x + offset, chunk_bytes, cudaMemcpyHostToDevice, stream));
        CUDA_CHECK(cudaMemcpyAsync(dy.data + offset, y + offset, chunk_bytes, cudaMemcpyHostToDevice, stream));
        saxpy<<<(count + 255) / 256, 256, 0, stream>>>(dx.data + offset, dy.data + offset,
                                                    dout.data + offset, 2.0f, count);
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaMemcpyAsync(out + offset, dout.data + offset, chunk_bytes, cudaMemcpyDeviceToHost, stream));
    }
    // Do not read/reuse/free host buffers while queued copies still access them.
    for (auto stream : streams) CUDA_CHECK(cudaStreamSynchronize(stream));
    std::vector<float> expected(n);
    for (int i = 0; i < n; ++i) expected[i] = 2.0f * x[i] + y[i];
    check_values(std::vector<float>(out, out + n), expected);
    for (auto stream : streams) CUDA_CHECK(cudaStreamDestroy(stream));
    CUDA_CHECK(cudaFreeHost(x));
    CUDA_CHECK(cudaFreeHost(y));
    CUDA_CHECK(cudaFreeHost(out));
    std::cout << "PASS: two ordered stream pipelines; actual overlap requires a profiler\n";
}
