from machine import Pin
from time import sleep
import network
import socket

led = Pin('LED', Pin.OUT)
led.value(0)


def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        led.value(1)
        sleep(0.5)
        led.value(0)
        sleep(0.5)
    print("Got this IP address: " + wlan.ifconfig()[0])

connect("ssid", "password")
led.value(1)