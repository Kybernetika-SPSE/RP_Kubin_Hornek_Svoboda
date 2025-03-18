class Client:
    def __init__(self, name, IP):
        self.name = name #adding name to identify clients
        self.IP = IP #client's IP address

Clients = []

Clients.append(Client("RPi Pico", "192.168.200.19"))