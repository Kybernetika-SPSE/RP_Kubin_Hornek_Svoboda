### main.py
import utime
import time
from machine import mem32,Pin
from i2cSlave import i2c_slave
import ArrOfBytes


### --- connect as slave over i2c--- ###
s_i2c = i2c_slave(0,sda=0,scl=1,slaveAddress=0x41)

rcvData = []
dataLen = 2 #len in bytes
rcvDone = False
data = []
print("Program started")

try:
    while True:
        if(s_i2c.any() and not rcvDone):
        ############################# send ############################# 
            tmp_rcv = s_i2c.get()
            print(tmp_rcv)
            if(tmp_rcv != 0):
                rcvData.append(tmp_rcv)
                if(len(rcvData) == dataLen):
                    #print("Recieved raw data: " + str(rcvData))
                    print("Recieved decoded data: " + str(ArrOfBytes.decode(rcvData)))
                    data = rcvData
                    rcvData = []
                    rcvDone = True
        if(s_i2c.anyRead() and rcvDone):
        ############################# receive #############################
            data = ArrOfBytes.encode(data)
            for i in range(len(data)):
                print("Posilam tato data: " + str(data[i]))
                s_i2c.put(data[i])
        #if(len(rcvData) == 1):
        #    rcvData = []
            #print(str(rcvData))
        
except KeyboardInterrupt:
    pass