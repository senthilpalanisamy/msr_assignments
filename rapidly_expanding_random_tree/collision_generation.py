from algo_constants import *
import numpy as np
np.random.seed(RANDOM_SEED)

class circle:
  def __init__(self, center, radius):
    self.center = np.array(center)
    self.radius = radius

class canvas_generator_2d_circular_obstacles:
  dimensions = NUM_DIMENSIONS
  canvas_x_start = X_START 
  canvas_x_end = X_END
  canvas_y_start = Y_START
  canvas_y_end = Y_END

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

  def genrate_canvas(self):
    
    for circle_index in range(self.no_of_circles):
      center = np.random.uniform(size=self.dimensions) * np.array([X_END, Y_END])
      radius = self.min_radii + np.random.uniform(size=1) * (self.max_radii - self.min_radii)
      new_circle = circle(center, radius)
      self.all_circles.append(new_circle)

  def does_line_intersect_circle(self, line):
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
      
      

if __name__ =='__main__':
  canvas_2d = canvas_generator_2d_circular_obstacles(no_of_circles=10, 
                                                     max_radii=10, min_radii=2)
  canvas_2d.genrate_canvas()
  line = np.array([[50,50], [60,60]])
  canvas_2d.does_line_intersect_circle(line)
  print canvas_2d 

    



  

  
