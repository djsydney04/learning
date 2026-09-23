#include "common.cuh"
#include "kernels.cuh"

int main() {
    for (int n : {1, 255, 256, 257, 1003, 65537}) {
        auto x = pattern(n), y = pattern(n, 23);
        DeviceBuffer dx(n), dy(n), out(n);
        dx.upload(x); dy.upload(y);
        for (float alpha : {0.0f, -2.0f, 0.125f}) {
            out.poison();
            saxpy<<<2, 128>>>(dx.data, dy.data, out.data, alpha, n);
            finish_kernel();
            std::vector<float> expected(n);
            for (int i = 0; i < n; ++i) expected[i] = alpha * x[i] + y[i];
            check_values(out.download(), expected);
        }
    }
    std::cout << "PASS: SAXPY with a deliberately small grid and 3 scale factors\n";
}
