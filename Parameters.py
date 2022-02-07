#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: PARAMETERS

Created on Fri Nov 17 01:23:34 2017

@author: MarMah
"""


class Parameters(object):

    def __init__(self):
        self.output_path = 'Figures/'
        self.seed = 517
        self.num_of_workers =  10
        self.num_of_merchants = self.num_of_workers
        self.num_of_offices = self.num_of_workers
        
        self.num_new_workers = 10
        self.num_new_merchants = self.num_new_workers
        self.num_new_offices = self.num_new_merchants
        
        self.num_new_workers_old = self.num_new_workers
        
        self.grid_height = 20
        self.grid_width = 20
        self.num_runs = 5000


        """ agent parameters """
        """ Firms """

        self.profit_parameter = 100    
        self.agg_parameter = 45  
 
        """ merchants and workers """
        
        self.worker_utility =  5.3 
        self.merchant_utility = 10.85  
        
        self.merchant_share = 0.4 
        self.worker_share = 0.2 
        
        self.utility_alpha = 1
        self.utility_beta = 0.30 
        self.utility_gamma = 1 - self.utility_beta 
        
        self.vacancy_utility_power = .05 # set to 0 for SUM
        self.utility_increment = 1.00 
        
        self.speed_foot = 10
        self.speed_car = 30 
        self.car_cost = 5
        self.pp = 1       
        
        """ developer/landlord parameters """
        self.cost_parameter = 6 # 6=medium coss, 3 or 4=low costs, 8+ high cots

        self.tax = 0.05
        self.interest = 0.03
        self.discount_rate = 0.05
        self.depreciation = 0.005
        self.demolition_cost = 2 
        self.construction_period = 1        
        self.developer_lag_period = 3
        self.developer_vacancy_assumption = 0.9   
                
        """ policy variables """
        self.height_cap = 5#  float("inf"). # Note: Can be set to any real # e.g. 5

    def setter(self, nw, seed, tax, costp, constp, nw_1):
        self.num_of_workers = int(nw)
        self.num_of_merchants = int(self.num_of_workers)
        self.num_of_offices = int(self.num_of_workers)

        self.num_new_workers = nw_1
        self.num_new_merchants = int(self.num_new_workers)
        self.num_new_offices = int(self.num_new_merchants)

        self.seed = int(seed)
        self.tax = tax
        self.construction_period = constp
        self.cost_parameter = costp
        