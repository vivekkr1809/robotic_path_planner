# vertex.py
# Author(s): Edvard Bruun

import numpy as np

class Vertex():
	""" A class with methods for starting a new RRT iteration by generating a new vertex.

	"""

	@classmethod
	def new_config(cls,domain_object):
		""" This function returns a new random configuration (point) found in the domain area.

		Calls The :meth:`~input.shape.Shape.sample_random_point()` method to generate a random configuration within the shape that defines the domain.

		Parameters:
			domain_object (:obj:`~input.domain_class.Domain` object):
				Object representing the assembled solution domain.

		Returns:
			new_q (:obj:`numpy.ndarray` of :obj:`float`): The coordinates of the new random configuration.
		"""
		new_q = domain_object.domain.sample_random_point()
		return new_q

	@classmethod
	def new_vertex(cls, vertices, new_q, step_size):
		""" This function returns a new vertex in the domain area.

		Calls The :meth:`~algorithm.vertex.Vertex.find_nearest_vertex()` method to find the vertex in the current vertices list in the :obj:`~solver.recorder.Recorder` object that is closest to the randomly generated configuration point.

		The new vertex is generated along the straight line connecting the closest vertex to the new configuration. The new vertex is at a maximum distance specified in the step size parameter set by the user. If the new configuration falls closer than the step size distance then the configuration is taken as the new vertex.

		Parameters:
			vertices (:obj:`numpy.ndarray` of :obj:`float`):
				The current set of vertices that make up the solution.
			new_q (:obj:`numpy.ndarray` of :obj:`float`):
				The coordinates of the newly generated configuration.
			step_size ( :obj:`float`):
				The maximum distance between the closest vertex and the new vetex.					

		Returns:
			new_v (:obj:`numpy.ndarray` of :obj:`float`): The coordinates of the new vertex.

			index (:obj:`int`): The index of the new vertex's parent.

			distance (:obj:`int`): The distance between the parent and the new vertex.

		"""
		index, distance = cls.find_nearest_vertex(vertices, new_q)
		v_near = vertices[index]

		if distance < step_size:
			return new_q, index, distance
		else:
			vector = (new_q - v_near)/distance
			new_v = np.round(v_near + vector*step_size,6)
			return new_v, index, step_size

	@classmethod
	def find_nearest_vertex(self,vertex_list,new_q):
		"""  This function finds the closest vertex and its distance to a randomly generated configuration point.

		Parameters:
			vertices (:obj:`numpy.ndarray` of :obj:`float`):
				The current set of vertices that make up the solution.
			new_q (:obj:`numpy.ndarray` of :obj:`float`):
				The coordinates of the newly generated configuration.

		Returns:

			shortest_index (:obj:`int`): The index of the vertex that is closest to the new configuration.

			shortest_distance (:obj:`float`): The distance from the closest vertex to the new configuration.

		"""
		existing_vertex_list = vertex_list[~np.isnan(vertex_list).any(axis=1)]
		dist_norm = np.linalg.norm(existing_vertex_list-new_q, axis = 1)
		return np.argmin(dist_norm), dist_norm[np.argmin(dist_norm)]

