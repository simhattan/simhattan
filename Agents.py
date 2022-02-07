#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: AGENTS

Created on Tue Jan  9 23:04:12 2018

@author: MarMah
"""
from numpy import append 
from SuperclassAgent import Worker,Office,Merchant

def agents_constructor(gen_run, parameters, extend = False, agents_list = None):
    
      if not extend:          
            offices = [Office(office, gen_run, parameters) for office in range(int(parameters.num_of_offices))]
            merchants = [Merchant(merchant, gen_run, parameters) for merchant in range(int(parameters.num_of_merchants))]
            workers = [Worker(worker, gen_run, parameters) for worker in range(int(parameters.num_of_workers))]
            agents = append(offices, merchants)
            agents = append(agents,workers)
            return agents       
      else:
          offices = [Office(office, gen_run, parameters, extend = True) for office in range(int(parameters.num_new_offices))]
          merchants = [Merchant(merchant, gen_run, parameters, extend = True) for merchant in range(int(parameters.num_new_merchants))]
          workers = [Worker(worker, gen_run, parameters, extend = True) for worker in range(int(parameters.num_new_workers))]
          agents = append(offices, merchants)
          agents = append(agents,workers)
          for agent in agents :
              agent.generation = gen_run
          agents_updated = append(agents_list, agents)
          return agents_updated  
    
    
       
    
