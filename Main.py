#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: MAIN 

Created on Tue Jul  3 01:41:43 2018

** MAIN IS Basically the Standard Urban Model Run 1 Time
** YOU can add policies before hand 
** But all versions of this model are avaible in the Policy_menu.py file

@author: mary
"""
#%%
import Plot
import pandas as pd
from Agents import agents_constructor
from Gridc import Gridc
from Parameters import Parameters
from Initialize import initialize_model
from Run_sim import run_sim
from Datacollector import dataCollector, agent_dataCollector, cell_dataCollector

#%%
output_data_0 = []
output_data_1 = []
output_data_2 = []
    
w_data = []
m_data = []
o_data = []

cell_data_0 = []
cell_data_1 = []
#%%

gen_run = 0
parameters = Parameters()
agents = agents_constructor(gen_run, parameters)
Grid = Gridc(Parameters().grid_height, Parameters().grid_width, Parameters())

print("Base City")

initialize_model(gen_run, agents, Grid, parameters)
Plot.plot_distribution(gen_run, agents, parameters)

run_sim(agents, Grid, parameters)

#%%
Plot.plot_distribution(gen_run, agents, parameters)
#Plot.heat_map(Plot.height_mat(Grid, parameters), parameters, graph_type='property')
Plot.heat_map(Plot.structure_height_mat(Grid, parameters), parameters, graph_type='height')

Plot.plot_3d(Grid)
#%%
output_data_0.append(dataCollector(gen_run, agents, Grid, parameters))
            
worker, merchant, office = agent_dataCollector(gen_run, agents, parameters)
w_data.append(worker)
m_data.append(merchant)
o_data.append(office)
    
cell_data_0.append(cell_dataCollector(agents, Grid, parameters))
            

#%%
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