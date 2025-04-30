from machine import Pin, UART, ADC
import time
import _thread

uart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))

button1 = Pin(2, Pin.IN, Pin.PULL_UP)
button2 = Pin(3, Pin.IN, Pin.PULL_UP)
button3 = Pin(4, Pin.IN, Pin.PULL_UP)

x_axis = ADC(26)  # GP26
y_axis = ADC(27)  # GP27  

X_CENTER = 32768  
Y_CENTER = 32768  

DEAD_ZONE = 2000  


class Achse:
    def __init__(self):
        self.desPos = 0
        self.curPos = 0
        self.homing = 0
        self.homed = 0
        self.enabled = 0
        self.enabledCMD = 0

A1 = Achse()
A2 = Achse()
A3 = Achse()
A4 = Achse()
A5 = Achse()
A6 = Achse()


def enableListByte(): 
    enableList = 0
    enableList = enableList | A1.enabledCMD
    enableList = enableList | (A2.enabledCMD << 1)
    enableList = enableList | (A3.enabledCMD << 2)
    enableList = enableList | (A4.enabledCMD << 3)
    enableList = enableList | (A5.enabledCMD << 4)
    enableList = enableList | (A6.enabledCMD << 5)
    return enableList



def map_value_with_deadzone(value, center):
    if abs(value - center) < DEAD_ZONE:
        return 50 
    
    if value < center:
        return map_value(value, 0, center - DEAD_ZONE, 0, 49)
    else:
        return map_value(value, center + DEAD_ZONE, 65535, 51, 100)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def send_to_nextion(command):
    end_cmd = b'\xff\xff\xff'
    uart.write(command.encode() + end_cmd)
    time.sleep(0.05)  
    
    # Vyčistit buffer od odpovědí
    if uart.any():
        uart.read()

def read_joystick():
    
    x_raw = x_axis.read_u16()
    y_raw = y_axis.read_u16()
    
    x_mapped = map_value_with_deadzone(x_raw, X_CENTER)
    y_mapped = map_value_with_deadzone(y_raw, Y_CENTER)
    
    return x_mapped, y_mapped

def calibrate_joystick():
    print("Vycentruj joystick a čekej")
    time.sleep(2)
    
    x_sum = 0
    y_sum = 0
    samples = 10
    
    for _ in range(samples):
        x_sum += x_axis.read_u16()
        y_sum += y_axis.read_u16()
        time.sleep(0.1)
    
    x_center = x_sum // samples
    y_center = y_sum // samples
    
    print(f"Kalibrovaný centr - X: {x_center}, Y: {y_center}")
    return x_center, y_center

