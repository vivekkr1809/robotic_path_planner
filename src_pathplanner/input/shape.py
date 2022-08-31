# shape.py
# Author(s): Vivek Kumar

# Python modules
import numpy as np
from abc import ABC, abstractmethod, abstractproperty

class Shape(ABC):
  """The abstract base class for the various shapes to be used in the software"""

  @abstractmethod
  def __init__(self, shape_info):
    """Constructor

    Parameters:
      shape_info (:obj: `dict`):
        dictionary containing information about the shape object to be created
    
    Attributes:
      name (:obj:`str`):
        The name of the shape type
      dim (:obj:`int`):
        The dimension of the shape
    """
    self.name = shape_info["shape_type"]
    self.dim = shape_info["dim"]
  
  @abstractmethod
  def is_point_inside(self):
    """ Abstract method for checking if point falls inside a shape.

    Parameters:
      point (:obj:`numpy.ndarray`):
        The (1,dim) numpy array defining the point to be tested

    Returns:
        bool::

        True -- Point is inside the shape
        False -- Point is not inside the shape
    """
    pass

  @abstractmethod
  def is_intersected_by_edge(self):
    """ Abstract method for checking if an edge connecting two vertices in the rrt graph is intersected by a shape.
    
    Parameters:
      point_1 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining one end of the edge
      point_2 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the other end of the edge
    
    Returns:
        bool::

        True -- The edge intersects the shape
        False -- The edge does not intersect the shape
    """
    pass

  @abstractmethod
  def sample_random_point(self):
    """ Abstract method for generating a random new point inside a shape.

    Returns:
      point (:obj:`np.ndarray`):
        A new point in the shape
    """
    pass