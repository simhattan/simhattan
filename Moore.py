#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: MOORE 

Created on Sun Jan 21 22:55:13 2018

@author: MarMah
"""

import numpy as np
import random
from random import choice
    
def moore_neighbor(i, j, d, parameters, exclusive = None):
    """
    Finds the moore neighbors around the given point 
    with the given distance. 
    
    Args:
        i: the x (first element) of the point
        j: the y (second element) of the point
        d: the distance that the neighbors are counted
        parameters: an instance of class Parameters
        Exclusive : optional argument that if set equals to True, will
                    return the mooreneighbors of the point by removing 
                    the previous moores calculated before. 
        
    Returns:
        A list of the moore neighbors points around the given [i,j] point. 
    
    """
    f= [x for x in range(i-d, i+d+1)]
    g = [y for y in range(j-d, j+d+1)]
    lst = [ [l,k] for l in f for k in g ]
    t = [[z,m] for [z,m] in lst if [z,m]!= [i,j] ]
    moore =[[i,j] for [i,j] in t if 0 <= i < parameters.grid_width if 0 <= j < parameters.grid_width] 
    if not exclusive:
        return moore
    else: 
        if d>1:     
            p_moores = moore_neighbor(i, j, d-1, parameters)
            moores = [i for i in moore if i not in p_moores]  
            return moores
             
def moore_list(agent, agents, d, parameters, exclusive = None): 
    """
    Finds the  moore neighbors based on agent ID ? 
    with the given distance. 
    
    Args:
        agent: the specific agent we are interested in
        agents: the list of agents 
        d: the distance that the neighbors are counted
        parameters: an instance of class Parameters
        
    Returns:
        A list of the moore neighbors points around agent's location [i,j] point. 
    
    """
    i = [agents[agent].location[0]]
    j = [agents[agent].location[1]]
    if not exclusive: 
        moores= moore_neighbor(i[0], j[0], d, parameters)
    else:
        moores= moore_neighbor(i[0], j[0], d, parameters, exclusive = True)
    return moores 

    
def find_empty(agent, agents, d, Grid, parameters):
    """
    Finds the empty blocks in the moore neighbors of a given agent 
    based on the given d  
    
    Args:
        agent: the agent id
        agents : a list of the instances of the agents in the model
        d: the distance that the neighbors are counted from
        parameters: an instance of class Parameters
        Grid : an instance of class Grid
                    
        
    Returns:
        A list of indices of the empty blocks  
    """
    agent_moore = moore_list(agent, agents, d, parameters)
    agent_moore_index = [Grid.grid.index(moore_points) for moore_points in agent_moore ]
    empty_lots = [block_index for block_index in agent_moore_index if Grid.cell[block_index].occupants == 0 or (Grid.cell[block_index].floors > len(Grid.cell[block_index].occupants)) ]
    if len(empty_lots) == 0:              
           return find_empty(agent, agents, d+1, Grid, parameters) 
    else :
        return empty_lots   
     
def new_closest_block(agent, d, Grid, parameters):
    """
    Finds the closest block for the given agent
    based on the given d  
    Args:
        agent: the agent id
        agents : a list of the instances of the agents in the model
        d: the distance that the neighbors are counted from
        parameters: an instance of class Parameters
        Grid : an instance of class Grid
    Returns:
        A new block in form of [i,j] point. 
    
    """
    # grid is an instance of class Grid
    #parameters is an instance of class Parameters
    
    if d > 7:        
        closest_block = Grid.grid.index(new_block(agent))
    else:    
        empty_lots = find_empty(agent, agents, d, Grid, parameters)                     
        empty_blocks = [Grid.grid[empty] for empty in empty_lots ] 
        if len(empty_lots) == 1 :            
            closest_block = empty_lots[0]                  
        else:
             if any([agents[agent].type == "Worker", agents[agent].type == "Merchant"]):
                 distance_to_work = [agents[agent].calc_block_distance(blocks) for blocks in empty_blocks ]
                 closest_to_work_index = distance_to_work.index(min(distance_to_work))                    
                 closest_block = empty_lots[closest_to_work_index]
             elif  agents[agent].type == "Office":
                 closest_block = choice(empty_lots)
    return  Grid.grid[closest_block]            

def new_block(parameters, Grid):
    """
    Finds a random block for the given agent 
    
    Returns:
        A new random block in form of [i,j] point. 
    
    """
    random_block = random.RandomState(parameters.seed).randint(0, parameters.grid_width* parameters.grid_height)
    if Grid.cell[random_block].availability():
        return Grid.grid[random_block]
    else:
        return new_block(parameters, Grid)
    
def height_cap_fn(block, Grid) :
    # Computes the average height of the moore neighbors of each cell and round it up 
    # grid is an instance of class Grid
    i= Grid[block][0]
    j= Grid[block][1]
    moore = moore_neighbor(i,j,2)
    moore.append([i,j])
    height = [Grid.cell[Grid.grid.index(points).floors] for points in moore]
    height_ar = np.array(height)    
    average_height = int(np.ceil(np.mmean(height_ar)))
    return average_height
             
