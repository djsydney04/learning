#include "common.cuh"
#include "kernels.cuh"
#include <array>

int main(int argc, char** argv) {
    std::string mode = argc == 2 ? argv[1] : "both";
    require(argc <= 2 && (mode == "both" || mode == "naive" || mode == "tiled"),
            "Usage: 05_matmul [naive|tiled|both]");
    for (auto shape : {std::array<int, 3>{1, 1, 1}, {2, 3, 4}, {16, 16, 16},
                       {17, 19, 23}, {31, 7, 33}, {32, 33, 15}}) {
        int m = shape[0], k = shape[1], n = shape[2];
        auto a = pattern(m * k), b = pattern(k * n, 23);
        auto expected = matmul_cpu(a, b, m, k, n);
        DeviceBuffer da(a.size()), db(b.size()), dc(m * n);
        da.upload(a); db.upload(b);
        dim3 threads(16, 16), blocks((n + 15) / 16, (m + 15) / 16);
        if (mode != "tiled") {
            dc.poison();
            matmul_naive<<<blocks, threads>>>(da.data, db.data, dc.data, m, k, n);
            finish_kernel();
            check_values(dc.download(), expected, 1e-4, 1e-4);
        }
        if (mode != "naive") {
            dc.poison();
            matmul_tiled<<<blocks, threads>>>(da.data, db.data, dc.data, m, k, n);
            finish_kernel();
            check_values(dc.download(), expected, 1e-4, 1e-4);
        }
    }
    std::cout << "PASS: " << mode << " matrix multiplication, 6 rectangular/tail shapes\n";
}
