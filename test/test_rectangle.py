import numpy as np


from input.shape_rectangle import Rectangle


def test_point_inside():
  shape_info = {'dim':2, 'shape_type':'rectangle','lower_left': np.array([-1.0, -1.0]), 'upper_right':np.array([1.0, 1.0])}
  rectangle = Rectangle(shape_info)

  point = np.array([0.0,0.0])
  assert(rectangle.is_point_inside(point)==True)
  point = np.array([10.0,0.0])
  assert(rectangle.is_point_inside(point)==False)
  # Test edge cases
  # Tests for points very close to the vertices
  point = np.array([1.0,1.0+1.0e-15])
  assert(rectangle.is_point_inside(point)==False)
  point = np.array([1.0,1.0-1.0e-15])
  assert(rectangle.is_point_inside(point)==True)

  point = np.array([1.0-1.0e-15,-1.0+1.0e-15])
  assert(rectangle.is_point_inside(point)==True)
  point = np.array([1.0+1.0e-15,-1.0-1.0e-15])
  assert(rectangle.is_point_inside(point)==False)
  # Tests for points very close to the edges

def test_is_intersected_by_edge():
  shape_info = {'dim':2, 'shape_type':'rectangle','lower_left': np.array([-1.0, -1.0]), 'upper_right':np.array([1.0, 1.0])}
  rectangle = Rectangle(shape_info)

  point_1 = np.array([-1.0,-3.0])
  point_2 = np.array([1.0,2.0])

  point_3 = np.array([0.0, -2.0])
  point_4 = np.array([0.0, 1.5])
  
  point_5 = np.array([-1.5, -0.5])
  point_6 = np.array([0.5, 1.5])
  
  point_7 = np.array([-2.0, 0.0])
  point_8 = np.array([2.0, 0.0])
  
  point_9 = np.array([-3.0, -1.0])
  point_10 = np.array([0.,-1.1])

  point_11 = np.array([-2.0, 0.0])
  point_12 = np.array([0, 2.0])

  assert(rectangle.is_intersected_by_edge(point_1, point_2)==True)
  assert(rectangle.is_intersected_by_edge(point_3, point_4)==True)
  assert(rectangle.is_intersected_by_edge(point_5, point_6)==True)
  assert(rectangle.is_intersected_by_edge(point_7, point_8)==True)
  assert(rectangle.is_intersected_by_edge(point_7, point_8)==True)
  assert(rectangle.is_intersected_by_edge(point_9, point_10)==False)
  assert(rectangle.is_intersected_by_edge(point_11, point_12)==True)
  
def test_sample_random_point():
  shape_info = {'dim':2, 'shape_type':'rectangle','lower_left': np.array([-1.0, -1.0]), 'upper_right':np.array([1.0, 1.0])}
  rectangle = Rectangle(shape_info)
  for i in range(10):
    new_random_point = rectangle.sample_random_point()
    assert(rectangle.is_point_inside(new_random_point)==True)