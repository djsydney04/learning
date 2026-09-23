#include "common.cuh"

__global__ void write_answer(int* answer) {
    *answer = 42;
}

int main() {
    int host_answer = 0;
    int* device_answer = nullptr;
    CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&device_answer), sizeof(int)));
    CUDA_CHECK(cudaMemcpy(device_answer, &host_answer, sizeof(int), cudaMemcpyHostToDevice));
    write_answer<<<1, 1>>>(device_answer);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    CUDA_CHECK(cudaMemcpy(&host_answer, device_answer, sizeof(int), cudaMemcpyDeviceToHost));
    CUDA_CHECK(cudaFree(device_answer));
    require(host_answer == 42, "Kernel did not write 42");
    std::cout << "PASS: first kernel wrote " << host_answer << '\n';
}
