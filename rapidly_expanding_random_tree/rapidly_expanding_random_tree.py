import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors

from collision_generation import *

np.random.seed(RANDOM_SEED)



class rrt_node:
  def __init__(self, position):
    self.position = position
    self.all_children = []
  def set_parent(self, parent):
    self.parent =  parent
  def add_child(self, child):
    self.all_children.append(child)


def generate_random_vector(dimensions=2, max_values=[X_END, Y_END]):
  random_vector = np.random.uniform(size=dimensions) * np.array(max_values)
  return random_vector

def find_the_nearest_node(nodes_list, target_node):
  best_distance = float("inf")
  nearest_node = None

  for node in nodes_list:
    distance = np.linalg.norm(node.position-target_node.position)
    # print distance
    if distance < best_distance:
      best_distance = distance
      nearest_node = node
  return nearest_node

def plot_rrt_tree(nodes_list, canvas_2d, max_values=[X_END, Y_END]):
  'Writren by referrring Matplot lib documentation'

  all_lines = []
  for node in nodes_list:
    for child in node.all_children:
      all_lines.append([node.position, child.position])

  lines = np.array(all_lines)
  # print 'total_lines', lines.shape
  fig, ax = plt.subplots()
  ax.set_xlim(0, max_values[0])
  ax.set_ylim(0, max_values[1])

  centers = [circle.center for circle in canvas_2d.all_circles]
  radii = [circle.radius for circle in canvas_2d.all_circles]

  patches = [plt.Circle(center, radius) for center, radius in zip(centers, radii)]
  coll = matplotlib.collections.PatchCollection(patches, facecolors='black')


  line_segments = LineCollection(lines, linewidths=(0.5, 1, 1.5, 2), linestyle='solid')
  #matplotlib.patches.circle()
  ax.add_collection(coll)
  ax.add_collection(line_segments)


  ax.set_title('rapidly expanding random tree')

  plt.show()
  

def build_expanding_rrt(qinit=[80.0,80.0], vertex_count=5000, incremental_distance=1,
                        planning_domain=NUM_DIMENSIONS):
  first_node = rrt_node(np.array(qinit))
  first_node.parent = None
  all_nodes = [first_node]

  canvas_2d = canvas_generator_2d_circular_obstacles(no_of_circles=10, 
                                                       max_radii=10, min_radii=2)
  canvas_2d.genrate_canvas()


  for i in range(vertex_count):
    random_position = generate_random_vector(planning_domain)
    new_node = rrt_node(random_position) 
    nearest_node = find_the_nearest_node(all_nodes, new_node)
    unit_distance_position = (new_node.position - nearest_node.position) / np.linalg.norm(new_node.position - nearest_node.position) * incremental_distance + nearest_node.position
    new_node.position = unit_distance_position
    line = np.array([nearest_node.position, new_node.position])
    is_intersect = canvas_2d.does_line_intersect_circle(line)



    if(not is_intersect):
      new_node.set_parent(nearest_node)
      nearest_node.add_child(new_node)
      all_nodes.append(new_node)

  plot_rrt_tree(all_nodes, canvas_2d)
  

  

if __name__=='__main__':
  build_expanding_rrt()


  

