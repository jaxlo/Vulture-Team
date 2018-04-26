#new server
from PIL import Image
import numpy as np
import h5py
import sys
import time
import pickle
import socket

order = '0'
NetworkPort = 59281

class NetworkServer:#run on the pi (May need to change to CNN)
    def __init__(self, sock=None, port=NetworkPort):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', NetworkPort))#allow any ip
            self.sock.listen(1)#limit connection to one client
            print('Waiting for the ML client')
            self.conn, self.addr = self.sock.accept()
            print('Successfully connected to the client.')
        else:
            self.sock = sock
            print('sock is sock')#is this ever used?

    def send(self, msg):
    	msg2 = order
        #msg2 = pickle.dumps(msg, protocol = 0)
        self.conn.sendall(msg2)

    def listen(self):
        final = b''#try the "final += data" trick if it errors
        while True:
            data = self.sock.recv(1024)
            if not data: break
            final += data
        print(final)
        final2 = pickle.loads(final)
        print('something was found')
        return final2#only exit for the loop/ function

image = net.listen()
print('image: '+str(image))

net.send(str(order))#this works(maybe not when we want it to)