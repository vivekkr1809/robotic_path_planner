import unittest
from unittest.mock import Mock, patch

import numpy as np

from algorithm.vertex import Vertex
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

class TestVertex(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass


	def test_vertex_00_distance_calc_normal1(self):
			vertices = np.array(
				[[0.0, 0.0],
				[1.0, 1.10],
				[1.0, 1.05]]
			)

			goal = np.array([1.0,1.0])

			index,dist = Vertex.find_nearest_vertex(vertices,goal)

			self.assertEqual(index,2,"shortest index incorrect")
			self.assertAlmostEqual(dist,0.05,7,"shortest distance incorrect")


	def test_vertex_01_distance_calc_normal3d(self):
		vertices = np.array(
			[[0.0, 0.0, 0.0],
			[1.0, 1.10, 1.0],
			[1.0, 1.05, 2.0]]
		)

		goal = np.array([1.0,1.0,2.0])

		index,dist = Vertex.find_nearest_vertex(vertices,goal)

		self.assertEqual(index,2,"shortest index incorrect")
		self.assertAlmostEqual(dist,0.05,7,"shortest distance incorrect")


	def test_vertex_02_distance_calc_zeros(self):
		vertices = np.array(
			[[1.0, 1.0],
			[0.0, 0.00],
			[1.0, 1.05]]
		)

		goal = np.array([0.0,0.0])

		index,dist = Vertex.find_nearest_vertex(vertices,goal)

		self.assertEqual(index,1,"shortest index incorrect")
		self.assertAlmostEqual(dist,0.0,7,"shortest distance incorrect")


	def test_vertex_03_distance_calc_between(self):
		vertices = np.array(
			[[0.0, 1.0],
			[0.0, 0.0],
			[1.0, 1.05]]
		)

		goal = np.array([0.0,0.5])

		index,dist = Vertex.find_nearest_vertex(vertices,goal)

		self.assertEqual(index,0,"shortest index incorrect")
		self.assertAlmostEqual(dist,0.5,7,"shortest distance incorrect")


	def test_vertex_04_distance_calc_nan(self):
		vertices = np.array(
			[[0.0, 0.0],
			[1.0, 1.1],
			[np.nan, np.nan]]
		)

		goal = np.array([1.0,1.0])

		index,dist = Vertex.find_nearest_vertex(vertices,goal)

		self.assertEqual(index,1,"shortest index incorrect")
		self.assertAlmostEqual(dist,0.1,7,"shortest distance incorrect")


	def test_vertex_05_distance_calc_inf(self):
		vertices = np.array(
			[[float('+inf'), float('+inf')],
			[float('+inf'), float('+inf')],
			[float('+inf'), float('+inf')]]
		)

		goal = np.array([0.0,0.0])

		index,dist = Vertex.find_nearest_vertex(vertices,goal)

		self.assertEqual(index,0,"shortest index incorrect")
		self.assertEqual(dist,float('+inf'),"shortest distance incorrect")


	def test_vertex_06_random_config(self):

		rand_config = Vertex.new_config(domain_test)

		self.assertEqual(
			len(rand_config),
			domain_test.dim,
			"config not right dimensions")


	def test_vertex_07_new_vertex_close1(self):
		
		vertices = np.array(
			[[1.0, 1.0],
			[0.0, 0.0],
			[1.0, 1.05]]
		)

		new_q = [0.0, 0.1]

		step_size = 0.2

		v, i, d = Vertex.new_vertex(vertices, new_q, step_size)

		self.assertEqual(v,new_q, "new vertex incorrect")
		self.assertEqual(i, 1, "index of vertex wrong")
		self.assertEqual(d, 0.1, "distance of vertex wrong")


	def test_vertex_08_new_vertex_close2(self):
		
		vertices = np.array(
			[[1.0, 1.0],
			[0.0, 0.0],
			[1.0, 1.05]]
		)

		new_q = [0.1, 0.1]

		step_size = 0.2

		v, i, d = Vertex.new_vertex(vertices, new_q, step_size)

		self.assertEqual(v,new_q, "new vertex incorrect")
		self.assertEqual(i, 1, "index of vertex wrong")
		self.assertAlmostEqual(d, 0.141421,6, "distance of vertex wrong")


	def test_vertex_08_new_vertex_close3D(self):
		
		vertices = np.array(
			[[1.0, 1.0, 1.0],
			[0.0, 0.0, 0.0],
			[1.0, 1.05, 0.0]]
		)

		new_q = [0.0, 0.15, 0.0]

		step_size = 0.2

		v, i, d = Vertex.new_vertex(vertices, new_q, step_size)

		self.assertEqual(v,new_q, "new vertex incorrect")
		self.assertEqual(i, 1, "index of vertex wrong")
		self.assertEqual(d, 0.15, "distance of vertex wrong")


	def test_vertex_09_new_vertex_far1(self):
		
		vertices = np.array(
			[[0.0, 1.0],
			[0.0, 0.0],
			[1.0, 1.05]]
		)

		new_q = [0.0, 0.5]

		step_size = 0.2

		v, i, d = Vertex.new_vertex(vertices, new_q, step_size)

		self.assertEqual(v[1],0.8, "new vertex incorrect")
		self.assertEqual(i, 0, "index of vertex wrong")
		self.assertEqual(d, 0.2, "distance of vertex wrong")


	def test_vertex_09_new_vertex_far2(self):
		
		vertices = np.array(
			[[0.0, 1.0],
			[0.0, 0.0],
			[1.0, 1.05]]
		)

		new_q = [0.3, 0.3]

		step_size = 0.2

		v, i, d = Vertex.new_vertex(vertices, new_q, step_size)

		self.assertEqual(v[1],0.141421, "new vertex incorrect")
		self.assertEqual(i, 1, "index of vertex wrong")
		self.assertEqual(d, 0.2, "distance of vertex wrong")


	def test_vertex_10_new_vertex_far3D(self):
		
		vertices = np.array(
			[[0.0, 1.0, 0.0],
			[0.0, 0.0, 0.0],
			[1.0, 1.05, 0.0]]
		)

		new_q = [0.3, 0.3, 0.3]

		step_size = 0.2

		v, i, d = Vertex.new_vertex(vertices, new_q, step_size)

		self.assertEqual(v[1],0.115470, "new vertex incorrect")
		self.assertEqual(i, 1, "index of vertex wrong")
		self.assertEqual(d, 0.2, "distance of vertex wrong")


if __name__ == '__main__':
	unittest.main()