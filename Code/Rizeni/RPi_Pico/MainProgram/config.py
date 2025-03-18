from machine import Pin

#region Motors

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
        self.movingStatus = 0

    def __str__(self):
        return f"{self.name},{self.axisNumber},{self.enPin},{self.dirPin},{self.stepPin},{self.homingSensorPin},{self.stepsPerRevolution},{self.maxDegree},{self.microstepping},{self.stepPin}, {self.pos}, {self.desiredPos}" 

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
    
    def setMovingStatus(self, numb):
        self.movingStatus = numb #0 - not started, 1 - moving, 2 - done
        #comm.sendMessage(self.name)
        
    def getMovingStatus(self):
        return self.movingStatus #0 - not started, 1 - moving, 2 - done
    

    

Achsen = []

#A1
Achsen.append(Achse("A1", 1,
                    0, #enPin
                    1, #dirPin
                    2, #stepPin
                    3, #homingSensorPin
                    200, #stepsPerRevolution
                    90, #maxDegree
                    1/4)) #microstepping
Achsen[0].setPos(0)
Achsen[0].setDesiredPos(0)
Achsen[0].setHomedStatus(0)
Achsen[0].setMovingStatus(0)

#A2
#Achsen.append(Achse("A2", 2,
#                    6, #enPin
#                    7, #dirPin
#                    8, #stepPin
#                    9, #homingSensorPin
#                    200, #stepsPerRevolution
#                    180, #maxDegree
#                    1/4)) #microstepping

Achsen.append(Achse("A2", 2,
                    22, #enPin
                    26, #dirPin
                    27, #stepPin
                    28, #homingSensorPin
                    200, #stepsPerRevolution
                    180, #maxDegree
                    1/4)) #microstepping
Achsen[1].setPos(0)
Achsen[1].setDesiredPos(0)
Achsen[1].setHomedStatus(0)
Achsen[1].setMovingStatus(0)





#endregion