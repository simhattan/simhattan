#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: EMPLOYERS 

Created on Thu Jun 28 02:34:48 2018

@author: Mary
"""
import numpy as np
from Moore import moore_list

def assign_employer(gen_run, agents, d, Grid,  parameters, grow_pop=False) :
    """
    Assing workers to the nearest employer

    Args:
        agents: the list of agents defined in  the model

        d: the distance that the moore neighbors are counted from
        parameters: an instance of class Parameters
        grow_pop: for the closed city format

    """
    if grow_pop:
        # Why workers id???
        #workers_id = [worker for worker in range(len(agents)) if agents[worker].generation == 1 if
        #              agents[worker].type == 'Worker']
        agents_gen = [agents[worker].generation for worker in range(len(agents))]
 
        #print ("gen")
        #print(agents_gen)
        #workers_id = [agents[worker].agent_id for worker in range(len(agents) - parameters.num_new_workers, len(agents))  if agents[worker].type == 'Worker']
        new_workers_id = [agents[worker].agent_id for worker in range(len(agents) - parameters.num_new_workers, len(agents))  if agents[worker].type == 'Worker']
        #print("new workers's id ", new_workers_id)
        #print("new employers id ", [agents[worker].agent_id for worker in range(len(agents))   if agents[worker].type == 'Office'])
        #for worker in np.random.RandomState(parameters.seed).permutation(workers_id) :
        #    find_employ(worker, agents, d, Grid, parameters, grow_pop=True)
        for worker in np.random.RandomState(parameters.seed).permutation(new_workers_id):
            find_employ(gen_run, worker, agents, d, Grid, parameters, grow_pop=True)
    else:
        for worker in np.random.RandomState(parameters.seed).permutation(
                range(len(agents) - int(parameters.num_of_workers), len(agents))) :
            find_employ(gen_run, worker, agents, d, Grid, parameters)
                    
def find_employ(gen_run, worker, agents, d, Grid, parameters, grow_pop=False):
    """
    Finds an available nearest employer for the given worker 
    This function uses moore_list function to find the moore neighbors 
    for each given worker 
    Args:
        worker : the id of the agent (worker)
        agents: the list of agents defined in  the model
        d: the distance that the moore neighbors are counted from 
        parameters: an instance of class Parameters
    Returns:
        the ID of the employer            
    """
    if d == 1:
        moores = moore_list(worker, agents, d, parameters)
    if d > 1:
        moores = moore_list(worker, agents, d, parameters, exclusive=True)
    if grow_pop:
        #gen_size = int(parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers)
        #print ("gen run in employers", gen_run)
        if gen_run == 1:
            gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers #+ 3*(gen_run-1)*(parameters.num_new_workers)
            #print ("gen size ", gen_size)
        else: 
            gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + 3*parameters.num_new_workers_old
        office_locations = [agents[office].location for office in
                            range(gen_size, gen_size + int(parameters.num_new_offices))]
        #print(office_locations)
        new_offices = [agents[new_offices].agent_id for new_offices in range(gen_size, len(agents)-parameters.num_new_workers - parameters.num_new_merchants) ]    
        #print("new office ", new_offices)
        for location in moores:
            #print("moores")
            #print (moores)
            if location in office_locations :
                #print ("office locattions", office_locations)
                #print ("office locations index ", gen_size + office_locations.index(location))
                #print ("office index", agents[gen_size + office_locations.index(location)].agent_id)
                """ #added this if statement (if doesn't work remove and move tabs back out) """
                if agents[gen_size + office_locations.index(location)].availability  == True:
                    agents[worker].employer_location = location
                    agents[worker].employer = gen_size + office_locations.index(location)
                    agents[gen_size + office_locations.index(location)].employee_index = worker
                    agents[gen_size + office_locations.index(location)].availability = False
                    break
            else:
                continue
            assigned_offices = [agents[worker].employer for worker in range(gen_size, len(agents)) if agents[worker].type =="Worker" ]    
            if sorted(assigned_offices) != new_offices:
                #print (sorted(assigned_offices))
                #print("Danger will robinson")
                #print (list(set(new_offices) - set(assigned_offices) ))
                emps_not_assigned = list(set(new_offices) - set(assigned_offices) )
                for emps in emps_not_assigned:
                    agents[worker].employer_location = agents[emps].location
                    agents[worker].employer = emps
                    agents[emps].employee_index = worker
                    agents[emps].availability = False  
    else:
        office_locations = [agents[i].location for i in range(0, int(parameters.num_of_offices))]
        for i in moores:
            if i in office_locations:
                if agents[office_locations.index(i)].availability == True:
                    agents[worker].employer_location = i
                    agents[worker].employer = office_locations.index(i)
                    agents[office_locations.index(i)].employee_index = worker
                    agents[office_locations.index(i)].availability = False
                    break
            else:
                continue
    if agents[worker].employer == -1 and d < parameters.grid_width:
        if grow_pop:
            find_employ(gen_run, worker, agents, d + 1, Grid, parameters, grow_pop=True)
        else:
            find_employ(gen_run, worker, agents, d + 1, Grid, parameters)
        # find_employ(worker, agents, d+1, Grid, parameters)
    return agents[worker].employer