def check_uart_for_data():
    """Čtení dat z UART a detekce stisknutí tlačítek"""
    global nextion_button0_active, nextion_button1_active, nextion_button2_active
    global nextion_button3_active, nextion_button4_active, nextion_button5_active
    global nextion_back_button_active
    
    if uart.any():
        data = uart.read()
        
        if data:
            # Hledání standardního vzoru dat z Nextion
            if len(data) >= 7 and data[0] == 0x65:
                component_id = data[2]
                event_type = data[3]
                page_id = data[4]
                
                print(f"Nextion event: component_id={component_id}, event_type={event_type}, page_id={page_id}")
                
            # Pokud používáte starší způsob komunikace nebo vlastní protokol
            # Ponecháme také původní detekci pro kompatibilitu
            for byte in data:
                if byte == 0x01:
                    nextion_button0_active = True
                    print("Detekováno tlačítko 1 z dat UART (jednobajtový kód)")
                elif byte == 0x02:
                    nextion_button1_active = True
                elif byte == 0x03:
                    nextion_button2_active = True
                elif byte == 0x04:
                    nextion_button3_active = True
                elif byte == 0x05:
                    nextion_button4_active = True
                elif byte == 0x06:
                    nextion_button5_active = True
                elif byte == 0x69:  
                    nextion_back_button_active = True
                    print("Detekováno tlačítko ZPĚT z dat UART (jednobajtový kód)")
                    
                elif byte == 0x20: #Enabled/Disabled
                    A1.enabledCMD = not A1.enabledCMD
                elif byte == 0x21: #Homing Enabled/Disabled
                    A1.homing = not A1.homing
                elif byte == 0x22: #A1 Pos +
                    A1.desPos =  A1.curPos + 5
                elif byte == 0x23: #A1 Pos -
                    A1.desPos =  A1.curPos - 5
                elif byte == 0x24: #A1 min
                    A1.desPos =  1
                elif byte == 0x25: #A1 max
                    A1.desPos =  360
                    
                elif byte == 0x30: #Enabled/Disabled
                    A2.enabledCMD = not A2.enabledCMD
                elif byte == 0x31: #Homing Enabled/Disabled
                    A2.homing = not A2.homing
                elif byte == 0x32: #A2 Pos +
                    A2.desPos =  A2.curPos + 5
                elif byte == 0x33: #A2 Pos -
                    A2.desPos =  A2.curPos - 5
                elif byte == 0x34: #A2 min
                    A2.desPos =  1
                elif byte == 0x35: #A2 max
                    A2.desPos =  360
                    
                elif byte == 0x40: #Enabled/Disabled
                    A3.enabledCMD = not A3.enabledCMD
                elif byte == 0x41: #Homing Enabled/Disabled
                    A3.homing = not A3.homing
                elif byte == 0x42: #A3 Pos +
                    A3.desPos =  A3.curPos + 5
                elif byte == 0x43: #A3 Pos -
                    A3.desPos =  A3.curPos - 5
                elif byte == 0x44: #A3 min
                    A3.desPos =  1
                elif byte == 0x45: #A3 max
                    A3.desPos =  360
                    
                elif byte == 0x50: #Enabled/Disabled
                    A4.enabledCMD = not A4.enabledCMD
                elif byte == 0x51: #Homing Enabled/Disabled
                    A4.homing = not A4.homing
                elif byte == 0x52: #A4 Pos +
                    A4.desPos =  A4.curPos + 5
                elif byte == 0x53: #A4 Pos -
                    A4.desPos =  A4.curPos - 5
                elif byte == 0x54: #A4 min
                    A4.desPos =  1
                elif byte == 0x55: #A4 max
                    A4.desPos =  360
                    
                elif byte == 0x60: #Enabled/Disabled
                    A5.enabledCMD = not A5.enabledCMD
                elif byte == 0x61: #Homing Enabled/Disabled
                    A5.homing = not A5.homing
                elif byte == 0x62: #A5 Pos +
                    A5.desPos =  A5.curPos + 5
                elif byte == 0x63: #A5 Pos -
                    A5.desPos =  A5.curPos - 5
                elif byte == 0x64: #A5 min
                    A5.desPos =  1
                elif byte == 0x65: #A5 max
                    A5.desPos =  360
                    
                elif byte == 0x70: #Enabled/Disabled
                    A6.enabledCMD = not A6.enabledCMD
                elif byte == 0x71: #Homing Enabled/Disabled
                    A6.homing = not A6.homing
                elif byte == 0x72: #A6 Pos +
                    A6.desPos =  A6.curPos + 5
                elif byte == 0x73: #A6 Pos -
                    A6.desPos =  A6.curPos - 5
                elif byte == 0x74: #A6 min
                    A6.desPos =  1
                elif byte == 0x75: #A6 max
                    A6.desPos =  360
                    
def setup_nextion_display():
    """Inicializace a nastavení Nextion displeje"""
    # Inicializační příkazy pro displej
    send_to_nextion("page 0")  # Přepnutí na stránku 0
    
    # Reset tlačítek na hodnotu 0
    send_to_nextion("t1.val=0")
    send_to_nextion("t2.val=0")
    send_to_nextion("t3.val=0")
    send_to_nextion("t4.val=0")
    send_to_nextion("t5.val=0")
    send_to_nextion("t6.val=0")
    
    # Nastavení detekce dotyků 
    send_to_nextion("bkcmd=3")  # Plná zpětná vazba

# Inicializace
X_CENTER, Y_CENTER = calibrate_joystick()

# Nastavení Nextion displeje
print("Nastavuji Nextion displej...")
setup_nextion_display()

# Předešlé stavy tlačítek
print("Inicializace dokončena, začínám hlavní smyčku")

