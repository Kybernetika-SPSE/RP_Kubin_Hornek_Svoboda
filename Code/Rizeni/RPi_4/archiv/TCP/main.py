import socket
addr = socket.getaddrinfo('0.0.0.0', 7777)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    print(cl.recv(1024))
    cl.send(bytes("response", "ascii"))
    cl.close()