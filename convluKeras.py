#from https://keras.io/getting-started/sequential-model-guide/#examples

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

x_train = np.array([])
y_train = []
x_test = np.array([])
y_test = ()
appendCountTrain = 0

#change from real and fake data
def loadImgs(filepath):
	global x_train, y_train, x_test, y_test
	imageFilepathSections = ('/forward','/turnLeft','/turnRight','/stop','/trainRandom')
	imageDirectoryFilepath = filepath
	appendCountTrain = 0
	appendCountTest = 0
	#x_train = np.array([])
	for folder in imageFilepathSections:
		currentFileFolder = (imageDirectoryFilepath+folder)#loops through each folder
		for pic in glob.glob(currentFileFolder+'/*.jpg'):
			loadImg = Image.open(pic)
			pixels = np.array(loadImg, dtype=np.float32)
			pixels /= 255#makes it 0-1 and it is faster
			if folder != '/trainRandom':
				if appendCountTrain != 0:
					x_train = np.concatenate((x_train, pixels))
				else:
					x_train = pixels
				if folder == '/forward': y_train += [0]
				if folder == '/turnLeft': y_train += [1]
				if folder == '/turnRight': y_train += [2]
				if folder == '/stop': y_train += [3]
				appendCountTrain += 1
			if folder == '/trainRandom':
				appendCountTest += 1
				#put similar code here when finished with the train
		print(' Loaded: '+folder.strip('/')+' Images')
	x_train.reshape(180, 320, appendCountTrain)#make another for x test
	#x_train.reshape((appendCountTrain, 57600))#make another for x test
	print(str(x_train)+'\n')


print(x_test.dtype)

loadImgs('/run/media/jax/DualOS/CompSci/finalCar/formattedData/format11-4-17')
print(str(y_train))
	#add to numpy array
if True:
	pass
	#fake training data  (for formatting)-----------------------------------------------------------------
	#x_train = np.random.random((1000, 57600))#picture
	#x_train = np.random.random((100, 320, 180, 1))#1 was 3
'''
	print('\n\nx_train:'+str(x_train))
	y_train = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
	#print('\n\ny_train:'+str(y_train))
	#test the network
	x_test = np.random.random((20, 100, 100, 3))#unchanged
	#print('\n\nx_test:'+str(x_test)
	y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)#unchanged
	#print('\n\ny_test:'+str(y_test))
	#fake training data  (for formatting)-----------------------------------------------------------------

x_train = np.random.random((100, 100, 100, 1))#1 was 3
y_train = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
x_test = np.random.random((20, 100, 100, 3))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)
'''
model = Sequential()
model.add(Dense(57600, input_shape=(320, 180), activation='relu'))#input layer
#              Input nodes     Expected Input number

model.add(Dense(28800, activation='relu'))#hidden layer
#             8 middle layer nodes

model.add(Dense(3, activation='sigmoid'))
#numbers of output layers

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, batch_size=appendCountTrain)

scores = model.evaluate(x_train, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
#prediction

#score = model.evaluate(x_test, y_test, batch_size=32)
#print(score)

#model.save('modelv1.h5')
#convert the outputs to what matches the car