def main_thread():
    last_display_update = time.time()
    
    pre_button1 = True
    pre_button2 = True
    pre_button3 = True
    
    # Stavy lokálních tlačítek na Pico, které kopírujeme do Nextion
    local_button0_state = 0
    local_button1_state = 0
    local_button2_state = 0

    nextion_button0_active = False
    nextion_button1_active = False
    nextion_button2_active = False
    nextion_button3_active = False
    nextion_button4_active = False
    nextion_button5_active = False
    nextion_button6_active = False
    nextion_back_button_active = False
    
    while True:
    # Kontrola dat z UART
        check_uart_for_data()
    
    # Čtení joysticku
        x, y = read_joystick()
    
    # Aktualizace hodnot na displeji (méně často)
        current_time = time.time()
        if current_time - last_display_update >= 1:  # Každou sekundu
            last_display_update = current_time
            send_to_nextion(f'txtX.txt="X Position: {x}"')
            send_to_nextion(f'txtY.txt="Y Position: {y}"')
            
            #A1
            send_to_nextion(f'en1.txt="{A1.enabled}"')
            
            send_to_nextion(f'A1Homed.txt="{A1.homed}"')
            
            send_to_nextion(f'm1r.txt="Rotace motoru: {A1.curPos}"')
            
            if (A1.homing):
                send_to_nextion(f'A1HomingCMD.txt="Homing enabled"')
            else:
                send_to_nextion(f'A1HomingCMD.txt="Homing disabled"')


            #A2
            send_to_nextion(f'en2.txt="{A2.enabled}"')
            
            send_to_nextion(f'A2Homed.txt="{A2.homed}"')
            
            send_to_nextion(f'm2r.txt="Rotace motoru: {A2.curPos}"')
            
            if (A2.homing):
                send_to_nextion(f'A2HomingCMD.txt="Homing enabled"')
            else:
                send_to_nextion(f'A2HomingCMD.txt="Homing disabled"')
            #A3
            send_to_nextion(f'en3.txt="{A3.enabled}"')
            send_to_nextion(f'A3Homed.txt="{A3.homed}"')
            send_to_nextion(f'm3r.txt="Rotace motoru: {A3.curPos}"')
            if (A3.homing):
                send_to_nextion(f'A3HomingCMD.txt="Homing enabled"')
            else:
                send_to_nextion(f'A3HomingCMD.txt="Homing disabled"')

            #A4
            send_to_nextion(f'en4.txt="{A4.enabled}"')
            send_to_nextion(f'A4Homed.txt="{A4.homed}"')
            send_to_nextion(f'm4r.txt="Rotace motoru: {A4.curPos}"')
            if (A4.homing):
                send_to_nextion(f'A4HomingCMD.txt="Homing enabled"')
            else:
                send_to_nextion(f'A4HomingCMD.txt="Homing disabled"')

            #A5
            send_to_nextion(f'en5.txt="{A5.enabled}"')
            send_to_nextion(f'A5Homed.txt="{A5.homed}"')
            send_to_nextion(f'm5r.txt="Rotace motoru: {A5.curPos}"')
            if (A5.homing):
                send_to_nextion(f'A5HomingCMD.txt="Homing enabled"')
            else:
                send_to_nextion(f'A5HomingCMD.txt="Homing disabled"')

            #A6
            send_to_nextion(f'en6.txt="{A6.enabled}"')
            send_to_nextion(f'A6Homed.txt="{A6.homed}"')
            send_to_nextion(f'm6r.txt="Rotace motoru: {A6.curPos}"')
            if (A6.homing):
                send_to_nextion(f'A6HomingCMD.txt="Homing enabled"')
            else:
                send_to_nextion(f'A6HomingCMD.txt="Homing disabled"')

    # Čtení aktuálního stavu fyzických tlačítek na Pico
        c_button1 = button1.value()
        c_button2 = button2.value()
        c_button3 = button3.value()
    
    # Zpracování fyzických tlačítek a aktualizace Nextion
        new_button0_state = 0
        new_button1_state = 0
        new_button2_state = 0
    
        if not c_button1 and pre_button1:  # Tlačítko 1 bylo stisknuto
            new_button0_state = 1
    
        if not c_button2 and pre_button2:  # Tlačítko 2 bylo stisknuto
            new_button1_state = 1
    
        if not c_button3 and pre_button3:  # Tlačítko 3 bylo stisknuto
            new_button2_state = 1
        
    # Aktualizace tlačítek na displeji pouze pokud se stav změnil
        if new_button0_state != local_button0_state:
            local_button0_state = new_button0_state
            send_to_nextion(f"r0.val=1")
            send_to_nextion(f"r1.val=0")
            send_to_nextion(f"r2.val=0")
        
        if new_button1_state != local_button1_state:
            local_button1_state = new_button1_state
            send_to_nextion(f"r0.val=0")
            send_to_nextion(f"r1.val=1")
            send_to_nextion(f"r2.val=0")
        
        if new_button2_state != local_button2_state:
            local_button2_state = new_button2_state
            send_to_nextion(f"r0.val=0")
            send_to_nextion(f"r1.val=0")
            send_to_nextion(f"r2.val=1")
    
    # Zpracování tlačítek z Nextion displeje
        if nextion_button0_active:
            print("Zpracování akce pro tlačítko 1 z Nextion displeje")
            nextion_button0_active = False  # Reset příznaku
        
        if nextion_button1_active:
            print("Zpracování akce pro tlačítko 2 z Nextion displeje")
            nextion_button1_active = False  # Reset příznaku
        
        if nextion_button2_active:
            print("Zpracování akce pro tlačítko 3 z Nextion displeje")
            nextion_button2_active = False  # Reset příznaku
        
        if nextion_button3_active:
            print("Zpracování akce pro tlačítko 4 z Nextion displeje")
            nextion_button3_active = False  # Reset příznaku
        
        if nextion_button4_active:
            print("Zpracování akce pro tlačítko 5 z Nextion displeje")
            nextion_button4_active = False  # Reset příznaku
        
        if nextion_button5_active:
            print("Zpracování akce pro tlačítko 6 z Nextion displeje")
            nextion_button5_active = False  # Reset příznaku
        
        if nextion_button6_active:
            print("Zpracování akce pro tlačítko 7 z Nextion displeje")
            nextion_button6_active = False  # Reset příznaku
        
        if nextion_back_button_active:
            print("Zpracování akce pro tlačítko ZPĚT z Nextion displeje")
        # send_to_nextion("page 0")  # například přechod na hlavní stránku
            nextion_back_button_active = False  # Reset příznaku
    
    # Aktualizace předešlých stavů fyzických tlačítek
        pre_button1 = c_button1
        pre_button2 = c_button2
        pre_button3 = c_button3
    
        time.sleep(0.05)
    
