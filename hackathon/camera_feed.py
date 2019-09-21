import cv2
from object_tracking import detect_object
from servo_control import *
import time

cap = cv2.VideoCapture(2)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

servo_motor1 = servo_details(device_name = '\x00')
servo_motor2 = servo_details(device_name = '\x01')
motors = [servo_motor1, servo_motor2]
servo_control = servo_motor_control()
image_center_x = 320
image_center_y = 240
max_error = 10
servo_control.initialise_motor_positions([servo_motor1, servo_motor2])

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_with_detection, centroid = detect_object(frame)

    # print frame.shape
    # out.write(frame)
    if frame_with_detection is not None:
      x_c, y_c = centroid
      if abs(x_c - image_center_x) > max_error and \
        abs(y_c - image_center_y)  > max_error:
        servo_control.adjust_motor_angles(centroid, [320, 240], motors)
      cv2.circle(frame_with_detection, (centroid[0], centroid[1]), 7, (255, 255, 255), -1)

    else:
      frame_with_detection = frame


    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame_with_detection)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
