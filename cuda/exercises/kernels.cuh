#pragma once
#include <cuda_runtime.h>
#include <cmath>

// Implement one exercise at a time. Empty kernels intentionally do no work.
// Outputs begin as NaN, so unfinished exercises fail comparisons visibly.
// Contracts and hints: guide/exercises.md and guide/hints.md.

// E01: one thread owns c[i]. Guard the final partial block.
__global__ void vector_add(const float* a, const float* b, float* c, int n) {
    // TODO
}

// E02: cover all n elements even when the grid has only two blocks.
__global__ void saxpy(const float* x, const float* y, float* out, float alpha, int n) {
    // TODO
}

// E03: power-of-two block size; dynamic shared bytes = blockDim.x*sizeof(float).
// Write one block sum to partial[blockIdx.x]. No early return at the tail.
__global__ void reduce_sum(const float* input, float* partial, int n) {
    // TODO
}

// E04: A[m,k] times B[k,n] gives C[m,n], all contiguous row-major arrays.
__global__ void matmul_naive(const float* a, const float* b, float* c, int m, int k, int n) {
    // TODO
}

// E05: fixed 16x16 blocks; zero-fill partial tiles; two barriers per tile.
__global__ void matmul_tiled(const float* a, const float* b, float* c, int m, int k, int n) {
    // TODO
}

// E06: one block per row; finite input; positive cols; power-of-two block size.
// Dynamic shared bytes = blockDim.x*sizeof(float). Support cols > blockDim.x.
__global__ void softmax_rows(const float* x, float* y, int cols) {
    // TODO
}
