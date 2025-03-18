#tady zatim nic neni, veskery kod je v testik
from machine import Pin
import machine
from time import sleep
import config
import _thread

uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5), timeout=1000)

 
def step(achse, direction):
    if (direction == 1): #clockwise
        config.Achsen[achse-1].dirPin.value(1)
    elif (direction == -1): #counter clockwise
        config.Achsen[achse-1].dirPin.value(0)

    config.Achsen[achse-1].stepPin.value(not config.Achsen[achse-1].stepPin.value())
    config.Achsen[achse-1].stepMade(direction)
    #print(config.Achsen[achse-1].name + ": " + str(config.Achsen[achse-1].getPos())) #printing current position
 

def spinMotor(achse, desPos):
    #checking limits
    if (desPos > config.Achsen[achse-1].maxDegree):
        desPos = config.Achsen[achse-1].maxDegree
        config.Achsen[achse-1].setDesiredPos(desPos)
    elif (desPos < 0):
        desPos = 0
        config.Achsen[achse-1].setDesiredPos(desPos)
    
    #checking in which direction should the rotation be
    if (config.Achsen[achse-1].getPos() <= desPos):
        step(achse, 1)
    else:
        step(achse, -1)


def home(achse):
    while (not config.Achsen[achse-1].getHomedStatus()):
        tmp = config.Achsen[achse-1].getHomingSensorValue()

        if (not config.Achsen[achse-1].getHomingSensorValue()): #if not staying on sensor
            step(achse, -1)        
        else:
            step(achse, 1)
        
        sleep(0.0125)

        if (tmp != config.Achsen[achse-1].getHomingSensorValue()): #homing finished
            config.Achsen[achse-1].setHomedStatus(True)
            config.Achsen[achse-1].setPos(0)
            break


#config.Achsen[0].setDesiredPos(90)
#config.Achsen[1].setDesiredPos(360)

homeAchseX = [0,0,0,0,0,0]


def uart_thread():
    while True:
        bufR = bytearray(24)
        uart.readinto(bufR)

        if(len(bufR) == 24): #received something
            if(bufR[0] == bufR[23] != 0): #data valid           
                config.Achsen[0].setDesiredPos(bufR[1] | bufR[2] << 8)
                homeAchseX[0] = bufR[3]
                
                config.Achsen[1].setDesiredPos(bufR[4] | bufR[5] << 8)
                homeAchseX[1] = bufR[6]
                
                #config.Achsen[2].setDesiredPos(bufR[7] | bufR[8] << 8)
                #homeAchseX[2] = bufR[9]
                
                #config.Achsen[3].setDesiredPos(bufR[10] | bufR[11] << 8)
                #homeAchseX[3] = bufR[12]
                
                #config.Achsen[4].setDesiredPos(bufR[13] | bufR[14] << 8)
                #homeAchseX[4] = bufR[15]
                
                #config.Achsen[5].setDesiredPos(bufR[16] | bufR[17] << 8)
                #homeAchseX[5] = bufR[18]
                
                print("A1 desired position je: " + str(config.Achsen[0].getDesiredPos()))
                print("A2 desired position je: " + str(config.Achsen[1].getDesiredPos()))


                bufS = bytearray(24)
                bufS = bufR
            

                print(bufR)
                uart.write(bufS)


def control_thread():
    while True:
        for i in range(len(config.Achsen)):
                if config.Achsen[i].getHomedStatus():
                    if abs(config.Achsen[i].getPos() - config.Achsen[i].getDesiredPos()) > config.Achsen[i].oneStep:
                        spinMotor(i+1, config.Achsen[i].getDesiredPos())
                        config.Achsen[i].setMovingStatus(1)
                    else:
                        config.Achsen[i].setMovingStatus(2)
                        print(config.Achsen[i].name + ": " + str(config.Achsen[i].getPos()))
                else:
                    #print("osa " + str(i+1) + " neni homed")
                    if (homeAchseX[i] == 1):
                        print("budu ji ale homovat")
                        home(i+1)
                sleep(0.001)




#Starting threads

second_thread = _thread.start_new_thread(control_thread, ())
uart_thread()