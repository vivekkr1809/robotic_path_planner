import unittest
from unittest.mock import Mock

import numpy as np

from algorithm.rrt_star import RRT_Star
from input.domain_class import Domain

domain_info = {
	'dim': 2, 
	'shape_type': 'rectangle',
	'lower_left': [0.0, 0.0],
	'upper_right': [3.0, 4.0]
	}

origin_goal_info = {
	'origin': [0.1, 0.1],
	'goals': {
		'goal_1': {'dim': 2, 'shape_type': 'circle', 'radius': 0.2, 'center': [0.3, 2.1]},
		'goal_2': {'dim': 2, 'shape_type': 'circle', 'radius': 0.1, 'center': [2.5, 3.5]}
		}
	}

obstacles_info = {
	'obstacle_1':{'dim': 2, 'shape_type': 'circle', 'radius': 0.1, 'center': [0.5, 0.5]},
	'obstacle_2': {'dim': 2, 'shape_type': 'circle', 'radius': 0.2, 'center': [1.5, 3.5]},
	'obstacle_3': {'dim': 2, 'shape_type': 'circle', 'radius': 0.4, 'center': [1.5, 0.5]}
	}

rrt_algorithm_info = {
	'method': 'rrt_star',
	'n_trials': 100,
	'step_size': 0.2,
	'dim': 2,
	'neighborhood': 0.3
	}


domain_test = Domain(domain_info, obstacles_info, origin_goal_info)

recorder = Mock()

