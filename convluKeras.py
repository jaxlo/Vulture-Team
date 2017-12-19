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
y_test = []
appendCountTrain = 0
appendCountTest = 0


#change from real and fake data
def loadImgs(filepath):
    global x_train, y_train, x_test, y_test, appendCountTrain, appendCountTest, pixels
    imageFilepathSections = ('\\forward','\\turnLeft','\\turnRight','\\stop','\\trainRandom')
    imageDirectoryFilepath = filepath
    appendCountTrain = 0
    appendCountTest = 0
    #x_train = np.array([])
    for folder in imageFilepathSections:
        currentFileFolder = (imageDirectoryFilepath+folder)#loops through each folder
        for pic in glob.glob(currentFileFolder+'\\*.jpg'):
            loadImg = Image.open(pic)
            pixels = np.array(loadImg, dtype=np.float32)
            pixels /= 255#makes it 0-1 and it is faster
            #print(pixels)
            if folder != '\\trainRandom':
                if appendCountTrain != 0:
                    #x_train += pixels
                    x_train = np.append(x_train, pixels)
                else:
                    x_train = pixels
                if folder == '\\forward': y_train += [0]
                if folder == '\\turnLeft': y_train += [1]
                if folder == '\\turnRight': y_train += [2]
                if folder == '\\stop': y_train += [3]
                appendCountTrain += 1
            if folder == '\\trainRandom':
                appendCountTest += 1
                #put similar code here when finished with the train
        print(' Loaded: '+folder.strip('\\')+' Images')
    x_train.shape = (-1, 320, 180, 1)
    print(x_train.shape)

'''
        print('Before'+str(pixels))
        x_train.reshape(appendCountTrain,320,180,1)
        print('After'+str(pixels))
'''
    #x_train.reshape((appendCountTrain, 57600))#make another for x test

print(x_test.dtype)

loadImgs('C:\\Users\\reyno\\Downloads\\BluescaleImages\\BluescaleImages')
print('x_train: ', x_train)
print('y_train: ', y_train)
print('x_test: ', x_test)
print('y_test: ', y_test)
print(appendCountTrain)
print(x_train.shape)

y_train = keras.utils.to_categorical(y_train, num_classes = 4)
print(y_train)


#print(str(y_train))
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

model.fit(x_train, y_train, batch_size=appendCountTrain, epochs=10)
score = model.evaluate(x_train, y_train, batch_size=appendCountTrain)         #does it work?
#score = model.evaluate(x_test, y_test, batch_size=appendCountTest)         real testing
print("\n%s: %.2f%%" % (model.metrics_names[1], score[1]*100))

#prediction

#score = model.evaluate(x_test, y_test, batch_size=20)
#print(score)

#model.save('modelv1.h5')
#convert the outputs to what matches the car

