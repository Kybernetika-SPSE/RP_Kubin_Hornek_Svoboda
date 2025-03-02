import smbus2 as smbus
import errno
import time
import ArrOfBytes

def scanI2C(bus_number):
    bus = smbus.SMBus(bus_number)
    device_count = 0
    foundDevices = [] #this stores devices found on i2c
    
    for device in range(3, 128):
        try:
            bus.write_byte(device, 0)
            #print("Found {0}".format(hex(device)))
            device_count = device_count + 1
            foundDevices.append(hex(device))
        except IOError as e:
            if e.errno != errno.EREMOTEIO:
                #print("Error: {0} on address {1}".format(e, hex(device)))
                pass
        except Exception as e: # exception if read_byte fails
            #print("Error unk: {0} on address {1}".format(e, hex(device)))
            pass
    
    bus.close()
    bus = None

    return foundDevices


print("This have been found on bus 1 I2C: " + str(scanI2C(1)))

bus = smbus.SMBus(1)
commBusy = 0
counter = 1

data = [counter, 25]
rcvData = []

while True:
    try:
        if not commBusy: 
        ############################# send ############################# 
            data = ArrOfBytes.encode(data)         
            for i in range(len(data)):
                bus.write_byte(0x41, data[i]) #bus.write_byte(0x41, counter)
                print("Posilam tato data: " + str(data[i]))
            commBusy = 1
            time.sleep(0.5)   
        else:
        ############################# receive #############################
            rcvData.append = bus.read_byte(0x41)
            
            if(len(rcvData) == 2):
                rcvData = ArrOfBytes.decode(rcvData)
                print("Recieved decoded data: " + str(rcvData))
                rcvData = []
                if rcvData == counter and False:
                    counter = counter + 1
                    commBusy = 0
                    print("Precetl jsem tato data: " + str(rcvData))
                    print("Counter je: " + str(counter))

            print("Ctu")
           
            

    except IOError as e:
        if e.errno != errno.EREMOTEIO:
            print("Error: {0} on address {1}".format(e, hex(41)))
            pass
    except Exception as e: # exception if read_byte fails
        print("Error unk: {0} on address {1}".format(e, hex(41)))
        pass

    time.sleep(0.5)