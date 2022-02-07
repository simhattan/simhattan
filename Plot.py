#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: PLOT

Created on Tue Jul 31 12:57:49 2018

@author: mary

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.spatial import ConvexHull
from matplotlib.path import Path
from numpy import transpose
from mpl_toolkits.mplot3d import axes3d

plt.isinteractive()

#Plot to show different generatins
def plot_distribution(gen_run, agents, parameters, pplot=None, plot=False, title = None):
    
    for gens in range(gen_run+1):
    # Plot the distribution of agents after cycle_num rounds of the loop
        x_values_m, y_values_m = {a : [] for a in range(gen_run+1)}, {a : [] for a in range(gen_run+1)}
        x_values_w, y_values_w = {a : [] for a in range(gen_run+1)}, {a : [] for a in range(gen_run+1)}
        x_values_o, y_values_o = {a : [] for a in range(gen_run+1)}, {a : [] for a in range(gen_run+1)}
        
    # Obtain locations of each type
    for gens in range(gen_run+1):
        for agent in range(len(agents)):
            if all([agents[agent].type == "Worker" , agents[agent].generation == gens]):
                x_values_w[gens].append(agents[agent].location[0])
                y_values_w[gens].append(agents[agent].location[1])
            elif all([agents[agent].type == "Merchant" , agents[agent].generation == gens]):
                x_values_m[gens].append(agents[agent].location[0])
                y_values_m[gens].append(agents[agent].location[1])
            elif all([agents[agent].type == "Office", agents[agent].generation == gens]):
                x_values_o[gens].append(agents[agent].location[0])
                y_values_o[gens].append(agents[agent].location[1])

    fig, ax = plt.subplots()
    plot_args = {'markersize' : 10, 'alpha' : 0.6}
    # Colors: orange, red, blue, cyan, magenta, yellow, bblack
    for gen in range(gen_run+1): 
        if gen==0:
            ax.plot(x_values_o[gen], y_values_o[gen], 'o', markerfacecolor='orange', label = 'Office_0', **plot_args)
            ax.plot(x_values_m[gen], y_values_m[gen], 'o', markerfacecolor='red', label = 'Owner_0', **plot_args)
            ax.plot(x_values_w[gen], y_values_w[gen], 'o', markerfacecolor='blue', label = 'Worker_0', **plot_args)

        if gen==1:
            ax.plot(x_values_o[gen], y_values_o[gen], 'D', markerfacecolor='orange', label = 'Office_1', **plot_args)
            ax.plot(x_values_m[gen], y_values_m[gen], 'D', markerfacecolor='red', label = 'Owner_1', **plot_args)
            ax.plot(x_values_w[gen], y_values_w[gen], 'D', markerfacecolor='blue', label = 'Worker_1', **plot_args)

        if gen==2:
            ax.plot(x_values_o[gen], y_values_o[gen], 's', markerfacecolor='orange', label = 'Office_2', **plot_args)
            ax.plot(x_values_m[gen], y_values_m[gen], 's', markerfacecolor='red', label = 'Owner_2', **plot_args)
            ax.plot(x_values_w[gen], y_values_w[gen], 's', markerfacecolor='blue', label = 'Worker_2', **plot_args)

    plt.xlim( (-1, parameters.grid_width) )
    plt.ylim( (-1, parameters.grid_height) )
    #ax.legend(loc='lower left', numpoints = 1)
    ax.legend(loc='best', numpoints = 1)
    #  x.set_title('City Map') FIXXXXXXXXXXXXXXXXXx
    if title:
        plt.show()
    
    if plot:
        expanded = np.array(pplot)
        hull1 = ConvexHull(expanded)
        hull_path = Path(expanded[hull1.vertices])
        plt.plot(expanded[:, 0], expanded[:, 1], 'o')
        for simplex in hull1.simplices :
            plt.plot(expanded[simplex, 0], expanded[simplex, 1], 'r--', lw=3)

        plt.plot(expanded[hull1.vertices, 0], expanded[hull1.vertices, 1], 'r--', lw=3)
        plt.plot(expanded[hull1.vertices[0], 0], expanded[hull1.vertices[0], 1], 'ro')
        plt.axis([0, parameters.grid_height, 0, parameters.grid_height])

        plt.show()
    
def heat_map(data, parameters, graph_type):

    if graph_type == 'property':
        title = 'Property Value Heat Map'
        file_name = ("Figures"+'Property.png')
        file_name = parameters.output_path+ 'Property.png'

    elif graph_type == 'height':
        title = 'Building Height Heat Map'
        file_name = (parameters.output_path+'Height.png')

    # Make plot with vertical (default) colorbar
    fig, ax = plt.subplots()

    cax = ax.imshow(data, interpolation='nearest', cmap=cm.Reds)
    ax.set_title(title)
    ax.invert_yaxis()

    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    cbar = fig.colorbar(cax, ticks=[data.min(), 0, data.max()])

    #fig.savefig(file_name)
    plt.show()
    
    
def height_mat(Grid, parameters):
    height = [Grid.cell[i].num_rented_units for i in range(len(Grid.cell))]
    return np.array([height]).reshape(parameters.grid_height, parameters.grid_width)

def structure_height_mat(Grid, parameters):
    height = [Grid.cell[i].floors for i in range(len(Grid.cell))]
    return np.array([height]).reshape(parameters.grid_height, parameters.grid_width)    

def plot_3d(Grid):
    xs = transpose(Grid.grid)[0]
    ys = transpose(Grid.grid)[1]
    Grid_floors = [Grid.cell[block].floors for block in range(len(Grid.grid))]
    zsz = [0]*len(xs)

    dx = [1]*len(xs)
    dy = dx
    dz = Grid_floors
    
    fig = plt.figure()   
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.view_init(elev=10, azim=-40)
    ax1.dist = 7  
    ax1.bar3d(xs,ys,zsz, dx, dy, dz, color = '#C1CDCD')
    ax1.set_xlabel('x axis')
    ax1.set_ylabel('y axis')
    ax1.set_zlabel('Builing Height')
    ax1.grid(False)
    ax1.axis('off')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    plt.show()
    
    #"""
    fig = plt.figure()
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.view_init(elev=18, azim=-10)
    ax2.dist = 7
    ax2.bar3d(xs,ys,zsz, dx, dy, dz, color = '#8B7D6B')
    ax2.grid(False)
    ax2.axis('off')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_zticks([])
    plt.show()
   # """
 