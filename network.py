import socket
import json
#Network class to init new client connection with the server. And get player id from the server.
class Network:
    def __init__(self):
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = self.connect()
    
    def get_id(self):
        return self.id
    
    def connect(self):
        try:
            self.server.connect(self.ADDR)
            return self.server.recv(4096).decode()
        except:
            pass
    #This function is used to send data to the server from the client.
    #By converting json to string and string to json.
    def send(self, data):
        try:
            self.server.send(str.encode(json.dumps(data)))
            return json.loads(self.server.recv(4096).decode())
        except socket.error as e:
            print(e)