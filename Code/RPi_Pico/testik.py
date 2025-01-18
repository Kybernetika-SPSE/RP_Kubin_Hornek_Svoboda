from machine import Pin
import config

 
def step(achse, direction):
    config.Achsen[achse-1].stepPin.value(not config.Achsen[achse-1].stepPin.value())
    config.Achsen[achse-1].stepMade(direction)
    print(config.Achsen[achse-1].name + ": " + str(config.Achsen[achse-1].getPos()))
 

def spinMotor(achse, desPos):
    if (config.Achsen[achse-1].getPos() <= desPos) or (abs(config.Achsen[0].getPos() - config.Achsen[0].getDesiredPos()) > 180): #checking in which direction should the rotation be
        config.Achsen[achse-1].dirPin.value(1)
        step(achse, 1)
    else:
        config.Achsen[achse-1].dirPin.value(0)
        step(achse, -1)




config.Achsen[0].setDesiredPos(360)
config.Achsen[1].setDesiredPos(360)


while True:

    if abs(config.Achsen[0].getPos() - config.Achsen[0].getDesiredPos()) > config.Achsen[0].oneStep:
        spinMotor(1, config.Achsen[0].getDesiredPos())
    else:
        config.Achsen[0].setDesiredPos(float(input("Enter new angle: "))%360)

    if abs(config.Achsen[1].getPos() - config.Achsen[1].getDesiredPos()) > config.Achsen[1].oneStep:
        spinMotor(2, config.Achsen[1].getDesiredPos())