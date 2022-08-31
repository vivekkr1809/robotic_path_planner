# solution.py
# Author(s): Edvard Bruun

"""
Imports the :class:`~solver.recorder.Recorder` class

Imports the :class:`~algorithm.rrt_basic.RRT_Basic` class

Imports the :class:`~algorithm.rrt_star.RRT_Star` class

"""
import numpy as np
from sys import exit

from solver.recorder import Recorder
from algorithm.rrt_basic import RRT_Basic
from algorithm.rrt_star import RRT_Star

class Solution:
	"""This class executes the path planning algorithm, and evaluates the completion of the path from the origin to the goals.
	"""

	def __init__(self,params,domain_object):
		"""Initialize the Solution class.

		Creates new Recorder object, which is initialized based on the params dictionary passed.

		Note:
			The input parameters dictionary is assigned to an instance attribute with same name.

		Parameters:
			params: Dictionary containing the user-specified algorithm parameters.
			domain (:obj:`~input.domain_class.Domain` object):
				Object containing the assembled solution domain.

		Attributes:
			params: see Parameters
			domain: see Parameters
			recorder (:class:`~solver.recorder.Recorder` object):
				Initialized recorder object with the given input parameters.	
			solution_path (:obj:`list` of :obj:`list` of :obj:`int`):
				Initialized as empty. Stores a path from origin to each goal in the form of vertex indices. A single path is generated for each goal.
			algorithm: Initialized as empty. Assigned the algorithm object, which is used to solve the path planning problem.
		
		"""
		self.params = params
		self.domain_object = domain_object

		self.recorder = Recorder(self.params)

		self.solution_path = [] 
		self.algorithm = []

	def run_algorithm(self, print_vertex=True):
		"""  This function runs through the full path planning algorithm.

		The chosen algorithm is initialized based on the input parameters. A single trial of the algorithm is executed in each iteration of the loop called in this function. The maximum number of trials is specified in the inout parameters.

		Note:
			Exits with an error if the user selects an algorithm that has not been implemented.	

		Calls the :meth:`RRT.rrt_step() <algorithm.rrt.RRT.rrt_step()>` function in the loop.

		"""
		if self.params["method"] == "rrt_basic":
			if print_vertex == True:
				print("-- Using Basic RRT Algorithm")
			self.algorithm = RRT_Basic(
				self.domain_object, 
				self.recorder,
				self.params
			)

		elif self.params["method"] == "rrt_star":
			print("-- Using RRT Star Algorithm")
			self.algorithm = RRT_Star(
				self.domain_object,
				self.recorder,
				self.params)
		else:
			exit("ERROR: No Valid Method")		

		for trial in range(1,self.params["n_trials"]):
			self.algorithm.rrt_step(trial,print_vertex)

	def process_vertex_list(self):
		"""  This function post-processes the full vertex list generated from completing the specified number of iterations.

		Iterates through the number of goals specified in the domain to find how many vertices in the :obj:`~solver.recorder.Recorder` object are within the goal area. Calls the :meth:`~solver.solution.Solution.check_if_goal_reached` function.

		Out of the vertices that have reached the goal it then find the index of the vertex that results in the lowest cost (most optimal) path to the goal. Calls the :meth:`~solver.solution.Solution.find_lowest_cost()` function.

		Appends the full lowest cost path (from origin to goal) returned by the :meth:`~solver.solution.Solution.find_path()` function to the `solution_path` variable.

		Note:
			If no vertex has reached the goal then the saved path is :obj:`numpy.nan`

		"""
		for goal in self.domain_object.goals:
			reached_goal_index = self.check_if_goal_reached(goal)

			if np.isnan(reached_goal_index[0]):
				index = reached_goal_index[0]
			else:
				index = self.find_lowest_cost(reached_goal_index)

			self.solution_path.append(self.find_path(index))

	def check_if_goal_reached(self,goal):
		"""  This function checks which vertices have reached a single goal.

		Uses the goal object's :meth:`~input.shape.Shape.is_point_inside()` method to find and save all the vertices that are inside and hence have reached the goal.

		Parameters:
			goal: A shape object specfied as the target for the algorithm.	
		Returns:
			reached_goal_index (:obj:`list` of :obj:`int`): A list of indices of all the vertices in the :obj:`~solver.recorder.Recorder` object that have reached the goal. This is set to the single value of :obj:`numpy.nan` if the goal is not reached.

		"""
		reached_goal_index = []

		for i, vertex in enumerate(self.recorder.vertices):
			if any(x == True for x in np.isnan(vertex)):
				return reached_goal_index
			else:
				if(goal.is_point_inside(vertex)):
					reached_goal_index.append(i)

		if len(reached_goal_index) == 0:
			reached_goal_index.append(np.nan)
			return reached_goal_index
		else:
			return reached_goal_index

	def find_lowest_cost(self,reached_goal_index):
		""" This function searches through a list of vertex indexes and returns the one with the lowest total path cost.

		Evaluates the total cost to reach each vertex specified in the input list, using the corresponding path costs in the :obj:`~solver.recorder.Recorder` object.

		Parameters:
			reached_goal_index (:obj:`list` of :obj:`int`): A list of indices of all the vertices in the :obj:`~solver.recorder.Recorder` object that have reached the goal.	
		Returns:
			lowest_cost_index (:obj:`int`): The index of the vertex with the lowest total path cost to the goal.

		"""
		cost = 0.0
		lowest_cost = float('+inf') 

		for index in reached_goal_index:

			cost = self.recorder.costs[index]

			if cost > lowest_cost:
				pass
			else:
				lowest_cost = cost
				lowest_cost_index = index

		return lowest_cost_index

	def find_path(self,index):
		"""  This function creates a list of indices of vertices that represent the lowest cost path from the origin to the end vertex.

		Finds the sequence of nodes working back from a specifed vertex index to the starting origin using the values by looping through the parents list, saved in the :obj:`~solver.recorder.Recorder` object. The loop terminates with the parent index of -1 is reached, which indicates the origin (has no parent).

		The list of vertex indices for the full path is appended to the `solution_path` variable.

		Parameters:
			index (:obj:`int`): The index of the end vertex.
		Returns:
			path_list(:obj:`list` of :obj:`int`): A list of ordered vertex indices for the path from the origin to end vertex.
		
		Note:
			Parent of vertex i is j, then recorder.parents[i] == j

			For the origin vertex, recorder.parents[0] == -1
		"""
		path_list = []
		path_list.append(index)
		child = index

		while child > 0:
			parent = int(self.recorder.parents[child])
			path_list.append(parent)
			
			child = parent #Set the parent index, as the child for next loop
		
		path_list.reverse()		

		return path_list