#include "common.cuh"

int main() {
    int count = 0;
    CUDA_CHECK(cudaGetDeviceCount(&count));
    require(count > 0, "No CUDA device available");
    for (int device = 0; device < count; ++device) {
        cudaDeviceProp p{};
        CUDA_CHECK(cudaGetDeviceProperties(&p, device));
        std::cout << "Device " << device << ": " << p.name
                  << "\n  Compute capability: " << p.major << '.' << p.minor
                  << "\n  SMs: " << p.multiProcessorCount << ", warp size: " << p.warpSize
                  << "\n  Max threads per block: " << p.maxThreadsPerBlock
                  << "\n  Shared bytes per block: " << p.sharedMemPerBlock
                  << "\n  Global memory GiB: " << p.totalGlobalMem / (1024.0 * 1024 * 1024) << '\n';
    }
    std::cout << "PASS: CUDA can query a device\n";
}
