#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

from utils_support import dirtyDerivative, dirtyDerivativeMat
import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin
from math import pi

ti = 0.0
tf = 2 * pi
n = 50.0
t = np.linspace(ti, tf, n)
dt = (tf - ti) / n
x1 = cos(t)
x2 = sin(t)
x = np.vstack((x1,x2))
dx1dt = np.zeros(x1.shape)
derivative_x1 = dirtyDerivative()
dxdt = np.zeros(x.shape)
derivative_x = dirtyDerivativeMat()
for idx in range(t.shape[0]):
    dx1dt[idx] = derivative_x1.calculate(x1[idx], dt)
    dxdt[:,[idx]] = derivative_x.calculate(x[:,idx], dt) # << see https://stackoverflow.com/questions/39824700/cant-broadcast-input-array-from-shape-3-1-into-shape-3/39825046

fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(t, x1, 'k-', t, dx1dt, 'r-')
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(t, x[0,:], 'k-', t, dxdt[0,:], 'r-',
         t, x[1,:], 'k--',t, dxdt[1,:], 'r--')
plt.show()
