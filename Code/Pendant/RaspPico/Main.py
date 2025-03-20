from machine import Pin, UART, ADC
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

button1 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)
button3 = Pin(4, Pin.IN, Pin.PULL_UP)

x_axis = ADC(26)  # GP26
y_axis = ADC(27)  # GP27
button = Pin(15, Pin.IN, Pin.PULL_UP)  

X_CENTER = 32768  
Y_CENTER = 32768  


DEAD_ZONE = 2000  

def map_value_with_deadzone(value, center):
    """Map joystick values considering center position and dead zone"""
    if abs(value - center) < DEAD_ZONE:
        return 50 
    
    if value < center:
        return map_value(value, 0, center - DEAD_ZONE, 0, 49)
    else:
        return map_value(value, center + DEAD_ZONE, 65535, 51, 100)

def map_value(x, in_min, in_max, out_min, out_max):
    """Map analog values to a different range"""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def send_to_nextion(command):
    """Send command to Nextion display"""
    end_cmd = b'\xff\xff\xff'
    uart.write(command.encode() + end_cmd)
    time.sleep(0.1)  

def read_joystick():
    """Read joystick values and return mapped coordinates"""
    
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()
    joy_btn = button.value()
    
    x_mapped = map_value_with_deadzone(x_raw, X_CENTER)
    y_mapped = map_value_with_deadzone(y_raw, Y_CENTER)
    
    return x_mapped, y_mapped, joy_btn


prev_button1 = True
prev_button2 = True
prev_button3 = True
prev_joy_button = True


def calibrate_joystick():
    """Calibrate joystick center position"""
    print("Center the joystick and wait...")
    time.sleep(2)
    
    
    x_sum = 0
    y_sum = 0
    samples = 10
    
    for _ in range(samples):
        x_sum += x_axis.read_u16()
        y_sum += y_axis.read_u16()
        time.sleep(0.1)
    
    x_center = x_sum // samples
    y_center = y_sum // samples
    
    print(f"Calibrated center - X: {x_center}, Y: {y_center}")
    return x_center, y_center


X_CENTER, Y_CENTER = calibrate_joystick()


while True:
    
    x, y, curr_joy_button = read_joystick()
    
    
    send_to_nextion(f'txtX.txt="X Position: {x}"')
    send_to_nextion(f'txtY.txt="Y Position: {y}"')
    
    
    curr_button1 = button1.value()
    curr_button2 = button2.value()
    curr_button3 = button3.value()
    
    
    if not curr_button1 and prev_button1:
        send_to_nextion('txtBtn.txt="Button 1 Pressed"')
        
    if not curr_button2 and prev_button2:
        send_to_nextion('txtBtn.txt="Button 2 Pressed"')
        
    if not curr_button3 and prev_button3:
        send_to_nextion('txtBtn.txt="Button 3 Pressed"')
        
    if not curr_joy_button and prev_joy_button:
        send_to_nextion('txtBtn.txt="Joystick Button Pressed"')
    
    
    prev_button1 = curr_button1
    prev_button2 = curr_button2
    prev_button3 = curr_button3
    prev_joy_button = curr_joy_button
    
    time.sleep(0.05)