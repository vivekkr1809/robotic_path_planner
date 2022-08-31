"""
This is the test file for the class to read the FreeForm class

Author(s) : Vivek Kumar
Last Updated: December 2019
"""
from pytest import approx
import numpy as np
from input.shape_free_form import FreeForm2D

def test_is_point_inside():
  shape_info = {'dim': 2, 'shape_type':'free_form', 'bitmap_file': './test/test_rectangle.pbm', 'bb_lower_left':np.array([1.5,1.5]), 'bb_upper_right':np.array([2.5,3.5])}
  free_shape = FreeForm2D(shape_info)
  point_1 = np.array([2.0,2.0])
  assert(free_shape.is_point_inside(point_1)==True)
  point_2 = np.array([3.4,0.063])
  assert(free_shape.is_point_inside(point_2)==False)
  assert(free_shape.is_point_inside(free_shape.centroid)==True)

def test_is_intersected_by_edge():
  shape_info = {'dim': 2, 'shape_type':'free_form', 'bitmap_file': './test/test_rectangle.pbm', 'bb_lower_left':np.array([1.5,1.5]), 'bb_upper_right':np.array([2.5,3.5])}
  free_shape = FreeForm2D(shape_info)
  point_1 = np.array([4.0, 4.0])
  point_2 = np.array([0.0, 0.0])
  assert(free_shape.is_intersected_by_edge(point_1, point_2)==True)

  point_3 = np.array([0.0, 2.0])
  point_4 = np.array([3.5, 2.0])
  assert(free_shape.is_intersected_by_edge(point_3, point_4)==True)

  point_5 = np.array([0.0, 0.0])
  point_6 = np.array([1.0, 1.0])
  assert(free_shape.is_intersected_by_edge(point_5, point_6)==False)


def test_new_random_point():
  shape_info = {'dim': 2, 'shape_type':'free_form', 'bitmap_file': './test/test_rectangle.pbm', 'bb_lower_left':np.array([1.5,1.5]), 'bb_upper_right':np.array([2.5,3.5])}
  free_shape = FreeForm2D(shape_info)
  for i in range(10):
    new_random_point = free_shape.sample_random_point()
    assert(free_shape.is_point_inside(new_random_point)==True)