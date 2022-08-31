import unittest
from unittest.mock import Mock

import numpy as np

from algorithm.rrt_basic import RRT_Basic
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
	'method': 'rrt_basic',
	'n_trials': 100,
	'step_size': 0.2,
	'dim': 2,
	'neighborhood': 0.3
	}


domain_test = Domain(domain_info, obstacles_info, origin_goal_info)

recorder = Mock()


class TestRRT_Basic(unittest.TestCase):
	def setUp(self):

		recorder.vertices = np.zeros((6,2), dtype=float)
		recorder.vertices.fill(np.nan)

		recorder.parents = np.zeros(6, dtype=float)
		recorder.parents.fill(np.nan)

		recorder.costs = np.zeros(6, dtype=float)
		recorder.costs.fill(np.nan)

		self.algorithm = RRT_Basic(domain_test, recorder, rrt_algorithm_info)

	def tearDown(self):
		self.algorithm = None


	def test_rrt_basic_00_vertices_increment(self):
		self.algorithm.recorder.vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.50],
			[np.nan, np.nan],
			[np.nan, np.nan]]
		)	

		step = 4
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
		

	def test_rrt_basic_01_parents_increment(self):
		self.algorithm.recorder.parents = np.array([0,1,3,np.nan,np.nan,np.nan])

		step = 3
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


	def test_rrt_basic_02_costs_increment(self):
		self.algorithm.recorder.costs = np.array([0.0,3.5,np.nan,np.nan,np.nan,np.nan])

		step = 2
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


	def test_rrt_abstract_00_edge_blocked(self):

		v1 = [0.5,0.7]
		v2 = [0.5,0.3]

		blocked = self.algorithm.is_new_edge_blocked(v1,v2)

		self.assertTrue(blocked,"line should return blocked")

	def test_rrt_abstract_01_edge_notblocked(self):

		v1 = [0.39,0.7]
		v2 = [0.39,0.3]

		blocked = self.algorithm.is_new_edge_blocked(v1,v2)

		self.assertFalse(blocked,"line should return not blocked")

	def test_rrt_abstract_02_updatecost(self):
		self.algorithm.recorder.costs = np.array([0.0,3.5,2.4,6.7])

		new_parent = 2
		new_cost = 1.7

		cost_update= self.algorithm.update_path_cost(new_parent,new_cost)

		self.assertEqual(cost_update,4.1,"line should return not blocked")



if __name__ == '__main__':
	unittest.main()