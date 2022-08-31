# rrt_star.py
# Author(s): Edvard Bruun

"""
Imports the :class:`~algorithm.rrt.RRT` class

Imports the :class:`~input.shape_circle.Circle` class

"""

import numpy as np

from algorithm.rrt import RRT
from input.shape_circle import Circle


class RRT_Star(RRT):
	""" A class for the RRT Star algorithm, which inherits from the :class:`~algorithm.rrt.RRT` abstract class.

	"""

	def __init__(self,domain_object,recorder,params):
		"""Initializes with abstract base class definition.
		
		Additional variables are initialized for the RRT Star algorithm. The first entry in any additional :class:`~solver.recorder.Recorder` object attributes are initialized.

		Example::

			self.recorder.parents_history[0,0:2] = -1	

		Attributes:
			neighbour_offset (:obj:`float`):
				A 10% increase modifier. Used to define the rectangular extents around a new vertex that will be used to select a subset of vertices to check if they are inside the circular neighborhood.

			neighbor_indices (:obj:`list` of :obj:`int`): 
				A list of the indices of the vertices that are found in the neighborhood of the newly generated vertex.

			neighbor_dist (:obj:`list` of :obj:`float`): 
				A list of the incremental path costs from all neighboring vertices to the newly generated vertex.	

		"""
		super().__init__(domain_object,recorder,params)
		self.neighbor_offset = 1.1 #10% larger radius to look in
		self.neighbor_indices = []
		self.neighbor_dist = []

		self.recorder.parents_history[0,0:2] = -1

	def rrt_step(self,trial, print_vertex=True):
		"""This function performs a single step/iteration using the RRT Star algorithm.

		Notes::

			Step 1. Find new configuration

			Step 2. Turn new configuration into a new vertex

			Step 3. Keep sampling new configurations until a new vertex creates a free edge
			
			Step 4. Record the iteration data (update: recorder.vertices)

			Step 5. Find the neighboring vertices in a radius around the new vertex

			Step 6. Connect the new vertex to a neighboring vertex that will lead to the shortest total path

			Step 7. Record the iteration data (update: recorder.parents, recorder.parents_history, recorder.costs lists)

			Step 8. Optimize the current solution by rewiring the vertex/edge graph to shorten paths

			Step 9. Record the iteration data (update: recorder.parents_history list)

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
		
		# Step 4. Record the iteration data (update: recorder.vertices list)
		self.recorder.vertices[trial,:] = self.new_v

		# Step 5. Find the neighboring vertices in a radius around the new vertex 
		self.find_vertices_in_neighborhood()

		# Step 6. Connect the new vertex to a neighboring vertex that will lead to the shortest total path
		self.new_parent,self.new_cost = self.find_parent_shortest_path()

		# Step 7. Record the iteration data (update: recorder.parents, recorder.parents_history, recorder.costs lists)
		self.recorder.parents[trial] = self.new_parent 
		self.recorder.parents_history[:,trial*2] = self.recorder.parents
		self.recorder.costs[trial] = self.update_path_cost(self.new_parent,self.new_cost)
	


		# Step 8. Optimize the current solution by rewiring the vertex/edge graph to shorten paths
		self.rewire(trial)

		# Step 9. Record the iteration data (update: recorder.parents_history list)
		self.recorder.parents_history[:,(trial*2 + 1)] = self.recorder.parents



	def find_vertices_in_neighborhood(self):
		""" This function finds the indices and distances to vertices that are found within a radius of the new vertex.

		A :class:`~input.shape_circle.Circle` object is initialized with the neighborhood distance specified by the user as its radius. The :meth:`~input.shape_circle.Circle.is_point_inside()` method is used to check which vertices fall inside this circular neighborhood.
		
		To reduce the number of points that need to be checked, the :meth:`~algorithm.rrt_star.RRT_Star.find_indices_in_extents()` is used to a find a subset of vertices.

		Indices of neighboring vertices are appended to the `neighbor_indices` list. Distances from the new vertex to the neighboring vertex are saved the the `neighbor_dist` list.

		"""
		del self.neighbor_indices[:]
		del self.neighbor_dist[:]

		neighbor_circle = Circle({
			'dim': 2,
			'shape_type':"circle",
			'radius':self.params["neighborhood"],
			'center':self.new_v})
		
		indices_in_box = self.find_indices_in_extents()
	
		for index in indices_in_box:

			point = self.recorder.vertices[index,:]

			if neighbor_circle.is_point_inside(point):

				dist_new = np.linalg.norm(point - self.new_v)

				self.neighbor_indices.append(index)
				self.neighbor_dist.append(dist_new)


	def find_indices_in_extents(self):
		""" This function finds a subset of vertex indices in a rectangular domain around the new vertex.

		Leveraging the computational speed of numpy array slicing to select a reduced set of vertices based on rectangular coordinates. As an additional buffer the rectangular extents are modified to be larger than the neighborhood radius by multiplying this value by the `neighbor_offset` variable.

		Returns:
			indices_in_box (:obj:`list` of :obj:`int`):
				The indices of vertices found in a rectangular extent around the new vertex.

		"""
		offset = self.neighbor_offset
		hx = [(self.new_v[0] - offset*self.params["neighborhood"]), (self.new_v[0] + offset*self.params["neighborhood"])]
		hy = [(self.new_v[1] - offset*self.params["neighborhood"]), (self.new_v[1] + offset*self.params["neighborhood"])]

		a = self.recorder.vertices[:,0] > hx[0]
		b = self.recorder.vertices[:,0] < hx[1]
		c = self.recorder.vertices[:,1] > hy[0]
		d = self.recorder.vertices[:,1] < hy[1]

		# indices of vertices found in bounding box
		indices_in_box =  [i for i, x in enumerate(a&b&c&d) if x]

		del indices_in_box[-1] #don't check last item since it's the new point itself

		return indices_in_box


	def find_parent_shortest_path(self):
		""" This function finds a vertex in the neighborhood that will lead to the lowest total cost to the new vertex.

		Calls the the :meth:`~algorithm.rrt.RRT.update_path_cost()` method to find the new total costs to go from any of the neighboring vertices to the new vertex. The :meth:`~algorithm.rrt.RRT.is_new_edge_blocked()` method is called to determine whether the new edge is unobstructed. 

		The lowest cost neighbor vertex that leads to an unobstructed edge becomes the parent for the new vertex.

		Returns:
			new_parent_index (:obj:`int`): The index of the vertex in the neighborhood that leads to the lowest cost unobstructed path to the new vertex
			new_parent_dist (:obj:`float`): The incremental cost (distance) between the parent and new vertex

		"""
		cost = 0.0
		lowest_cost = float('+inf') 

		for index,dist in zip(self.neighbor_indices, self.neighbor_dist):

			cost = self.update_path_cost(index,dist)

			if cost > lowest_cost:
				pass
			else:
				if not self.is_new_edge_blocked(self.new_v,self.recorder.vertices[index]):
					lowest_cost = cost
					new_parent_index = index
					new_parent_dist = dist

		return new_parent_index, new_parent_dist


	def rewire(self,trial):
		""" This function updates the vertex conectivity in the neighboring area to reduce overall path costs. 

		Checks to see if the total path from the new vertex to any of the remaining neighboring vertices leads to a shorter overall path. If it does then the connectivity of that neighboring vertex is changed so that the new vertex overwrites its old parent vertex.
		
		If a shorter path is found then the :meth:`~algorithm.rrt.RRT.is_new_edge_blocked()` method is called to determine whether the new edge is unobstructed. The vertex/edge connecticity is only rewired if the new edge is unobstructed.

		"""
		for index,dist in zip(self.neighbor_indices, self.neighbor_dist):

			if (self.recorder.costs[trial] + dist) < self.recorder.costs[index]:

				if not self.is_new_edge_blocked(self.new_v,self.recorder.vertices[index]):
					self.recorder.costs[index] = self.recorder.costs[trial] + dist
					self.recorder.parents[index] = trial

