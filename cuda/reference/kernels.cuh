#pragma once
#include <cuda_runtime.h>
#include <cmath>

__global__ void vector_add(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

__global__ void saxpy(const float* x, const float* y, float* out, float alpha, int n) {
    int start = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
    for (int i = start; i < n; i += stride) out[i] = alpha * x[i] + y[i];
}

// Contract: 1D blocks, power-of-two blockDim.x, blockDim.x*sizeof(float)
// dynamic shared bytes. One input per thread; one partial sum per block.
__global__ void reduce_sum(const float* input, float* partial, int n) {
    extern __shared__ float scratch[];
    int t = threadIdx.x;
    int i = blockIdx.x * blockDim.x + t;
    scratch[t] = i < n ? input[i] : 0.0f;
    __syncthreads();
    for (int stride = blockDim.x / 2; stride > 0; stride /= 2) {
        if (t < stride) scratch[t] += scratch[t + stride];
        __syncthreads();
    }
    if (t == 0) partial[blockIdx.x] = scratch[0];
}

__global__ void matmul_naive(const float* a, const float* b, float* c, int m, int k, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row >= m || col >= n) return; // No block barrier in this kernel.
    float sum = 0.0f;
    for (int inner = 0; inner < k; ++inner) sum += a[row * k + inner] * b[inner * n + col];
    c[row * n + col] = sum;
}

// Contract: exactly dim3(16,16) threads per block; contiguous row-major arrays.
__global__ void matmul_tiled(const float* a, const float* b, float* c, int m, int k, int n) {
    constexpr int tile = 16;
    __shared__ float a_tile[tile][tile];
    __shared__ float b_tile[tile][tile];
    int tx = threadIdx.x, ty = threadIdx.y;
    int row = blockIdx.y * tile + ty, col = blockIdx.x * tile + tx;
    float sum = 0.0f;
    for (int base = 0; base < k; base += tile) {
        a_tile[ty][tx] = (row < m && base + tx < k) ? a[row * k + base + tx] : 0.0f;
        b_tile[ty][tx] = (base + ty < k && col < n) ? b[(base + ty) * n + col] : 0.0f;
        __syncthreads(); // Entire tile is ready before any thread consumes it.
        for (int inner = 0; inner < tile; ++inner) sum += a_tile[ty][inner] * b_tile[inner][tx];
        __syncthreads(); // No thread may replace a tile still in use.
    }
    if (row < m && col < n) c[row * n + col] = sum;
}

// One block per row. Finite inputs, positive cols, power-of-two blockDim.x.
// Dynamic shared storage is blockDim.x*sizeof(float).
__global__ void softmax_rows(const float* x, float* y, int cols) {
    extern __shared__ float scratch[];
    int t = threadIdx.x, row = blockIdx.x;
    float maximum = -INFINITY;
    for (int col = t; col < cols; col += blockDim.x) maximum = fmaxf(maximum, x[row * cols + col]);
    scratch[t] = maximum;
    __syncthreads();
    for (int stride = blockDim.x / 2; stride > 0; stride /= 2) {
        if (t < stride) scratch[t] = fmaxf(scratch[t], scratch[t + stride]);
        __syncthreads();
    }
    maximum = scratch[0];
    __syncthreads(); // Everyone must read the maximum before scratch is reused.
    float total = 0.0f;
    for (int col = t; col < cols; col += blockDim.x) total += expf(x[row * cols + col] - maximum);
    scratch[t] = total;
    __syncthreads();
    for (int stride = blockDim.x / 2; stride > 0; stride /= 2) {
        if (t < stride) scratch[t] += scratch[t + stride];
        __syncthreads();
    }
    total = scratch[0];
    for (int col = t; col < cols; col += blockDim.x)
        y[row * cols + col] = expf(x[row * cols + col] - maximum) / total;
}
