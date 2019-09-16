import math

import numpy as np
import skimage
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors

import algo_constants as cnst

class circle:
  def __init__(self, center, radius):
    self.center = np.array(center)
    self.radius = radius

class canvas_generator_2d_circular_obstacles:
  dimensions = cnst.NUM_DIMENSIONS
  canvas_x_start = cnst.X_START 
  canvas_x_end = cnst.X_END
  canvas_y_start = cnst.Y_START
  canvas_y_end = cnst.Y_END

  def __init__(self, no_of_circles, max_radii, min_radii):
    self.no_of_circles = no_of_circles
    self.max_radii = max_radii
    self.min_radii = min_radii
    self.all_circles = []

  def is_this_point_collision_free(self, point):
    for each_circle in self.all_circles:
      if( np.linalg.norm(each_circle.center - point) <= each_circle.radius): 
        return False
    return True

  def generate_canvas(self):
    
    for circle_index in range(self.no_of_circles):
      center = np.random.uniform(size=self.dimensions) * np.array([self.canvas_x_end, self.canvas_y_end])
      radius = self.min_radii + np.random.uniform(size=1) * (self.max_radii - self.min_radii)
      new_circle = circle(center, radius)
      self.all_circles.append(new_circle)

  def does_line_intersect_obstacle(self, line):
    '''
     u value is the scalar mulitple of P2-P1 at which the shortest distance
     between the point and line lies
    '''
    (x1, y1), (x2,y2) = line
    minimum_line_length = 1e-6

    for each_circle in self.all_circles:
      xc, yc = each_circle.center

      distance_p1_to_p2 = np.linalg.norm(line[0] - line[1])

      if(distance_p1_to_p2 > minimum_line_length):
        u_value = ((xc - x1) * (x2 - x1) + (yc - y1) * (y2 - y1)) / (distance_p1_to_p2 ** 2)
        shortest_distance_point = np.array([x1 + u_value * (x2-x1), y1 + u_value * (y2 - y1)])
        shortest_distance = np.linalg.norm(each_circle.center - shortest_distance_point)
        if(shortest_distance > each_circle.radius):
          continue
        elif(0<= u_value <=1):
          return True
        elif(np.linalg.norm(line[1] - each_circle.center) <= each_circle.radius or
             np.linalg.norm(line[0] - each_circle.center) <= each_circle.radius):
          return True
          
      else:
        print 'points P1=', line[0], 'P2=', line[1], 'are coincident and' + \
                                                     'do\'t form a line'
        raise 
    return False


  def get_lines_from_nodes(self, nodes_list):
  
    lines = []
    for node in nodes_list:
      for child in node.all_children:
        lines.append([node.position, child.position])
    return np.array(lines)

  def plot_rrt_tree(self, nodes_list, start_to_goal_path):
    'Writren by referrring Matplot lib documentation'
  
    max_values=[cnst.X_END, cnst.Y_END]
    non_path_nodes = [node for node in nodes_list if node not in start_to_goal_path]
    path_lines = self.get_lines_from_nodes(start_to_goal_path)
    non_path_lines = self.get_lines_from_nodes(non_path_nodes)
  
    fig, ax = plt.subplots()
    ax.set_xlim(0, max_values[0])
    ax.set_ylim(0, max_values[1])
  
    centers = [circle.center for circle in self.all_circles]
    radii = [circle.radius for circle in self.all_circles]
  
    patches = [plt.Circle(center, radius) for center, radius in zip(centers, radii)]
    coll = matplotlib.collections.PatchCollection(patches, facecolors='black')
  
  
    non_path_colors = [(1.0, 0, 0, 0) for i in range(len(non_path_lines))]
  
    non_path_segments = LineCollection(non_path_lines, linewidths=(0.5, 1, 1.5, 2), linestyle='solid')
    path_segments = LineCollection(path_lines, linewidths=(0.5, 1, 1.5, 2), colors='red', linestyle='solid')
  
    ax.add_collection(coll)
    ax.add_collection(path_segments)
    ax.add_collection(non_path_segments)
    ax.set_title('rapidly expanding random tree')
    plt.show()


  

