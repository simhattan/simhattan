#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: POLICY

Created on Sat Jun 22 14:34:00 2019

@author: mary
"""

import pandas as pd 
from Iterate import iterate 
from Parameters import Parameters

""" ********* PF Files ************ 
- PF_N20 is hold n=20, new=10, randomize costs
*******************************"""
gen_run = 0

pRun = 0

if pRun==1:

    #p = pd.read_csv('./PF_N20.csv')
    #p =  pd.read_csv('./PF_C3.csv')
    p =  pd.read_csv('./PF_C8.csv')
    
else:
    p = pd.read_csv('./PF.csv')

parameters = Parameters()

policy_num = 1

# Base only with policiees

#parameters.height_cap = float(7) 
#iterate(gen_run, parameters, p, base = True,  rent_control_0 = True)

#iterate(gen_run, policy_num, parameters, p, base= True, closed = True, rent_control_1 = True, height_cap = True)


#always when running closed city, you need to have both base and closed as True
# def iterate(parameters, p, base= False, closed=False, base_grow=False, rent_control=False):

#iterate(gen_run, parameters, p, base_grow = True)

#iterate(gen_run ,parameters, p, base_grow = True, rent_control = True)
  
""" 
*******************************************************************
** Run and Expand Only
** Open Grow: base = False, closed = False, base_grow = True
** Closed Grow: base = True, closed = True, base_grow = False
 ******************************************************************
"""


# open grow 
#iterate(gen_run, parameters, p, base = False, closed = False, base_grow = True, rent_control = False)
#iterate(gen_run, parameters, p,  base_grow = True, height_cap = False)

# grow closed 
iterate(gen_run, policy_num, parameters, p, base= True, closed = True, base_grow = False, rent_control_1 = True)

 ####################################################################

""" 
*******************************************************************
** Run, Expand, and Expand Again
** Open Grow: base = False, closed = False, base_grow = True, grow_again=True
** Closed Grow: base = True, closed = True, base_grow = False
 ******************************************************************
"""

# grow again open
#iterate(gen_run, parameters, p, base = False, closed = False, base_grow = True, rent_control = False, grow_again = True)


# **********************************************************************************
# grow again close the city
# note if we want it remain closed or to be opened, # we need to change closed 
# feature in grow_again function in the Iterate file where where closed=True,
# keeps it closed and closed=False opens it up again
# **********************************************************************************
#print ("closed and keep closed")
#iterate(gen_run, parameters, p, base= True, closed = True, base_grow = False, rent_control = False, grow_again = True)

#print ("closed and open")
#iterate(gen_run, parameters, p, base= True, closed = True, base_grow = False, rent_control = False, grow_again = True)

#grow closed  grow open
#iterate(gen_run, parameters, p, base= True, closed = True, base_grow = False, rent_control = False, grow_again=True)

