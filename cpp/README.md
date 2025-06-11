# GPU Utilities

This folder contains optional CUDA-accelerated operations compiled via `pybind11`.

## Build

You need `nvcc`, `pybind11` and a C++ compiler. Compile with:

```bash
nvcc -O2 --compiler-options=-fPIC -shared \
    parallel_add.cu bindings.cpp -o gpu_ops$(python3-config --extension-suffix) \
    -I$(python -m pybind11 --includes)
```

The resulting `gpu_ops` module exposes `vec_add(a, b, c)` for fast vector addition.
