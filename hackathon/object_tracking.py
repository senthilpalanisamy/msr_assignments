import cv2
import numpy as np



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
    safety_margin = 0.2

    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
     
      

    lower_blue = np.array([blue_min, saturation_value, value])
    upper_blue = np.array([blue_max ,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
      
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


def detect_and_trackobject(video_stream, detection_function):

  cap = cv2.VideoCapture(video_stream)
  is_detection_initialised = False
  tracker = None

  while(cap.isOpened()):
    ret, frame = cap.read()

    if(not is_detection_initialised):
      op_image, bbox = detection_function(frame)

      if(bbox is not None):

        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, bbox)
        is_detection_initialised = True

        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    else:
      is_success, box = tracker.update(frame)
      print 'tracking', box, is_success
      if not is_success:
        is_detection_initialised = False

      x, y, w, h = [int(num) for num in box]
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    

    cv2.imshow('output_image', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

  cap.release()
  cv2.destroyAllWindows()



if __name__=='__main__':
  detect_and_trackobject(video_stream=0, detection_function=detect_blue_cube)
  file_name = '/home/senthil/work/msr_assignments/data/frames/blue_square_images/blue_square.avi'
  # process_video(file_name)
  # track_using_tracker()
  # image = cv2.imread('/home/senthil/work/msr_assignments/data/frames/blue_square_images/input_image0218.jpg')
  # detect_object(image)
