// This enumerates ownership on the CPU. It does NOT simulate GPU scheduling.
#include "math.hpp"

int main() {
    for (int n : {0, 1, 7, 8, 9, 31, 32, 33, 255, 256, 257, 1003}) {
        for (int threads : {1, 4, 32, 128, 256}) {
            int blocks = (n + threads - 1) / threads;
            std::vector<int> writes(n, 0);
            for (int block = 0; block < blocks; ++block)
                for (int thread = 0; thread < threads; ++thread) {
                    int i = block * threads + thread;
                    if (i < n) ++writes[i];
                    if (n == 9 && threads == 4)
                        std::cout << "block=" << block << " thread=" << thread
                                  << " i=" << i << (i < n ? " writes\n" : " skips\n");
                }
            for (int count : writes) require(count == 1, "Missing or duplicate owner");
            // Deliberately few threads; the stride loop must still cover n.
            std::fill(writes.begin(), writes.end(), 0);
            const int grid = 2;
            for (int block = 0; block < grid; ++block)
                for (int thread = 0; thread < threads; ++thread)
                    for (int i = block * threads + thread; i < n; i += grid * threads)
                        ++writes[i];
            for (int count : writes) require(count == 1, "Grid-stride ownership failed");
        }
    }
    std::cout << "PASS: indexing covers every element exactly once (including empty input)\n";
}
