# rrt.py
# Author(s): Edvard Bruun

"""
Imports the :class:`~algorithm.vertex.Vertex` class

"""

from abc import ABC, abstractmethod
import numpy as np

from algorithm.vertex import Vertex


class RRT(ABC):
	""" An abstract base class for RRT algorithms. The defined attributes and functions are used across all RRT algorithms.
	"""
	@abstractmethod
	def __init__(self,domain_object,recorder,params):
		"""Initialize the RRT base class.

		The first entries in the :class:`~solver.recorder.Recorder` object are initialized to their starting values (representing the user-specifed origin/starting point of the algorithm).

		Example::

			self.recorder.vertices[0,:] = domain_object.origin

			self.recorder.parents[0] = -1

			self.recorder.costs[0] = 0


		Note:
			The input parameters dictionary is assigned to an instance attribute with same name. The domain and recorder objects are assigned to instance attributes of the same name to be accessed by the algorithm throughout the iterations.


		Parameters:
			domain_object (:obj:`~input.domain_class.Domain` object):
				Object representing the assembled solution domain.
			recorder (:obj:`~solver.recorder.Recorder` object):
				Object representing the initialized recorder.
			params: Dictionary containing the user-specified algorithm parameters.

		Attributes:
			domain_object: see Parameters
			recorder: see Parameters
			params: see Parameters

			new_q (:obj:`numpy.ndarray` of :obj:`float`):
				A single set of coordinates representing a new random configuration point generated at the start of an iteration. The number size of the array is based on the dimensions of the solution space (2d=x,y and 3d=x,y,z) specified by the user.
			new_v (:obj:`numpy.ndarray` of :obj:`float`):
				A single set of coordinates representing a new vertex generated during an iteration. To be saved to the :obj:`~solver.recorder.Recorder` object.
			new_parent (:obj:`int`):
				A single value representing the parent of the new vertex generated during an iteration. To be saved to the :obj:`~solver.recorder.Recorder` object.
			new_cost (:obj:`float`):
				A single value representing the incremental path cost (distance) from the parent to the new vertex generated during an iteration.				

		"""		
		self.domain_object = domain_object
		self.recorder = recorder
		self.params = params

		self.recorder.vertices[0,:] = domain_object.origin
		self.recorder.parents[0] = -1
		self.recorder.costs[0] = 0

		self.new_q = []
		self.new_v = []
		self.new_parent = []
		self.new_cost = []

	@abstractmethod
	def rrt_step(cls, i):
		""" This function executes a single step in the specified algorithm. Empty placeholder in abstract class definition since each algorithm defines a step in a different way.

		"""
		pass

	def new_config(self):
		""" This function returns a new random configuration point found in the domain area.

		Calls the :meth:`~algorithm.vertex.Vertex.new_config()` method.

		Returns:
			new_q (:obj:`numpy.ndarray` of :obj:`float`): The coordinates of the new random configuration.
		"""

		return Vertex.new_config(self.domain_object)

	def new_vertex(self):
		""" This function returns a new vertex based on the random configuration generated.

		Calls the :meth:`~algorithm.vertex.Vertex.new_vertex()` method.

		Returns:
			new_v (:obj:`numpy.ndarray` of :obj:`float`): The coordinates of the new vertex.

			new_parent (:obj:`int`): The index of the new vertex's parent.

			new_cost (:obj:`int`): The distance between the parent and the new vertex.

		"""
		return Vertex.new_vertex(
			self.recorder.vertices,
			self.new_q,
			self.params["step_size"]
		)

	def update_path_cost(self,new_parent,new_cost):
		""" This function returns the updated total path cost to a vertex.

		Given a parent index and new incremental distance, the total path cost for the new vertex is found  by referencing the total cost up to the parent froms the `costs` list in the :obj:`~solver.recorder.Recorder` object and adding the new distance to this value.
		
		Example::

			new_total_cost = self.recorder.costs[new_parent] + new_cost

		Parameters:
			new_parent (:obj:`int`): index of the parent for the new vertex.
			new_cost (:obj:`float`): incrememntal cost to go from parent to new vertex.

		Returns:
			new_total_cost (:obj:`float`): The total cost to reach the new vertex.

		"""
		return self.recorder.costs[new_parent] + new_cost


	def is_new_edge_blocked(self,v1,v2):
		""" This function checks whether a path between two vertices (edge) is blocked by an obstacle.
		
		Loops through the number of obstacles specified in the domain and checks whether the specified start and end points of an edge will be blocked. Calls the the :meth:`~input.shape.Shape.is_point_inside()` and :meth:`~input.shape.Shape.is_intersected_by_edge()` methods for the specific obstacle.

		Parameters:
			v1 (:obj:`numpy.ndarray` of :obj:`float`): coordinates of start vertex of a line.
			v2 (:obj:`numpy.ndarray` of :obj:`float`): coordinates of end vertex of a line.

		Returns:
			bool::

				True -- the edge is blocked
				False -- the edge is not blocked
		"""
		for obstacle in self.domain_object.obstacles:
			if(obstacle.is_point_inside(v1) or obstacle.is_point_inside(v2)):
				return True
			if(obstacle.is_intersected_by_edge(v1,v2)):
				return True
		return False

