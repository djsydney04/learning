#include "common.cuh"
#include "kernels.cuh"
#include <numeric>

int main() {
    for (int threads : {32, 128, 256}) {
        for (int n : {1, 31, 32, 33, 255, 256, 257, 1003, 65537}) {
            auto input = pattern(n);
            // Include a non-dyadic fraction; reference accumulates in double.
            for (int i = 0; i < n; ++i) input[i] += 0.01f;
            int blocks = (n + threads - 1) / threads;
            DeviceBuffer x(n), partial(blocks);
            x.upload(input); partial.poison();
            reduce_sum<<<blocks, threads, threads * sizeof(float)>>>(x.data, partial.data, n);
            finish_kernel();
            auto sums = partial.download();
            for (int block = 0; block < blocks; ++block) {
                int begin = block * threads, end = std::min(begin + threads, n);
                double expected = std::accumulate(input.begin() + begin, input.begin() + end, 0.0);
                require(close(sums[block], expected, 2e-4, 2e-5), "Block reduction mismatch");
            }
            // Complete the reduction on the host; this is intentionally a hybrid lab.
            double got = std::accumulate(sums.begin(), sums.end(), 0.0);
            double expected = std::accumulate(input.begin(), input.end(), 0.0);
            require(close(got, expected, 2e-4 * blocks, 2e-5), "Total reduction mismatch");
        }
    }
    std::cout << "PASS: every block partial and total, across 3 block sizes\n";
}
