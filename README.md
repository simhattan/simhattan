# The Simhattan Project
***
Here are some notes for the SIMHATTAN MODEL 1.0. More details can be found in main text and appendix to
 "The Simhattan Project: An Agent-based Model of Housing Affordability" by Jason Barr (jmbarr@newark.rutgers.edu), Maryam Hosseini, and Daniel Scheer

You are free to use and maniputate the code. If you use the code for research please cite the paper.
CAVEAT EMPTOR: There are a lot of moving parts. This code runs for the purpose it was designed. We make no guarantees that it will function in the same 
manner if you make changes to the code. This code was last written in Spyder 5.1.5 (Jan 2022) and run in Python 3.7.7

Please email Jason Barr if any coding errors are found. 

Happy Simulating!

***
MAIN.py will run the simulation one time for an open city. It will use the parameters in Parmaters.py (more about this file below). 
So MAIN is a good way to get started with the code. If you want run the code for the first time simplye open Main.py and run it. You can change paramters like 
the number of agents, grid size, and costs in Parameter.py file.

POLICY_MENU.py is the key file to initiate different kinds of simulations. You choose one type of policy configureation. It then imports some parameter from a csv file and runs repeated simulations
and output the results in various csv files. You can also run the code for one generation using given paramters in Parameter file or you can run the code over multpile parameter sweeps
by importng a CSV file with different paramter values.

***
The basic structre of the simulation is as follows:
1. Start by running one of the above modules
2. It will read the Parameter.py which establishes things like # of agents, utility and profit functions, size of city, construction costs, transportation costs, etc. (and will important 
   the parameter CSV file if multiple parameter value runs are chosen)
3. Then it runs the simulation by calling the function run_sim() (or interator when running the POLICY_MENU)
4. If MAIN is run, then Run_sim.py module will run the rounds, where each round is a series of auctions for each cell. Agents bid on cells and decide what they are willing to pay
   and if they win the auction they move there.
5. After a round (ie. auction for each cell), the module calls the tear_down() function in Grid.py, where landlords decided if they want to tear down their properties
6. After convergence (i.e., no one wants to move or teardown), the run ends. 
7. If POLICY_MENU is run, then ITERATE.py is called if the user wants to run simulations over multiple paramter values. This runs the sims till convergence, then calls in a new set of paratemeters given in the csv file and runs the similuations again.
If the policy_menu dictates growth, each run for a given set of parameters repeated with more agents and with new policy changes.
8. Results are output into various csv files in Datacollecter.py and plots are given from Plot.py

***
Summary of the files (in alphabetical order):
- Agents.py creates the agents as objects (offices, merchants=owners, and workers). If multiple runs are called it adds new agents for population growth
- Auction.py runs the auction for a cell by taking bids, determining the winning bid, and putting the winner in the location (via eviction if necessary)
- Cell.py gives some formulas and keeps track of data at the grid cell level
- Datacollector.py keeps track of simulation output and results and will output them into csv files
- Employers.py is a module that assigns workers to firms
- Gridc.py has functions and keeps track of data related to all the grid cells.
- Grow_again.py intiates three runs: first run till convergence, then second run till convergence, then third run till convergence.
- Initialize.py intializes the city--it creates the grid and randomly distributes agents and calculates their intial values
- Iterate.py will run the simulaiton and iterate over different parameters cobminations, where some parameters are kept the same from the Parameter.py module
  and some are imported from a csv file.
- Main.py initiates one run
- Moore.py is used to collect information about cell neighbors within a "Moore neighborhood"
- Parameters.py give set of parameter of the model
- Plot.py generates some plots (e.g. heat maps, plots of agents locations, and 3D box plots)
- Policy_menu.py gives full range of policy options that we have programmed.
- Run_Sim.py will run the simulation when Main or Closedcity is called
- Superclass_Agent.py keeps track of the agents--their rents, their locations, their communting costs and transportation choices, etc.


NOTES:
The model is intended to be run on a square grid, so adjust the parameters accordingly.