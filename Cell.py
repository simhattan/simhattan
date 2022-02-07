#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: CELL

Created on Fri Nov 17 22:15:07 2017

@author: MarMah
"""
#import numpy as np 
import math
import pandas as pd

class Cell(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        
        position: 
        active: 
        val:
        val_tot:
        age:
        avg_rent:
        optimal_height:
        occupants:
        num_occupants:
        num_bids:
        num_successful_bids:
    """

    def __init__(self, parameters):
        
        self.position = [0,0]
        self.active = False
        self.val = 0
        self.val_tot = 0 
        self.avg_rent = 0
        self.floors = 1
        self.age = 0              
        self.optimal_height = 0
        self.height_cap = parameters.height_cap
        self.num_tear_downs = 0 
        self.occupants = {}
        self.collected_rents = {}
        self.num_rented_units = 0
        self.num_bids = 0
        self.num_successful_bids = 0
        self.rent_lag_vec = [0]*int(parameters.developer_lag_period)
        self.avg_total_rent = 0
        self.counted = False

    def reset(self, parameters):

        self.val = 0
        self.val_tot = 0 
        self.avg_rent = 0
        self.floors = 1
        self.age = 0              
        self.optimal_height = 0
        self.height_cap = parameters.height_cap
        self.num_tear_downs = 0 
        self.occupants = {}
        self.collected_rents = {}
        self.num_rented_units = 0
        self.num_bids = 0
        self.num_successful_bids = 0
        self.rent_lag_vec = [0]*int(parameters.developer_lag_period)
        self.avg_total_rent = 0
        self.counted = False
         
    @property
    def vacancy(self):
    
        return self.floors - self.num_rented_units

    @property
    def empty(self):
        if self.num_rented_units > 0:
            return False
        else:
            return True
    
    def reset_values(self):
        
        self.val = 0        
        self.val_tot = 0 
        self.avg_rent = 0
        self.avg_total_rent = 0
    
    def calculate_values(self):
        
        if len(self.collected_rents) > 0:
            if self.num_rented_units > 0:
                self.val = max(self.collected_rents.values())
                self.val_tot = sum(self.collected_rents.values())
                self.avg_rent = self.val_tot/self.num_rented_units
                self.avg_total_rent = self.val_tot/len(self.occupants)
            else:
                self.reset_values()
        else:
            self.reset_values()
            
    @property
    def available_place(self):
        
        #keeps track of the availability of a place
        if self.floors - self.num_rented_units > 0:
            return True
        else:
            return False 
    
    def availability(self, demand ):
        
        #returns True if we have enough units
        #to meet the demand(number of units) and False otherwise
        if self.vacancy >= demand:
            return True
        else:
            return False

    def add_renter (self, renter_id, agents, units):
               
        if self.available_place:
            self.occupants.update({renter_id: units})
            self.num_rented_units += units 
            self.collected_rents.update({renter_id:agents[renter_id].total_rent})
            self.calculate_values()
        else:
             print("No available place in here to add new renter")

    def remove_renter(self, renter_id, agents, units):
        
        if renter_id in self.occupants:
            del self.occupants[renter_id]
            del self.collected_rents[renter_id]                
            self.num_rented_units -= units        
            self.calculate_values()
        else:
            print("Wrong ID, the agent is not living here!")

    def moore_neighbor(self, d, parameters, exclusive =False):
        """
        Finds the moore neighbors around the given point 
        with the given distance. 
        
        Args:
            i: the x (first element) of the point
            j: the y (second element) of the point
            d: the distance that the neighbors are counted
            parameters: an instance of class Parameters
            Grid: an instance of class Grid
            Exclusive : optional argument that if set equals to True, will
                        return the mooreneighbors of the point by removing 
                        the moores calculated before.
        Returns:
            A list of the moore neighbors points around the given [i,j] point. 
        
        """
        #
        f = [x for x in range(self.position[0]-d, self.position[0]+d+1) if x >= 0 and x < parameters.grid_width ]
        s = [y for y in range(self.position[1]-d, self.position[1]+d+1) if y >= 0 and y < parameters.grid_width]
        points = [[x, y] for x in f for y in s if [x, y] != [self.position[0], self.position[1]]]
        moore = [[i, j] for [i, j] in points ]

        if not exclusive:
            return moore
        else: 
            if d > 1:
                p_moores = self.moore_neighbor(d-1, parameters)
                moores = [m for m in moore if m not in p_moores]  
                return moores
            
    def eviction(self, Grid, agents, parameters):
                  
         # When building is torn-down, remove all tenents, move them to a closest availble location

        for tenent in list(self.occupants):        
            new_location = Grid.find_closest(agents[tenent], 1, parameters)
            agents[tenent].move(new_location, agents[tenent].bid_value(agents, new_location, Grid, parameters, real_bid=True), Grid, agents, parameters, agents[tenent].housing, 1, evict = True)
            Grid.cell[Grid.grid.index(new_location)].calculate_values()
        if self.floors > 1:
            Grid.total_floors -= self.floors - 1
        self.occupants = {}
        self.collected_rents = {}
        self.num_rented_units = 0
        self.floors = 1
        self.reset_values()

    def tear_down(self, Grid, agents, parameters):
   
        # Developers decide whether to tear-down their building and build larger structure
        # Developers weigh benefit of larger building against building cost/time off the market

        avg_rent_lag = sum(self.rent_lag_vec)/len(self.rent_lag_vec)
        self.optimal_height = max(1, self.floors, int(math.ceil( (1-parameters.tax)*(avg_rent_lag/(2*parameters.cost_parameter)))))
            
        if self.optimal_height > self.height_cap:
            self.optimal_height = self.height_cap

        P_old = (1-parameters.tax) * self.val_tot - (parameters.interest * parameters.cost_parameter * (self.floors ** 2)) - parameters.depreciation * (self.age + 2)* self.floors
        P_new = (parameters.developer_vacancy_assumption)*(1-parameters.tax)*(avg_rent_lag * self.optimal_height) - parameters.interest * parameters.cost_parameter*(self.optimal_height ** 2) - parameters.demolition_cost*(self.floors)#**2 #but not sure why
       
          # if profits higher at new height, tear-down and build new building
        if P_old >= P_new or self.age < 0: # assume that if profits are equal, developer does nothing (status-quo bias)
            self.age += 1
        elif all([P_old < P_new , P_new > 0 , self.optimal_height >self.floors]):
            self.eviction(Grid, agents, parameters)
            self.age = -1 * parameters.construction_period
            self.floors = self.optimal_height
            Grid.total_vacancy += self.floors
            if self.floors > 1:
                Grid.total_floors += self.floors - 1
                Grid.nonempty_floors -= self.floors
            self.val = 0
            self.val_tot = 0
            self.counted = False
            self.num_tear_downs += 1


    def get_all_atts(self):
        
        """Gets all the attributes of a cell
        """
#        print ("position : ", self.position, "\n",
#        "val: ", self.val, "\n",
#        "val_tot: ", self.val_tot, "\n",
#        "age: ", self.age, "\n",
#        "avg_rent: ", self.avg_rent, "\n",
#        "num_rented_units: ", self.num_rented_units, "\n",
#        "optimal_height: ", self.optimal_height, "\n",
#        "occupants: " , self.occupants, "\n",
#        "collected_rents: ", self.collected_rents, "\n",
#        "num_bids: ", self.num_bids, "\n",
#        "num_successful_bids: ", self.num_successful_bids)
        
        data = pd.DataFrame({"position " : [self.position], "val" : self.val, "val_tot" : self.val_tot, "age " : self.age, "avg_rent" : self.avg_rent, 
        "num_rented_units " : self.num_rented_units, "optimal_height" : self.optimal_height, "occupants " : [self.occupants], "collected_rents" : [self.collected_rents],
        "num_bids" : self.num_bids, "num_successful_bids" : self.num_successful_bids})
        
        return data
    