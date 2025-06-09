#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

void launch_vec_add(const float* a, const float* b, float* c, int n);

namespace py = pybind11;

void vec_add_py(py::array_t<float> a, py::array_t<float> b, py::array_t<float> c) {
    int n = a.size();
    launch_vec_add(a.data(), b.data(), c.mutable_data(), n);
}

PYBIND11_MODULE(gpu_ops, m) {
    m.def("vec_add", &vec_add_py, "Vector addition on GPU");
}
