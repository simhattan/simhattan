# -*- coding: utf-8 -*-
"""
FILE: DATA COLLECTOR
UPDATED 6AUG2019 FOR
Created on Tue Aug  6 10:54:33 2019
@author: Jason
NOTE: ONCE I GET THE AVERAGE RENT SHARE WORKERS CALC WORKING--ADD TO ALL GROW CITY VERSIONS BELOW
"""

import numpy as np
import pandas as pd
from openpyxl import load_workbook

# add generation

def dataCollector(gen_run, agents, Grid, parameters):
    
    if gen_run == 0:    
        avg_rent_offices = np.mean(np.array([agents[office].rent for office in range(len(agents)) if agents[office].type=="Office"]))
        avg_cutility_workers = np.mean(np.array(
            [agents[worker].consumption_utility for worker in range(len(agents)) if agents[worker].type=="Worker"]))
        avg_cutility_merchants = np.mean(np.array([agents[merchant].consumption_utility for merchant in range(len(agents)) if agents[merchant].type=="Merchant"]))
        avg_rentshare_w = np.mean(np.array([agents[worker].rent / agents[worker].wage for worker in range(len(agents)) if agents[worker].type=="Worker"]))
        avg_rentshare_m = np.mean(np.array([agents[merchant].rent / agents[merchant].wage for merchant in range(len(agents)) if agents[merchant].type=="Merchant"]))
        avg_rentshare_net_w = np.mean(np.array( [ agents[worker].rent / (agents[worker].wage - agents[worker].commuting_cost) for worker in range(len(agents)) if agents[worker].type=="Worker"]))
        avg_commuteD_w = np.mean(np.array([agents[worker].calc_block_distance(agents[worker].location) for worker in range(len(agents)) if agents[worker].type=="Worker"]))
        avg_commuteD_m = np.mean(np.array([agents[merchant].calc_block_distance(agents[merchant].location) for merchant in range(len(agents)) if agents[merchant].type=="Merchant"]))
        
        data = pd.DataFrame(
            {' seed': [parameters.seed], 
             'num agents': [len(agents)], 
             'tax rate': [parameters.tax],
             'cost parameter': [parameters.cost_parameter], 
             'construction period': [parameters.construction_period],
             'number teardowns': [Grid.count_teardowns()],
             'number of non empty buildings': [Grid.count_nonempty_buildings()],
             'avg non empty buildings height': [Grid.avg_nonempty_bheight()],
             'tallest building': [Grid.tallest_nonempty_b()], 
             'avg height': [Grid.avg_height],
             'avg number people per building': [len(agents) / Grid.count_nonempty_buildings()],
             'avg offices rent': [avg_rent_offices], 
             'avg worker utility': [avg_cutility_workers],
             'avg merchants utility': [avg_cutility_merchants], 
             'avg rent share workers': [avg_rentshare_w],
             'avg rent share workers net': [avg_rentshare_net_w],
             'avg rent share merchants': [avg_rentshare_m], 
             'avg commuting distance worker': [avg_commuteD_w],
             'avg commuting distace merchant': [avg_commuteD_m],
             'city area': [Grid.city_area(Grid.convex_hull(parameters))],
             'CC Vacancy': [Grid.cc_vacancy(Grid.convex_hull(parameters, pplot=False, closed_city=True))[1]],
             "vacancy in the occupied builings": [Grid.vacancy_avg], 
             "convergence Count": [Grid.convergence_count]})
    
    elif gen_run == 1:
        gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers
        # data for the original folks
        avg_rent_offices = np.mean(np.array([agents[office].rent for office in range(0, parameters.num_of_offices)]))
        avg_cutility_workers = np.mean(np.array(
            [agents[worker].consumption_utility for worker in range(gen_size - parameters.num_of_workers,  gen_size)]))
        avg_cutility_merchants = np.mean(np.array([agents[merchant].consumption_utility for merchant in
                                                    range(parameters.num_of_offices,
                                                          parameters.num_of_offices + parameters.num_of_merchants)]))

        avg_rentshare_w = np.mean(np.array([agents[worker].rent / agents[worker].wage for worker in
                                            range(gen_size - parameters.num_of_workers,  gen_size)]))

        avg_rentshare_net_w = np.mean(np.array([agents[worker].rent / (agents[worker].wage - agents[worker].commuting_cost) for worker in
                                            range(gen_size - parameters.num_of_workers,  gen_size)])

        avg_rentshare_m = np.mean(np.array([agents[merchant].rent / agents[merchant].wage for merchant in
                                            range(parameters.num_of_offices,
                                                  parameters.num_of_offices + parameters.num_of_merchants)]))

        avg_commuteD_w = np.mean(np.array([agents[worker].calc_block_distance(agents[worker].location) for worker in
                                           range(gen_size - parameters.num_of_workers,  gen_size)]))

        avg_commuteD_m = np.mean(np.array([agents[merchant].calc_block_distance(agents[merchant].location) for merchant in
                                           range(parameters.num_of_offices,
                                                 parameters.num_of_offices + parameters.num_of_merchants)]))
        # data for new agents
        avg_rent_offices_1 = np.mean(
            np.array([agents[office].rent for office in range(gen_size, gen_size + parameters.num_new_offices)]))
        avg_cutility_workers_1 = np.mean(np.array([agents[worker].consumption_utility for worker in
                                                 range(len(agents) - parameters.num_new_workers, len(agents))]))

        avg_cutility_merchants_1 = np.mean(np.array([agents[merchant].consumption_utility for merchant in
                                                    range(gen_size + parameters.num_new_offices,
                                                                  len(agents) - parameters.num_new_workers)]))

        avg_rentshare_w_1 = np.mean(np.array([agents[worker].rent / agents[worker].wage for worker in
                                            range(len(agents) - parameters.num_new_workers, len(agents))]))

        avg_rentshare_m_1 = np.mean(np.array([agents[merchant].rent / agents[merchant].wage for merchant in
                                              range(gen_size + parameters.num_new_offices,
                                                                  len(agents) - parameters.num_new_workers)]))

        avg_commuteD_w_1 = np.mean(np.array([agents[worker].calc_block_distance(agents[worker].location) for worker in
                                           range(len(agents) - parameters.num_new_workers, len(agents))]))

        avg_commuteD_m_1 = np.mean(
            np.array([agents[merchant].calc_block_distance(agents[merchant].location) for merchant in
                      range(gen_size + parameters.num_new_offices, len(agents) - parameters.num_new_workers)]))

        data = pd.DataFrame(
            {'base seed': [parameters.seed], 
             'num of agents': [len(agents)], 
             'tax rate': [parameters.tax],
             'cost parameter': [parameters.cost_parameter], 
             'construction period': [parameters.construction_period],
             'number of teardowns': [Grid.count_teardowns()],
             'number of non empty buildings': [Grid.count_nonempty_buildings()],
             'avg non empty buildings height': [Grid.avg_nonempty_bheight()],
             'tallest building': [Grid.tallest_nonempty_b()], 
             'avg height': [Grid.avg_height],
             'avg number people per building': [len(agents) / Grid.count_nonempty_buildings()],
             'avg offices rent': [avg_rent_offices],
             'avg new offices rent': [avg_rent_offices_1], 
             'avg worker utility': [avg_cutility_workers],
             'avg new worker utility': [avg_cutility_workers_1],
             'avg merchants utility': [avg_cutility_merchants], 
             'avg new merchants utility': [avg_cutility_merchants_1],
             'avg rent share workers': [avg_rentshare_w],
             'avg rent share new workers': [avg_rentshare_w_1],
             'avg rent share merchants': [avg_rentshare_m], 
             'avg rent share new merchants': [avg_rentshare_m_1], 
             'avg commuting distance worker': [avg_commuteD_w],             
             'avg commuting distance new worker': [avg_commuteD_w_1],
             'avg commuting distance merchant': [avg_commuteD_m],
             'avg commuting distance new merchants': [avg_commuteD_m_1],   
             'city area': [Grid.city_area(Grid.convex_hull(parameters))],
             'CC Vacancy ': [Grid.cc_vacancy(Grid.convex_hull(parameters, pplot=False, closed_city=True))[1]],
             "vacancy in the occupied buildings": [Grid.vacancy_avg],
             "convergence Count": [Grid.convergence_count]})    
    else:
        gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers
        gen_size_1 = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + 3*parameters.num_new_workers_old
        # this is data for the original folks
        avg_rent_offices = np.mean(np.array([agents[office].rent for office in range(0, parameters.num_of_offices)]))
        print("dingle")
        avg_cutility_workers = np.mean(np.array(
            [agents[worker].consumption_utility for worker in range(gen_size - parameters.num_of_workers,  gen_size)]))

        avg_cutility_merchants = np.mean(np.array([agents[merchant].consumption_utility for merchant in
                                                    range(parameters.num_of_offices,
                                                          parameters.num_of_offices + parameters.num_of_merchants)]))

        avg_rentshare_w = np.mean(np.array([agents[worker].rent / agents[worker].wage for worker in
                                            range(gen_size - parameters.num_of_workers,  gen_size)]))

        avg_rentshare_m = np.mean(np.array([agents[merchant].rent / agents[merchant].wage for merchant in
                                            range(parameters.num_of_offices,
                                                  parameters.num_of_offices + parameters.num_of_merchants)]))

        avg_commuteD_w = np.mean(np.array([agents[worker].calc_block_distance(agents[worker].location) for worker in
                                           range(gen_size - parameters.num_of_workers,  gen_size)]))

        avg_commuteD_m = np.mean(np.array([agents[merchant].calc_block_distance(agents[merchant].location) for merchant in
                                           range(parameters.num_of_offices,
                                                 parameters.num_of_offices + parameters.num_of_merchants)]))
        # avereages for new agents
        avg_rent_offices_1 = np.mean(
            np.array([agents[office].rent for office in range(gen_size, gen_size + parameters.num_new_offices_old)]))     
        
        avg_cutility_workers_1 = np.mean(np.array([agents[worker].consumption_utility for worker in
                                                 range(gen_size+parameters.num_new_workers_old + parameters.num_new_merchants_old,gen_size+parameters.num_new_workers_old + parameters.num_new_merchants_old+ parameters.num_new_workers_old)]))

        avg_cutility_merchants_1 = np.mean(np.array([agents[merchant].consumption_utility for merchant in
                                                    range(gen_size+parameters.num_new_workers_old, gen_size + parameters.num_new_workers_old + parameters.num_new_merchants_old)]))
        
        avg_rentshare_w_1 = np.mean(np.array([agents[worker].rent / agents[worker].wage for worker in
                                            range(gen_size+parameters.num_new_workers_old + parameters.num_new_merchants_old,gen_size+parameters.num_new_workers_old + parameters.num_new_merchants_old+ parameters.num_new_workers_old)]))
        avg_rentshare_m_1 = np.mean(np.array([agents[merchant].rent / agents[merchant].wage for merchant in
                                              range(gen_size+parameters.num_new_workers_old, gen_size + parameters.num_new_workers_old + parameters.num_new_merchants_old)]))
        avg_commuteD_w_1 = np.mean(np.array([agents[worker].calc_block_distance(agents[worker].location) for worker in
                                           range(gen_size+parameters.num_new_workers_old + parameters.num_new_merchants_old,gen_size+parameters.num_new_workers_old + parameters.num_new_merchants_old+ parameters.num_new_workers_old)]))
        avg_commuteD_m_1 = np.mean(
            np.array([agents[merchant].calc_block_distance(agents[merchant].location) for merchant in
                      range(gen_size+parameters.num_new_workers_old, gen_size + parameters.num_new_workers_old + parameters.num_new_merchants_old)]))
    
            # avereages for grow again agents
        avg_rent_offices_2 = np.mean(np.array([agents[office].rent for office in range(gen_size_1, len(agents)) if agents[office].type=="Office"]))
        avg_cutility_workers_2 = np.mean(np.array([agents[worker].consumption_utility for worker in range(gen_size_1, len(agents)) if agents[worker].type=="Worker"]))
    
        avg_cutility_merchants_2 = np.mean(np.array([agents[merchant].consumption_utility for merchant in
                                                    range(gen_size_1 + parameters.num_new_offices,
                                                                  len(agents) - parameters.num_new_workers)]))
       
        avg_rentshare_w_2 = np.mean(np.array([agents[worker].rent / agents[worker].wage for worker in
                                            range(gen_size_1, len(agents)) if agents[worker].type=="Worker"]))

        avg_rentshare_m_2 = np.mean(np.array([agents[merchant].rent / agents[merchant].wage for merchant in
                                              range(gen_size_1, len(agents)) if agents[merchant].type=="Merchant"]))

        avg_commuteD_w_2 = np.mean(np.array([agents[worker].calc_block_distance(agents[worker].location) for worker in
                                           range(gen_size_1, len(agents)) if agents[worker].type=="Worker"]))

        avg_commuteD_m_2 = np.mean(
            np.array([agents[merchant].calc_block_distance(agents[merchant].location) for merchant in
                      range(gen_size_1, len(agents)) if agents[merchant].type=="Merchant"]))
    
        data = pd.DataFrame(
            {'base seed': [parameters.seed], 
             'num of agents': [len(agents)], 
             'tax rate': [parameters.tax],
             'cost parameter': [parameters.cost_parameter], 
             'construction period': [parameters.construction_period],
             'number of teardowns': [Grid.count_teardowns()],
             'number of non empty buildings': [Grid.count_nonempty_buildings()],
             'avg non empty buildings height': [Grid.avg_nonempty_bheight()],
             'tallest building': [Grid.tallest_nonempty_b()], 
             'avg height': [Grid.avg_height],
             'avg number people per building': [len(agents) / Grid.count_nonempty_buildings()],
             'avg offices rent' : [avg_rent_offices],
             'avg new offices rent': [avg_rent_offices_1], 
             'avg grow again offices rent': [avg_rent_offices_2], 
             'avg worker utility' : [avg_cutility_workers],
             'avg new worker utility': [avg_cutility_workers_1],
             'avg grow again worker utility': [avg_cutility_workers_2],
             'avg merchants utility' : [avg_cutility_merchants], 
             'avg new merchants utility': [avg_cutility_merchants_1],
             'avg grow again merchants utility': [avg_cutility_merchants_2],             
             'avg rent share workers' : [avg_rentshare_w],
             'avg rent share new workers': [avg_rentshare_w_1],
             'avg rent share grow again workers': [avg_rentshare_w_2],
             'avg rent share merchants': [avg_rentshare_m], 
             'avg rent share new merchants': [avg_rentshare_m_1], 
             'avg rent share grow again merchants': [avg_rentshare_m_2],              
             'avg commuting distance worker': [avg_commuteD_w],             
             'avg commuting distance new worker': [avg_commuteD_w_1],
             'avg commuting distance grow again worker': [avg_commuteD_w_2],             
             'avg commuting distance merchant': [avg_commuteD_m],
             'avg commuting distance new merchants': [avg_commuteD_m_1],  
             'avg commuting distance grow again merchants': [avg_commuteD_m_2],  
             'city area': [Grid.city_area(Grid.convex_hull(parameters))],
             'CC Vacancy ': [Grid.cc_vacancy(Grid.convex_hull(parameters, pplot=False, closed_city=True))[1]],
             "vacancy in the occupied buildings": [Grid.vacancy_avg],
             "convergence count": [Grid.convergence_count]})    
    return data


def agent_dataCollector(gen_run, agents, parameters):

    if gen_run == 0:
        ats_workers   = pd.concat([agents[worker].get_all_atts() for worker in range(len(agents)) if agents[worker].type == "Worker"], sort=False)
        ats_merchants = pd.concat([agents[merchant].get_all_atts() for merchant in range(len(agents)) if agents[merchant].type == "Merchant" ], sort=False)
        ats_offices   = pd.concat([agents[office].get_all_atts() for office in range(len(agents)) if agents[office].type == "Office"], sort = False)
        return ats_workers, ats_merchants, ats_offices
    elif gen_run == 1:
        gen_size = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers
        ats_workers_1 = pd.concat(
            [agents[worker].get_all_atts() for worker in range(len(agents) - parameters.num_new_workers, len(agents)) if
             agents[worker].generation == 1])
        ats_merchants_1 = pd.concat([agents[merchant].get_all_atts() for merchant in range(gen_size + parameters.num_new_offices,
                                                                  len(agents) - parameters.num_new_workers)
                                     if agents[merchant].generation == 1])
        ats_offices_1 = pd.concat([agents[office].get_all_atts() for office in range(gen_size, gen_size + parameters.num_new_offices) if
                                   agents[office].generation == 1])
        return ats_workers_1, ats_merchants_1, ats_offices_1
    else:
        gen_size_1 = parameters.num_of_offices + parameters.num_of_merchants + parameters.num_of_workers + 3*parameters.num_new_workers_old
        ats_workers_2 = pd.concat(
            [agents[worker].get_all_atts() for worker in range(gen_size_1, len(agents)) if agents[worker].type=="Worker" if agents[worker].generation == 2  ])
        ats_merchants_2 = pd.concat([agents[merchant].get_all_atts() for merchant in range(gen_size_1 , len(agents))
                                     if agents[merchant].generation == 2 if agents[merchant].type=="Merchant"])
        ats_offices_2 = pd.concat([agents[office].get_all_atts() for office in range(gen_size_1 , len(agents)) if
                                   agents[office].generation == 2 if agents[office].type == "Office"])
        return ats_workers_2, ats_merchants_2, ats_offices_2
    
def cell_dataCollector(agents, Grid, parameters) :

    atts_cell = pd.concat([Grid.cell[i].get_all_atts() for i in range(len(Grid.grid))])
    return atts_cell
