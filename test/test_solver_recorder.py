import unittest
from unittest.mock import Mock

import numpy as np

from solver.recorder import Recorder

testparams = Mock()
testparams.n_trials = 10
testparams.dims = 2

rrt_algorithm_info = {
	'method': 'rrt_basic',
	'n_trials': 100,
	'step_size': 0.2,
	'dim': 2,
	'neighborhood': 0.3
	}

class TestRecorder(unittest.TestCase):
	def setUp(self):
		self.recorder = Recorder(rrt_algorithm_info)

	def tearDown(self):
		self.recorder = None		

	def test_recorder_00_vert_size(self):
		self.assertEqual(self.recorder.vertices.shape,
						(self.recorder.params["n_trials"],
							self.recorder.params["dim"]),
						"vert, not right matrix size")		

	def test_recorder_01_cost_length(self):
		self.assertEqual(self.recorder.params["n_trials"],
						len(self.recorder.costs),
						"costs, not right length")

	def test_recorder_02_parent_length(self):
		self.assertEqual(self.recorder.params["n_trials"],
						len(self.recorder.parents),
						"parents, not right length")

	def test_recorder_03_zeros(self):
		self.assertTrue(np.all(np.isnan(self.recorder.vertices)),
						"vertices, not fully initialized to NaN")

		self.assertTrue(np.all(np.isnan(self.recorder.parents)),
						"parents, not initialized to NaN")

		self.assertTrue(np.all(np.isnan(self.recorder.costs)),
						"costs, not initialized to NaN")

	def test_recorder_04_no_history(self):
		rrt_algorithm_info['method'] = "rrt_basic"

		self.assertFalse(hasattr(self.recorder, 'parents_history'),
			"parents history exists for rrt_basic")	

	def test_recorder_05_yes_history(self):
		rrt_algorithm_info['method'] = "rrt_star"
		self.recorder = Recorder(rrt_algorithm_info)

		self.assertTrue(hasattr(self.recorder, 'parents_history'),
			"parents history does not exist for rrt_star")	

	def test_recorder_05_yes_history_len(self):
		rrt_algorithm_info['method'] = "rrt_star"
		self.recorder = Recorder(rrt_algorithm_info)

		self.assertEqual(self.recorder.parents_history.shape,
						(self.recorder.params["n_trials"],
						2*self.recorder.params["n_trials"]),
						"p_history, not right matrix size")		



if __name__ == '__main__':
	unittest.main()