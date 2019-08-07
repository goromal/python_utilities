#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

import numpy as np
import utils_logging as logging
from utils_xform import Xform
from utils_quat import from_axis_angle
from transform_plotting import mesh_plotter_3D
from math import pi
import os

PWD = os.path.dirname(os.path.abspath(__file__))

# Transform from UAV body frame to NED inertial frame
T_UAV_NED = logging.logToMatrix('pronav_uav_states.log', 7)
T_UAV_NED = T_UAV_NED[:, ::15]

# Transform from NED inertial frame to plotting frame
T_NED_0 = Xform([0, 0, 0], from_axis_angle([1, 0, 0], pi))

# Transform from UAV body frame to plotting frame
# (robotics convention from frame of interest to plotting frame -> ready to animate!)
n = T_UAV_NED.shape[1]
T_UAV_0 = np.zeros(T_UAV_NED.shape)
for i in range(0, n):
    T_UAV_0[:, i] = (T_NED_0 * Xform(T_UAV_NED[:, i])).elements()

# Quadrotor animation from T_UAV_0
meshfile = os.path.join(PWD,'..','meshes','quadrotor.json')
plotter = mesh_plotter_3D(title='UAV Animation',xlabel='North',ylabel='West',zlabel='Up')
plotter.add_mesh(meshfile, T_UAV_0)
plotter.animate()
