from machine import Pin

class Achse:
    def __init__(self, name, axisNumber, enPin, dirPin, stepPin, homingSensorPin, stepsPerRevolution, maxDegree, microstepping):
        self.name = name #adding name to identify axes
        self.axisNumber = axisNumber #adding axis number
        self.enPin = Pin(enPin, Pin.OUT) #enable pin
        self.dirPin = Pin(dirPin, Pin.OUT) #direction change pin, high should be clockwise
        self.stepPin = Pin(stepPin, Pin.OUT) #step pin
        self.homingSensorPin = Pin(homingSensorPin, Pin.IN, Pin.PULL_DOWN) #pin with end position sensor, if homed the value is zero
        self.stepsPerRevolution = stepsPerRevolution #steps per revolution
        self.maxDegree = maxDegree #max degree in axis
        self.microstepping = microstepping #microstepping value like full-step or half-step
        self.oneStep = 360/((stepsPerRevolution/microstepping) * 2) #angle change by one step

    #current positon related things
    def setPos(self, pos):
        self.pos = pos
    
    def getPos(self):
        return self.pos
    
    def stepMade(self, direction): #direction 1 means clockwise
        self.pos = ((self.getPos() + (self.oneStep * direction)) % 360)


    #homing related things
    def setHomedStatus(self, homed):
        self.homed = homed

    def getHomedStatus(self):
        return self.homed
    
    def getHomingSensorValue(self):
        return self.homingSensorPin.value()
    
    
    #desired positon related things
    def setDesiredPos(self, desiredPos):
        self.desiredPos = desiredPos #% 360

    def getDesiredPos(self):
        return self.desiredPos
    

Achsen = []

#A1
Achsen.append(Achse("A1", 1, 2, 0, 1, 6, 200, 90, 1/4))
Achsen[0].setPos(0)
Achsen[0].setHomedStatus(0)

#A2
Achsen.append(Achse("A2", 2, 5, 3, 4, 22,200, 90, 1/4))
Achsen[1].setPos(0)
Achsen[1].setHomedStatus(0)