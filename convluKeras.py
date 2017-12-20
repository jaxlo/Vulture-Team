import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from PIL import Image
import numpy as np
import glob
import os
#np.set_printoptions(threshold=np.nan)
#user = 0

x_train = np.array([])
y_train = []
x_test = np.array([])
y_test = []
appendCountTrain = 0
appendCountTest = 0

batch_size = 27

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

#change from real and fake data
def loadImgs():
	global x_train, y_train, x_test, y_test, appendCountTrain, appendCountTest, pixels
	
	user, slash = findUserSlash()
	print(user, slash)
	if slash == '\\' and user == '1':
		filepath = 'C:\\Users\\reyno\\Downloads\\BluescaleImages\\BluescaleImages'
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
				if appendCountTrain != batch_size:
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
				if pic.find('forward') == -1: y_test += [0]
				elif pic.find('left') == -1: y_test += [1]
				elif pic.find('right') == -1: y_test += [2]
				elif pic.find('stop') == -1: y_test += [3]
				appendCountTest += 1
				#put similar code here when finished with the train
		print('Loaded: '+folder.strip(slash)+' Images')
	print(appendCountTrain, 'aaaa')
	x_train.shape = (-1, 320, 180, 1)
	x_test.shape = (-1, 320, 180, 1)
	print(x_train.shape)
	print(x_test.shape)

'''
		print('Before'+str(pixels))
		x_train.reshape(appendCountTrain,320,180,1)
		print('After'+str(pixels))
'''
	#x_train.reshape((appendCountTrain, 57600))#make another for x test


loadImgs()

print(x_test.dtype)
print('x_train: ', x_train)
print('y_train: ', y_train)
print('x_test: ', x_test)
print('y_test: ', y_test)
print(appendCountTrain)
print(appendCountTest)
print(x_train.shape)

y_train = keras.utils.to_categorical(y_train, num_classes = 4)
y_test = keras.utils.to_categorical(y_test, num_classes = 4)
print('y_train: ', y_train)
print('y_test: ', y_test)

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

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

model.fit(x_train, y_train, batch_size=20, epochs=10)
#score = model.evaluate(x_train, y_train, batch_size=appendCountTrain)         #does it work? 
score = model.evaluate(x_test, y_test, batch_size=20)         #real testing
print(score)

#prediction

#score = model.evaluate(x_test, y_test, batch_size=20)
#print(score)

model.save('FirstDatasetv1.h5')#change to match what we are saving
