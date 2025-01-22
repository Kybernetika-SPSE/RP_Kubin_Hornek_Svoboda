import socket
import config

def sendMessage(MESSAGE):
    TCP_IP = config.Endpoints[0].IP
    TCP_PORT = config.Endpoints[0].Port
    BUFFER_SIZE = config.Endpoints[0].BufferSize
    #MESSAGE = "Hello, World!"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = 0
    data = s.recv(BUFFER_SIZE)

    s.close()

    #print(config.Endpoints[0].name)
    #print(config.Endpoints[0].IP)
    #print(config.Endpoints[0].Port)
    #print(config.Endpoints[0].BufferSize)
    print(data)