#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

from utils_quat import Quat, skew, exp, log, from_R, from_axis_angle, from_euler, from_two_unit_vectors
import utils_quat as uquat
import numpy as np
from math import pi, acos, sqrt

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

print()
print('FROM TWO UNIT VECTORS TESTING')
print()
u = np.array([[0],[1],[2]])
u = u / np.linalg.norm(u)
v = np.array([[1],[1],[2.0]])
v = v / np.linalg.norm(v)
q1 = from_two_unit_vectors(u, v)
theta = acos(np.dot(u.transpose(),v))
print('theta:',theta*180.0/pi)
delta = np.dot(skew(u),v)
delta = delta / np.linalg.norm(delta)
# delta = np.cross(u.transpose()[0],v.transpose()[0])
print('delta:',delta,'norm:',np.linalg.norm(delta))
q2 = exp(theta*delta)
print('q1:', q1)
print('q2:', q2)
print('q1.rota(u) =', q1.rota(u))
print('q2.rota(u) =', q2.rota(u))
print('diff norm:', np.linalg.norm(q1.rota(u)-q2.rota(u)))

print()
print('MATRIX COMPARISON TEST')
print()
q1 = from_euler(0,0,pi/2)
v1 = np.array([[1/sqrt(2)],[1/sqrt(2)],[0]])
print('q1 = from_euler(0,0,pi/2) =', q1)
print('v1 =', v1)
print('q1.rota(v1) =', q1.rota(v1))
print('q1.rotp(v1) =', q1.rotp(v1))
print('q1.R =\n', q1.R())
print('q1.R*v1 =', np.dot(q1.R(),v1).transpose()[0])
print('q1.R\'*v1 =', np.dot(q1.R().transpose(),v1).transpose()[0])
q2 = from_euler(0,pi/4,0)
print('q2 = from_euler(0,pi/4,0) =', q2)
print('q2.R() * q1.R() * v1 =', np.dot(q2.R(),np.dot(q1.R(),v1)).transpose()[0])
print('(q1 * q2).rotp(v1) =', (q1 * q2).rotp(v1))
print('inv(q2.R() * q1.R()) * v1 =', np.dot(np.linalg.inv(np.dot(q2.R(),q1.R())),v1).transpose()[0])
print('(q1 * q2).rota(v1) =', (q1 * q2).rota(v1))
