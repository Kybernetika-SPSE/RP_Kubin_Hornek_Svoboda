from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)
led.value(1) #Only to know if the Raspberry is on

print('Raspberry started')