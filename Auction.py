#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: AUCTION

Created on Mon Jul  2 20:50:56 2018

@author: mary
"""
import numpy as np
#import random 


def auction(agents, Grid, parameters, rent_control=False, closed=False):
    """
    """
    # for the outliers
    for agent in range(len(agents)):
        if agents[agent].type != 'Office':
            agents[agent].housing_cost_check
    if not rent_control:
        bidable_blocks = [blocks for blocks in range(len(Grid.grid)) if Grid.cell[blocks].active if Grid.cell[blocks].age >=0]
    else:
        bidable_blocks = [blocks for blocks in range(len(Grid.grid)) if Grid.cell[blocks].active if Grid.cell[blocks].age >= 0 if Grid.cell[blocks].vacancy > 0]

    for block in np.random.RandomState(parameters.seed).permutation(bidable_blocks):
        
        #Landlords decide on the total rent that each agent is offering, which is the rent per floor multiplied by the number of housing demanded 
        if not rent_control:
            bid_list = [agents[agent].bid_value(agents, Grid.grid[block], Grid, parameters) * agents[agent].housing_demand(agents, Grid.grid[block], Grid, parameters)
                        if agents[agent].housing_demand(agents, Grid.grid[block], Grid, parameters) <= Grid.cell[block].floors else 0 for agent in range(len(agents))]
        else:
            bid_list = [agents[agent].bid_value(agents, Grid.grid[block], Grid, parameters) * agents[agent].housing_demand(agents, Grid.grid[block], Grid, parameters)
                        if agents[agent].housing_demand(agents, Grid.grid[block], Grid, parameters) <= Grid.cell[block].vacancy else 0
                        for agent in range(len(agents))]

        Grid.cell[block].num_bids = sum(k>0 for k in bid_list) # Changed 1.25 to 1
        Grid.cell[block].num_successful_bids = sum(k > 1.25*Grid.cell[block].avg_total_rent for k in bid_list)
        max_bid = max(bid_list)
        high_bidder = bid_list.index(max_bid)
        housing_units = agents[high_bidder].housing_demand(agents, Grid.grid[block], Grid, parameters)
       
        #for now if the winner's demand is more, we move to the next block
#        winner_old_grid_index = Grid.grid.index(agents[high_bidder].location)
  
        if max_bid > 0 and Grid.cell[block].num_successful_bids > 0:

            # if rent_control:
            #     if Grid.cell[block].vacancy < housing_units:
            #        print('rentcontrol is not working')

            #if we have vacancy, the agent moves right in
            
            if Grid.cell[block].vacancy >= housing_units:
                agents[high_bidder].move(Grid.cell[block].position, max(bid_list)/housing_units, Grid, agents, parameters, agents[high_bidder].housing, housing_units)
                Grid.cell[block].calculate_values()
            elif Grid.cell[block].vacancy < housing_units:
                 #preparing the location so it becomes available 
                if len(Grid.cell[block].collected_rents) == 0:
                    pass
                    print("Seems it is empty", Grid.cell[block].occupants, Grid.cell[block].collected_rents, Grid.cell[block].vacancy, Grid.cell[block].num_rented_units)
                else:
                    units_needed = housing_units - Grid.cell[block].vacancy
                    sorted_renters = sorted(Grid.cell[block].collected_rents, key=Grid.cell[block].collected_rents.get)
                    if units_needed > 1:
                        c = 0
                        s = 0
                        low_bidders = []
                        # & c <= len(low_bidders)
                        while s < units_needed :
                            s += Grid.cell[block].occupants[sorted_renters[c]]
                            low_bidders.append(sorted_renters[c])

                            c = c + 1

                            if c > len(sorted_renters):
                                print("something fishy is going on")
                                break

                        for low_bidder in low_bidders:
                            if closed:
                                new_location = Grid.find_closest(agents[low_bidder], 1, parameters, closed=True)
                                if new_location == agents[low_bidder].location:
                                    new_location = Grid.find_closest(agents[low_bidder], 1, parameters, closed=True)
                                agents[low_bidder].move(new_location,
                                                        agents[low_bidder].bid_value(agents, Grid.cell[block].position,
                                                                                     Grid, parameters, real_bid=True),
                                                        Grid, agents, parameters, agents[low_bidder].housing, 1)
                                Grid.cell[Grid.grid.index(new_location)].calculate_values()
                            else:
                                 new_location = Grid.find_closest(agents[low_bidder], 1, parameters)
                                 agents[low_bidder].move(new_location, agents[low_bidder].bid_value(agents, Grid.cell[block].position, Grid, parameters, real_bid=True), Grid, agents, parameters, agents[low_bidder].housing, 1)
                                 Grid.cell[Grid.grid.index(new_location)].calculate_values()
                    else:
                        if closed:
                            low_bidder = sorted_renters[0]
                            new_location = Grid.find_closest(agents[low_bidder], 1, parameters, closed=True)
                            agents[low_bidder].move(new_location,
                                                    agents[low_bidder].bid_value(agents, Grid.cell[block].position,
                                                                                 Grid, parameters, real_bid=True), Grid,
                                                    agents, parameters, agents[low_bidder].housing, 1)
                            Grid.cell[Grid.grid.index(new_location)].calculate_values()
                        else:

                            low_bidder = sorted_renters[0]
                            new_location = Grid.find_closest(agents[low_bidder], 1, parameters)
                            agents[low_bidder].move(new_location, agents[low_bidder].bid_value(agents, Grid.cell[block].position, Grid, parameters, real_bid=True), Grid, agents, parameters, agents[low_bidder].housing, 1)
                            Grid.cell[Grid.grid.index(new_location)].calculate_values()     
                    units = Grid.cell[block].vacancy - housing_units
                    if units >= 0:
                         pass
                    else:
                        print("Not enough units", block, housing_units, Grid.cell[block].vacancy, Grid.cell[block].occupants, Grid.cell[block].floors)
                        
                    #now high bidder can move 
                    if Grid.cell[block].availability(demand=housing_units):
                        agents[high_bidder].move(Grid.cell[block].position, max(bid_list)/ housing_units, Grid, agents, parameters, agents[high_bidder].housing, housing_units)
                        agents[high_bidder].consumption_utility=agents[high_bidder].utility_value(parameters)
                        Grid.cell[block].calculate_values()
                    else: 
                        print("need one unit, but not there ")
                    Grid.cell[block].empty
                    if not Grid.cell[block].empty:
                        if not Grid.cell[block].counted:
                           Grid.cell[block].counted = True

    Grid.nonempty_floors = sum(Grid.cell[Grid.grid.index(i)].floors for i in Grid.active_grid if Grid.cell[Grid.grid.index(i)].num_rented_units > 0)
    Grid.nonempty_vacancy = sum(Grid.cell[Grid.grid.index(i)].vacancy for i in Grid.active_grid if Grid.cell[Grid.grid.index(i)].num_rented_units > 0)

def position_to_index(Grid, position):

        return Grid.grid.index(position)    