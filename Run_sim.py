#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: RUN SIM

Created on Sun Jul 29 14:06:51 2018

@author: mary
"""

import timeit
from Auction import auction

num_runs = 5000

start = timeit.default_timer()

def run_sim(agents, Grid, parameters, rent_control=False, closed=False):

    global count
    count = 0 
    for run_num in range(num_runs):         
        # Loop until no one wishes to move
        count += 1
        if count % 10==0:
            print("Run num ", count)
        for agent in range(len(agents)):
            agents[agent].old_location = agents[agent].location
        if not rent_control:
            if not closed:
                auction(agents, Grid, parameters)
            else:
                auction(agents, Grid, parameters, closed=True)
        else:
            if not closed:
                auction(agents, Grid, parameters, rent_control=True)
            else:
                auction(agents, Grid, parameters, rent_control=True, closed=True)
        for block in range(len(Grid.grid)):
            if Grid.cell[block].active:
                Grid.cell[block].rent_lag_vec[run_num % int(parameters.developer_lag_period)] = Grid.cell[block].avg_rent
                Grid.cell[block].tear_down( Grid, agents, parameters)
        if all(agents[agent].old_location == agents[agent].location for agent in range(len(agents))):
            print("Converged after ", count, " periods.")
            Grid.convergence_count = count 
            break
