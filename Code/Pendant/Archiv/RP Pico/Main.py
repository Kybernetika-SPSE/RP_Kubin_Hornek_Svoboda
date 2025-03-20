from machine import Pin, UART
import time

# UART komunikace s displejem
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Pull up rezistory pro tlačítka
button1 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)
button3 = Pin(4, Pin.IN, Pin.PULL_UP)

def send_to_nextion(command):
    end_cmd = b'\xff\xff\xff'
    uart.write(command.encode() + end_cmd)
    time.sleep(0.1)

# Předešlé stavy tlačítek
pre_button1 = True
pre_button2 = True
pre_button3 = True

while True:
    # Čtení aktualního stavu tlačítka
    c_button1 = button1.value()
    c_button2 = button2.value()
    c_button3 = button3.value()
    
    if not c_button1 and pre_button1:
        send_to_nextion("b0.val=1")
        send_to_nextion("b1.val=0")
        send_to_nextion("b2.val=0")
        
    if not c_button2 and pre_button2:
        send_to_nextion("b0.val=0")
        send_to_nextion("b1.val=1")
        send_to_nextion("b2.val=0")
        
    if not c_button3 and pre_button3:
        send_to_nextion("b0.val=0")
        send_to_nextion("b1.val=0")
        send_to_nextion("b2.val=1")
    
    # Po zmáčknutí jiného talčítka se stav přehazuje zpět na předešlý (neboli vypnutý)
    pre_button1 = c_button1
    pre_button2 = c_button2
    pre_button3 = c_button3
    
    # Zdržení proti deboucingu
    time.sleep(0.05)  