class canvas_generator_with_random_obstacles:

  def __init__(self, image_path):
    self.image_path = image_path
    self.binary_map = None


  def generate_canvas(self, image_path='./input_map.png'):

    binary_map = skimage.io.imread(image_path, as_gray=True)
    if(len(np.unique(binary_map)) > 2):
      print 'given image is not binary'
      raise
    self.binary_map = np.flipud(binary_map) 
    cnst.X_END, cnst.Y_END = [num-1 for num in np.shape(binary_map)] 

  def is_this_point_collision_free(self, input_point):
     x, y = [int(math.floor(num)) for num in input_point]
     if self.binary_map[y, x] == 0:
       return False
     else:
       return True

  def generate_line_coordinates(self, line):

      (x1, y1), (x2, y2) = line
      delta_x = x2 - x1
      delta_y = y2 - y1
      if delta_x != 0:
        slope = delta_y / delta_x
        unsigned_slope = abs(slope)

      line_coordinates = []
      error = 0

      if delta_x == 0:
        if y1 > y2:
          y1, y2 = y2, y1
        x_coord = int(math.floor(x1))

        while( y1 <= y2):
          line_coordinates.append([ x_coord, int(math.floor(y1))])
          y1 += 1 

      elif unsigned_slope <= 1:
        if x1 > x2:
          x1, x2 = x2, x1
          y1, y2 = y2, y1
        y_coord = y1 
        # while(int(math.floor(x1)) <= int(math.floor(x2))):
        while( x1 <= x2):
          line_coordinates.append([int(math.floor(x1)), int(math.floor(y_coord))]) 
          y_coord = y_coord + slope
          x1 += 1

      else:
        if y1 > y2:
          y1, y2 = y2, y1
          x1, x2= x2, x1
        inv_slope = 1.0 / slope
        x_coord  = x1 

        # while(int(math.floor(y1)) <= int(math.floor(y2))):
        while( y1 <= y2):
          line_coordinates.append([int(math.floor(x_coord)), int(math.floor(y1))])
          y1 += 1
          x_coord = x_coord + inv_slope

      return line_coordinates

  def does_line_intersect_obstacle(self, line):
      '''
      check if any part of the line is impeded by an obstacle using
      Bresenham\'s algorithm
      '''
      line_coordinates = self.generate_line_coordinates(line)
      #line_coordinates = [(x-1, y-1) for (x,y) in line_coordinates]

      for (x1, y1) in line_coordinates:
        if self.binary_map[y1, x1] == 0: 
          return True
      return False

  def get_lines_from_nodes(self, nodes_list):
  
    lines = []
    for node in nodes_list:
      for child in node.all_children:
        lines.append([node.position, child.position])
    return np.array(lines)


  def plot_rrt_tree(self, nodes_list, start_to_goal_path):
  
    max_values=[cnst.X_END, cnst.Y_END]
    non_path_nodes = [node for node in nodes_list if node not in start_to_goal_path]
    path_lines = self.get_lines_from_nodes(start_to_goal_path)
    non_path_lines = self.get_lines_from_nodes(non_path_nodes)
  
    fig, ax = plt.subplots()
    ax.set_xlim(0, max_values[0])
    ax.set_ylim(0, max_values[1])
  
    binary_map = skimage.io.imread('input_map.png', as_gray=True)
    binary_map = np.flipud(binary_map) 
    ax.imshow(binary_map, interpolation = 'none')
  
    non_path_segments = LineCollection(non_path_lines, linewidths=(0.5, 1, 1.5, 2), linestyle='solid')
    path_segments = LineCollection(path_lines, linewidths=(0.5, 1, 1.5, 2), colors='red', linestyle='solid')
  
    ax.add_collection(non_path_segments)
    ax.add_collection(path_segments)
    ax.set_title('rapidly expanding random tree')
  
    plt.show()






      
      

if __name__ =='__main__':

  np.random.seed(cnst.RANDOM_SEED)
  canvas_2d = canvas_generator_2d_circular_obstacles(no_of_circles=10, 
                                                     max_radii=10, min_radii=2)
  canvas_2d.generate_canvas()
  line = np.array([[50,50], [60,60]])
  canvas_2d.does_line_intersect_obstacle(line)
  print canvas_2d 

  canvas_2d = canvas_generator_with_random_obstacles(image_path='./input_map.png')
  canvas_2d.generate_canvas()
  canvas_2d.does_line_intersect_obstacle([[20.0, 30.0], [31.2, 41.3]])
  canvas_2d.does_line_intersect_obstacle([[20.0, 30.0], [29.2, 38.3]])
  canvas_2d.does_line_intersect_obstacle([[20.0, 30.0], [20.0, 38.3]])
 
