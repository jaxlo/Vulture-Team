import numpy as np
from PIL import Image
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import sys
import time
import pickle
import socket

NetworkHost = '192.168.1.102'
NetworkPort = 59281

img_width, img_height = 320, 180
bestclass = -1

def create_model():
	model = Sequential()#uncomment this------------------------------------------------------------------------
	model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(320, 180, 1)))
	model.add(Conv2D(32, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))

	model.add(Conv2D(64, (3, 3), activation='relu'))
	model.add(Conv2D(64, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))

	model.add(Flatten())
	model.add(Dense(256, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(4, activation='softmax'))

	model.summary()

	return model

class NetworkClient:#run on ML /remote computer
    def __init__(self, sock=None, host=NetworkHost, port=NetworkPort):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((NetworkHost, NetworkPort))
        	print('Connected to: '+NetworkHost+ ' on port: '+str(NetworkPort))
        else:
            self.sock = sock

    def send(self, msg):#used for sending orders
        self.sock.sendall(msg.encode())#sendall only stops sending when everything is sent

    def listen(self):#used for getting images
        final = ''#try the "final += data" trick if it errors
        while True:
            data = self.sock.recv(1024)
            data = data.decode()
            if data != '':#if something was received
                return data#only exit for the loop/ function

def pred():
	global image, img_width, img_height, bestclass
	img = image
	img.resize(img_width, img_height)
	model = create_model()
	keras.models.load_model('C:\\Users\\reyno\\FirstDatasetv1\\FirstDatasetv1.h5')
	arr = np.array(img).reshape((img_width,img_height,1))
	arr = np.expand_dims(arr, axis=0)
	prediction = model.predict(arr)[0]
	bestclass = ''
	bestconf = -1
	for n in [0,1,2,3]:
		if (prediction[n] > bestconf):
			bestclass = int(n)
			bestconf = prediction[n]
	print ('I think this road is ' + str(bestclass) + ' with ' + str(bestconf * 100) + '% confidence.')
	return bestclass

def Main():
	print('Starting...')
	net = NetworkClient()#makes the "net" object and connects to the server
	while True:
		image = net.listen()
		pred()
		net.send(bestclass)

if __name__ == "__main__":
	Main()
