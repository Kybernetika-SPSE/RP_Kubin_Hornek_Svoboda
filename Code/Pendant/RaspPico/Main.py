from machine import Pin, UART, ADC
import time
import _thread

# Setup UART communication with Nextion
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


# Setup buttons with pull-up resistors
button1 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)
button3 = Pin(6, Pin.IN, Pin.PULL_UP)

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

def read_joystick():
    """Read joystick values and return mapped coordinates"""
    
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()

    
    x_mapped = map_value_with_deadzone(x_raw, X_CENTER)
    y_mapped = map_value_with_deadzone(y_raw, Y_CENTER)
    
    return x_mapped, y_mapped

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


# Previous button states
prev_button1 = True
prev_button2 = True
prev_button3 = True

def send_to_nextion(command):
    """Send command to Nextion display"""
    end_cmd = b'\xff\xff\xff'
    uart.write(command.encode() + end_cmd)
    time.sleep(0.1)
    
# Main loop
def main_thread():
    while True:
        # Read current button states
        curr_button1 = button1.value()
        curr_button2 = button2.value()
        curr_button3 = button3.value()
        
        # Read joystick values
        x, y = read_joystick()
        
        # Send joystick values to Nextion
        # Assuming you have number variables n0 and n1 on your Nextion display for x and y

        send_to_nextion(f'txtX.txt="X Position: {x}"')  # Check if this command matches your Nextion text field name
        send_to_nextion(f'txtY.txt="Y Position: {y}"')  # Check if this command matches your Nextion text field name
        
        # Handle other buttons
        if curr_button1: #and prev_button1:
            send_to_nextion("b0.val=1")
            send_to_nextion("b1.val=0")
            send_to_nextion("b2.val=0")
            
        if curr_button2: #and prev_button2:
            send_to_nextion("b0.val=0")
            send_to_nextion("b1.val=1")
            send_to_nextion("b2.val=0")
            
        if curr_button3: #and prev_button3:
            send_to_nextion("b0.val=0")
            send_to_nextion("b1.val=0")
            send_to_nextion("b2.val=1")
        
        # Update previous states
        prev_button1 = curr_button1
        prev_button2 = curr_button2
        prev_button3 = curr_button3
        
        
        time.sleep(0.05)  # Small delay for debouncing


def uart_thread():
    uart2 = UART(1, baudrate=115200, tx=Pin(4), rx= Pin(5))
    while True:
        bufR = bytearray(24)
        uart2.readinto(bufR)

        if(len(bufR) == 24): #received something
            if(bufR[0] == bufR[23] != 0): #data valid           
                

                bufS = bytearray(24)
                bufS[0] = bufR[0]
                bufS[23] = bufR[23]
           
                print(bufR)
                uart2.write(bufS)

hlavni_vlakno = _thread.start_new_thread(uart_thread, ())
main_thread()