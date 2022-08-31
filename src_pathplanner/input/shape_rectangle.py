# shape_rectangle.py
# Author(s): Vivek Kumar
# Last Updated: January 2019

# Python modules
import numpy as np
# Package modules
from input.shape import Shape

class Rectangle(Shape):
  """A class used to create rectangular objects which could act as domain or obstacle shape.  
  """
  def __init__(self, shape_info):
    """Constructor method
    
    Parameters:
      shape_info (:obj: `dict`):
        dictionary containing information about the shape object to be created
    
    Attributes:
      ll_corner (:obj:`numpy.ndarray`):
        The lower left corner of the rectangle
      ur_corner (:obj:`numpy.ndarray`):
        The upper right corner of the rectangle
      vertices (:obj: `numpy.ndarray`):
        The vertices of the rectangle
      width (:obj: `float`):
        The width (horizontal length) of the rectangle
      height (:obj: `float`):
        The height (vertical length) of the rectangle
      centroid (:obj: `numpy.ndarray`):
        The centroid of the rectangle

    """
    super().__init__(shape_info)

    self.ll_corner = np.asarray(shape_info['lower_left'])
    self.ur_corner = np.asarray(shape_info['upper_right'])
    # Assert the order of points
    assert(self.ll_corner[0] < self.ur_corner[0])
    assert(self.ll_corner[1] < self.ur_corner[1])

    # Compute the vertices
    self.vertices = np.array([[self.ll_corner[0], self.ll_corner[1]], [self.ur_corner[0],self.ll_corner[1]], [self.ur_corner[0], self.ur_corner[1]], [self.ll_corner[0], self.ur_corner[1]]])
    
    # The dimensions of the rectangle
    self.width = abs(self.vertices[0][0]-self.vertices[2][0])
    self.height = abs(self.vertices[0][1]-self.vertices[2][1])
    # The centroid of the rectangle
    self.centroid = np.mean(self.vertices, axis=0)


  def is_point_inside(self, point):
    """Checks if a given point is inside the rectangle

    Find the method at https://math.stackexchange.com/a/190373
    
    Parameters:
      point (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the point to be tested

    Returns:
      bool.::

        True -- Point is inside
        False -- Point is not inside

    """
    if ((0.0 <= (np.dot(self.vertices[0]-point, self.vertices[0]-self.vertices[1])) <= (np.dot(self.vertices[0]-self.vertices[1], self.vertices[0]-self.vertices[1]))) and ( 0 <= (np.dot(self.vertices[0]-point, self.vertices[0]-self.vertices[3])) <= (np.dot(self.vertices[0]-self.vertices[3], self.vertices[0]-self.vertices[3])))):
      return True
    else:
      return False

  def check_line_segment_intersection(self, point_1, point_2, point_3, point_4):
    """Checks if two line segments defined by the end points intersect each other

    Find the method at     https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

    Parameters:
      point_1 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining one end of the line segment 1
      point_2 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the other end of the line segment 1
      point_3 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining one end of the line segment 2
      point_4 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the other end of the line segment 2

    Returns:
      bool.::

        True -- The two line segments intersect
        False -- The two line segments do not intersect

    """
    denominator = (point_1[0]-point_2[0])*(point_3[1]-point_4[1])- (point_1[1]-point_2[1])*(point_3[0]-point_4[0])
    if(denominator == 0):
      # If 0, then the lines are parallel
      return False
    else:
      numerator_alpha = (point_1[0]-point_3[0])*(point_3[1]-point_4[1]) -(point_1[1]-point_3[1])*(point_3[0]-point_4[0])
      if (0.0 <= (numerator_alpha/denominator) <= 1.0):
        numerator_beta = -1.*((point_1[0]-point_2[0])*(point_1[1]-point_3[1])-(point_1[1]-point_2[1])*(point_1[0]-point_3[0]))
        if(0.0 <= (numerator_beta/denominator) <= 1.0):
          return True
        else:
          return False
      else:
        return False

  def is_intersected_by_edge(self, point_1, point_2):
    """Checks if the line segment connecting two points intersects the rectangle
    
    Here the intersection of the line segment defined by the points (point_1 and point_2) is tested against all the sides of the rectangle.

    Note:
      The method assumes/asserts that the two points are outside the rectangle.

    Parameters:
      point_1 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining one end of the edge
      point_2 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the other end of the edge

    Returns:
      bool::

        True -- The line segment intersects or is tangent
        False -- The line segment does not intersect
        
    """
    assert(self.is_point_inside(point_1)==False)

    # The implementation of code repetition was preferred as it was faster than the for loop
    if(self.check_line_segment_intersection(self.vertices[0], self.vertices[1], point_1, point_2)):
      return True

    if(self.check_line_segment_intersection(self.vertices[1], self.vertices[2], point_1, point_2)):
      return True

    if(self.check_line_segment_intersection(self.vertices[2], self.vertices[3], point_1, point_2)):
      return True
    
    if(self.check_line_segment_intersection(self.vertices[3], self.vertices[0], point_1, point_2)):
      return True

    return False

  def sample_random_point(self):
    """Generates a random point in the rectangle

    Returns:
      A new point
        
    """
    new_random_point = np.random.rand(2)
    new_random_point[0] = new_random_point[0]*(self.width)+self.vertices[0][0]
    new_random_point[1] = new_random_point[1]*(self.height)+self.vertices[0][1]
    return new_random_point