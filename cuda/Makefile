CXX ?= c++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra -Wpedantic
NVCC ?= nvcc
NVCCFLAGS ?= -O2 -std=c++17 -lineinfo
# Example: make gpu CUDA_ARCH=sm_80. Choose an architecture supported by both
# your GPU and toolkit. Leave empty to use the compiler's default.
CUDA_ARCH ?=
ARCH_FLAG = $(if $(CUDA_ARCH),-arch=$(CUDA_ARCH),)
CPU_LABS = 01_cpu 02_indexing 03_layout 04_reduction
GPU_LABS = 00_device 01_first_kernel 02_vector_add 03_grid_stride 04_reduce 05_matmul 06_timing 07_streams 08_softmax
CPU_BINS = $(addprefix build/cpu/,$(CPU_LABS))
GPU_BINS = $(addprefix build/gpu/,$(GPU_LABS))
LAB ?= 02_vector_add
ARGS ?=

.PHONY: all cpu check-cpu gpu check-gpu check-tools student sanitize help
all: cpu
cpu: $(CPU_BINS)
check-cpu: cpu
	@set -e; for lab in $(CPU_BINS); do ./$$lab; done
build/cpu/%: labs/cpu/%.cpp include/math.hpp
	@mkdir -p build/cpu
	$(CXX) $(CXXFLAGS) -Iinclude $< -o $@
check-tools:
	@command -v $(NVCC) >/dev/null 2>&1 || { echo 'nvcc not found. See guide/00-start.md; make check-cpu works without CUDA.'; exit 1; }
gpu: check-tools $(GPU_BINS)
build/gpu/%: labs/gpu/%.cu include/common.cuh include/math.hpp include/kernels.cuh reference/kernels.cuh | check-tools
	@mkdir -p build/gpu
	$(NVCC) $(NVCCFLAGS) $(ARCH_FLAG) -Iinclude $< -o $@
check-gpu: gpu
	@set -e; for lab in $(GPU_BINS); do ./$$lab; done
# Always compile here so edits to any student exercise are picked up.
student: check-tools
	@case "$(LAB)" in 02_vector_add|03_grid_stride|04_reduce|05_matmul|08_softmax) ;; *) echo 'Choose LAB=02_vector_add, 03_grid_stride, 04_reduce, 05_matmul, or 08_softmax'; exit 1;; esac
	@mkdir -p build/student
	$(NVCC) $(NVCCFLAGS) $(ARCH_FLAG) -DUSE_STUDENT -Iinclude labs/gpu/$(LAB).cu -o build/student/$(LAB)
	./build/student/$(LAB) $(ARGS)
sanitize: gpu
	@command -v compute-sanitizer >/dev/null 2>&1 || { echo 'compute-sanitizer not found in PATH'; exit 1; }
	@set -e; for lab in $(GPU_BINS); do compute-sanitizer --error-exitcode 1 --tool memcheck ./$$lab; done
	@set -e; for lab in 04_reduce 05_matmul 08_softmax; do \
		compute-sanitizer --error-exitcode 1 --tool racecheck ./build/gpu/$$lab; \
		compute-sanitizer --error-exitcode 1 --tool synccheck ./build/gpu/$$lab; \
	done
help:
	@echo 'make check-cpu                 Build and run four CPU learning labs'
	@echo 'make check-gpu                 Build and run the CUDA reference labs'
	@echo 'make student LAB=02_vector_add Build and check your exercise'
	@echo 'make sanitize                  Check reference GPU memory and barriers'
