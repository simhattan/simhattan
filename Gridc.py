#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE: GRIDC
Created on Fri Nov 17 03:04:38 2017

@author: MarMah
"""
from Cell import Cell
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.path import Path
import matplotlib.pyplot as plt
#from iteration_utilities import flatten
import random

class Gridc(object) :
    """The grid of the game. 

    Longer class information....
    Longer class information....

    Attributes:
        cell: 
        grid: 
        
    """
    def __init__(self, width, height, parameters, close=None) :

        self.cell = [[i, j] for i in range(width) for j in range(height)]
        for i in range(width * height) :
            self.cell[i] = Cell(parameters)
        for i, j in enumerate(self.cell) :
            j.active = True
            j.position = [[i, j] for i in range(width) for j in range(height)][i]
        self.grid = [j.position for i, j in enumerate(self.cell)]
        self.convergence_count = 0
        self.active_grid = [j.position for i, j in enumerate(self.cell) if self.cell[i].active]
        self.total_vacancy = len(self.active_grid)
        self.total_floors = len(self.active_grid)
        self.nonempty_floors = 0
        self.nonempty_vacancy = 0

    def alternate_grid(self, points, expansion=False):
        """Create an alternate Grid
        This method is used to create a costomized grid
        Assigns the correct postion and creates the grid list
        based on the given points . 
        This can be used for closing the city 
        
        Args:
           points: A list of the points we want to have in our grid 
            
        Returns:
            Makes the cell not in the list of points, inactive (active = False)    
        """ 
        if expansion:
            for c in points:
                if c not in self.active_grid:
                    self.cell[self.grid.index(c)].active = True
            for l in self.cell:
                if l.position not in points:
                    l.active = False
        else:
            for c in self.cell:
                if c.position not in points:
                    c.active = False

        self.active_grid = [j.position for i, j in enumerate(self.cell) if self.cell[i].active]

    def find_empty(self, cell, d, parameters, exclusive=False):
        """
        Finds the empty blocks in the moore neighbors of a given agent 
        based on the given d  
        
        Args:
            cell: index of the cell we want the empty cells around 
            d: the distance that the neighbors are counted from
            parameters: an instance of class Parameters
            exclusive:  optional argument that if set equals to True, will
                        return the moore neighbors of the cell by removing 
                        the previous moores calculated before. 
            
        Returns:
            A list of indices of the empty blocks
        """
        if exclusive:
            cell_moore = self.cell[cell].moore_neighbor(d, parameters, exclusive=True)
        else:
            cell_moore = self.cell[cell].moore_neighbor(d, parameters)

        empty_lots = [self.grid.index(lot) for lot in cell_moore if
                          self.cell[self.grid.index(lot)].available_place]
        if len(empty_lots) == 0:
            return self.find_empty(cell, d + 1, parameters, exclusive=True)
        else:
            return empty_lots

    def new_random_block(self, parameters, lst=False):
        """
        Finds a random available block 
        
        Returns:
            A new random block in form of [i,j] point. 
        """
        if lst :
            lots = [self.grid.index(point) for point in self.active_grid
                    if self.cell[self.grid.index(point)].available_place]
            return lots
        else:
            random_block = np.random.choice([self.grid.index(point) for point in self.active_grid 
                                             if self.cell[self.grid.index(point)].available_place])
            if self.cell[random_block].availability(1):
                return self.grid[random_block]
            else:
                return self.new_random_block(parameters)
            
    def find_closest(self, agent, d, parameters, closed=False) :
        """
        Finds the closest block for the given agent
        based on the given d  
        Args:
            agent: The instance of the class Agents that we want
                    to find a new closest location for 
            d: the distance that the neighbors are counted from
            parameters: an instance of class Parameters
        Returns:
            A new block in form of [i,j] point. 
        
        """
        if closed: 
            lots = self.new_random_block(parameters, lst=True)
            random_lot = np.random.choice([lot for lot in lots if agent.location != self.grid[lot]])
            return self.grid[random_lot]
        else:
            if d > 7:
                closest_block = self.grid.index(self.new_random_block(parameters))
            else:
                empty_lots = self.find_empty(self.grid.index(agent.location), d, parameters)
                if len(empty_lots) == 1 :
                    closest_block = empty_lots[0]
                else:
                    if agent.type != "Office" :
                        distance_to_work = [agent.calc_block_distance(self.grid[blocks]) for blocks in empty_lots]
                        closest_to_work_index = distance_to_work.index(min(distance_to_work))
                        closest_block = empty_lots[closest_to_work_index]
                    else:
                        closest_block = np.random.RandomState(parameters.seed).choice(empty_lots)
            return self.grid[closest_block]

    def count_teardowns(self):
        n = 0
        for i in range(len(self.cell)):
            n += self.cell[i].num_tear_downs
        return n

    def count_nonempty_buildings(self):
        n = 0
        for i in range(len(self.cell)):
            if len(self.cell[i].occupants) > 0:
                n += 1
        return n

    @property
    def update_grid_data(self):
        self.total_vacancy = sum(self.cell[self.grid.index(i)].vacancy for i in self.active_grid)
        self.total_floors = sum(self.cell[self.grid.index(i)].floors for i in self.active_grid)
        self.vacancy_avg

    @property
    def vacancy_avg(self):
        if self.nonempty_floors > 0:
            return self.nonempty_vacancy/self.nonempty_floors #self.total_vacancy/self.total_floors
        else:
            return 0

    def avg_nonempty_bheight(self):
        avg_ne_height = np.mean(
            np.array([self.cell[i].floors for i in range(len(self.cell)) if len(self.cell[i].occupants) > 0]))
        return avg_ne_height

    def tallest_nonempty_b(self):
        tallest = np.max(
            np.array([self.cell[i].floors for i in range(len(self.cell)) if len(self.cell[i].occupants) > 0]))
        return tallest

    @property
    def avg_height(self):
        avg_height = self.total_floors/len(self.cell)
        return avg_height

    def city_area(self, points):
        hull = ConvexHull(points)
        city_area = hull.area
        return city_area

    def convex_hull(self, parameters, pplot=False, closed_city=False):
        '''
        :param parameters:

        :param pplot:
        :param closed_city: if true, it will return the points within the convex hull
                            if false, it will return the (i,j) points of the not vacant cells
        :return:
        '''
        points = np.array(
            [tuple(self.cell[i].position) for i in range(len(self.cell)) if len(self.cell[i].occupants) > 0])
        
        hull = ConvexHull(points)
        hull_path = Path(points[hull.vertices])
        cc = [i for i in self.grid if hull_path.contains_point(tuple(i)) == True]
        close_city = [list(x) for x in set(tuple(x) for x in points) | set(tuple(x) for x in cc)]
        if pplot:
            plt.plot(points[:, 0], points[:, 1], 'o')
            for simplex in hull.simplices :
                plt.plot(points[simplex, 0], points[simplex, 1], 'r--', lw=3)
            plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'r--', lw=3)
            plt.plot(points[hull.vertices[0], 0], points[hull.vertices[0], 1], 'ro')
            plt.axis([0, parameters.grid_height, 0, parameters.grid_height])
            plt.show()
        else:
            if closed_city:
                return close_city
            else:
                return points

    def expansion(self, points, d, parameters):
        '''
        expands the points passed by certain radius

        points: must be np array the outer points of the city center
        d: the radius of expansion
        return:
            expanded grid (the outer points to set the new grid
        '''
        expanded = []
        hull = ConvexHull(points)
        hull_path = Path(points[hull.vertices])
        mini, maxi = (hull_path.get_extents()).get_points()
        middle_point = [(maxi[0] + mini[0])/2, (maxi[1] + mini[1])/2]

        for point in points:
            if point[0] < middle_point[0]:
                ex = point[0] - d
            else:
                ex = point[0] + d
            if point[1] < middle_point[1]:
                ey = point[1] - d
            else:
                ey = point[1] + d
            expanded.append([ex, ey])
        expanded = np.array(expanded)
        hull1 = ConvexHull(expanded)
        hull_path = Path(expanded[hull1.vertices])
        cc = [i for i in self.grid if hull_path.contains_point(tuple(i))]
        return cc

    def custom_vacancy(self, custom):
        # for custom pass the indices
        vac = []
        for celli in custom:
            if self.cell[celli].vacancy > 0:
                vac += self.cell[celli].vacancy
        return vac

    def cc_vacancy(self, points):
        vac = 0
        floors = 0
        for i in points:
            floors += self.cell[self.grid.index(i)].floors
            vac += self.cell[self.grid.index(i)].vacancy
        return [vac, vac/floors]

    def height_cap_fn(self, lot, d, parameters):
        '''
         Computes the average height of the moore neighbors of each cell and round it up
        Args:
            lot: the index of the cell
            d: the  radius of the neighborihng cells
            parameters: an instance of the class parameters
        Returns:
            The average height
        '''
        moore = self.cell[lot].moore_neighbor(d, parameters)
        moore.append(self.cell[lot].position)

        height = np.array([self.cell[self.grid.index(point)].floors for point in moore])

        average_height = int(np.ceil(np.mean(height)))

        # parameters.height_cap = average_height
        return average_height

    def impose_height_cap (self, d, parameters, unified=None):
        '''
            Impose the height cap on each cell, based on the height cap fn
            sets the height_cap attributes of the cells to the calculated number

            d: the radius of the moore neighbors
            parameters: an instance of class parameters
            
            unified: if passed will set the passed number as the height cap for all the cells
        '''
        for block in self.active_grid:
            if not unified: 
                self.cell[self.grid.index(block)].height_cap = self.height_cap_fn(self.grid.index(block), d, parameters)
            else:
                self.cell[self.grid.index(block)].height_cap = unified 
