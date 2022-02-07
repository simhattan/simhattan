#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: ITERATE

Created on Wed Sep 19 18:27:12 2018

@author: mary
"""

#import os
from math import floor
import Plot
import pandas as pd
import numpy as np
from Grow_again import grow_again_fn
from Agents import agents_constructor
from Gridc import Gridc
from Parameters import Parameters
from Initialize import initialize_model
from Run_sim import run_sim
from Datacollector import dataCollector, agent_dataCollector, cell_dataCollector

def iterate(a, gen_run, policy_num,  parameters, p, base= False, closed=False, base_grow=False, 
            rent_control_0 = False, rent_control_1 = False,  height_cap = False, grow_again = False): 
    """
        this function feeds the parameters into the model 
        to do multiple runs over different parameters and 
        record the results in a csv file
        Args:
            parameters: an instance of class parameters
            p: the set of data to set values accordingly
            closed: pass this to get the new data for the closed city
        :returns
        writes the colleceted data to a csv file

    """
    c = 0
    
    output_data_0 = []
    output_data_1 = []
    output_data_2 = []
    
    w_data = []
    m_data = []
    o_data = []

    cell_data_0 = []
    cell_data_1 = []
   
    while c < len(p):
        if a==0:
            parameters.setter(p.iloc[c,0], p.iloc[c,1], p.iloc[c, 2], p.iloc[c, 3], p.iloc[c, 4], p.iloc[c, 5])
        Grid = Gridc(Parameters().grid_height, Parameters().grid_width, Parameters(), Parameters())
        agents = agents_constructor(gen_run, parameters)

        for cell in range(len(Grid.cell)):
            Grid.cell[cell].reset(parameters)

        for agent in range(len(agents)):
            agents[agent].reset(agent, parameters)
                        
        if base:
            print('Base City', "Run Num ", c+1, "out of ", len(p))
            print("Num agents =", 3*parameters.num_of_workers)
            initialize_model(gen_run, agents, Grid, parameters)
            if rent_control_0: 
                run_sim(agents, Grid, parameters, rent_control=True)
            else:
                run_sim(agents, Grid, parameters)
            Plot.plot_distribution(gen_run, agents, parameters, title = 'Base city {}.png'.format(c))
            #Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
            Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')
            Plot.plot_3d(Grid)
            output_data_0.append(dataCollector(gen_run, agents, Grid, parameters))
            worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
            w_data.append(worker)
            m_data.append(merchant)
            o_data.append(office)
            cell_data_0.append(cell_dataCollector(agents, Grid, parameters))
        
        if base_grow:
            print('Base City', "Run Num ", c+1, "out of ", len(p))
            initialize_model(gen_run, agents, Grid, parameters)
            # Note: I turned off rent control here, since I would never use it in open city case
            #if rent_control: 
            #   run_sim(agents, Grid, parameters, rent_control=True) 
            #else:
            run_sim(agents, Grid, parameters)
            Plot.plot_distribution(gen_run, agents, parameters, title = 'base city {}.png'.format(c))
            #Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
            Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')
            Plot.plot_3d(Grid)
            output_data_0.append(dataCollector(gen_run, agents, Grid, parameters))
            worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
            w_data.append(worker)
            m_data.append(merchant)
            o_data.append(office)
            cell_data_0.append(cell_dataCollector(agents, Grid, parameters))
            
            print('only grow')
            gen_run = gen_run + 1
            agents = agents_constructor(gen_run, parameters, extend=True, agents_list=agents)
            print("# agents ", len(agents))
            initialize_model(gen_run, agents, Grid, parameters, grow_pop=True)
            
            """ Height cap restrictions """
            if height_cap:
                print ("height cap is on")
                 # Comment out if you dont want height restriction, note average of moore 2 
                #Grid.impose_height_cap(2, parameters)
                #This will impose the height restriction of 7 for all active cells
                Grid.impose_height_cap(2, parameters, 7)           
            
            """ rent control """
            if rent_control_1: 
                run_sim(agents, Grid, parameters, rent_control=True)
            else:
                run_sim(agents, Grid, parameters)
            output_data_1.append(dataCollector(gen_run, agents, Grid, parameters))
            worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
            w_data.append(worker)
            m_data.append(merchant)
            o_data.append(office)
            cell_data_1.append(cell_dataCollector(agents, Grid, parameters))
            Plot.plot_distribution(gen_run, agents, parameters, title = 'grow {}.png'.format(c))
            #Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
            Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')
            Plot.plot_3d(Grid)

        if closed:
            print('closed city')
            closed_city_points = Grid.convex_hull(parameters, closed_city=True)
            new_points = Grid.expansion(np.array(closed_city_points), 0, parameters)
            Grid.alternate_grid(new_points)
            Grid.update_grid_data
            gen_run = gen_run + 1
            """ height cap option """
            # Comment out if you dont want height restriction 
            if height_cap:
                Grid.impose_height_cap(2, parameters)
            
            #This will impose the height restriction of 7 for all active cells
            #Grid.impose_height_cap(2, parameters, 7)

            #print ("vacant units",Grid.total_vacancy, "num new agents ",3*parameters.num_new_workers )
            if Grid.total_vacancy< 1.25*(3*parameters.num_new_workers):
                #print ("vacant units",Grid.total_vacancy, "num agents ",3*parameters.num_new_workers )
                print("Grow Closed: Limit agent entry")
                #parameters.num_new_workers = floor(((Grid.total_vacancy-7)/3))
                parameters.num_new_workers = floor(((.5*Grid.total_vacancy)/3))  #.8
                parameters.num_new_merchants = parameters.num_new_workers
                parameters.num_new_offices = parameters.num_new_workers
                print ("vacant units",Grid.total_vacancy, "num new agents again ",3*parameters.num_new_workers )
            agents = agents_constructor(gen_run, parameters, extend=True, agents_list=agents)
            
            initialize_model(gen_run, agents, Grid, parameters, grow_pop=True, cc_points=np.array(closed_city_points))
            if rent_control_1:
                run_sim(agents, Grid, parameters, closed=True, rent_control = True)
            else:
                run_sim(agents, Grid, parameters, closed=True) 
            Plot.plot_distribution(gen_run, agents, parameters, pplot=np.array(Grid.active_grid), plot=True, title= 'closed {}.png'.format(c) )
            #Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
            Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')
            Plot.plot_3d(Grid)
            output_data_1.append(dataCollector(gen_run, agents, Grid, parameters))
            worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
            w_data.append(worker)
            m_data.append(merchant)
            o_data.append(office)
            cell_data_1.append(cell_dataCollector(agents, Grid, parameters))
        
        if grow_again:
            # here we need to pass to closed whatever is in second Round gen_run 1
            # if gen_run=1 is closed then pass true here
            # this will then set grow_again to admit min(# new agents, # vacant slots)
            #def grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control = False)        

            if policy_num == 1000:
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True)        
               output_data_2.append(output_2)
               
            elif policy_num == 1001:
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = False)        
               output_data_2.append(output_2)  
              
            elif policy_num == 1002:
                # CLosed closed not caps 
               #output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = False)        
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True)        
               output_data_2.append(output_2)  

            elif policy_num == 1005:
                # CLosed and height cap, remove both
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = False, height_cap_1 = False)        
               output_data_2.append(output_2)  

            elif policy_num == 1010:
               #1010: Base, Full monty, keep full monty
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = True, height_cap_1 = True)        
               output_data_2.append(output_2)  
                     
            elif policy_num == 1012:
               #1012: Base, Full monty, open and keep RC&HC 
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = False, rent_control_2 = True, height_cap_1 = True)        
               output_data_2.append(output_2)  

            elif policy_num == 1014:
               #1014: Base, Full monty, keep closed and no RC&HC
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = False, height_cap_1 = False)        
               output_data_2.append(output_2)  

            elif policy_num == 1016:
               #1016  Base, Full monty, keep closed and keep RC get rid of HC
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = True, height_cap_1 = False)        
               output_data_2.append(output_2)  

            elif policy_num == 1018:
               #1016  Base, Full monty, get rid RC Keep HC
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = False, height_cap_1 = True)        
               output_data_2.append(output_2)  
  
            elif policy_num == 1020:
               #1016  Base, Full monty, get rid of all
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = False, rent_control_2 = False, height_cap_1 = False)        
               output_data_2.append(output_2)  

            elif policy_num == 1022:
               #1016  Base, Full monty, get rid of all and set costs to 4
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = False, rent_control_2 = False, height_cap_1 = False, change_costs = True)        
               output_data_2.append(output_2)  

            elif policy_num == 1024:
               #1016  Base, Full monty, get rid of all and set costs to 4
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = True, height_cap_1 = False, change_costs = True)        
               output_data_2.append(output_2)  

            elif policy_num == 1026:
               #1016  Base, Full monty, keep all costs to 4
               output_2 = grow_again_fn(gen_run, agents, Grid, parameters, p, keep_status_quo = True, rent_control_2 = True, height_cap_1 = True, change_costs = True)        
               output_data_2.append(output_2)  

        gen_run = 0
        c += 1
        #Plot.plot_distribution(gen_run, agents, parameters, pplot=np.array(Grid.active_grid), plot=True, title= 'closed {}.png'.format(c) )
    
    """
    # Make a master output file 
    """
    result = pd.concat(output_data_0)
    writer = pd.ExcelWriter('simoutput_0.xlsx', engine='xlsxwriter') 
    result.to_excel(writer, "output")
    writer.save()

    writer_1 = pd.ExcelWriter('cells_overiew_0.xlsx', engine='xlsxwriter')
    pd.concat(cell_data_0).to_excel(writer_1, "Cells")
    writer_1.save()
            
    agnt_w = pd.concat(w_data, sort=False)   
    agnt_m = pd.concat(m_data, sort=False)
    agnt_o = pd.concat(o_data, sort=False)
        
    writer_2 = pd.ExcelWriter('agent_overiew_0.xlsx', engine='xlsxwriter') 
    agnt_w.to_excel(writer_2, "workers")
    agnt_m.to_excel(writer_2, "merchants")
    agnt_o.to_excel(writer_2, "offices")
    writer_2.save()        
    
    if base_grow | closed:
        
        result = pd.concat(output_data_1)
        writer = pd.ExcelWriter('simoutput_1.xlsx', engine='xlsxwriter')
        result.to_excel(writer, "Output 1")
        writer.save()

        agnt_w = pd.concat(w_data)   
        agnt_m = pd.concat(m_data)
        agnt_o = pd.concat(o_data)
        
        writer_1 = pd.ExcelWriter('agent_overiew_1.xlsx', engine='xlsxwriter') 
        agnt_w.to_excel(writer_1, "workers")
        agnt_m.to_excel(writer_1, "merchants")
        agnt_o.to_excel(writer_1, "offices")
        writer_1.save()

        writer_2 = pd.ExcelWriter('cells_overiew_1.xlsx', engine='xlsxwriter')
        pd.concat(cell_data_1).to_excel(writer_2, "Cells 1")
        writer_2.save()


    if grow_again:
        
        result = pd.concat(output_data_2)
        writer = pd.ExcelWriter('simoutput_2.xlsx', engine='xlsxwriter')
        result.to_excel(writer, "output 2")
        writer.save()

    