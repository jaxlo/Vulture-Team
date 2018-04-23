#---IMOPRTANT--- This sends the image and does not go into the CNN
from PIL import Image
import numpy as np
import glob
import os
import h5py
import sys
import time
import pickle
import socket

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

class NetworkServer:#run on the pi
    def __init__(self, sock=None, port=NetworkPort):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', NetworkPort))#allow any ip
            self.sock.listen(1)#limit connection to one client
            print('Waiting for the ML client')
            self.conn, addr = self.sock.accept()
            print('Successfully connected to the client.')
        else:
            self.sock = sock
            print('sock is sock')#is this ever used?

    def send(self, msg):
        msg2 = pickle.dumps(msg, protocol = 0)
        self.conn.sendall(msg2)

    def listen(self):
        while True:
            data = self.conn.recv(1024)
            data = data.decode()
            if data != '':#if something was received
                return data#only exit of the loop/ function


net = NetworkServer()#Waits for a connection to the ML program
net.send(img)
order = net.listen()
print(order)
