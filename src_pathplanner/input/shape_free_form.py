# shape_rectangle.py
# Author(s): Vivek Kumar
# Last Updated: January 2019

# Python modules
import numpy as np
import sys
import math
import random
# Thir party modules
import cv2
# Package modules
from input.shape import Shape

class FreeForm2D(Shape):
  """A class used to create free form objects which could act as obstacle shape.

  The class generates 2D free form shapes using ASCII bitmap files.
  """
  def __init__(self, shape_info):
    """Constructor method

    Parameters:
      shape_info (:obj: `dict`):
        dictionary containing information about the shape object to be created
    
    Attributes:
      file (:obj:`str`):
        The bitmap file to be used to create the object
      bb_lower_left (:obj: `np.ndarray`)
        The lower left corner of the bounding box of the free form
      bb_upper_right (:obj: `np.ndarray`)
        The upper right corner of the bounding box of the free form

    """
    super().__init__(shape_info)
    
    assert self.dim == 2 # Only implemented for 2D objects

    self.file = shape_info['bitmap_file']
    self.bb_lower_left = shape_info['bb_lower_left'] # The lower left location of the bounding box
    self.bb_upper_right = shape_info['bb_upper_right'] # The upper right location of the bounding box
    self.obtain_geometric_info()


  def obtain_geometric_info(self):
    """Computes geomterical information from the bitmap points

    This function converts the bitmap [0,1] array to coordinates and computes geometrical properties such as centroid
  
    Attributes:
      img ():
        The bitmap image]
      hx (:obj: `float`):
        The center to center distance between pixels along horizontal[0] direction
      hy (:obj: `float`):
        The center to center distance between pixels along vertical[1] direction
      all_points_array (:obj: `np.ndarray`):
        The numpy array containg the coordinate of the points of the free form image
      x_min_val (:obj: `float`):
        The minimum value of the x-coordinate
      x_max_val (:obj: `float`):
        The maximum value of the x-coordinate
      y_min_val (:obj: `float`):
        The minimum value of the y-coordinate
      y_max_val (:obj: `float`):
        The maximum value of the y-coordinate
      centroid (:obj: `np.ndarray`)
        The centroid of the free form shape

    Note:
      The image final form is a scaled version of the original image to fit the bounding box

    """
    self.img = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)

    n_rows = self.img.shape[0]
    n_columns = self.img.shape[1]
    self.hx = 1./(n_rows-1) # This makes sure that the x-values are b/w 0-1
    self.hy = (1./(n_columns-1)) *((n_rows-1)/(n_columns-1))
    
    self.all_points_array = np.asarray([[j*self.hx, 1.0-i*self.hy] for i in range(n_rows) for j in range(n_columns) if self.img[i,j]==0])

    # The left most corner 
    self.x_min_val = np.min(self.all_points_array[:,0])
    self.y_min_val = np.min(self.all_points_array[:,1])
    

    # Traslate the coordinates
    self.all_points_array[:,0] = self.all_points_array[:,0]-self.x_min_val
    self.all_points_array[:,1] = self.all_points_array[:,1]-self.y_min_val
    
    # The original bounding box
    self.x_min_val = np.min(self.all_points_array[:,0])
    self.y_min_val = np.min(self.all_points_array[:,1])
    self.x_max_val = np.max(self.all_points_array[:,0])
    self.y_max_val = np.max(self.all_points_array[:,1])
    
    original_bb_width = self.x_max_val - self.x_min_val
    original_bb_height = self.y_max_val - self.y_min_val

    new_bb_width = self.bb_upper_right[0] - self.bb_lower_left[0]
    new_bb_height = self.bb_upper_right[1] - self.bb_lower_left[1]

    x_scale = new_bb_width/original_bb_width
    y_scale = new_bb_height/original_bb_height

    self.all_points_array[:,0] = self.all_points_array[:,0]*x_scale
    self.all_points_array[:,1] = self.all_points_array[:,1]*y_scale

    self.all_points_array[:,0] = self.all_points_array[:,0]+self.bb_lower_left[0]
    self.all_points_array[:,1] = self.all_points_array[:,1]+self.bb_lower_left[1]

    self.x_min_val = np.min(self.all_points_array[:,0])
    self.y_min_val = np.min(self.all_points_array[:,1])
    self.x_max_val = np.max(self.all_points_array[:,0])
    self.y_max_val = np.max(self.all_points_array[:,1])

    self.hx = self.hx*x_scale
    self.hy = self.hy*y_scale
    # Compute the centroid of the shape
    self.centroid = np.mean(self.all_points_array, axis=0)

  # Check if a new point is inside the shape
  # This is slow!!!
  def is_point_inside(self, point):
    """Checks if a given point is inside the free form shape

    The following steps are performed::
      Step 1. Checks if the point is inside the bounding box of the shape

      Step 2. If the point is inside the bounding box, find the points in the free form which are within a certain y  values

      Step 3. Establish the radius in which to look for points of the free form and check if such a point exist
    
    Parameters:
      point (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the point to be tested

    Returns:
      bool.::

        True -- Point is inside
        False -- Point is not inside

    """
    # If inside_bounding box
    if(point[0] < self.x_min_val or point[0] > self.x_max_val or point[1] < self.y_min_val or point[1] > self.y_max_val):
      return False
    else:

      # Select all the points whose y values are within +/- y_band
      y_band = 2.1*self.hy
      shape_points = self.all_points_array[self.all_points_array[:,1] < point[1]+y_band]
      shape_points = shape_points[shape_points[:,1] > point[1] -y_band]
      _eps = 1.0e-1
      relative_distance_array = np.linalg.norm(shape_points-point, axis = 1)
      test_radius = max(self.hx,self.hy)*(2.+_eps)
      if(relative_distance_array[np.argmin(relative_distance_array)] < test_radius):
        return True
      return False

  def is_intersected_by_edge(self, point_1, point_2):
    """Checks if the line segment connecting two points intersects the free
    
    Here the intersection of the line segment defined by the points (point_1 and point_2) is tested 

    Note:
      The method assumes/asserts that the two points are outside the free form
    
    The following steps are performed:
      Step 1. Compute the length of the segment and compute the number of points to be chosen between the point_1 and point_2

      Step 2. Divide the line segment into appropriate number of points to test

      Step 3. Check if any of the points is inside the shape

    Parameters:
      point_1 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining one end of the edge
      point_2 (:obj:`np.ndarray`):
        The (1,dim) numpy array defining the other end of the edge

    Returns:
      bool::

        True -- The edge intersects
        False -- The edge does not intersect
        
    """
    assert self.is_point_inside(point_1)==False
    assert self.is_point_inside(point_2)==False
    
    # Compute the number of points based on the hx value
    length_of_edge = np.linalg.norm(point_1-point_2)
    # Divide the edge into appropriate number of segments
    n_divisions = math.ceil(length_of_edge*(1./self.hx))
    if point_1[0] == point_2[0]:
      points_to_test = [[point_1[0], point_1[1]+(i+1)*((point_2[1]-point_1[1])/n_divisions)] for i in range(n_divisions-1)]
    else:
      line_slope = (point_2[1]-point_1[1])/(point_2[0]-point_1[0])
      points_to_test = [[point_1[0]+(i+1)*(point_2[0]-point_1[0])/(n_divisions), line_slope*(point_1[0]+(i+1)*(point_2[0]-point_1[0])/(n_divisions) - point_1[0])+ point_1[1]] for i in range(n_divisions-1)]

    for point in points_to_test:
      if(self.is_point_inside(point)):
        return True
    return False

  def sample_random_point(self):
    """Generates a random point in the shape free form

    The following steps are performed:
      Step 1. Randomly select a point in the free form shape

      Step 2. Move the point by a randomly chosen delta value in x and y direction

      Step 3. If the new point lies within the shape return the point else find a new point

    Returns:
      A new point

    """
    random_point = (self.all_points_array[np.random.randint(self.all_points_array.shape[0], size=1), :]).flatten()
    delta = np.random.rand(2)

    delta[0] = delta[0]*self.hx
    delta[1] = delta[1]*self.hy
    random_point = random_point+delta
    while(not self.is_point_inside(random_point)):
      random_point = (self.all_points_array[np.random.randint(self.all_points_array.shape[0], size=1), :]).flatten() + delta
    return random_point

