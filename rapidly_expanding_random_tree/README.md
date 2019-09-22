Instructions to run
1. Install libraries from requirements.txt
2. python rapidly_expanding_random_tree.py to run the file 

File descriptions:-
1. collision_generation.py files contains classes for generating obstacles and 
   plotting the final RRT graph
2. rapidly_expanding_random_tree contains logic for generating the rrt details


Note:-
Edit line 85 to canvas_2d = canvas_generator_2d_circular_obstacles(no_of_circles=10,                                                                                                                                                                                     max_radii=10, min_radii=2)  
for generating rrt with circular obstacles
Exit line 85 to canvas_2d = canvas_generator_with_random_obstacles(image_path = path_to_image)
for generating rrt with irregular obstacles defined by bitmap
