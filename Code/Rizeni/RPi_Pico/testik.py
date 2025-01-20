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
    print(config.Achsen[achse-1].name + ": " + str(config.Achsen[achse-1].getPos())) #printing current position
 

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
        
        sleep(0.025)

        if (tmp != config.Achsen[achse-1].getHomingSensorValue()): #homing finished
            config.Achsen[achse-1].setHomedStatus(True)
            config.Achsen[achse-1].setPos(0)
            break


config.Achsen[0].setDesiredPos(90)
config.Achsen[1].setDesiredPos(90)


while True:

    
    if config.Achsen[0].getHomedStatus():
        if abs(config.Achsen[0].getPos() - config.Achsen[0].getDesiredPos()) > config.Achsen[0].oneStep:
            spinMotor(1, config.Achsen[0].getDesiredPos())
        else:
            config.Achsen[0].setDesiredPos(float(input("Enter new desired angle angle for " + config.Achsen[0].name + ": ")) % 360)
    else:
        print(config.Achsen[0].name + " is not homed. Do you want to home it? Y/N: ")
        if (input() == "y"):
            print("Homing...")
            home(1)
        else:
            print("Homing cancelled")