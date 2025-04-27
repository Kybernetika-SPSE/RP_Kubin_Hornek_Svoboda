import serial
import time
from serial.serialutil import SerialException
import random
from threading import Thread

control = serial.Serial("/dev/ttyAMA3", 115200) #UART3, TX=4 RX=5
pendant = serial.Serial("/dev/ttyAMA4", 115200) #UART4, TX=8 RX=9

class Achse:
    def __init__(self):
        self.desPos = 0
        self.curPos = 0
        self.homing = 0
        self.homed = 0

A1 = Achse()
A2 = Achse()
A3 = Achse()
A4 = Achse()
A5 = Achse()
A6 = Achse()

#Allowing homing
A1.homing = 1
A2.homing = 1
A3.homing = 1
A4.homing = 1
A5.homing = 1
A6.homing = 1

#Enabling axis
A1.enabled = 1
A2.enabled = 0
A3.enabled = 0
A4.enabled = 0
A5.enabled = 0
A6.enabled = 0


def enableListByte(): 
    #Value for byte with enabling axis
    enableList = 0
    enableList = enableList | A1.enabled
    enableList = enableList | (A2.enabled << 1)
    enableList = enableList | (A3.enabled << 2)
    enableList = enableList | (A4.enabled << 3)
    enableList = enableList | (A5.enabled << 4)
    enableList = enableList | (A6.enabled << 5)
    return enableList


def randomPos():
    A1.desPos = random.randint(0, 90)
    A2.desPos = random.randint(0, 90)
    A3.desPos = random.randint(0, 90)
    A4.desPos = random.randint(0, 90)
    A5.desPos = random.randint(0, 90)
    A6.desPos = random.randint(0, 90)



#print("Axis 4 is: " + str((enableList & 0x8) >> 3))

#region Control

def comm_Control():

    counter = 1
    lastTime = 0

    print("PySerial version: " + serial.__version__)

    while True:

        control.reset_input_buffer() #reset input before, without this occured many problems
        control.reset_output_buffer()

        #randomPos()
        A1.desPos = 90
        
        #prepare buffer for sending
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
        
        bufS[19] = enableListByte()
        
        bufS[23] = counter
        
        control.write(bufS) #send buffer
        print("Control Data sent!") 
        
        time.sleep(0.2) #wait before receiving
                
        #receiving
        if (control.inWaiting() > 10):
            print("Pico availible!")
            
            bufR = control.read(24)
         
            if(len(bufR) == 24): #received something
                if(bufR[0] == bufR[23] == counter): #data valid
                    counter = counter + 1
                    if(counter >= 256):
                        counter = 1
                    lastTime = time.time() #time when last message was received

                A1.curPos = bufR[1] | bufR[2] << 8
                A1.homed = bufR[3]
                
                A2.curPos = bufR[4] + bufR[5]
                A2.homed = bufR[6]
                
                A3.curPos = bufR[7] + bufR[8]
                A3.homed = bufR[9]
                
                A4.curPos = bufR[10] + bufR[11]
                A4.homed = bufR[12]
                
                A5.curPos = bufR[13] + bufR[14]
                A5.homed = bufR[15]
                
                A6.curPos = bufR[16] + bufR[17]
                A6.homed = bufR[18]
                

                print("Control - Counter1 je: " + str(bufR[0]))
                print("Control - Counter2 je: " + str(bufR[23]))

                #print("{} osa je {}, current pos je: {}, ale desired pos je: {}".format("A1:", str((enableList & 0x1)), str(A1.curPos), str(A1.desPos)))
                #print("{} osa je {}, current pos je: {}, ale desired pos je: {}".format("A2:", str((enableList & 0x2) >> 1), str(A2.curPos), str(A2.desPos)))
                #print("{} osa je {}, current pos je: {}, ale desired pos je: {}".format("A3:", str((enableList & 0x4) >> 2), str(A3.curPos), str(A3.desPos)))
                #print("{} osa je {}, current pos je: {}, ale desired pos je: {}".format("A4:", str((enableList & 0x8) >> 3), str(A4.curPos), str(A4.desPos)))
                #print("{} osa je {}, current pos je: {}, ale desired pos je: {}".format("A5:", str((enableList & 0x10) >> 4), str(A5.curPos), str(A5.desPos)))
                #print("{} osa je {}, current pos je: {}, ale desired pos je: {}".format("A6:", str((enableList & 0x20) >> 5), str(A6.curPos), str(A6.desPos)))


        #print(time.time() - lastTime)
        #print(time.time() - lastTime >= 2.0)
        
        if ((time.time() - lastTime >= 2.0)):
            control.reset_input_buffer() #reset input before, without this occured many problems
            control.reset_output_buffer()
            counter = 1
            print("Control - Connection timed out, current time out time: " + str(time.time() - lastTime))

