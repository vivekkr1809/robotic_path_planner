# test_plot.py
# Author(s): Jessica Flores
import unittest
from unittest.mock import Mock
import numpy as np
import os

from solver.solution import Solution
from solver.recorder import Recorder
from input.domain_class import Domain
from output.plot import Plot

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

string_title = "string"
float_title = 123.5
integer_title = 5


class TestResults(unittest.TestCase):

	def test_plot_domain(self):
		self.plot = Plot(string_title, domain_test)
		self.plot.plot_domain()
		self.assertEqual(self.plot.fig.layout['title']['text'], string_title, "title doesn't work")
		self.assertEqual(self.plot.fig.layout['xaxis']['constrain'], 'domain', "domain shape is not implemented")

		self.plot2 = Plot(float_title, domain_test)
		self.plot2.plot_domain()
		self.assertEqual(self.plot2.fig.layout['title']['text'], str(float_title), "title doesn't work")

		self.plot3 = Plot(integer_title, domain_test)
		self.plot3.plot_domain()
		self.assertEqual(self.plot3.fig.layout['title']['text'], str(integer_title), "title doesn't work")


	def test_plot_obstacles(self):
		self.plot = Plot(string_title, domain_test)
		self.plot.plot_obstacles()
		self.assertTrue(self.plot.fig.layout.shapes)

		#no obstacles
		obstacles_info_empty = {}
		domain_test_noobstacles = Domain(domain_info, obstacles_info_empty, origin_goal_info)	
		self.plot_noobstacles = Plot(string_title, domain_test_noobstacles)
		self.plot_noobstacles.plot_obstacles()
		self.assertFalse(self.plot_noobstacles.fig.layout.shapes)
		
	def test_plot_origin_goals(self):
		self.plot = Plot(string_title, domain_test)
		self.plot.plot_origin_goals()
		self.assertTrue(self.plot.fig.layout.shapes)

	def test_plot_solution_graph(self):
		self.plot = Plot(string_title, domain_test)
		self.plot.plot_solution_graph(solution_test)
		self.assertTrue(self.plot.fig.data)

		#do not plot solution
		self.plot_empty = Plot(string_title, domain_test)
		self.plot_empty.plot_solution_graph()
		self.assertFalse(self.plot_empty.fig.data)

	def test_draw(self):
		self.plot = Plot(string_title, domain_test)
		self.plot.filename = "./src_pathplanner/output/output_files/" + string_title + ".html"
		self.plot.draw()
		self.assertTrue(os.path.exists("./src_pathplanner/output/output_files/" + string_title + ".html"))

if __name__ == '__main__':
	unittest.main()


