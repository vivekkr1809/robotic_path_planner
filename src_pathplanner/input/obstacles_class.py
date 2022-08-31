# obstacle_class.py
# Author(s): Vivek Kumar
# Last Updated: January 2019

import numpy as np

from input.shape_circle import Circle
from input.shape_rectangle import Rectangle
from input.shape_free_form import FreeForm2D
from input.parse_data_class import ParseDataJSON


class Obstacle():
  """A class used to represent the obstacles in the RRT software.

  Obstacles denote regions of the domain which are inaccessible to the robot. Hence a new point in the path cannot be generated inside the obstacles

  :param obstacle_info: The information of the obstacle being created
  :type obstacle_info: dict
  :param origin_goal_info: The coordinates of the path starting location (called origin) and where the path should end (called goal)
  :type origin_goal_info: dict
  
  """
  def __init__(self, obstacle_info, origin_goal_info):
    """Constructor method

    Parameters:

      obstacle_info:
        Dictionary containing information about the obstacles in the domain
      origin_goal_info:
        Dictionary containing information about the origin and goal

    Attributes:
      obstacle_info:
        Dictionary containing information about the obstacles in the domain
      dim :
        Dimensions of the domain
      obstacle_shape:
        The shape of the obstacle
      origin:
        The point from where the rrt algorithm begins
    """
    self.obstacle_info = obstacle_info
    self.dim = self.obstacle_info["dim"]
    self.obstacle_shape = self.obstacle_info["shape_type"]

    self.origin = np.asarray(origin_goal_info["origin"]).flatten()

    self.create_obstacle()

  def create_obstacle(self):
    """Creates the obstacle based on the shape and geometrical information provided in the obstacle information list
    """
    if(self.obstacle_shape=="rectangle"):
      self.obstacle = Rectangle(self.obstacle_info)
    elif(self.obstacle_shape=="circle"):
      self.obstacle = Circle(self.obstacle_info)
    elif(self.obstacle_shape=="free_form"):
      self.obstacle = FreeForm2D(self.obstacle_info)
    else:
      raise Exception('The obstacle shape is not implemented')

    # Assert that origin and domain are not inside the obstacle
    assert(self.obstacle.is_point_inside(self.origin)==False)

