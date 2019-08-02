#include "utils/logging.h"
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

using namespace Eigen;

namespace logging_bridge {

MatrixXd logToMatrix(const std::string &filename, int rowSize)
{
  MatrixXd dataMatrix;
  logging::logToMatrix(filename, dataMatrix, rowSize);
  return dataMatrix;
}

} // end namespace logging_bridge

namespace py = pybind11;

PYBIND11_MODULE(utils_logging, m)
{
  m.doc() = "Python binding module for utils logging functionality.";
  m.def("matrixToLog", &logging::matrixToLog);
  m.def("logToMatrix", &logging_bridge::logToMatrix);
}
