#new client
from PIL import Image
import numpy as np
import h5py
import sys
import time
import pickle
import socket

NetworkHost = '192.168.1.101'
NetworkPort = 59281


def makeArray(): #turns image into an array
    global pixels
    currentImg = 'C:\\Users\\reyno\\Pictures\\blueroadforward1.jpg' #change to image location
    loadImg = Image.open(currentImg)
    #print(loadImg)
    pixels = np.array(loadImg)#only gets the blue band of the image
    pixels.resize(320,180)#makes it a 2D array
    #print(pixels)
    return pixels

img = makeArray()


class NetworkClient:#run on ML /remote computer
    #global NetworkHost, NetworkPort

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host=NetworkHost, port=NetworkPort):#put in init?
        self.sock.connect((NetworkHost, NetworkPort))
        print('Connected to: '+NetworkHost+ ' On port: '+str(NetworkPort))

    def send(self, msg):#used for sending orders
    	msg2 = pickle.dumps(msg, protocol = 0)
        self.sock.sendall(msg2.encode())#sendall only stops sending when everything is sent

    def listen(self):#used for getting images
        while True:
            #self.conn.settimeout(1.0)
            data = self.conn.recv(1024)
            #self.conn.settimeout(None)
            data = data.decode()
            if data != '':#if something was received
                return data#only exit of the loop/ function



net = NetworkServer()#Waits for a connection to the ML program
net.connect()

try:   
    net.send(img)
    print('image sent')
except:
    print('failed at send')
#----------------------------------------------------------
try:
    order = net.listen()
    print(order)
    print('order recieved')
except:
    print('failed at first recieve')