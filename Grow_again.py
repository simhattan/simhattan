# -*- coding: utf-8 -*-
"""
File: ITERATE_2

Created on Mon Jul 29 18:48:30 2019
This codes adds one more round of iterations where we:
1. grow the city
2. remove one or more policies and see how it affects housing prices

@author: Jason
"""

import Plot
import pandas as pd
import numpy as np
from Agents import agents_constructor
from Gridc import Gridc
from Parameters import Parameters
from Initialize import initialize_model
from Run_sim import run_sim
from Datacollector import dataCollector, agent_dataCollector, cell_dataCollector
from math import floor

# note if city is closed after round 1 it remains closed
def grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = False, height_cap_1 = False, change_costs = False):

    print ("Initiate grow again, ladies and gents")
    gen_run = gen_run + 1
    
    parameters.num_new_workers_old = parameters.num_new_workers
    parameters.num_new_merchants_old = parameters.num_new_workers
    parameters.num_new_offices_old = parameters.num_new_workers
    
    if change_costs:
        parameters.cost_parameter = 4
    
    c = 0
    output_2 = []
    w_data_2 = []
    m_data_2 = []
    o_data_2 = []
    cell_data_2 = []
    
    # Status quo refers to closed city or not, but have option to change other policies
    if keep_status_quo:
        #if Grid.total_vacancy<3*parameters.num_new_workers:
        # was 1.2 and 0.8
        if Grid.total_vacancy< 1.25*(3*parameters.num_new_workers):
            print("Grow_again: Limit agent entry")
            #parameters.num_new_workers = floor(((Grid.total_vacancy-7)/3))
            parameters.num_new_workers = floor(((0.5*Grid.total_vacancy)/3))
            parameters.num_new_merchants = parameters.num_new_workers
            parameters.num_new_offices = parameters.num_new_workers
            print ("Grow again # workers = ", parameters.num_new_workers)
                   
        agents = agents_constructor(gen_run, parameters, extend=True, agents_list=agents)
           
        initialize_model(gen_run, agents, Grid, parameters, grow_pop=True)
    
        """ Height cap restrictions """
        if height_cap_1==False:
            Grid.impose_height_cap(2, parameters, 1000)
            #self.height_cap = float("inf")  

        """ Delete once works
        if height_cap_1: 
            # Comment out if you dont want height restriction, note average of moore 2 
            Grid.impose_height_cap(2, parameters)
            
            #This will impose the height restriction of 7 for all active cells
            #Grid.impose_height_cap(2, parameters, 7)           
        else: 
            Grid.impose_height_cap(2, parameters, 1000)
        """    
        if rent_control_2: 
            run_sim(agents, Grid, parameters, rent_control=True)
        else:
            run_sim(agents, Grid, parameters)
        output_2 = (dataCollector(gen_run, agents, Grid, parameters))
        #worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
        
        #w_data_2.append(worker)
        #m_data_2.append(merchant)
        #o_data_2.append(office)
            
        # to fix do
        # cell_2 =cell_dataCollector(agents, Grid, parameters)
        # then return cell_2
        # then interate append cell_2 to cell_data_2
        #cell_data_2.append(cell_dataCollector(agents, Grid, parameters))
        Plot.plot_distribution(gen_run, agents, parameters, title = 'grow {}.png'.format(c))
        #Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
        Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')
        Plot.plot_3d(Grid)    
    else:
        print ("Getting Rid of Growth Boundary")
        # else is triggered if keep_status_quo is false
        # only to be triggered when round1 is closed and we want to open it
        # is expands the convex hull by d=6
        # which should be open enought be like the open city
        
        #closed_city_points1 = Grid.convex_hull(parameters, closed_city=True)
        #print ("closed city points")
        #print (closed_city_points1)
        #new_points1 = Grid.expansion(np.array(closed_city_points1), 6, parameters)
        #Grid.alternate_grid(new_points1)
        #
        for blocks in range(len(Grid.grid)):   
            Grid.cell[blocks].active = True
        new_points = [ Grid.cell[blocks].position for blocks in range(len(Grid.grid)) if Grid.cell[blocks].active == True]
        Grid.alternate_grid(new_points)
        Grid.update_grid_data
        
        agents = agents_constructor(gen_run, parameters, extend=True, agents_list=agents)
        
        #agent_id = [agents[agent].agent_id for agent in range(len(agents)) ]
        #agent_employers = [agents[agent].employer for agent in range(len(agents)) if agents[agent].type=="Worker"]
        #print("agent id")
        #print(agent_id)
            
        initialize_model(gen_run, agents, Grid, parameters, grow_pop=True)
    
        """ Height cap restrictions """ 
        if height_cap_1==False:
            Grid.impose_height_cap(2, parameters, 1000)
        
        """ Delete once fixed
        if height_cap_1: 
            # Comment out if you dont want height restriction, note average of moore 2 
            Grid.impose_height_cap(2, parameters)
            
            #This will impose the height restriction of 7 for all active cells
            #Grid.impose_height_cap(2, parameters, 7)           
        else: 
            Grid.impose_height_cap(2, parameters, 1000) 
        """
        if rent_control_2:      
            run_sim(agents, Grid, parameters, rent_control=True)
        else:
            run_sim(agents, Grid, parameters)
        output_2 = (dataCollector(gen_run, agents, Grid, parameters))
        #worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
        #w_data_2.append(worker)
        #m_data_2.append(merchant)
        #o_data_2.append(office)
        #cell_data_2.append(cell_dataCollector(agents, Grid, parameters))
        Plot.plot_distribution(gen_run, agents, parameters, title = 'grow {}.png'.format(c))
        #Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
        Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')
        Plot.plot_3d(Grid)
    return  output_2