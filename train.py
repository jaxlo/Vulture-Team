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

print('Starting...')
print(' _____     _ _                   _____               ')
print('|  |  |_ _| | |_ _ _ ___ ___ ___|_   _|___ ___ ___ __')
print('|  |  | | | |  _| | |  _| -_|___| | | | -_| . |     |')
print(' \___/|___|_|_| |___|_| |___|     |_| |___|__,|_|_|_|')
print('                    By Jackson Lohman and TJ Reynolds\n')

x_train = np.array([])
y_train = []
x_test = np.array([])
y_test = []
appendCountTrain = 0
appendCountTest = 0

batch_size = 50
epochs = 10

def findUserSlash():
	user = str(input('Who are you? (For the correct filepath)\n  (1)TJ\n  (2)Jackson\nEnter [1,2]: '))
	if user == '1':#lower confusing errors if the input is invalid later
		slash = '\\'
		print('Hello, TJ\nSlash: '+slash)
	elif user == '2':
		slash = '/'#linux is better lol (yet tensorflow(running in backgrund) is optimized for windows, lol)
		print('Hello, Jackson\nSlash: '+slash)
	else:
		print('Invalid Input\n')
		findUserSlash()
	return user, slash

def loadImgs():
	global x_train, y_train, x_test, y_test, appendCountTrain, appendCountTest, pixels
	
	user, slash = findUserSlash()
	print(user, slash)
	if slash == '\\' and user == '1':
		filepath = 'E:\\BlueNew'
		print(filepath)
	else:
		filepath = '/run/media/jax/DualOS/CompSci/finalCar/formattedData/format11-4-17'
		print(filepath)
		
	imageFilepathSections = (slash+'forward',slash+'test')
	imageDirectoryFilepath = filepath
	appendCountTrain = 0
	appendCountTest = 0

	for folder in imageFilepathSections:
		currentFileFolder = (imageDirectoryFilepath+folder)#loops through each folder
		for pic in glob.glob(currentFileFolder+slash+'*.jpg'):
			loadImg = Image.open(pic)
			pixels = np.array(loadImg, dtype=np.float32)
			pixels /= 255#makes it 0-1 and it is faster
			#print(pixels)
			if folder != (slash+'test'):
				if appendCountTrain != 0:
					#x_train += pixels
					x_train = np.append(x_train, pixels)
				else:
					x_train = pixels
				if folder == slash+'forward': y_train += [0]
				elif folder == slash+'left': y_train += [1]
				appendCountTrain += 1

			if folder == slash+'test':
				if appendCountTest != 0:
					x_test = np.append(x_test, pixels)
				else:
					x_test = pixels
				if pic.find('forward') >= 0:
					y_test += [0]
					print('forward')
				
				elif pic.find('left') >= 0  or pic.find('Left') >= 0:
					y_test += [1]
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

model.save('04262018.h5')#change to match what we are saving

