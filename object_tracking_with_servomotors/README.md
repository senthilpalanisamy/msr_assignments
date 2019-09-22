This file contains code for tracking an object using camera mounted on 
servo motor

Instructions to run:-
1. Install requirements.txt (This file may include a few extra libraries 
   that are used in other assignments)
2. Run python object_tracking.py

Description of files:-
1. servo_control.py contains a class which is used for controlling the servo
   motors
   1. The servo controller used here is the pololu micro maestro controller
   2. UART signals are communicated using serial library to the maestro 
      controller
   Hints:-
   1. Depending on the board you are using and the preferred communication 
   mode, this class should be rewritten
   2. If the important method interfaces are written in a way that is 
      consistent with this class definition, the object_tracking code can be
      used without any modifications
   3. The servo motor adjustment logic in this class is strictly based on the
      assumption that the intial configuration of the camera is such that
      the x-axis of the camera is opposite to the direction in which the pan
      servo moves and the y-axis of the camera points in the same direction 
      as the pan movement of the camera. You will need to change this logic
      if this assumption is violated.
2. Object_tracking.py
   1. This file contains code for detecting a simple blue cube and tracking 
      it using CSRT tracker.
   2. This file also contains the main loop that acquires images from the 
      cameras and continuously controlling the camera based on x and y 
      disparity of the object centroid from the image centroid.
   Hints:-
   1. If you wish to track more complex objects, just replace the detect_blue_cude
      functions with a fucntion that detects objects of your interest. If the 
      function interface is preserved, the rest of the code can be run without
      any modifications
   2. You may like to change the vide_stream number based on the camera
     source you are using.


