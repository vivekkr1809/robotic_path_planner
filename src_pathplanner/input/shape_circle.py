# shape_circle.py
# Author(s): Vivek Kumar
# Last Updated: January 2019

# Python modules
import numpy as np
import math
import random
# Package modules
from input.shape import Shape

class Circle(Shape):
  """A class used to create circular objects which could act as domain or obstacle shape.
  """
  def __init__(self, shape_info):
    """Constructor method

    Parameters:
      shape_info (:obj: `dict`):
        dictionary containing information about the shape object to be created
    
    Attributes:
      radius (:obj:`str`):
        The radius of the circle
      center (:obj:`np.ndarray`):
        The center of the circle
      centroid (:obj: `np.ndarray`):
        The centroid of the circle
    """
    super().__init__(shape_info)
    self.radius = shape_info["radius"]
    self.center = np.asarray(shape_info["center"]).flatten()
    self.centroid = shape_info["center"]
  
  def is_point_inside(self, point):
    """Checks if a given point is inside the circle

    Computes the distance of the point from the center of the circle and compares it with the radius. A point on the perimeter is considered as inside
    
    Parameters:
      point (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the point to be tested
    
    Returns:
      bool::

        True -- Point is inside
        False -- Point is not inside

    """
    if(np.linalg.norm(self.center-point) <= self.radius):
      return True
    else:
      return False

  def is_intersected_by_edge(self, point_1 , point_2):
    """Checks if the line segment connecting two points intersects the circle
    
    The method is adopted from https://math.stackexchange.com/a/275537.

    Note:
      The method assumes/asserts that the two points are outside the circle.

    Parameters:
      point_1 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining one end of the edge
      point_2 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the other end of the edge

    Returns:
      bool::

        True -- The edge intersects or is tangent to the circle
        False -- The edge does not intersect the circle
        
    """
    
    assert self.is_point_inside(point_1)==False
    assert self.is_point_inside(point_2)==False
    
    # Create temporary variables to prevent mutation of original points
    tmp_point_1 = point_1.copy()
    tmp_point_2 = point_2.copy()

    # Move the coordinate system so that the center is at (0,0)
    tmp_point_1[0] = tmp_point_1[0] - self.center[0]
    tmp_point_1[1] = tmp_point_1[1] - self.center[1]
    
    tmp_point_2[0] = tmp_point_2[0] - self.center[0]
    tmp_point_2[1] = tmp_point_2[1] - self.center[1]

    # Create the quadratic system
    a = (tmp_point_2[0]-tmp_point_1[0])**2 + (tmp_point_2[1]-tmp_point_1[1])**2

    b = 2.0*(tmp_point_1[0]*(tmp_point_2[0]-tmp_point_1[0])+tmp_point_1[1]*(tmp_point_2[1]-tmp_point_1[1]))

    c = tmp_point_1[0]**2 + tmp_point_1[1]**2 - self.radius**2

    # Compute discriminant and check if no intersection
    if(b**2 - 4.0*a*c < 0):
      return False

    # Compute discriminant to check if tangent
    if(b**2 -4.*a*c ==0):
      if(0 <= -b/(2.0*a) <= 1):
        return True

    # Check if the point of intersection is within the line segment
    t_1 = (-b + math.sqrt(b**2 -4.*a*c))/(2.0*a)
    t_2 = (-b - math.sqrt(b**2 -4.*a*c))/(2.0*a)
    if((0 <= t_1 <=1) and (0 <= t_2 <=1)):
      return True

    return False

  def sample_random_point(self):
    """Generates a random point in the circle

    The current implementation is adopted from https://stackoverflow.com/a/50746409 to have a uniform distribution of points
    
    Returns:
     point (:obj:`np.ndarray`):
    """
    r = self.radius*math.sqrt(random.random())
    theta = random.random()*2.0*math.pi
    new_random_point = np.asarray([[self.center[0]+r*math.cos(theta), self.center[1]+r*math.sin(theta)]]).flatten()
    return new_random_point