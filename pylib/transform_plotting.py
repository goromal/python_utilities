#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import utils_xform
from utils_xform import Xform
from utils_quat import from_two_unit_vectors
from utils_quat import Identity as quat_identity
import json

def active_transform_points(transform, orig_points):
    trans_points = np.zeros(orig_points.shape)
    n = orig_points.shape[1]
    for i in range(0, n):
        trans_points[:, i] = transform.transforma(orig_points[:, i])
    return trans_points

# NOTE: this function works with the assumption that mesh arrow definitions start
#       at the origin and have their arrow at +x = 1
def arrow_plot_data_3D(origin, arrow_vector):
    T = np.zeros((7, 1))
    vector_len = np.linalg.norm(arrow_vector)
    T[:3] = origin.reshape(3,1)
    if vector_len > 0:
        T[3:] = from_two_unit_vectors([1, 0, 0], arrow_vector / vector_len).elements().reshape(4,1)
    else:
        T[3:] = quat_identity().elements().reshape(4,1)
    return T, vector_len

class mesh_plotter_3D(object):
    def __init__(self, **kwargs):
        # parse kwargs
        if 'title' in kwargs:
            title = kwargs['title']
        else:
            title = '3D Plot'
        if 'xlim' in kwargs:
            xlim = kwargs['xlim']
        else:
            xlim = [-10.0, 10.0]
        if 'xlabel' in kwargs:
            xlabel = kwargs['xlabel']
        else:
            xlabel = 'X'
        if 'ylim' in kwargs:
            ylim = kwargs['ylim']
        else:
            ylim = [-10.0, 10.0]
        if 'ylabel' in kwargs:
            ylabel = kwargs['ylabel']
        else:
            ylabel = 'Y'
        if 'zlim' in kwargs:
            zlim = kwargs['zlim']
        else:
            zlim = [0.0, 10.0]
        if 'zlabel' in kwargs:
            zlabel = kwargs['zlabel']
        else:
            zlabel = 'Z'
        if 'fig_width_in' in kwargs:
            fig_width_in = kwargs['fig_width_in']
        else:
            fig_width_in = 8
        if 'fig_height_in' in kwargs:
            fig_height_in = kwargs['fig_height_in']
        else:
            fig_height_in = 6
        # initialize class
        self.meshes = []
        self.transforms = []
        self.scales = []
        self.n = -1
        self.fig = plt.figure(figsize=(fig_width_in, fig_height_in))
        self.ax = p3.Axes3D(self.fig) # <<<< ACCESSIBLE TO OUTSIDE <<<< ++ add method for adding lines ++
        self.ax.set_title(title)
        self.ax.set_xlim3d(xlim)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylim3d(ylim)
        self.ax.set_ylabel(ylabel)
        self.ax.set_zlim3d(zlim)
        self.ax.set_zlabel(zlabel)
        self.meshAdded = False
    def add_mesh(self, mesh_json, xform_matrix, scale_factors=None):
        with open(mesh_json, 'r') as meshfile:
            mesh = json.load(meshfile)
        mesh_data = {}
        mesh_data["points"] = []
        mesh_data["lines"] = []
        for obj in mesh["objects"]:
            num_points = int(len(obj["points"])/3)
            # construct points matrix
            points_mat = np.zeros((3, num_points))
            for i in range(0, num_points):
                points_mat[0, i] = obj["points"][3*i]
                points_mat[1, i] = obj["points"][3*i+1]
                points_mat[2, i] = obj["points"][3*i+2]
            # add to mesh_data["points"]
            mesh_data["points"].append(points_mat)
            # add constructed line object to mesh_data["lines"]
            mesh_data["lines"].append(self.ax.plot(points_mat[0,:], points_mat[1,:],
                points_mat[2,:], linestyle=obj["linestyle"],
                linewidth=obj["linewidth"], color=obj["linecolor"])[0])
            # NOTE: supported colors = [blue, green, red, cyan, magenta, yellow,
            #                           black, white]
            #       supported styles = [...]
        self.meshes.append(mesh_data)
        self.transforms.append(xform_matrix)
        if self.n == -1:
            self.n = xform_matrix.shape[1]
        if not scale_factors is None:
            self.scales.append(scale_factors)
        else:
            self.scales.append(np.ones(self.n))
        self.meshAdded = True
    def update_plot(self, i):
        for mesh, transformset, scaleset in zip(self.meshes, self.transforms, self.scales):
            transform = Xform(transformset[:, i])
            scale = scaleset[i]
            for pointset, line in zip(mesh["points"], mesh["lines"]):
                # transform_points, set line data
                tr_points = active_transform_points(transform, scale * pointset)
                line.set_data(tr_points[0:2,:])
                line.set_3d_properties(tr_points[2,:])
    def animate(self):
        if self.meshAdded:
            self.anim = animation.FuncAnimation(self.fig, self.update_plot, self.n, interval=50)
            plt.show()
