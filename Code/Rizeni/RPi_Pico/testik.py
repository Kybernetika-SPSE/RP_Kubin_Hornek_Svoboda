from machine import Pin
from time import sleep
import config

 
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

while True:
    for i in range(len(config.Achsen)):
        if ((config.Achsen[0].getMovingStatus() == 2) and (config.Achsen[1].getMovingStatus() == 2)):
            positions = str(input("Enter new desired positions in following format: A1,A2: "))
            config.Achsen[0].setDesiredPos(float(positions.split(",")[0]) % 360)
            config.Achsen[1].setDesiredPos(float(positions.split(",")[1]) % 360)


        if config.Achsen[i].getHomedStatus():
            if abs(config.Achsen[i].getPos() - config.Achsen[i].getDesiredPos()) > config.Achsen[i].oneStep:
                spinMotor(i+1, config.Achsen[i].getDesiredPos())
                config.Achsen[i].setMovingStatus(1)
            else:
                config.Achsen[i].setMovingStatus(2)
                print(config.Achsen[i].name + ": " + str(config.Achsen[i].getPos()))
        else:
            print(config.Achsen[i].name + " is not homed. Do you want to home it? Y/N: ")
            if (input() == "y"):
                print("Homing...")
                home(i+1)
            else:
                print("Homing cancelled")
        sleep(0.001)