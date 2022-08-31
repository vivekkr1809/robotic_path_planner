# rrt_basic.py
# Author(s): Edvard Bruun

"""
Imports the :class:`~algorithm.rrt.RRT` class

"""

import numpy as np

from algorithm.rrt import RRT

class RRT_Basic(RRT):
	""" A class for the Basic RRT algorithm, which inherits from the :class:`~algorithm.rrt.RRT` abstract class.

	"""
	def __init__(self,domain_object,recorder,params):
		"""Initializes with abstract base class definition.
		"""
		super().__init__(domain_object,recorder,params)

	def rrt_step(self,trial, print_vertex=True):
		"""This function performs a single step/iteration using the Basic RRT algorithm.

		Notes::

			Step 1. Find new configuration

			Step 2. Turn new configuration into a new vertex

			Step 3. Keep sampling new configurations until a new vertex creates a free edge
			
			Step 4. Record the iteration data (update: recorder.vertices, recorder.parents, recorder.costs lists)

		"""
		if print_vertex == True:
			print("-- -- Calculating Vertex:", trial+1)

		# Step 1. Find new configuration
		self.new_q = self.new_config()

		# Step 2. Turn new configuration into a new vertex
		self.new_v, self.new_parent, self.new_cost = self.new_vertex()
		
		# Step 3. Keep sampling new configurations until a free edge is created with new vertex
		while self.is_new_edge_blocked(self.recorder.vertices[self.new_parent],self.new_v):  
		  self.new_q = self.new_config()
		  self.new_v, self.new_parent, self.new_cost = self.new_vertex()

		# Step 4. Record the iteration data (update: recorder.vertices, recorder.parents, recorder.costs lists)
		self.recorder.vertices[trial,:] = self.new_v
		self.recorder.parents[trial] = self.new_parent
		self.recorder.costs[trial] = self.recorder.costs[self.new_parent] + self.new_cost

