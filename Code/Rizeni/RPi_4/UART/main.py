import serial
import time
from serial.serialutil import SerialException

ser = serial.Serial("/dev/serial0", 115200)

counter = 1

while True:
    bufS = bytearray(2)
    
    bufS[0] = counter
    bufS[1] = 256 - counter
    ser.write(bufS)
    
    
    time.sleep(0.2)
    
    bufR = ser.read(2)
    print(bufR[0])
    print(bufR[1])

    if(bufR[0] == counter):
        counter = counter + 1
        if(counter >= 256):
            counter = 1