#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

from utils_quat import from_axis_angle as quat_from_aa
from utils_quat import from_euler
from utils_xform import Xform, Identity, Random, exp, log
from math import pi, sqrt
import numpy as np

print('==== TEST INITIALIZATION AND PRINT FUNCTIONS ====')
xf1 = Xform()
print('Initialized raw:', xf1)
xf2 = Xform([2, 1, 2], quat_from_aa([1, 0, 1], pi/2))
print('Initialized from t and q:', xf2)
e2 = xf2.elements()
xf3 = Xform(e2) # QUAT AND XFORM: DO NOT ATTEMPT TO INSERT THE .ELEMENTS() FUNCTION
                # INSIDE THE INITIALIZER--YOU GET A ZERO 1st ENTRY!
print('Initialized from elements:', xf3)
xf4 = Xform([2, 1, 2], quat_from_aa([1, 0, 1], pi/2).R())
print('Initialized from t and R:', xf4)

print('==== TEST GETTERS AND SETTERS ====')
xf1 = Xform()
xf1.sett([1, 2, 3])
xf1.setq(quat_from_aa([1, 0, 0], pi/2))
print('t and q from setting:', xf1.t(), xf1.q())

print('==== TEST OPERATOR OVERLOADING ====')
print('xf1 =', xf1)
print('xf2 =', xf2)
xf1c = xf1
xf2c = xf2
print('Equals xf1 test:', xf1c)
print('Equals xf2 test:', xf2c)
print('xf1 * xf2 = ', xf1c * xf2c)
xf1c *= xf2c
print('xf1 *= xf2:', xf1c)
xf1c = xf1
xf2m1 = xf2 - xf1
print('xf2 - xf1 =', xf2m1)
print('xf1 + (xf2 - xf1) =', xf1 + xf2m1)
xf1c += xf2m1
print('xf1 += (xf2 - xf1):', xf1c)

print('==== TEST SUPPORTING FUNCTIONS ====')
print('xf1 =', xf1)
print('xf2 =', xf2)
print('H1 =\n', xf1.H())
print('xf1 rel. to xf2 =', xf1.relativeTo(xf2))
print('Adj1 =', xf1.Adj())
print('inv(xf1) =', xf1.inverse())
xf1c = xf1
# xf1c.invert() # DOES NOT WORK...SEGMENTATION FAULT
# print('xf1 = xf1.invert():', xf1c)
v = [0, 0, 0]
print('v =', v)
print('H1*v (active) =', xf1.transforma(v))
print('H1*v (passive) =', xf1.transformp(v))
u = [0.5, 0.5, 0.5]
print('u =', u)
print('H1*u (active) =', xf1.transforma(u))
print('H1*u (passive) =', xf1.transformp(u))
print('Identity:', Identity())
print('Random:', Random())
print('log(xf1) =', log(xf1))
print('exp(log(xf1)) =', exp(log(xf1)))

print('==== TEST OTIMES EXPLICITLY ====')
a = Xform([1.0,2.0,-3.0],from_euler(1.0,-2.0,-0.5))
b = Xform([0.5,-0.5,0.0],from_euler(0.2,0.2,0.2))
print('a:', a)
print('b:', b)
print('a * b:', a * b)
print('b * a:', b * a)
""" C++:
tr::Xformd a((Eigen::Vector3d() << 1.0, 2.0, -3.0).finished(), tr::Quatd::from_euler(1.0, -2.0, -0.5));
tr::Xformd b((Eigen::Vector3d() << 0.5, -0.5, 0.0).finished(), tr::Quatd::from_euler(0.2, 0.2, 0.2));
std::cout << "a: " << a << std::endl;
std::cout << "b: " << b << std::endl;
std::cout << "a.otimes(b): " << a.otimes(b) << std::endl;
std::cout << "b.otimes(a): " << b.otimes(a) << std::endl;
----
a: t: [ 1, 2, -3] q: [ 0.559228, 0.068284i, -0.77959j, 0.273572k]
b: t: [ 0.5, -0.5, 0] q: [ 0.986082, 0.0889215i, 0.108755j, 0.0889215k]
a.otimes(b): t: [ 1.02362, 1.67926, -2.37026] q: [ 0.605831, 0.0179863i, -0.689666j, 0.396241k]
b.otimes(a): t: [ 0.457585, 2.09953, -2.69084] q: [ 0.605831, 0.216136i, -0.726175j, 0.242744k]
"""
print('a.q * b.q:', a.q() * b.q())
print('b.q * a.q:', b.q() * a.q())

print()
print('MATRIX COMPARISON TEST')
print()
q1 = from_euler(0,0,pi/2)
t1 = [1, 0, 0]
x1 = Xform(t1, q1)
v1 = np.array([[1/sqrt(2)],[1/sqrt(2)],[0]])
v1_h = np.array([[1/sqrt(2)],[1/sqrt(2)],[0],[0]])
# v1 = np.array([[1],[0],[0]])
# v1_h = np.array([[1],[0],[0],[1]])
print('x1 = Xform([1,0,0],from_euler(0,0,pi/2)) =', x1)
print('v1 =', v1.transpose()[0])
print('x1.transforma(v1) =', x1.transforma(v1))
print('x1.transformp(v1) =', x1.transformp(v1))
print('x1.H =\n', x1.H())
print('x1.H*v1 =', np.dot(x1.H(),v1_h).transpose()[0])
print('inv(x1.Mat)*v1 =', np.dot(np.linalg.inv(x1.H()),v1_h).transpose()[0])
q2 = from_euler(0,pi/4,0)
t2 = [0, 1, 0]
x2 = Xform(t2, q2)
print('x2 = Xform([0,1,0],from_euler(0,pi/4,0)) =', x2)
print('x2.H() * x1.H() * v1 =', np.dot(x2.H(),np.dot(x1.H(),v1_h)).transpose()[0])
print('(x1 * x2).transformp(v1) =', (x1 * x2).transformp(v1))
print('inv(x2.H() * x1.H()) * v1 =', np.dot(np.linalg.inv(np.dot(x2.H(),x1.H())),v1_h).transpose()[0])
print('(x1 * x2).transforma(v1) =', (x1 * x2).transforma(v1))
