import cv2
import numpy as np



def detect_object(image):
    '''
    source code credit - https://www.learnopencv.com/invisibility-cloak-using-color-detection-and-segmentation-with-opencv/
    '''


    blurred_image = cv2.GaussianBlur(image, (7, 7), 0)
    saturation_value = 120
    value = 100
    blue_max = 150
    blue_min = 90
    expected_contour_area = 16954
    safety_margin = 1.5

    # converting from BGR to HSV color space
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
     
      

    lower_blue = np.array([blue_min, saturation_value, value])
    upper_blue = np.array([blue_max ,255,255])
    mask1 = cv2.inRange(hsv,lower_blue,upper_blue)
       
    # Generating the final mask to detect red color

     
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
      
    #creating an inverted mask to segment out the cloth from the frame
    mask2 = cv2.bitwise_not(mask1)
     
      
    #Segmenting the cloth out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(image,image,mask=mask2)

    cnts, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    selected_contours = []
    
    for contour in cnts: 
        area = cv2.contourArea(contour)
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area

        if expected_contour_area / safety_margin < area < expected_contour_area * safety_margin and\
           solidity > 0.8:
           selected_contours.append(contour)


    if selected_contours:
      largest_contour = max(selected_contours, key = cv2.contourArea)[0]
      if len(largest_contour) > 0:
        bounding_box = cv2.boundingRect(largest_contour) 
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3) 
        return image, bounding_box

    return None, None





def display_thresholded_image(image):

    cv2.namedWindow('threshold_window')
    cv2.createTrackbar('red_upper', 'threshold_window', 0, 30, r_lower)
    cv2.createTrackbar('red_lower', 'threshold_window', 160, 180, r_higher)

    mask = detect_ball(image) 


    while True:


      cv2.imshow('threshold_window', mask)
      min_val = int(cv2.getTrackbarPos('Min', 'threshold_window'))
      max_val = int(cv2.getTrackbarPos('Max', 'theshold_window'))
      if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

def process_video(file_name):
  cap = cv2.VideoCapture(file_name)

  while(True):
      # Capture frame-by-frame
      ret, frame = cap.read()
  
      # Our operations on the frame come here
      image_with_detection, _ = detect_object(frame)
  
      # Display the resulting frame
      cv2.imshow('frame',image_with_detection)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  # When everything done, release the capture

  cap.release()
  cv2.destroyAllWindows()

def track_using_tracker():
  tracker = cv2.TrackerCSRT_create()
  cap = cv2.VideoCapture('/home/senthil/work/msr_assignments/data/videos/blue_square.avi')

  is_detection_initialised = False

  while(cap.isOpened()):
    ret, frame = cap.read()

    if(not is_detection_initialised):
      op_image, bbox = detect_object(frame)

      if(bbox is not None):

        print 'detecting object'
        tracker.init(frame, bbox)
        is_detection_initialised = True
    else:
      mask_image, box = tracker.update(frame)
      print 'tracking'
      x, y, w, h = [int(num) for num in box]
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      op_image = frame

    if op_image is None:
      op_image = frame

    cv2.imshow('frame', op_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  cap.release()
  cv2.destroyAllWindows()



if __name__=='__main__':
  file_name = '/home/senthil/work/msr_assignments/data/frames/blue_square_images/blue_square.avi'
  # process_video(file_name)
  track_using_tracker()
  # image = cv2.imread('/home/senthil/work/msr_assignments/data/frames/blue_square_images/input_image0218.jpg')
  # detect_object(image)