class TestRRT_Star(unittest.TestCase):
	def setUp(self):

		recorder.vertices = np.zeros((6,2), dtype=float)
		recorder.vertices.fill(np.nan)

		recorder.parents = np.zeros(6, dtype=float)
		recorder.parents.fill(np.nan)

		recorder.costs = np.zeros(6, dtype=float)
		recorder.costs.fill(np.nan)

		recorder.parents_history = np.zeros((6,6*2), dtype=float)
		recorder.parents_history.fill(np.nan)

		self.algorithm = RRT_Star(domain_test, recorder, rrt_algorithm_info)

	def tearDown(self):
		self.algorithm = None


	def test_rrt_star_00_vertices_increment(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[np.nan, np.nan],
			[np.nan, np.nan],
			[np.nan, np.nan]]
		)	

		step = 3
		self.algorithm.rrt_step(step)

		bool_array = (np.isnan(self.algorithm.recorder.vertices))
		bool_index = np.where(bool_array == False)
		index = np.amax(bool_index[0])

		self.assertEqual(step,index,"vertices list not incremented")

		step += 1
		self.algorithm.rrt_step(step)

		bool_array = (np.isnan(self.algorithm.recorder.vertices))
		bool_index = np.where(bool_array == False)
		index = np.amax(bool_index[0])
		self.assertEqual(step,index,"vertices list not incremented")	


	def test_rrt_star_01_parents_increment(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[np.nan, np.nan],
			[np.nan, np.nan]]
		)	

		step = 4
		self.algorithm.rrt_step(step)

		bool_array = (np.isnan(self.algorithm.recorder.parents))
		bool_index = np.where(bool_array == False)
		index = np.amax(bool_index[0])

		self.assertEqual(step,index,"parents list not incremented")

		step += 1
		self.algorithm.rrt_step(step)

		bool_array = (np.isnan(self.algorithm.recorder.parents))
		bool_index = np.where(bool_array == False)
		index = np.amax(bool_index[0])

		self.assertEqual(step,index,"parents list not incremented")


	def test_rrt_star_02_costs_increment(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[np.nan, np.nan],
			[np.nan, np.nan]]
		)
		
		step = 4
		self.algorithm.rrt_step(step)

		bool_array = (np.isnan(self.algorithm.recorder.costs))
		bool_index = np.where(bool_array == False)
		index = np.amax(bool_index[0])
		self.assertEqual(step,index,"costs list not incremented")

		step += 1
		self.algorithm.rrt_step(step)

		bool_array = (np.isnan(self.algorithm.recorder.costs))
		bool_index = np.where(bool_array == False)
		index = np.amax(bool_index[0])
		self.assertEqual(step,index,"costs list not incremented")

	def test_rrt_star_03_indices_extents1(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[1.0,1.39],
			[np.nan, np.nan]]
		)	

		self.algorithm.new_v = [1.0,1.39]

		indices = self.algorithm.find_indices_in_extents()

		self.assertEqual(indices,[1,2,3],"correct indices in the extents not returned")

	def test_rrt_star_04_indices_neighbor1(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[1.0,1.39],
			[np.nan, np.nan]]
		)	

		self.algorithm.new_v = [1.0,1.39]

		self.algorithm.find_vertices_in_neighborhood()

		self.algorithm.neighbor_dist = [ round(elem, 6) for elem in self.algorithm.neighbor_dist]

		self.assertEqual(self.algorithm.neighbor_indices,[1,2,3],"correct indices in the neighborhood not returned")
		self.assertEqual(self.algorithm.neighbor_dist,[0.09,0.01,0.06],"distances from neighbor to point incorrect")

	def test_rrt_star_05_indices_extents2(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[1.0,1.779],
			[np.nan, np.nan]]
		)	

		self.algorithm.params["neighborhood"] = 0.3
		self.algorithm.neighbor_offset = 1.1
		self.algorithm.new_v = [1.0,1.779]

		indices = self.algorithm.find_indices_in_extents()

		self.assertEqual(indices,[3],"corrent indices in the extents not returned")

	def test_rrt_star_06_indices_neighbor2(self):
		self.algorithm.recorder.parents = np.array([-1,0,0,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.2,3.2,1.4,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[1.0,1.779],
			[np.nan, np.nan]]
		)	

		self.algorithm.params["neighborhood"] = 0.3
		self.algorithm.neighbor_offset = 1.1
		self.algorithm.new_v = [1.0,1.779]

		self.algorithm.find_vertices_in_neighborhood()

		self.assertEqual(self.algorithm.neighbor_indices,[],"corrent indices in the neighborhood not returned")
		self.assertEqual(self.algorithm.neighbor_dist,[],"distances from neighbor to point incorrect")


	def test_rrt_star_07_parent_shortest_path(self):
		self.algorithm.recorder.parents = np.array([-1,0,1,2,np.nan,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.3,1.4,1.5,np.nan,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[1.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[0.9, 1.40],
			[np.nan, np.nan]]
		)	

		self.algorithm.new_v = [0.9,1.4]

		self.algorithm.neighbor_indices = [1,2,3]
		self.algorithm.neighbor_dist= [10,0.1,10]

		new_parent_index, new_parent_dist = self.algorithm.find_parent_shortest_path()

		new_parent_dist = round(new_parent_dist,6)

		self.assertEqual(new_parent_index,2,"closest parent index incorrect")
		self.assertEqual(new_parent_dist,0.1,"distances to new parent incorrect")

	def test_rrt_star_08_rewire(self):
		self.algorithm.recorder.parents = np.array([-1,0,1,2,2,np.nan])
		self.algorithm.recorder.costs = np.array([0.0,1.7,1.4,1.9,1.5,np.nan])

		self.algorithm.recorder.vertices = np.array(
			[[1.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.45],
			[0.9, 1.40],
			[np.nan, np.nan]]
		)	

		self.algorithm.new_v = [0.9,1.4]

		self.algorithm.neighbor_indices = [1,2,3]
		self.algorithm.neighbor_dist= [0.1,0.1,0.1]

		self.algorithm.rewire(trial=4)

		self.assertTrue(np.allclose([-1,4,1,4,2],self.algorithm.recorder.parents[0:5]),"rewire parents list incorrect")
		self.assertTrue(np.allclose([0,1.6, 1.4, 1.6, 1.5],self.algorithm.recorder.costs[0:5]),"distances to new parent incorrect")


if __name__ == '__main__':
	unittest.main()