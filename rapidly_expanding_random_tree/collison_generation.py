from algo_constants import *
import numpy as np
np.random.seed(RANDOM_SEED)

class circle:
  def __init__(self, center, radius):
    self.center = center
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

  def genrate_canvas(self):
    
      for circle_index in range(self.no_of_circles):
        center = np.random.uniform(size=self.dimensions) * np.array([X_END, Y_END])
        radius = self.min_radii + np.random.uniform(size=1) * (self.max_radii - self.min_radii)
        new_circle = circle(center, radius)
        self.all_circles.append(new_circle)
  def check_point_circle_intersection(self, point)
    point_x, point_y = point

    is_intersect = False
    for each_circle in self.all_circles:
      

if __name__ =='__main__':
  canvas_2d = canvas_generator_2d_circular_obstacles(no_of_circles=10, 
                                                     max_radii=10, min_radii=2)
  canvas_2d.genrate_canvas()
  print canvas_2d 

    



  

  
