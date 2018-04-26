import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
import h5py
import time
import pickle
import socket

img_width, img_height = 320, 180
bestclass = -1
NetworkPort = 59281
final2 = ''

def create_model(): #this defines the layers that will be used to process the image. They are the same ones that are used in training.
	model = Sequential()
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

#need to put new network here... using pickle to send not send it over socket


def pred(var): #This is where the NN actually does the prediction
	global img_width, img_height, bestclass
	img = var
	img.resize(img_width, img_height)
	model = create_model()
	keras.models.load_model('C:\\Users\\reyno\\FirstDatasetv1\\FirstDatasetv1.h5')
	arr = np.array(img).reshape((img_width,img_height,1))
	arr = np.expand_dims(arr, axis=0)
	prediction = model.predict(arr)[0]
	bestclass = ''
	bestconf = -1
	for n in [0,1]:
		if (prediction[n] > bestconf):
			bestclass = int(n)
			bestconf = prediction[n]
	print ('I think this road is ' + str(bestclass) + ' with ' + str(bestconf * 100) + '% confidence.')
	return bestclass


def network():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('', NetworkPort))#allow any ip
	sock.listen(1)
	print('Listening for Connection...')
	conn, addr = sock.accept()
	print('connected to' + str(addr))

	final = b''
	while True:
		data = conn.recv(1024)
		if not data: break
		final += data
	final2 = pickle.loads(final)
	print('Image Received')
	#print(final2)

	pred(final2)

	conn.sendall(str(bestclass).encode())
	print('bestclass sent')
	sock.close()
	return final2


print('Starting...')
print(' _____     _ _                   _____               ')
print('|  |  |_ _| | |_ _ _ ___ ___ ___|_   _|___ ___ ___ __')
print('|  |  | | | |  _| | |  _| -_|___| | | | -_| . |     |')
print(' \___/|___|_|_| |___|_| |___|     |_| |___|__,|_|_|_|')
print('                    By Jackson Lohman and TJ Reynolds\n')

while True:
	network()
