import serial

class servo_motor_control:

  PULSE_START = 992
  PULSE_END = 2000
  ANGLE_START = 0
  ANGLE_END = 180

  def __init__(self, device_number, port_name = '/dev/ttyACM0' ):
    self.servo_port = None
    self.device_number = device_number
    self.port_name = port_name 



  def generate_uart_command_for_angle(self, angle):
    pulse_range = self.PULSE_END - self.PULSE_START
    angle_range = self.ANGLE_END - self.ANGLE_START
    starting_header = '\x84'
    mask_7_bits = 0x7F 
    bits_per_command_value = 7
    pulse_per_angle = float(pulse_range) / angle_range
    pulse_value = int(self.PULSE_START + angle * pulse_per_angle * 4)
    servo_value_msb = chr(pulse_value & mask_7_bits)
    pulse_value = pulse_value >> bits_per_command_value
    servo_value_lsb = chr(pulse_value & mask_7_bits)
    command_to_servo = starting_header + self.device_number + servo_value_msb + \
                       servo_value_lsb
    return command_to_servo

  def start_port_connection(self):
    self.servo_port = serial.Serial(self.port_name)

  def send_command_to_servo(self, command):
    self.servo_port.write(command)

  def generate_uarts_commands_for_sequence(angles)

  def close_connection(self):
    self.servo_port.close()

if __name__=='__main__':
    angle = 180
    servo_control = servo_motor_control(device_number='\x00')
    command = servo_control.generate_uart_command_for_angle(angle)
    print command
    servo_control.start_port_connection()
    servo_control.send_command_to_servo(command)
    servo_control.close_connection()
  

