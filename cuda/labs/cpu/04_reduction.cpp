#include "math.hpp"
#include <numeric>

int main() {
    std::vector<float> values{1, 2, 3, 4, 5, 6, 7, 8};
    const double expected = std::accumulate(values.begin(), values.end(), 0.0);
    for (int stride = 4; stride > 0; stride /= 2) {
        for (int lane = 0; lane < stride; ++lane) values[lane] += values[lane + stride];
        std::cout << "04 Reduction: stride " << stride << ", active results:";
        for (int lane = 0; lane < stride; ++lane) std::cout << ' ' << values[lane];
        std::cout << '\n';
    }
    require(close(values[0], expected), "Tree reduction failed");
    // A legal interleaving of two non-atomic increments loses an update.
    int counter = 0;
    int thread_a = counter, thread_b = counter;
    counter = thread_a + 1;
    counter = thread_b + 1;
    require(counter == 1, "Lost-update illustration failed");
    auto y = softmax_cpu({1000, 1001, 1002, -1000, -1000, -1000}, 2, 3);
    require(close(y[0], 0.09003057317) && close(y[2], 0.66524095577), "Softmax values failed");
    require(close(y[3], 1.0 / 3.0), "Equal logits should have equal probabilities");
    for (int row = 0; row < 2; ++row)
        require(close(y[row * 3] + y[row * 3 + 1] + y[row * 3 + 2], 1), "Row sum failed");
    require(!close(std::numeric_limits<float>::quiet_NaN(), 0), "NaN must fail validation");
    std::cout << "PASS: reduction, lost-update example, and stable softmax\n";
}