#endregion

#region Pendant

def comm_Pendant():
    counter = 1
    lastTime = 0

    print("PySerial version: " + serial.__version__)

    while True:
        pendant.reset_input_buffer() #reset input before, without this occured many problems
        pendant.reset_output_buffer()
       
        #prepare buffer for sending
        bufS = bytearray(24)
            
        bufS[0] = counter
        
        bufS[1] = A1.curPos & 0xff
        bufS[2] = A1.curPos >> 8
        bufS[3] = A1.homing & 0xff
        
        bufS[4] = A2.curPos & 0xff
        bufS[5] = A2.curPos >> 8
        bufS[6] = A2.homing & 0xff
        
        bufS[7] = A3.curPos & 0xff
        bufS[8] = A3.curPos >> 8
        bufS[9] = A3.homing & 0xff
        
        bufS[10] = A4.curPos & 0xff
        bufS[11] = A4.curPos >> 8
        bufS[12] = A4.homing & 0xff
        
        bufS[13] = A5.curPos & 0xff
        bufS[14] = A5.curPos >> 8
        bufS[15] = A5.homing & 0xff
        
        bufS[16] = A6.curPos & 0xff
        bufS[17] = A6.curPos >> 8
        bufS[18] = A6.homing & 0xff
        
        bufS[19] = enableListByte()
        
        bufS[23] = counter
        
        pendant.write(bufS) #send buffer
        print("Pendant - Data sent!") 
        
        time.sleep(0.2) #wait before receiving
                
        #receiving
        if (pendant.inWaiting() > 10):
            print("Pendant availible!")
            
            bufR = pendant.read(24)
         
            if(len(bufR) == 24): #received something
                if(bufR[0] == bufR[23] == counter): #data valid
                    counter = counter + 1
                    if(counter >= 256):
                        counter = 1
                    lastTime = time.time() #time when last message was received

                A1.desPos = bufR[1] | bufR[2] << 8
                A1.homed = bufR[3]
                
                A2.desPos = bufR[4] + bufR[5]
                A2.homed = bufR[6]
                
                A3.desPos = bufR[7] + bufR[8]
                A3.homed = bufR[9]
                
                A4.desPos = bufR[10] + bufR[11]
                A4.homed = bufR[12]
                
                A5.desPos = bufR[13] + bufR[14]
                A5.homed = bufR[15]
                
                A6.desPos = bufR[16] + bufR[17]
                A6.homed = bufR[18]

                print("Pendant - Counter1 je: " + str(bufR[0]))
                print("Pendant - Counter2 je: " + str(bufR[23]))

        
        if ((time.time() - lastTime >= 2.0)):
            pendant.reset_input_buffer() #reset input before, without this occured many problems
            pendant.reset_output_buffer()
            counter = 1
            print("Pendant - Connection timed out, current time out time: " + str(time.time() - lastTime))
#endregion


Thread(target = comm_Control).start()
Thread(target = comm_Pendant).start()




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
