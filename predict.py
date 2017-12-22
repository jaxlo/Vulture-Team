import numpy
import cv2
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Flatten, Dense
import sys

img_width, img_height = 320, 180

def create_model():
  model = Sequential()

  model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 1)))
  model.add(MaxPooling2D(2, 2))

  model.add(Convolution2D(64, (3, 3), activation='relu'))
  model.add(MaxPooling2D(2, 2))

  model.add(Flatten())
  model.add(Dense(1000, activation='relu'))

  model.add(Dense(10, activation='softmax'))

  model.summary()

  return model


img = cv2.imread(sys.argv[1])
img = cv2.resize(img, (img_width, img_height))
model = create_model()
keras.models.load_model('C:\\Users\\reyno\\FirstDatasetv1\\FirstDatasetv1.h5')
arr = numpy.array(img).reshape((img_width,img_height,1))
arr = numpy.expand_dims(arr, axis=0)
prediction = model.predict(arr)[0]
bestclass = ''
bestconf = -1
for n in [0,1,2,3,4]:
	if (prediction[n] > bestconf):
		bestclass = str(n)
		bestconf = prediction[n]
print 'I think this road is ' + bestclass + ' with ' + str(bestconf * 100) + '% confidence.'