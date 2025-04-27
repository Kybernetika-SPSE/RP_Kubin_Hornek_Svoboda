from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)


for i in range(5):
    led.value(0)
    sleep(0.5)
    led.value(1)
    sleep(0.5)