def encode(rawdata, checkNumLen = 3, checkNum = 0x01):
    currentChecknum = checkNum
    dataToBeSent = []

    for data in rawdata:
        if (data <= (0xff >> checkNumLen)): #determining max value to be sent based on checkNumLen
            currentChecknum = 7
            dataToBeSent.append(data << checkNumLen | currentChecknum)      
        else:
            pocetOpakovani = (data // (0xff >> checkNumLen)) + 1
            for i in range(pocetOpakovani):     
                tmp_msg = 0
                if (i == (pocetOpakovani - 1)): #pokud je v poslednim pruchodu
                    tmp_msg = data % (0xff >> checkNumLen)
                    currentChecknum = 0
                else:
                    tmp_msg = (0xff >> checkNumLen)
                    data -= (0xff >> checkNumLen)
                    currentChecknum = checkNum
                    
                dataToBeSent.append(tmp_msg << checkNumLen | currentChecknum)
        checkNum += 1
        if(checkNum == 7):
            checkNum = 1
    return(dataToBeSent)


def decode(rawdata, checkNumLen = 3, checkNum = 0x01):
    tmpMsg = 0
    decodedMsg = 0
    decodedData = []

    for data in rawdata:
        checkNum = data & 0x7
        content = data >> checkNumLen

        if (checkNum == 0):
            tmpMsg += content
            decodedMsg = tmpMsg
            tmpMsg = 0
            #return fullMsg
            decodedData.append(decodedMsg)
        elif (checkNum == 7):
            tmpMsg = content
            decodedMsg = tmpMsg
            tmpMsg = 0
            #return fullMsg
            decodedData.append(decodedMsg)
        else:
            tmpMsg += content
            decodedMsg = tmpMsg          
    return decodedData