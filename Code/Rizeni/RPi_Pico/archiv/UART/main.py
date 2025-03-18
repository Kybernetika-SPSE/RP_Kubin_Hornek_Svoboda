import machine
import time

uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5), timeout=1000)

while True:
    bufR = bytearray(2)

    uart.readinto(bufR)

    bufS = bytearray(2)
    bufS = bufR

    print(bufR)

    uart.write(bufS)
    time.sleep(0.1)



    #data = uart.read(5)
    #data = uart.readline()