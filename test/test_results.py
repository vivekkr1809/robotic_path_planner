# test_results.py
# Author(s): Jessica Flores
import unittest
from unittest.mock import Mock
import numpy as np

from solver.solution import Solution
from solver.recorder import Recorder
from input.domain_class import Domain
from output.results import Results

domain_info = {
	'dim': 2, 
	'shape_type': 'rectangle',
	'lower_left': [0.0, 0.0],
	'upper_right': [3.0, 4.0]
	}

origin_goal_info = {
	'origin': [0.1, 0.1],
	'goals': {
		'goal_1': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [1.0, 1.1]},
		'goal_2': {'dim': 2, 'shape_type': 'circle', 'radius': 0.25, 'center': [0.5, 2.2]}
		}
	}

obstacles_info = {
	'obstacle_1':{'dim': 2, 'shape_type': 'circle', 'radius': 0.2, 'center': [0.5, 3.5]},
	'obstacle_2': {'dim': 2, 'shape_type': 'circle', 'radius': 0.2, 'center': [1.5, 3.5]},
	'obstacle_3': {'dim': 2, 'shape_type': 'circle', 'radius': 0.4, 'center': [1.5, 0.5]}
	}

domain_test = Domain(domain_info, obstacles_info, origin_goal_info)	

#Solution object with a solution path
rrt_algorithm_info = {
	'method': 'rrt_basic',
	'n_trials': 100,
	'step_size': 1.0,
	'dim': 2,
	'neighborhood': 1.1
	}	
solution_test = Solution(rrt_algorithm_info,domain_test)
solution_test.run_algorithm(print_vertex=False)
solution_test.process_vertex_list()

#Solution object without a solution path 
rrt_algorithm_info_nosolution = {
	'method': 'rrt_basic',
	'n_trials': 1,
	'step_size': 1.0,
	'dim': 2,
	'neighborhood': 1.1
	}	
solution_test_nosolution = Solution(rrt_algorithm_info_nosolution,domain_test)
solution_test_nosolution.run_algorithm(print_vertex=False)
solution_test_nosolution.process_vertex_list()

class TestResults(unittest.TestCase):

	def test_get_solution_vertices_yessolution(self):
		#test if the correct number of vertices are recorded when a solution is found  

		self.results = Results(solution_test)
		
		self.assertEqual(len(self.results.solution_vertices), len(self.results.solution_path),
			"not enough vertices lists saved")

		for i, path in enumerate(self.results.solution_path):
			self.assertEqual(len(self.results.solution_vertices[i]), len(path),
				"not enough vertices saved")

	def test_get_solution_vertices_nosolution(self):
		#test test if the correct number of vertices are recorded when a solution is not found 
		
		self.results = Results(solution_test_nosolution)
		
		self.assertEqual(self.results.solution_vertices, self.results.solution_path,
			"not enough vertices lists saved")

		for i, path in enumerate(self.results.solution_path):
			self.assertEqual(self.results.solution_vertices[i], path,
				"not enough vertices saved")

	def test_get_solution_costs_yessolution(self):
		#test if the correct number of solution costs are recorded when a solution is found  
		
		self.results = Results(solution_test)
		
		self.assertEqual(len(self.results.solution_costs), len(self.results.solution_path),
			"not enough solution costs saved")

	def test_get_solution_costs_nosolution(self):
		#test if the correct number of solution costs are recorded when a solution is not found  

		self.results = Results(solution_test_nosolution)
		
		self.assertEqual(len(self.results.solution_costs), len(self.results.solution_path),
			"not enough solution costs saved")


if __name__ == '__main__':
	unittest.main()

