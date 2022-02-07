# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: INITIALIZE

Created on Wed Jun 27 14:32:29 2018

@author: mary
"""

from Parameters import Parameters
import numpy as np
from Employers import assign_employer
from Moore import moore_list

def initialize_model(gen_run, agents, Grid, parameters, grow_pop=False, cc_points=None) :
    """
    This function starts the game by randomly assiginig agents to a location,
    randomly assign workers and merchants to an office.  
    
    """

    if gen_run < 2:
        gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers #+ 3*(gen_run-1)*(parameters.num_new_workers)

    else: 
        gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + 3*parameters.num_new_workers_old
        
    if grow_pop:

        d = 1

        available_units = np.array([point for point in range(Parameters().grid_height * Parameters().grid_width)
                                    if Grid.cell[point].active if Grid.cell[point].available_place])
        
        np.random.seed(parameters.seed)

        random_grid = np.random.permutation(np.concatenate([np.repeat(x, Grid.cell[x].vacancy) for x in available_units]))
        
        
        for agent in range(gen_size, len(agents)):
            
            if agents[agent].generation > 0 :
                
                agents[agent].move(Grid.grid[random_grid[len(agents) - agent -1]],
                                   agents[agent].bid_value(agents, Grid.cell[random_grid[len(agents) - agent ]].position, Grid,
                                                           parameters, real_bid=True), Grid, agents, parameters, 1, 1, pop_grow_in=True)

                Grid.cell[random_grid[len(agents) - agent - 1]].calculate_values()
                
    else:
        random_grid = np.array([point for point in np.random.RandomState(parameters.seed).permutation(
            (Parameters().grid_height * Parameters().grid_width))
                               if Grid.cell[point].available_place == True])
        for agent in range(len(agents)) :
            agents[agent].location = Grid.grid[random_grid[agent]]
            Grid.cell[random_grid[agent]].occupants.update({agents[agent].agent_id : 1})

    # assign workers to the nearest employers

    if grow_pop:

        # assign workers to the nearest employers
        assign_employer(gen_run, agents, 1, Grid, parameters, grow_pop=True)
        
        for worker in range(len(agents) - parameters.num_new_workers, len(agents)) :
                        
            agents[worker].wage = agents[agents[worker].employer].profit * parameters.worker_share
            agents[worker].commuting_cost = agents[worker].trans_cost(agents[worker].location,
                                                                      agents[worker].employer_location, parameters)
            agents[worker].reservation_utility = agents[worker].reservation_utility_base * parameters.utility_increment

            # set merchants wages
        for merchant in range(gen_size + parameters.num_new_offices,
                              gen_size + parameters.num_new_offices + parameters.num_new_merchants):
            agents[merchant].office_index = merchant - parameters.num_new_offices
            agents[merchant].office_location = agents[agents[merchant].office_index].location
            agents[merchant - parameters.num_new_offices].merchant_index = merchant
            agents[merchant].wage = agents[agents[merchant].office_index].profit * parameters.merchant_share
            agents[merchant].commuting_cost = agents[merchant].trans_cost(agents[merchant].location, agents[
                agents[merchant].office_index].location, parameters)
            agents[merchant].reservation_utility = agents[
                                                       merchant].reservation_utility_base * parameters.utility_increment
    else :

        # assign workers to the nearest employers
        assign_employer(gen_run, agents, 1, Grid, parameters)
        # set workers wages

        for worker in range(len(agents) - parameters.num_of_workers, len(agents)) :
            agents[worker].wage = agents[agents[worker].employer].profit * Parameters().worker_share
           
            agents[worker].commuting_cost = agents[worker].trans_cost(agents[worker].location,
                                                                      agents[worker].employer_location, parameters)
            agents[worker].reservation_utility = agents[worker].reservation_utility_base * parameters.utility_increment

            # set merchants wages

        for merchant in range(parameters.num_of_offices, parameters.num_of_offices + parameters.num_of_merchants) :
            agents[merchant].office_index = merchant - parameters.num_of_offices
            agents[merchant].office_location = agents[agents[merchant].office_index].location
            agents[merchant - parameters.num_of_offices].merchant_index = merchant
            agents[merchant].wage = agents[agents[merchant].office_index].profit * parameters.merchant_share
            agents[merchant].commuting_cost = agents[merchant].trans_cost(agents[merchant].location, agents[
                agents[merchant].office_index].location, parameters)
            agents[merchant].reservation_utility = agents[
                                                       merchant].reservation_utility_base * parameters.utility_increment

    for agent in range(len(agents)):

        if not grow_pop:
            agents[agent].rent = agents[agent].bid_value(agents, agents[agent].location, Grid, parameters, real_bid=True)
            Grid.cell[random_grid[agent]].collected_rents.update({agents[agent].agent_id : agents[agent].total_rent})
            Grid.cell[random_grid[agent]].num_rented_units += 1
            Grid.cell[random_grid[agent]].calculate_values()
