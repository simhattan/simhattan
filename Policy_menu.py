# -*- coding: utf-8 -*-
"""
File: POLICY MENU

Created on Mon Aug  5 08:24:31 2019

@author: Jason
"""

import pandas as pd 
from Iterate import iterate 
from Parameters import Parameters

gen_run = 0

""" ********* PF Files ************ 

- PF_N20 is n=20, new=10, randomize costs

*******************************"""
"""
if pRun==0, it runs one of given files below 
     - "C" files do runs over agents holding costs contant (e.g C8 is C=8)
     - "N" files do runs over costs for fixed N, number of agents (N20=workers set at 20, agents=60)
     
if pRun ==1 that uses a small CSV file with varying agents and costs

if pRun ==2 , it runs one time with paramters from Paramter.py file
"""
pRun = 1

if pRun==0:
    a = 0
    #p = pd.read_csv('./PF_N20.csv')
    p =  pd.read_csv('./PF_C3.csv')
    #p =  pd.read_csv('./PF_C5.csv')
    #p =  pd.read_csv('./PF_C6.csv')
    #p =  pd.read_csv('./PF_C8.csv')
    #p =  pd.read_csv('./PF_N30_500.csv')
    
elif pRun==1:
    a = 0
    p = pd.read_csv('./PF.csv') # "PF.csv' has few paramaters values. Good for a relatively quick paramter sweep

elif pRun==2:
    a = 1
    p = [0]
        
parameters = Parameters()

""" ***********************************************
*** ********** Policy Menu ************************
*** ***********************************************
** Base city
1: Run open city once
2: Run open city once with height cap (must be fixed number set in #2)
3: Run open city once with rent control
4: Run open city once with heigh cap and rent control

** Grow city one time **
100: Base then grow (no policies)
101: Base then height cap
102: Base then rent control   
103: Base then close only
104: Base then close & height cap
105: Base then close, height cap, rent control
106: Height cap in base (set to 10), then grow closed, height cap average
* note that probably need to add heightcap_0 and height_cap_1


** Base, Grow, Grow **
1000: Base then grow, then grow again
1001: Base, close, open
1002: Base, close, close
1005: Base, close & height cap, open & no cap 

1010: Base, Full monty, keep full monty                        
1012: Base, Full monty, open and keep RC&HC                     
1014: Base, Full monty, keeped close and get rid of RC&HC       
1016  Base, Full monty, keep closed and keep RC get rid of HC   
1018  Base, Full monty, keep closed and keep HC get rid of RC   
1020  Base, Full monty, get rid of all         
1022  Base, Full monty, get rid of all, but set costs to 4 
1024  Base, full monty, no zoning and set costs to 4      
1026  Base. full monty, keep all, costs to 4       
*************************************************** """

# **********************************************************
# ******* set policy_num to one from the menu  *************
# **********************************************************
policy_num = 1001
# **********************************************************
# **********************************************************

"""
calling iterate is what runs the various generations
iterate determines how the whole thing will run
The function determines if the city is to grow or not and the policies
iterate( gen_run, policy_num,  parameters, p, base= False, closed=False, base_grow=False, 
            rent_control_0 = False, rent_control_1 = False,  height_cap = False, grow_again = False):
    
** Note for One Generation only **   
base=True means run the model one time using the basic model

** Note for Two Generations **
No City Wall: base_grow = True means grow the city in cases where where there is no city wall closure
Add City Wall: Runs base=True & closed=True. Closed then calls "closed function and then adds 
                pop based on # of available units. THe close function also includes height cap/zoning and rent control"

*** Note for Three Generations
Runs Based Grow=True and grow_again = True
"""

if policy_num < 100:
    
    if policy_num == 1:
        iterate(a, gen_run, policy_num, parameters, p, base = True)
    
    elif policy_num == 2:
        parameters.height_cap = float(5) 
        iterate(a, gen_run, policy_num, parameters, p, base = True)
    
    elif policy_num == 3:
        iterate(a, gen_run, policy_num, parameters, p, base = True, rent_control_0 = True)
    
    else:
        parameters.height_cap = float(7) 
        iterate(a, gen_run, policy_num, parameters, p, base = True, rent_control_0 = True)


elif policy_num < 1000:
    
    if policy_num == 100:
      iterate(a, gen_run, policy_num, parameters, p, base_grow = True)
    
    elif policy_num == 101:
        # note in this scenario - it implements zoning in the second round
        # other versions of height cap must be implemented 'by hand'
        iterate(a, gen_run, policy_num, parameters, p, base_grow = True, height_cap = True)
    
    elif policy_num == 102:
        iterate(a, gen_run, policy_num, parameters, p, base_grow = True, rent_control_1 = True)
    
    elif policy_num == 103:
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True)
        
    elif policy_num == 104: 
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, height_cap = True)        
        
    elif policy_num == 105: 
        iterate(a,gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True)

    elif policy_num == 106: 
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, height_cap = True)        

else:
    if policy_num == 1000:
        iterate(a, gen_run, policy_num,  parameters, p,  base_grow = True, grow_again = True)
    
    elif policy_num == 1001: 
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, grow_again = True )
    
    elif policy_num == 1002:
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, grow_again = True )       

    elif policy_num == 1005:
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, height_cap = True, grow_again = True )

    elif policy_num == 1010:
        #1010: Base, Full monty, keep full monty
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1012:
        #1012: Base, Full monty, open and keep RC&HC 
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1014:
        #1014: Base, Full monty, close and no RC&HC
        # SEEMS SOME PROBLEM HERE
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1016:
        #1016  Base, Full monty, keep closed and keep RC get rid of HC
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1018:
        #1018  Base, Full monty, keep closed and keep HV get rid of RC
         iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1020:
        #1020  Base, Full monty,  get rid of all
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1022:
        #1022  Base, Full monty,  get rid of all, but set costs to 4
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1024:
        #1022  Base, Full monty,  get rid of all, but set costs to 4
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )

    elif policy_num == 1026:
        #1022  Base, Full monty,  get rid of all, but set costs to 4
        iterate(a, gen_run, policy_num, parameters, p, base = True, closed = True, rent_control_1 = True, height_cap = True, grow_again = True )
       
 





