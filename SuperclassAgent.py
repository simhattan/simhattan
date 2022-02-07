#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: SUPERCLASS AGENTS

Created on Wed Jan 10 03:18:20 2018

@author: Mary
"""
import math
import random
import pandas as pd
from collections import OrderedDict

class Agents(object) :

    def __init__(self, agent):

        self.location = [-1, -1]
        self.location_value = 0
        self.generation = 0
        self.commuting_cost = 0
        self.housing = 1
        self.rent = 0
        self.old_location = [-1, -1]
        self.rent_control_tenent = 0
        self.rental_tenure = 0
        self.move_tracker = []
        self.decision_tracker = OrderedDict()
        self.bid_tracker = OrderedDict()
        self.consumption_utility = 0

    def reset(self, agent, parameters):
        self.location = [-1, -1]
        self.location_value = 0
        self.generation = 0
        self.commuting_cost = 0
        self.housing = 1
        self.rent = 0
        self.old_location = [-1, -1]
        self.housing_cost_share = 0
        self.rent_control_tenent = 0
        self.rental_tenure = 0
        self.move_tracker = []
        self.decision_tracker = OrderedDict()
        self.bid_tracker = OrderedDict()

    @property
    def total_rent(self):

        return self.rent * self.housing

    def calc_distance(self, other):
        # Computes euclidean distance between self and other agent
        a = (self.location[0] - other[0]) ** 2
        b = (self.location[1] - other[1]) ** 2
        return math.sqrt(a + b)

        # fix this for the new agents in initialize function to move

    def calc_new_distance(self, location1, location2):
        """
        Computes euclidean distance between any two points.

        Args:

            location 1: [i,j] position
            location 2: [i,j] position

        Returns:
           The Eclidian distance
        """
        a = (location1[0] - location2[0]) ** 2
        b = (location1[1] - location2[1]) ** 2
        return math.sqrt(a + b)

    def move(self, new_location, bid, Grid, agents, parameters, b_units, a_units, evict=False, pop_grow_in=False):
        # takes care of everything related to the change of agent's location
        # removes the renter from the old location, updates the availability of
        # the old location
        # b_units : #units before move
        # a_units: #units after move

        if evict:

            self.location = new_location
            self.rent = bid
            self.housing = 1
            Grid.cell[Grid.grid.index(new_location)].add_renter(self.agent_id, agents, 1)
            Grid.total_vacancy -= 1
            
            if not Grid.cell[Grid.grid.index(new_location)].empty:
                if not Grid.cell[Grid.grid.index(new_location)].counted:
                    Grid.cell[Grid.grid.index(new_location)].counted = True

        else:

            if pop_grow_in:
                
                self.location = new_location
                self.rent = bid
                self.housing = a_units
                Grid.cell[Grid.grid.index(new_location)].add_renter(self.agent_id, agents, a_units)
                Grid.total_vacancy -= a_units             
                Grid.cell[Grid.grid.index(new_location)].empty
                if not Grid.cell[Grid.grid.index(new_location)].empty:
                    if not Grid.cell[Grid.grid.index(new_location)].counted:
                        Grid.cell[Grid.grid.index(new_location)].counted = True
            else:
                Grid.cell[Grid.grid.index(self.location)].remove_renter(self.agent_id, agents, b_units)
                Grid.total_vacancy += b_units
                Grid.cell[Grid.grid.index(self.location)].empty
                if Grid.cell[Grid.grid.index(self.location)].empty:
                    if Grid.cell[Grid.grid.index(self.location)].counted:
                        Grid.cell[Grid.grid.index(self.location)].counted = False
                self.location = new_location
                self.rent = bid
                self.housing = a_units
                Grid.cell[Grid.grid.index(new_location)].add_renter(self.agent_id, agents, a_units)
                Grid.total_vacancy -= a_units
                Grid.cell[Grid.grid.index(new_location)].empty
                if not Grid.cell[Grid.grid.index(new_location)].empty:
                    if not Grid.cell[Grid.grid.index(new_location)].counted:
                        Grid.cell[Grid.grid.index(new_location)].counted = True
        if not pop_grow_in:
            if self.type == "Office":
                # updates the work location of merchants and workers
                # as well as their utilities
                self.update_workers(agents, Grid, parameters)
            else:
                self.consumption_utility = self.utility_value(parameters)
                self.update_work_tcost(new_location, parameters)
                self.reservation_utility = self.reservation_utility_base * parameters.utility_increment
                if self.wage > 0:
                    self.housing_cost_share = self.rent / self.wage
                else:
                    print(self.agent_id, "0 wage!!!")

    def reset_location(self):

        self.location = [-1, -1]

    def utility_value(self, parameters):

        if self.type != "Office":
            numeraire = self.wage - self.commuting_cost - self.housing * self.rent
            if numeraire > 0:
                utils = (self.housing ** parameters.utility_beta) * numeraire ** (1 - parameters.utility_beta)
            else:
                utils = 0
            return utils


class Office(Agents):

    def __init__(self, office, gen_run, parameters, extend=False):
        Agents.__init__(self, office)
        if extend :
            if gen_run == 1:
                self.agent_id = office + parameters.num_of_workers + parameters.num_of_offices + parameters.num_of_merchants
            else:
                self.agent_id = office + parameters.num_of_workers + parameters.num_of_offices + parameters.num_of_merchants + 3*(parameters.num_new_workers_old)
        else :
            self.agent_id = office
        self.type = "Office"
        self.profit = parameters.profit_parameter
        self.merchant_index = -1
        self.employee_index = -1
        self.agglom_val = 0
        self.availability = True
        self.agent_gen = 0

    def reset(self, office, parameters):
        Agents.__init__(self, office)
        self.profit = parameters.profit_parameter
        self.merchant_index = -1
        self.employee_index = -1
        self.agglom_val = 0
        self.availability = True
        self.agent_gen = 0


    def update_workers(self, agents, Grid, parameters):
        # just for now we update the rents of the merchants and workers if the office moves
        agents[self.employee_index].employer_location = self.location
        agents[self.employee_index].consumption_utility = agents[self.employee_index].utility_value(parameters)
        agents[self.employee_index].update_work_tcost(agents[self.employee_index].location, parameters)
        agents[self.employee_index].rent = agents[self.employee_index].bid_value(agents,
                                                                                 agents[self.employee_index].location,
                                                                                 Grid, parameters, real_bid=True)
        # update the rents for the location:
        Grid.cell[Grid.grid.index(agents[self.employee_index].location)].collected_rents.update(
            {agents[self.employee_index].agent_id : agents[self.employee_index].total_rent})
        
        Grid.cell[Grid.grid.index(agents[self.employee_index].location)].calculate_values()

        agents[self.merchant_index].office_location = self.location
        agents[self.merchant_index].consumption_utility = agents[self.merchant_index].utility_value(parameters)
        agents[self.merchant_index].update_work_tcost(agents[self.merchant_index].location, parameters)
        agents[self.merchant_index].rent = agents[self.employee_index].bid_value(agents,
                                                                                 agents[self.merchant_index].location,
                                                                                 Grid, parameters, real_bid=True)
        # update the rents for that location:
        Grid.cell[Grid.grid.index(agents[self.merchant_index].location)].collected_rents.update(
            {agents[self.merchant_index].agent_id : agents[self.merchant_index].total_rent})
        
        Grid.cell[Grid.grid.index(agents[self.merchant_index].location)].calculate_values()

    def trans_cost(self, location1, location2, parameters, mode=None):
        pass
        print("Agent Office does not have transit cost")

    def agglomeration(self, agents, location, Grid, parameters):
        """
        Computes agglomeration function for a given location.
        that is, this function get the distance of a firm to all the others
        #    creates a paramter 1/(sum of distances); lower average distance gives higher weight
        #    meant to model that firm clustering increases profits
           
        Args:

            agents:the list of instances of the class Agent (Offices, Merchants, Workers ) 
            location: the [i,j] location for which the agglomoration is calculated
            parameters: an instance of class Parameters
            
        Returns:
           The agglomeration cost 
    
        """
        a_list = [max(self.calc_new_distance(location, agents[office].location), 0.5) for office in
                  range(parameters.num_of_offices) if self.agent_id != agents[office].agent_id]
        num_firms = len(a_list)
        power_value = .333 
        agg_p = parameters.agg_parameter*( (num_firms**power_value)/(sum(a_list)/num_firms)) # the original function 
        return agg_p
                                           
                                           
    def bid_value(self, agents, other, Grid, parameters, real_bid=False):

        bid_value = self.agglomeration(agents, other, Grid, parameters)
        if real_bid:
            return bid_value
        else:
            if bid_value > self.rent:
                return bid_value
            else:
                return 0

    def housing_demand(self, agents, block, Grid, parameters):

        return 1

    def get_all_atts(self):
        """Gets all the attributes of a cell
        """
        data = pd.DataFrame(
            {'agent ID': self.agent_id, 
             'type': self.type, 
             'location': [self.location], 
             'rent': self.rent,
             'merchant_index': self.merchant_index,
             'employee_index': self.employee_index})
        return data


class Merchant(Agents) :
    # Note "Merchants are owners"

    def __init__(self, merchant, gen_run, parameters, extend=False):
        Agents.__init__(self, merchant)
        self.type = "Merchant"
        if extend :
            if gen_run == 1:
                self.agent_id = merchant + parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + parameters.num_new_offices 
            else:
                self.agent_id = merchant + 3*(parameters.num_new_offices_old) + parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + parameters.num_new_offices 
    
        else :
            self.agent_id = merchant + parameters.num_of_offices

        self.office_index = -1
        self.office_location = [-1, -1]
        self.wage = 0
        self.mode = 0
        self.distance = 0

        self.reservation_utility_base = parameters.merchant_utility
        self.reservation_utility = self.reservation_utility_base
        self.consumption_utility = 0
        self.cd_dv = (parameters.utility_beta ** parameters.utility_beta) * (
                (1 - parameters.utility_beta) ** (1 - parameters.utility_beta))
        self.housing_cost_share = 0
        self.agent_gen = 0

    def reset(self, merchant, parameters):

        Agents.__init__(self, merchant)
        self.office_index = -1
        self.office_location = [-1, -1]
        self.wage = 0
        self.mode = 0
        self.distance = 0

        self.reservation_utility_base = parameters.merchant_utility
        self.reservation_utility = self.reservation_utility_base
        self.consumption_utility = 0
        self.housing_cost_share = 0
        self.agent_gen = 0

    @property
    def housing_cost_check(self):
        if self.housing_cost_share < .1 :  # parameters.nudge_threshold : #.05
            self.reservation_utility = self.reservation_utility * (1 - .2)  # .05(1-parameters.nudge_factor)

    def calc_block_distance(self, other):
        # Computes euclidean distance between workplace and other agent
        a = (self.office_location[0] - other[0]) ** 2
        b = (self.office_location[1] - other[1]) ** 2
        return math.sqrt(a + b)

    def trans_cost(self, location1, location2, parameters, mode=None, set_mode=False):
        """
            Computes the commuting cost for a given agent between two given locations.    
            Args:
                agent: the specific agent we are interested in
                location 1: [i,j] position 
                location 2: [i,j] position
                parameters: an instance of class Parameters
                mode: walk or ride   
            Returns:
               if the  mode is passed, the function will return the commuting cost using that mode
               if not, it will calculate the commuting cost of both modes and return the one with the minimum cost
        """
        if not mode:
            cost_walk = (self.wage * self.calc_new_distance(location1, location2)) / parameters.speed_foot
            cost_ride = ((self.wage * self.calc_new_distance(location1,
                                                         location2))/parameters.speed_car) + parameters.car_cost
            if set_mode:
                self.distance = self.calc_new_distance(self.office_location, location2)
                if cost_walk < cost_ride:
                    self.mode = "walk"
                else:
                    self.mode = "ride"
            return min(cost_walk, cost_ride)
        else:
            if mode == "walk" :
                return (self.wage * self.calc_new_distance(location1, location2)) / parameters.speed_foot
            elif mode == "ride" :
                return ((((self.wage * self.calc_new_distance(location1,
                                                         location2)) / parameters.speed_car)) + parameters.car_cost)


    def bid_value(self, agents, other, Grid, parameters, real_bid=False):
        """
        Computes the bid values for each agent
        
        Args:
            agents: the list of agents 
            other: the [i,j] location for which we are bidding 
            parameters: an instance of class Parameters
            real_bid: if set to True, it will set the commuting cost and distance of the agent as well as the transit mode
                        by calling the trans_cost method with the set_mode = True 
                
        Returns :
            The bid value of each agent 
        """
        commute_cost = self.trans_cost(self.office_location, other, parameters)

        if Grid.vacancy_avg == 0:
            vacancy_av = 0.001
        else:
            vacancy_av = Grid.vacancy_avg

        a_u = parameters.utility_alpha / (
                self.reservation_utility_base * (vacancy_av ** parameters.vacancy_utility_power))

        w_w = max([0, self.wage - commute_cost])

        bid_value = (self.cd_dv * a_u * w_w) ** (1 / parameters.utility_beta)

        if real_bid:
            return bid_value
        else:
            if bid_value > self.rent:
                return bid_value
            else:
                return 0

    def update_work_tcost(self, new_location, parameters):

        self.commuting_cost = self.trans_cost(self.office_location, new_location, parameters)

    def housing_demand(self, agents, block, Grid, parameters):

        if self.bid_value(agents, block, Grid, parameters) > 0:

            h = int(math.floor((parameters.utility_beta / (parameters.utility_gamma + parameters.utility_beta)) *
                               (self.wage - self.trans_cost(self.office_location, block, parameters)) / self.bid_value(
                agents, block, Grid, parameters)))
            if h < 1:
                return 1
            else:
                return h
        else:
            return 0

    def get_all_atts(self):
        """
        Gets all the attributes of a cell
        """
        data = pd.DataFrame(
            {'agent ID' : self.agent_id, 'type' : self.type, 'location' : [self.location], 'rent': self.rent,
             "office_index" : self.office_index,
             "office_location" : [self.office_location], 'wage' : self.wage})
        return data


class Worker(Agents):
    def __init__(self, worker, gen_run, parameters, extend=False):
        Agents.__init__(self, worker)
        if extend:
            if gen_run == 1:
                self.agent_id = worker + parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + parameters.num_new_offices + parameters.num_new_merchants

            else:  
                self.agent_id = worker + 3*(parameters.num_new_offices_old) + parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + parameters.num_new_offices + parameters.num_new_merchants
        else :
            self.agent_id = worker + parameters.num_of_offices + parameters.num_of_merchants

        self.type = "Worker"
        self.mode = 0
        self.employer = -1
        self.employer_location = [-1, -1]
        self.wage = 0
        self.distance = 0

        self.reservation_utility_base = parameters.worker_utility
        self.reservation_utility = self.reservation_utility_base
        self.consumption_utility = 0
        self.cd_dv = (parameters.utility_beta ** parameters.utility_beta) * (
                (1 - parameters.utility_beta) ** (1 - parameters.utility_beta))
        self.housing_cost_share = 0
        self.agent_gen = 0
        self.commuting_cost = 0 #delete after test

    def reset(self, worker, parameters):

        Agents.__init__(self, worker)
        self.mode = 0
        self.employer = -1
        self.employer_location = [-1, -1]
        self.wage = 0
        self.distance = 0

        self.reservation_utility_base = parameters.worker_utility
        self.reservation_utility = self.reservation_utility_base
        self.consumption_utility = 0
        self.housing_cost_share = 0
        self.agent_gen = 0
        
        self.commuting_cost = 0 #delete after test

    @property
    def housing_cost_check(self):
        if self.housing_cost_share < .15 : #.15 :  # parameters.nudge_threshold : #.05
            self.reservation_utility = self.reservation_utility * (1 - .1)  #.1 (1-parameters.nudge_factor)

    def calc_block_distance(self, other):
        # Computes euclidean distance between workplace and other agent
        a = (self.employer_location[0] - other[0]) ** 2
        b = (self.employer_location[1] - other[1]) ** 2
        return math.sqrt(a + b)

    def trans_cost(self, location1, location2, parameters, mode=None, set_mode=False):
        """
        Computes the commuting cost for a given agent between two given locations.
        Args:
            agent: the specific agent we are interested in
            location 1: [i,j] position 
            location 2: [i,j] position
            parameters: an instance of class Parameters
            mode: walk or ride                 
        Returns:
            if the  mode is passed, the function will return the commuting cost using that mode
            if not, it will calculate the commuting cost of both modes and return the one with the minimum cost
         """
        if not mode:
            cost_walk = ((self.wage * self.calc_new_distance(location1, location2)) / parameters.speed_foot)
            cost_ride = (((self.wage * self.calc_new_distance(location1,
                                                        location2)) / parameters.speed_car)) + parameters.car_cost
            if set_mode:
                if cost_walk < cost_ride:
                    self.mode = "walk"
                else:
                    self.mode = "ride"
            return min(cost_walk, cost_ride)
        else:
            if mode == "walk":
                return (
                       ((self.wage * self.calc_new_distance(location1, location2)) / parameters.speed_foot)).pp
            elif mode == "ride":
                return ((((self.wage * self.calc_new_distance(location1,
                                                         location2)) / parameters.speed_car)) + parameters.car_cost)

    def bid_value(self, agents, other, Grid, parameters, real_bid=False):

        """
        Computes the bid values for each agent
        
        Args:

            other: the [i,j] location for which we are bidding 
            parameters: an instance of class Parameters
            real_bid: if set to True, it will set the commuting cost of the agent as well as the transit mode
                        by calling the trans_cost method with the set_mode = True 
                
        Returns :
            The bid value of each agent 
        """
        if real_bid:
            commute_cost = self.trans_cost(self.employer_location, other, parameters, set_mode=True)
            self.commuting_cost = commute_cost
        else:
            commute_cost = self.trans_cost(self.employer_location, other, parameters)
        if Grid.vacancy_avg == 0:
            vacancy_av = 0.001
        else:
            vacancy_av = Grid.vacancy_avg
        a_u = parameters.utility_alpha / (
                self.reservation_utility_base * (vacancy_av ** parameters.vacancy_utility_power))
        w_w = max([0, self.wage - commute_cost])
        bid_value = (self.cd_dv * a_u * w_w) ** (1 / parameters.utility_beta)
        if real_bid:
            return bid_value
        else:
            if bid_value > self.rent:
                return bid_value
            else:
                return 0

    def update_work_tcost(self, new_location, parameters):

        self.commuting_cost = self.trans_cost(self.employer_location, new_location, parameters)

    def housing_demand(self, agents, block, Grid, parameters):

        if self.bid_value(agents, block, Grid, parameters) > 0:
            h = int(math.floor((parameters.utility_beta / (parameters.utility_gamma + parameters.utility_beta)) * (
                        self.wage - self.trans_cost(self.employer_location, block, parameters)) / self.bid_value(agents, block, Grid,
                                                                                                                 parameters)))
            if h < 1:
                return 1
            else:
                return h
        else:
            return 0

    def get_all_atts(self):

        """
        Gets all the attributes of a cell
        """
        data = pd.DataFrame(
            {'agent ID': self.agent_id, 
             'type': self.type, 
             'location': [self.location], 
             'rent': self.rent,
             'employer': self.employer, 
             'employer location': [self.employer_location], 
             'wage': self.wage, 
             'commuting cost': self.commuting_cost
             })

        return data




