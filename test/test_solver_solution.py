import unittest
from unittest.mock import Mock

import numpy as np

from solver.solution import Solution
from solver.recorder import Recorder
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
	'obstacle_1':{'dim': 2, 'shape_type': 'circle', 'radius': 0.2, 'center': [0.5, 3.5]},
	'obstacle_2': {'dim': 2, 'shape_type': 'circle', 'radius': 0.2, 'center': [1.5, 3.5]},
	'obstacle_3': {'dim': 2, 'shape_type': 'circle', 'radius': 0.4, 'center': [1.5, 0.5]}
	}

rrt_algorithm_info = {
	'method': 'rrt_basic',
	'n_trials': 5,
	'step_size': 0.2,
	'dim': 2,
	'neighborhood': 0.3
	}

domain_test = Domain(domain_info, obstacles_info, origin_goal_info)	

print(domain_test.goals)

class TestSolution(unittest.TestCase):
	def setUp(self):
		self.solution = Solution(rrt_algorithm_info,domain_test)

	def tearDown(self):
		self.solution = None


	def test_solution_00_goal_check_multiple(self):
		origin_goal_info = {
			'origin': [0.1, 0.1],
			'goals': {
				'goal_1': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [1.0, 1.1]}
				}
			}		

		domain_test = Domain(domain_info, obstacles_info, origin_goal_info)
		self.solution = Solution(rrt_algorithm_info,domain_test)

		self.solution.recorder.vertices = np.array(
			[[0.5, 1.0],
			[1.0, 1.09],
			[1.0, 1.05]]
		)

		#self.solution.recorder.parents = np.array([[-1 0,0]])

		a = self.solution.check_if_goal_reached(domain_test.goals[0])

		self.assertEqual(a,[1,2],"index list of goal vertex wrong")


	def test_solution_01_goal_check_none(self):
		origin_goal_info = {
			'origin': [0.1, 0.1],
			'goals': {
				'goal_1': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [1.0, 1.1]}
				}
			}		

		domain_test = Domain(domain_info, obstacles_info, origin_goal_info)
		self.solution = Solution(rrt_algorithm_info,domain_test)

		self.solution.recorder.vertices = np.array(
			[[0.5, 1.0],
			[0.5, 1.09],
			[0.5, 1.05]]
		)

		a = self.solution.check_if_goal_reached(domain_test.goals[0])

		self.assertTrue(np.isnan(a),"index of goal vertex wrong")


	def test_solution_02_findpath1(self):
		self.solution.recorder.parents = np.array([-1, 0, 4, 1, 3, 3])

		index = 2
		a = self.solution.find_path(index)

		self.assertTrue(a == [0, 1, 3, 4, 2], "goal path incorrect")


	def test_solution_03_findpath2(self):
		self.solution.recorder.parents = np.array([-1, 0, 4, 1, 3, 3])

		index = 5
		a = self.solution.find_path(index)

		self.assertTrue(a == [0, 1, 3, 5], "goal path incorrect")


	def test_solution_04_findpath3(self):
		self.solution.recorder.parents = np.array([-1, 0, 4, 1, 3, 3])

		index = 1
		a = self.solution.find_path(index)

		self.assertTrue(a == [0, 1], "goal path incorrect")	

	def test_solution_05_findpath4(self):
		self.solution.recorder.parents = np.array([-1, 0, 4, 1, 3, 3])

		index = 0
		a = self.solution.find_path(index)

		self.assertTrue(a == [0], "goal path incorrect")	


	def test_solution_06_findpath5(self):
		self.solution.recorder.parents = np.array([-1, 0, 4, 1, 3, 3])

		index = np.nan
		a = self.solution.find_path(index)

		self.assertTrue(np.isnan(a), "goal path incorrect")


	def test_solution_07_solutionpath(self):
		origin_goal_info = {
			'origin': [0.1, 0.1],
			'goals': {
				'goal_1': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [1.0, 1.41]},
				'goal_2': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [1.0, 3.10]},
				'goal_3': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [1.0, 1.71]},
				}
			}		

		domain_test = Domain(domain_info, obstacles_info, origin_goal_info)
		self.solution = Solution(rrt_algorithm_info,domain_test)

		self.solution.recorder.vertices = np.array(
			[[1.0, 1.20],
			[1.0, 1.30],
			[1.0, 1.40],
			[1.0, 1.50],
			[1.0, 1.60],
			[1.0, 1.70]]
		)

		self.solution.recorder.costs = np.array([0, 21, 31.2, 10.0, 3.2, 4.0])
		self.solution.recorder.parents = np.array([-1, 0, 4, 1, 3, 3])

		self.solution.process_vertex_list()

		self.assertEqual(len(self.solution.solution_path), 3,
			"not enough path lists saved")
		

	def test_solution_08_runalgorithm_basic(self):
		rrt_algorithm_info['method'] = "rrt_basic"
		self.solution = Solution(rrt_algorithm_info,domain_test)

		self.solution.run_algorithm()

		self.assertFalse(np.all(np.isnan(self.solution.recorder.vertices)),
						"vertices, not fully filled")

		self.assertFalse(np.all(np.isnan(self.solution.recorder.parents)),
						"parents, not fully filled")

		self.assertFalse(np.all(np.isnan(self.solution.recorder.costs)),
						"costs, not fully filled")		


	def test_solution_09_runalgorithm_star(self):
		rrt_algorithm_info['method'] = "rrt_star"
		self.solution = Solution(rrt_algorithm_info,domain_test)

		self.solution.run_algorithm()

		self.assertFalse(np.all(np.isnan(self.solution.recorder.vertices)),
						"vertices, not fully filled")

		self.assertFalse(np.all(np.isnan(self.solution.recorder.parents)),
						"parents, not fully filled")

		self.assertFalse(np.all(np.isnan(self.solution.recorder.costs)),
						"costs, not fully filled")	


	def test_solution_10_unknown_method(self):
		rrt_algorithm_info['method'] = "unknown"
		self.solution = Solution(rrt_algorithm_info,domain_test)
		
		with self.assertRaises(SystemExit) as cm:
			self.solution.run_algorithm()
		
		self.assertEqual(cm.exception.code, "ERROR: No Valid Method")


if __name__ == '__main__':
	unittest.main()