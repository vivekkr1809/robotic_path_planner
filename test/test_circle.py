# test_circle.py
# Author(s): Vivek Kumar
# Last Updated: January 2019
import numpy as np
from input.shape_circle import Circle


def test_point_inside():
  shape_info = {'dim':2, 'shape_type':'circle','radius': 1.0, 'center':np.array([0.0, 0.0])}
  circle = Circle(shape_info)
  # center is inside
  assert circle.is_point_inside(shape_info['center'])==True
  point = np.array([0.0, shape_info['radius']-1.0e-7])
  assert circle.is_point_inside(point)==True
  point = np.array([0.0, shape_info['radius']-1.0e-15])
  assert circle.is_point_inside(point)==True # Floating arithmetic limit 
  point = np.array([0.0, shape_info['radius']+1.0e-7])
  assert circle.is_point_inside(point)==False 
  point = np.array([0.0, shape_info['radius']+1.0e-15])
  assert circle.is_point_inside(point)==False # Floating arithmetic limit 

# 
def test_point_on_perimeter():
  shape_info = {'dim':2, 'shape_type':'circle','radius': 1.0, 'center':np.array([0.0, 0.0])}
  circle = Circle(shape_info)

  point = np.array([0.0,shape_info['radius']])
  assert circle.is_point_inside(point)==True
  point = np.array([0.0,-shape_info['radius']])
  assert circle.is_point_inside(point)==True
  point = np.array([shape_info['radius'], 0.0])
  assert circle.is_point_inside(point)==True
  point = np.array([-shape_info['radius'], 0.0])
  assert circle.is_point_inside(point)==True

def test_tangent_line():
  shape_info = {'dim':2, 'shape_type':'circle','radius': 1.0, 'center':np.array([0.0, 0.0])}
  circle = Circle(shape_info)

  point_1 = np.array([-2.0, 1.0])
  point_2 = np.array([2.0, 1.0])
  assert circle.is_intersected_by_edge(point_1, point_2)==True
  point_2 = np.array([2.0, 2.0])
  assert circle.is_intersected_by_edge(point_1, point_2)==False

def test_is_intersected_by_edge():
  shape_info = {'dim':2, 'shape_type':'circle','radius': 1.0, 'center':np.array([0.0, 0.0])}
  circle = Circle(shape_info)
  point_1 = np.array([-2.0, 1.0])
  point_2 = np.array([2.0, -1.0])
  assert circle.is_intersected_by_edge(point_1, point_2)==True
  point_2 = np.array([2.0, 2.0])
  assert circle.is_intersected_by_edge(point_1, point_2)==False
  point_2 = np.array([1.0, 1.0])
  assert circle.is_intersected_by_edge(point_1, point_2)==True
  point_2 = np.array([-1.0, 1.0])
  assert circle.is_intersected_by_edge(point_1, point_2)==False

def test_sample_random_point():
  shape_info = {'dim':2, 'shape_type':'circle','radius': 1.0, 'center':np.array([0.0, 0.0])}
  circle = Circle(shape_info)
  for i in range(10):
    new_random_point = circle.sample_random_point()
    assert(circle.is_point_inside(new_random_point)==True)