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

img_width, img_height = 320, 180
carIpAddress = '192.168.1.100'
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

def sendOrder(order):
  global carIpAddress
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = (carIpAddress, 10000)#change to the Tensorflow computer's address add a try statement?
  print('Connecting to the car')# use this for the IP on the tensorflow side
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect(server_address)
    sendOrder = str(order).encode()
    sock.send(sendOrder)
  except OSError:
    print('Could not send order to the car')
    time.sleep(.1)
  else:
    print('Image sent to the car')

def getImage():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = (socket.gethostbyname(socket.gethostname()), 10000)
  try:
    sock.bind(server_address)
  except OSError:
    time.sleep(5)
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
    #return finalArray.astype(np.float32)
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

