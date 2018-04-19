import socket, pickle
NetworkPort = 59281
NetworkHost = '192.168.1.2'

class NetworkClient:#run on ML /remote computer
    #global NetworkHost, NetworkPort

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host=NetworkHost, port=NetworkHost):#put in init?
        self.sock.connect((NetworkHost, NetworkPort))
        print('Connected to: '+NetworkHost+ ' On port: '+str(NetworkPort))

    def send(self, msg):#used for sending orders
        self.sock.sendall(msg.encode())#sendall only stops sending when everything is sent

    def listen(self):#used for getting images
        final = b''#try the "final += data" trick if it errors
        while True:
            data = self.sock.recv(1024)
            if not data: break
            final += data
        print(final)
        final2 = pickle.loads(data)
        print('something was found')
        return final2#only exit for the loop/ function

net = NetworkClient()#this works
net.connect(host='192.168.1.2')#this works

net.send(str('order'))#this works

image = net.listen()

#final = pickle.loads(image)
print('image: '+str(final))
