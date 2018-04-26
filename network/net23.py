#Server ML
import socket
import numpy as np
import pickle

NetworkPort = 59281
order = '3'

def sendnet(order):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', NetworkPort))#allow any ip
    print('Waiting for connection to send...')
    conn, addr = self.sock.accept()
    conn.sendall(msg.encode())
    print('order: '+msg+' sent.')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def recvnet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', NetworkPort))#allow any ip
    print('Waiting for connection to send...')
    conn, addr = self.sock.accept()
    final = b''
    while True:
        data = sock.recv(1024)
        if not data: break
        final += data
    final2 = pickle.loads(final)
    print(final2)
    return final2
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

while True:
    img = recvnet()
    time.sleep(2)#predict function
    sendnet(order)


'''
#Client Car

import socket
import numpy as np
import pickle

NetworkHost = '192.168.0.15'
NetworkPort = 59281
image = np.random.rand(180,320)

def sendnet(image):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((NetworkHost, NetworkPort))
    msg = pickle.dumps(image, protocol = 0)
    sock.sendall(msg)
    print('Image sent')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def recvnet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((NetworkHost, NetworkPort))
    while True:
        data = self.sock.recv(1024)
        data = data.decode()
        if not data: break#if something was received
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return data#only exit of the loop/ function

while True:
    sendnet(image)
    order = recvnet()
    #move the car
'''