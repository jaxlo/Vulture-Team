import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
import glob
import os
import h5py
import sys
import time
import pickle
import socket


#training part of the CNN
def train():
	x_train = np.array([])
	y_train = []
	x_test = np.array([])
	y_test = []
	appendCountTrain = 0
	appendCountTest = 0

	batch_size = 50
	epochs = 10

	def findUserSlash():
		user = str(input('Who are you? (For the correct filepath)\n  (1)TJ\n  (2)Jackson\n  (3)Kevin\nEnter [1,2,3]: '))
		if user == '1':#lower confusing errors if the input is invalid later
			slash = '\\'
			print('Hello, TJ\nSlash: '+slash)
		elif user == '2':
			slash = '/'#linux is better lol (yet tensorflow(running in backgrund) is optimized for windows, lol)
			print('Hello, Jackson\nSlash: '+slash)
		elif user == '3':#lower confusing errors if the input is invalid later
			slash = '\\'
			print('Hello, Kevin\nSlash: '+slash)
		else:
			print('Invalid Input\n')
			findUserSlash()
		return user, slash

	def loadImgs():
		global x_train, y_train, x_test, y_test, appendCountTrain, appendCountTest, pixels
		
		user, slash = findUserSlash()
		print(user, slash)
		if slash == '\\' and user == '1':
			filepath = 'C:\\Users\\reyno\\Downloads\\finalTrainingData\\finalTrainingData\\format12-11-17'
			print(filepath)
		elif slash == '\\' and user == '3':
			filepath = ''
			print(filepath)
		else:
			filepath = '/run/media/jax/DualOS/CompSci/finalCar/formattedData/format11-4-17'
			print(filepath)
			
		imageFilepathSections = (slash+'forward',slash+'turnLeft',slash+'turnRight',slash+'stop',slash+'trainRandom')
		imageDirectoryFilepath = filepath
		appendCountTrain = 0
		appendCountTest = 0
		#x_train = np.array([])
		for folder in imageFilepathSections:
			currentFileFolder = (imageDirectoryFilepath+folder)#loops through each folder
			for pic in glob.glob(currentFileFolder+slash+'*.jpg'):
				loadImg = Image.open(pic)
				pixels = np.array(loadImg, dtype=np.float32)
				pixels /= 255#makes it 0-1 and it is faster
				#print(pixels)
				if folder != (slash+'trainRandom'):
					if appendCountTrain != 0:
						#x_train += pixels
						x_train = np.append(x_train, pixels)
					else:
						x_train = pixels
					if folder == slash+'forward': y_train += [0]
					elif folder == slash+'turnLeft': y_train += [1]
					elif folder == slash+'turnRight': y_train += [2]
					elif folder == slash+'stop': y_train += [3]
					appendCountTrain += 1
				if folder == slash+'trainRandom':
					if appendCountTest != 0:
						x_test = np.append(x_test, pixels)
					else:
						x_test = pixels
					if pic.find('forward') >= 0:
						y_test += [0]
						print('forward')
					
					elif pic.find('left') >= 0  or pic.find('Left') >= 0:
						y_test += [1]
						#print('left')
					elif pic.find('right') >= 0 or pic.find('Right') >= 0:
						y_test += [2]
						#print('right')
					elif pic.find('stop') >= 0:
						y_test += [3]
						#print('stop')
					appendCountTest += 1
					#put similar code here when finished with the train
			print('Loaded: '+folder.strip(slash)+' Images')
		print(appendCountTrain)
		print(y_test)
		x_train.shape = (-1, 320, 180, 1)
		x_test.shape = (-1, 320, 180, 1)
		print(x_train.shape)
		print(x_test.shape)


	loadImgs()

	y_train = keras.utils.to_categorical(y_train, num_classes = 4)
	y_test = keras.utils.to_categorical(y_test, num_classes = 4)

	print(x_test.dtype)
	print('x_train: ', x_train)
	print('y_train: ', y_train)
	print('x_test: ', x_test)
	print('y_test: ', y_test)
	print(appendCountTrain)
	print(appendCountTest)
	print(x_train.shape)



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

	sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer=sgd)

	model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs)
	score = model.evaluate(x_test, y_test, batch_size=batch_size)
	print(score)

	model.save('FirstDatasetv1.h5')#change to match what we are saving


#prediction part of the CNN
def predict():
	img_width, img_height = 320, 180
	carIpAddress = '192.168.1.102'#change to the IP address of your car
	bestclass = -1

	def create_model():
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

	def sendOrder(order):
		global carIpAddress
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try: 
			server_address = (carIpAddress, 10000)
			print('server address: ', server_address)
		except:
			print('did not get server_address')
		print('Connecting to the car')# use this for the IP on the tensorflow side
		try:
			try:
				sock.connect(server_address)
			except: 
				print('failed at .connect')
				print('Could not send order to the car')
				sendOrder(bestclass)
			try:
				sendorder = str(bestclass).encode()
			except:
				print('failed at .encode')
				print('Could not send order to the car')
			try:
				sock.send(sendorder)
				print('Order sent to the car')
			except:
				print('failed at .send')
				print('Could not send order to the car')
		except OSError:
			print('Could not send order to the car')
			time.sleep(.1)
			

	def getImage():
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (socket.gethostbyname(socket.gethostname()), 10000)
		try:
			sock.bind(server_address)
		except OSError:
			time.sleep(.5)
			print('ERROR socket.bind')
			getImage()
		sock.listen(1)
		print('Waiting for image...')
		while True:
			try:
				connection, carIpAddress = sock.accept()
			except OSError:
				time.sleep(.5)
				print('ERROR accept')
				getImage()
			get = b''
			while True:
				packet = connection.recv(4096)
				if not packet: break
				get += packet
			end = pickle.loads(get)
			return end

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

	print('Starting...')

	while True:
		image = getImage()
		pred()
		sendOrder(bestclass)


#Choice part of the NN
def choose():
	print('[1] = Train\n[2] = Predict')
	choice = int(input("what is your choice [1] or [2]: "))
	print('\nYou chose:', choice,'\n')
	if choice == 1:
		train()
	elif choice == 2:
		predict()
	else:
		print('Try Again')
		choose()

choose()
