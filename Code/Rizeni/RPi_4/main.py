import serial
import time
from serial.serialutil import SerialException
import random

#ser = serial.Serial("/dev/serial0", 115200) #UART1, TX=14 RX=15
control = serial.Serial("/dev/ttyAMA3", 115200) #UART3, TX=4 RX=5
pendant = serial.Serial("/dev/ttyAMA4", 115200) #UART4, TX=8 RX=9

class Achse:
    def __init__(self):
        self.desPos = 0
        self.curPos = 0
        self.homing = 0

A1 = Achse()
A2 = Achse()
A3 = Achse()
A4 = Achse()
A5 = Achse()
A6 = Achse()

A1.desPos = 45
A1.homing = 1
A2.desPos = 45
A2.homing = 1

counter = 1
lastTime = 0



while True:
    try:
        #prepare buffer for sending
        
        A1.desPos = random.randint(0, 90)
        A2.desPos = random.randint(0, 90)
        
        bufS = bytearray(24)
            
        bufS[0] = counter
        bufS[1] = A1.desPos & 0xff
        bufS[2] = A1.desPos >> 8
        bufS[3] = A1.homing & 0xff
        bufS[4] = A2.desPos & 0xff
        bufS[5] = A2.desPos >> 8
        bufS[6] = A2.homing & 0xff
        bufS[7] = A3.desPos & 0xff
        bufS[8] = A3.desPos >> 8
        bufS[9] = A3.homing & 0xff
        bufS[10] = A4.desPos & 0xff
        bufS[11] = A4.desPos >> 8
        bufS[12] = A4.homing & 0xff
        bufS[13] = A5.desPos & 0xff
        bufS[14] = A5.desPos >> 8
        bufS[15] = A5.homing & 0xff
        bufS[16] = A6.desPos & 0xff
        bufS[17] = A6.desPos >> 8
        bufS[18] = A6.homing & 0xff
        bufS[23] = counter
        
        control.write(bufS) #send buffer
        
            
        time.sleep(0.2) #wait before receiving
        
        #receiving
        bufR = control.read(24)

        if(len(bufR) == 24): #received something
            if(bufR[0] == bufR[23] == counter): #data valid
                counter = counter + 1
                if(counter >= 256):
                    counter = 1
                lastTime = time.time() #time when last message was received

            A1.curPos = bufR[1] + bufR[2]
            A2.curPos = bufR[3] + bufR[4]
            A3.curPos = bufR[5] + bufR[6]
            A4.curPos = bufR[7] + bufR[8]
            A5.curPos = bufR[9] + bufR[10]
            A6.curPos = bufR[11] + bufR[12]

            print("1Counter je: " + str(bufR[0]))
            print("2Counter je: " + str(bufR[23]))
    except:
        print("An exception occurred") 

    #print(time.time() - lastTime)
    print(time.time() - lastTime >= 2.0)
    if (time.time() - lastTime >= 2.0):
        control.reset_input_buffer() #reset input before, without this occured many problems
        control.reset_output_buffer()
        counter = 1
        print("Connection timed out")



#region Struct

#buf[0] = counter
#buf[1] = A1 desPos
#buf[2] = A1 desPos
#buf[3] = A1 Homing
#buf[4] = A2 desPos
#buf[5] = A2 desPos
#buf[6] = A2 Homing
#buf[7] = A3 desPos
#buf[8] = A3 desPos
#buf[9] = A3 Homing
#buf[10] = A4 desPos
#buf[11] = A4 desPos
#buf[12] = A4 homing
#buf[13] = A5 desPos
#buf[14] = A5 desPos
#buf[15] = A5 Homing
#buf[16] = A6 desPos
#buf[17] = A6 desPos
#buf[18] = A6 Homing
#buf[19] = Reserve
#buf[20] = Reserve
#buf[21] = Reserve
#buf[22] = Reserve
#buf[23] = counter

#endregion