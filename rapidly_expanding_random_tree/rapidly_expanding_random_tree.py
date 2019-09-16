import numpy as np

from collision_generation import *


class rrt_node:
  def __init__(self, position):
    self.position = position
    self.all_children = []
  def set_parent(self, parent):
    self.parent =  parent
  def add_child(self, child):
    self.all_children.append(child)


def generate_random_vector(dimensions=2): 

  max_values = np.array([cnst.X_END, cnst.Y_END])
  random_vector = np.random.uniform(size=dimensions) * np.array(max_values)
  return random_vector

def find_the_nearest_node(nodes_list, target_node):
  best_distance = float("inf")
  nearest_node = None

  for node in nodes_list:
    distance = np.linalg.norm(node.position-target_node.position)
    if distance < best_distance:
      best_distance = distance
      nearest_node = node
  return nearest_node, best_distance


def find_the_nearest_node_to_goal(qout, all_nodes, canvas_2d):

  max_termination_distance = 60.0
  new_node = rrt_node(qout) 
  nearest_node, distance = find_the_nearest_node(all_nodes, new_node)
  if(distance < max_termination_distance):
    line = np.array([nearest_node.position, new_node.position])
    is_intersect = canvas_2d.does_line_intersect_obstacle(line)
    if(is_intersect):
      return False, all_nodes
    else:
      new_node.set_parent(nearest_node)
      nearest_node.add_child(new_node)
      all_nodes.append(new_node)
      return True, all_nodes
  else:
    return False, all_nodes

def find_path_between_two_nodes(start_node, end_node):
   
  path = []
  current_node = end_node

  while(current_node !=  start_node):
    path.append(current_node)
    current_node = current_node.parent
  path.append(current_node)

  return path


def generate_a_valid_point(input_point, canvas_2d):

  if(not input_point):
    input_point = generate_random_vector(cnst.NUM_DIMENSIONS)
    while(not canvas_2d.is_this_point_collision_free(np.array(input_point))):
      input_point = generate_random_vector(cnst.NUM_DIMENSIONS)
  elif(not canvas_2d.is_this_point_collision_free(np.array(input_point))):
    print 'start or goal point lies inside obstacles'
    raise

  return input_point


def build_expanding_rrt(qinit=[], qout=[], max_vertex_count=10000, 
                        incremental_distance=1):

  #qinit=[80.0,80.0]  
  #qout=[10.0, 10.0]
  start_to_goal_path = []

  # canvas_2d = canvas_generator_2d_circular_obstacles(no_of_circles=10, 
  #                                                  max_radii=10, min_radii=2)
  canvas_2d = canvas_generator_with_random_obstacles(image_path = './input_map.png')
  canvas_2d.generate_canvas()
  qinit = generate_a_valid_point(qinit, canvas_2d)
  qout = generate_a_valid_point(qout, canvas_2d)
  print 'qinit', qinit
  print 'qinit', qout
   
  first_node = rrt_node(np.array(qinit))
  first_node.parent = None
  all_nodes = [first_node]


  for i in range(max_vertex_count):
    random_position = generate_random_vector(cnst.NUM_DIMENSIONS)
    new_node = rrt_node(random_position) 
    nearest_node, _ = find_the_nearest_node(all_nodes, new_node)
    unit_distance_position = (new_node.position - nearest_node.position) / \
                             np.linalg.norm(new_node.position - nearest_node.position) *\
                             incremental_distance + nearest_node.position
    new_node.position = unit_distance_position
    line = np.array([nearest_node.position, new_node.position])
    is_intersect = canvas_2d.does_line_intersect_obstacle(line)



    if(not is_intersect):
      new_node.set_parent(nearest_node)
      nearest_node.add_child(new_node)
      all_nodes.append(new_node)
    is_goal_reached, all_nodes = find_the_nearest_node_to_goal(qout, all_nodes, 
                                                                     canvas_2d)

    if(is_goal_reached):
      start_node = first_node
      end_node = filter(lambda node:np.array_equal(node.position, np.array(qout)), 
                                                   all_nodes)[0]
      start_to_goal_path = find_path_between_two_nodes(start_node, end_node)
      print 'path found'
      break

  canvas_2d.plot_rrt_tree(all_nodes, start_to_goal_path)
  

  

if __name__=='__main__':
  np.random.seed(cnst.RANDOM_SEED)
  build_expanding_rrt()
  # canvas_2d = canvas_generator_with_random_obstacles(image_path='./input_map.png')
  # print cnst.X_END, cnst.Y_END


  

