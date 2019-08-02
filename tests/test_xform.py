#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

from utils_quat import from_axis_angle as quat_from_aa
from utils_xform import Xform, Identity, Random, exp, log
from math import pi
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
print('H1 =\n', xf1.Mat())
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
