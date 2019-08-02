#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

from utils_quat import Quat, skew, exp, log, from_R, from_axis_angle, from_euler, from_two_unit_vectors
import utils_quat as uquat
import numpy as np
from math import pi

quat1 = Quat()
quat1.setW(1.0)
quat1.setX(0.0)
quat1.setY(0.0)
quat1.setZ(1.0)
print(quat1)
print(quat1.elements())
q = Quat(quat1.elements())
print(q)
e = quat1.elements()
q = Quat(e)
print(q)
quat1.normalize()
print(quat1)
quat1.invert()
print(quat1)
quat1inv = quat1.inverse()
print(quat1inv)
print(quat1.R())

quat2 = from_axis_angle([1, 0, 1], pi/2)
print(quat2)

quat3 = from_euler(pi/4, pi/2, -1)
print(quat3)
print('roll: %f, pitch: %f, yaw: %f' % (quat3.roll(), quat3.pitch(), quat3.yaw()))
print('euler:', quat3.euler())
print('probably want to fix that like it is in matlab_utilities...')

quat4 = from_two_unit_vectors([1,0,0],[0,1,0])
print(quat4, quat4.euler())

quat5 = uquat.Identity()
print(quat5)

quat6 = uquat.Random()
print(quat6)

quat5t6 = quat5 * quat6
print(quat5t6)

quat4t6 = quat4 * quat6
print(quat4t6)

quat4 = quat6
print(quat4)

quat5 *= quat6
print(quat5)

q3mq2 = quat3 - quat2
print(q3mq2)
print(quat2 + q3mq2)
quat2 += q3mq2
print(quat2)
print(quat3)

print()
print('Lie testing:')
print()
print(quat3.R())
q = from_R(quat3.R())
print(q)
print(log(q))
print(skew(log(q)))
print(exp(log(q)))
print(from_euler(0.0, pi, 0.0).rotp([1, 0, 0]))
