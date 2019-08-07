#include "utils/support.h"
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

using namespace Eigen;
namespace py = pybind11;

PYBIND11_MODULE(utils_support, m)
{
  m.doc() = "Python binding module for the utils supporting functions.";

  py::class_<utils::dirtyDerivatived>(m, "dirtyDerivative")
    .def(py::init())
    .def(py::init<py::float_>())
    .def("calculate", &utils::dirtyDerivatived::calculate);

  py::class_<utils::dirtyDerivativeMatd>(m, "dirtyDerivativeMat")
    .def(py::init())
    .def(py::init<MatrixXd>())
    .def("calculate", &utils::dirtyDerivativeMatd::calculate);
}