def uart_thread():
    uart2 = UART(1, baudrate=115200, tx=Pin(4), rx= Pin(5))
    while True:
        bufR = bytearray(24)
        uart2.readinto(bufR)

        if(len(bufR) == 24): #received something
            if(bufR[0] == bufR[23] != 0): #data valid           
                
                A1.curPos = bufR[1] | bufR[2] << 8
                A1.homed = bufR[3]
                A1.enabled = bufR[19] & 0x1
                
                A2.curPos = bufR[4] | bufR[5] << 8
                A2.homed = bufR[6]
                A2.enabled = (bufR[19] & 0x2) >> 1
                
                A3.curPos = bufR[7] | bufR[8] << 8
                A3.homed = bufR[9]
                A3.enabled = (bufR[19] & 0x4) >> 2
                
                A4.curPos = bufR[10] | bufR[11] << 8
                A4.homed = bufR[12]
                A4.enabled = (bufR[19] & 0x8) >> 3
                
                A5.curPos = bufR[13] | bufR[14] << 8
                A5.homed = bufR[15]
                A5.enabled = (bufR[19] & 0x10) >> 4
                
                A6.curPos = bufR[16] | bufR[17] << 8
                A6.homed = bufR[18]
                A6.enabled = (bufR[19] & 0x20) >> 5
                              
                
                bufS = bytearray(24)
                bufS[0] = bufR[0]


                bufS[1] = A1.desPos & 0xff
                bufS[2] = A1.desPos >> 8
                bufS[3] = A1.homing & 0xff
                
                bufS[4] = A2.desPos & 0xff
                bufS[5] = A2.desPos >> 8
                bufS[6] = A2.homing & 0xff
                
                bufS[7] = A3.desPos & 0xff
                bufS[8] = A3.desPos >> 8
                bufS[9] = A3.homing & 0xff
                
                bufS[10] = A4.desPos & 0xff
                bufS[11] = A4.desPos >> 8
                bufS[12] = A4.homing & 0xff
                
                bufS[13] = A5.desPos & 0xff
                bufS[14] = A5.desPos >> 8
                bufS[15] = A5.homing & 0xff
                
                bufS[16] = A6.desPos & 0xff
                bufS[17] = A6.desPos >> 8
                bufS[18] = A6.homing & 0xff

                bufS[19] = enableListByte()
                
                bufS[23] = bufR[23]
                

                print(bufR)
                uart2.write(bufS)
                
hlavni_vlakno = _thread.start_new_thread(uart_thread, ())
main_thread()