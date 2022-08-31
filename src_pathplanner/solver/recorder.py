# recorder.py
# Author(s): Edvard Bruun

import numpy as np

class Recorder:
	"""This class acts as a container for the algorithm solution values.

	"""
	
	def __init__(self,params):
		"""Initialize the Recorder class.

		The attributes arrays are initialized to the length specified by the number of trials in the params dictionary passed. These arrays are initialized to value of :obj:`numpy.nan`. Algorithm specific attributes are initialized are created and initialized.

		Note:
			The input parameters dictionary is assigned to an instance attribute with same name.

		Parameters:
			params: Dictionary containing the user-specified algorithm parameters.

		Attributes:
			params: see Parameters	
					
			vertices (:obj:`numpy.ndarray` of :obj:`float`):
				A multi-column array of coordinates for the graph vertices. The number of rows is equal to the number of trials specified by the user. The number of columns is based on the dimensions of the solution space (2d=x,y and 3d=x,y,z) specified by the user.

			parents (:obj:`numpy.ndarray` of :obj:`float`):
				A single column array of indices for the parent of the vertex at the specified row index. Specifies the connectivity of the graph. The number of rows is equal to the number of trials specified by the user.

			costs (:obj:`numpy.ndarray` of :obj:`float`):
				A single column array of total cost (distance) to reach the vertex at the specified row index. The number of rows is equal to the number of trials specified by the user.

			parents_history (:obj:`numpy.ndarray` of :obj:`float`):
				algorithm specific variable (rrt_star). A multi-column array of indices for the parent of the vertex at the specified row index. This variable tracks the evolution of the graph connectivity during the solution, to be used for the plotting and animation modules. The number of rows is equal to the number of trials specified by the user. The number of columns is equal to 2 times the number of trials specified by the user. Two adjacent columns represent the connectivity of the graph before and after after re-wiring.

		Note:
			vertex `j` is connected to vertex `i`. Therefore the parent of vertex j is i, recorder.parents[j] == i

			record.parents_history[:,n] = the parent list (connectivity) of the graph before re-wiring in iteration n

			record.parents_history[:,n+1] = the parent list (connectivity) of the graph after re-wiring in iteration n

		"""
		self.params = params

		self.vertices = np.zeros((self.params["n_trials"],self.params["dim"]),
			dtype=float)
		self.vertices.fill(np.nan)

		self.parents = np.zeros(self.params["n_trials"], dtype=float)
		self.parents.fill(np.nan)

		self.costs = np.zeros(self.params["n_trials"], dtype=float)
		self.costs.fill(np.nan)

		if self.params["method"] == "rrt_star":
			self.parents_history = np.zeros((self.params["n_trials"],self.params["n_trials"]*2),
				dtype=float)
			self.parents_history.fill(np.nan)
