import time

uyxcvnm,;;llkjhgnb n,?
'kigt'import serial

class servo_motor_control:

  PULSE_START = 992
  PULSE_END = 2000
  ANGLE_START = 0
  ANGLE_END = 180

  def __init__(self, port_name = '/dev/ttyACM0' ):
    self.servo_port = None
    self.port_name = port_name 



  def generate_uart_command_for_angle(self, angle, device_number):
    pulse_range = self.PULSE_END - self.PULSE_START
    angle_range = self.ANGLE_END - self.ANGLE_START
    starting_header = '\x84'
    mask_7_bits = 0x7F 
    bits_per_command_value = 7
    quarters_per_microsecond = 4
    pulse_per_angle = float(pulse_range) / angle_range
    pulse_value = int(self.PULSE_START + angle * pulse_per_angle) * quarters_per_microsecond
    servo_value_lsb = chr(pulse_value & mask_7_bits)
    pulse_value = pulse_value >> bits_per_command_value
    servo_value_msb = chr(pulse_value & mask_7_bits)
    command_to_servo = starting_header + device_number + servo_value_lsb + \
                       servo_value_msb
    return command_to_servo

  def start_port_connection(self):
    self.servo_port = serial.Serial(self.port_name, baudrate=9600)

  def send_command_to_servo(self, command):
    self.servo_port.write(command)

  def generate_uart_commands_for_sequence(self, angles, device_number):
    commands = []
    for angle in angles:
      uart_command = self.generate_uart_command_for_angle(angle, device_number)
      commands.append(uart_command)
    return commands

  def send_angle_sequence(self, commands):

    angles = [0, 30, 60, 90, 120, 150, 180, 150, 120, 90, 60, 30, 0]
    for index, uart_command in enumerate(commands):

      self.send_command_to_servo(uart_command)
      print 'command sent', angles[index]
      time.sleep(3)

  def close_connection(self):
  #  self.servo_port.close()

if __name__=='__main__':
    angle = 30
    angles = [0, 30, 60, 90, 120, 150, 180, 150, 120, 90, 60, 30, 0]
    servo_control = servo_motor_control()
    command_sequence_motor1 = servo_control.generate_uart_commands_for_sequence(angles, 
                                                                   device_number='\x00')
    command_sequence_motor2 = servo_control.generate_uart_commands_for_sequence(angles, 
                                                                   device_number='\x01')

    command = servo_control.generate_uart_command_for_angle(angle)
    command = servo_control.generate_uart_command_for_angle(angle, device_number='\x00')
    # print command
    #servo_control.start_port_connection()
    servo_control.send_angle_sequence(command_sequence_motor1)
    servo_control.send_angle_sequence(command_sequence_motor2)
    servo_control.close_connection()
  

