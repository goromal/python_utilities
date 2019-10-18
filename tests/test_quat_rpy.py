#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

import numpy as np
from utils_quat import from_euler, Identity
from utils_xform import Xform
from transform_plotting import mesh_plotter_3D
from math import pi
import os

PWD = os.path.dirname(os.path.abspath(__file__))

r = pi
p = pi/4
y = pi/2

# r = 2.896614
# p = 1.570796
# y = 1.107149

quat = from_euler(r, p, y)
print('roll: %f, pitch: %f, yaw: %f' % (quat.roll(), quat.pitch(), quat.yaw()))

T_0_X = np.zeros((7, 2))
T_0_X[:,0] = Xform([0, 0, 0], quat).elements()
T_0_X[:,1] = Xform([0, 0, 0], quat).elements()
T_0_X0 = np.zeros((7, 2))
T_0_X0[:,0] = Xform([0,0,0],Identity()).elements()
T_0_X0[:,1] = Xform([0,0,0],Identity()).elements()

meshfile = os.path.join(PWD,'..','meshes','axes.json')
meshfile2 = os.path.join(PWD,'..','meshes','dashed_axes.json')
plotter = mesh_plotter_3D(title='Euler Tests',xlim=[-1.5,1.5],ylim=[-1.5,1.5],zlim=[-1.5,1.5])
plotter.add_mesh(meshfile2, T_0_X0)
plotter.add_mesh(meshfile, T_0_X)
plotter.animate()
