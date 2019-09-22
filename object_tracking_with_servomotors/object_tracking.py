import time

import cv2
import numpy as np

from servo_control import *


def detect_blue_cube(image):
    '''
    source code credit - 
    https://www.learnopencv.com/invisibility-cloak-using-color-detection-
    and-segmentation-with-opencv/
    '''


    blurred_image = cv2.GaussianBlur(image, (7, 7), 0)
    saturation_value = 120
    value = 100
    blue_max = 150
    blue_min = 90
    expected_contour_area = 16954
    safety_margin = 0.5

    # Generating mask for spotting blue cube
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([blue_min, saturation_value, value])
    upper_blue = np.array([blue_max ,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))


    # Finding and filtering all contours  
    cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    selected_contours = []
    
    for contour in cnts: 
        area = cv2.contourArea(contour)
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area

        if (expected_contour_area * (1 - safety_margin) < area < 
           expected_contour_area * (1 + safety_margin)) and\
           solidity > 0.8:
           selected_contours.append(contour)

    if selected_contours:
      largest_contour = max(selected_contours, key = cv2.contourArea)
      if len(largest_contour) > 0:
        bounding_box = cv2.boundingRect(largest_contour) 
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3) 
        return image, bounding_box

    return None, None


def detect_and_track_object(video_stream, detection_function):

  # Initialising variables
  cap = cv2.VideoCapture(video_stream)
  is_detection_initialised = False
  tracker = None
  servo_motor1 = servo_details(device_name = '\x00')
  servo_motor2 = servo_details(device_name = '\x01')
  motors = [servo_motor1, servo_motor2]
  servo_control = servo_motor_control()
  image_center_x = 320
  image_center_y = 240
  max_error = 10
  servo_control.initialise_motor_positions([servo_motor1, servo_motor2])

  while(cap.isOpened()):
    ret, frame = cap.read()

    # Object detection and tracking logic

    if(not is_detection_initialised):
      _, bbox = detection_function(frame)
      if(bbox is not None):
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, bbox)
        is_detection_initialised = True
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    else:
      is_success, bbox = tracker.update(frame)
      print 'tracking', bbox, is_success
      if not is_success:
        is_detection_initialised = False
      x, y, w, h = [int(num) for num in bbox]
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)



    # Motor control logic
    if bbox is not None:
      x_c, y_c = x + w //2, y + h //2
      centroid = [x_c, y_c]
      if abs(x_c - image_center_x) > max_error and \
        abs(y_c - image_center_y)  > max_error:
        servo_control.adjust_motor_angles(centroid, [320, 240], motors)
      cv2.circle(frame, (centroid[0], centroid[1]), 7, (255, 255, 255), -1)

    

    cv2.imshow('output_image', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    # time.sleep(0.2)

  cap.release()
  cv2.destroyAllWindows()



if __name__=='__main__':
  detect_and_track_object(video_stream=2, detection_function=detect_blue_cube)
  file_name = '/home/senthil/work/msr_assignments/data/frames/blue_square_images/blue_square.avi'
