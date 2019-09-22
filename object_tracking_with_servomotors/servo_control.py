import time

import serial
import random

# horizontal_angle = 11
# vertical_angle = 7.6

# horizontal_angle = 6
# vertical_angle = 3.8 

horizontal_angle = 3
vertical_angle = 1.9 

class servo_details:

    def __init__(self, device_name):
      self.device_name = device_name
      self.current_position = 0


class servo_motor_control:

  PULSE_START = 480
  PULSE_END = 2400
  ANGLE_START = 0
  ANGLE_END = 180

  def __init__(self, port_name = '/dev/ttyACM0' ):
    self.servo_port = None
    self.port_name = port_name 
    self.servo_port = serial.Serial(self.port_name, baudrate=9600)
 
  def initialise_motor_positions(self, motors):
    command = self.generate_uart_command_for_angle( 120, motors[0].device_name)
    self.send_command_to_servo(command)
    command = self.generate_uart_command_for_angle( 120, motors[1].device_name)
    self.send_command_to_servo(command)


  def generate_uart_command_for_pulse(self, pulse_value, device_number):

    starting_header = '\x84'
    mask_7_bits = 0x7F 
    bits_per_command_value = 7
    servo_value_lsb = chr(pulse_value & mask_7_bits)
    pulse_value = pulse_value >> bits_per_command_value
    servo_value_msb = chr(pulse_value & mask_7_bits)
    command_to_servo = starting_header + device_number + servo_value_lsb + \
                       servo_value_msb
    return command_to_servo



  def generate_uart_command_for_angle(self, angle, device_number):
    pulse_range = self.PULSE_END - self.PULSE_START
    angle_range = self.ANGLE_END - self.ANGLE_START
    quarters_per_microsecond = 4
    pulse_per_angle = float(pulse_range) / angle_range
    pulse_value = int(self.PULSE_START + angle * pulse_per_angle) * \
                                                      quarters_per_microsecond

    command_to_servo = self.generate_uart_command_for_pulse(pulse_value, 
                                                            device_number)
    return command_to_servo

  def convert_pulse_to_angle(self, pulse_value):

    pulse_value = pulse_value / 4.0 - self.PULSE_START
    angle = pulse_value / (self.PULSE_END - self.PULSE_START) * 180
    return angle


  def adjust_motor_angles(self, error_point, actual_location, motors):
    error_limit = 10 
    x,y = error_point
    xc, yc = actual_location
    #x_error = xc - x
    #y_error = yc - y
    motor1, motor2 = motors
    delta_theta_pan = abs(xc - x) / 640.0 * horizontal_angle 
    delta_theta_tilt = abs(yc - y) / 480.0 * vertical_angle 

    pan_angle = self.convert_pulse_to_angle(self.get_servo_position(motor1))

    print 'current_x_position', pan_angle, 'pulse_value', 
    print self.get_servo_position(motor1)
    print 'delta_thera_x', delta_theta_pan, 'delta_theta_y', delta_theta_tilt

    tilt_angle = self.convert_pulse_to_angle(self.get_servo_position(motor2))

 
    print 'current_y_position', tilt_angle, 'pulse_value', self.get_servo_position(motor2)
    print 'delta_angle', delta_theta_tilt

    # if 80 < pan_angle < 100:
    #   print 'current x position near 90'
    #   angle_to_move_x = random.choice([100, 80])
    if(tilt_angle < 90): 
      if xc > x: 
        angle_to_move_x = pan_angle + delta_theta_pan
      else:
        angle_to_move_x = pan_angle - delta_theta_pan

    else:
      if xc > x: 
        angle_to_move_x = pan_angle - delta_theta_pan
      else:
        angle_to_move_x = pan_angle + delta_theta_pan

    if yc > y:
      angle_to_move_y = tilt_angle - delta_theta_tilt
    else:
      angle_to_move_y = tilt_angle + delta_theta_tilt



    # if 80 < tilt_angle < 100:
    #   print 'cuurent_y position near 90'
    #   angle_to_move_y = random.choice([100, 80])
    # if tilt_angle < 90:
    #   if yc > y:
    #     angle_to_move_y = tilt_angle + delta_theta_tilt
    #   else:
    #     angle_to_move_y = tilt_angle - delta_theta_tilt
    # else:
    #   print 'angle > 90'
    #   if yc > y:
    #     print 'point above centroid'
    #     angle_to_move_y = tilt_angle - delta_theta_tilt
    #   else:
    #     angle_to_move_y = tilt_angle + delta_theta_tilt
    command = self.generate_uart_command_for_angle(angle_to_move_x, motor1.device_name)
    self.send_command_to_servo(command)
    command = self.generate_uart_command_for_angle(angle_to_move_y, motor2.device_name)
    self.send_command_to_servo(command)
    print 'angle to move_x', angle_to_move_x, 'angle_to_move_y', angle_to_move_y



  def send_command_to_servo(self, command):
    self.servo_port.write(command)

  def generate_uart_commands_for_sequence(self, angles, device_number):
    commands = []
    for angle in angles:
      uart_command = self.generate_uart_command_for_angle(angle, device_number)
      commands.append(uart_command)
    return commands

  def send_angle_sequence(self, commands):

    for index, uart_command in enumerate(commands):
      self.send_command_to_servo(uart_command)
      print 'command sent', angles[index]
      time.sleep(0.1)

  def get_servo_position(self, servo_motor):
     position = self.servo_port.write('\x90'+ servo_motor.device_name)
     motor_position = self.servo_port.read(2)
     pulse_width = (ord(motor_position[1]) << 8) + ord(motor_position[0])
     return pulse_width


  def __del__(self):
    self.servo_port.close()

if __name__=='__main__':
    angle = 10
    angles = [0, 30, 60, 90, 120, 150, 180, 150, 120, 90, 60, 30, 0]
    servo_motor1 = servo_details(device_name = '\x00')
    servo_motor2 = servo_details(device_name = '\x01')
    servo_control = servo_motor_control()
    #servo_control.initialise_motor_positions([servo_motor1, servo_motor2])
    #servo_control.adjust_motor_angles([100, 300], [320, 240], [servo_motor1, servo_motor2])

    # command_sequence_motor1 = servo_control.generate_uart_commands_for_sequence(angles, 
    #                                                                device_number='\x00')
    # command_sequence_motor2 = servo_control.generate_uart_commands_for_sequence(angles, 
    #                                                               device_number='\x01')

    command = servo_control.generate_uart_command_for_angle(angle, servo_motor2.device_name)
    servo_control.send_command_to_servo(command)

    # print servo_control.get_servo_position(servo_motor1)
    # command = servo_control.generate_uart_command_for_angle(angle, device_number=servo_motor1.device_name)
    # servo_control.send_command_to_servo(command)
    # print servo_control.get_servo_position(servo_motor1)
    # print command
    # servo_control.start_port_connection()
    # servo_control.send_angle_sequence(command_sequence_motor1)
    # servo_control.send_angle_sequence(command_sequence_motor2)
    # servo_control.close_connection()
  

