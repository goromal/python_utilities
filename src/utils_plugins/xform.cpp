#include "utils/xform.h"
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <sstream>

using namespace Eigen;
namespace py = pybind11;

PYBIND11_MODULE(utils_xform, m)
{
  m.doc() = "Python binding module for the utils xform class.";

  py::class_<transforms::Xformd>(m, "Xform")
    .def(py::init())
    .def(py::init<const Ref<const Matrix<double,7,1>>>())
    .def(py::init<const Matrix<double,3,1>, const transforms::Quatd>())
    .def(py::init<const Matrix<double,3,1>, const Matrix<double,3,3>>())
    .def("t", &transforms::Xformd::t)
    .def("q", &transforms::Xformd::q)
    .def("sett", &transforms::Xformd::sett)
    .def("setq", &transforms::Xformd::setq)
    .def(py::self * py::self)
    .def(py::self + Matrix<double,6,1>())
    .def(py::self - py::self)
    .def("elements", &transforms::Xformd::elements)
    .def("H", &transforms::Xformd::H)
    .def("relativeTo", &transforms::Xformd::relativeTo)
    .def("Adj", &transforms::Xformd::Adj)
    .def("inverse", &transforms::Xformd::inverse)
    .def("transforma", &transforms::Xformd::transforma)
    .def("transformp", &transforms::Xformd::transformp)
    .def("invert", &transforms::Xformd::invert)
    .def("__repr__",
      [](const transforms::Xformd &t) {
        std::stringstream ss;
        ss << t;
        return ss.str();
      }
    );

    m.def("Identity", &transforms::Xformd::Identity);
    m.def("Random", &transforms::Xformd::Random);
    m.def("exp", &transforms::Xformd::exp);
    m.def("log", &transforms::Xformd::log);
}
