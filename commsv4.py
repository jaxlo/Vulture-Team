#Made for Python 3, By Jackson Lohman and TJ Reynolds
#To be run by a Raspberry Pi on an RC car

NetworkHost = '192.168.1.102'#Where the ML server is on the local network

#global variables
imgCounter = 0

def inputScrubber(inputStr, optionTuple, errorStr):#optionTuple needs to be a str
	responce = input(inputStr)
	x = 0
	while x <= len(optionTuple):
		try:
			if optionTuple[x] == responce:
				return responce
			else:
				x += 1
		except IndexError:#If the tuple runs out of places to index`
			x = len(optionTuple) +1
	if errorStr != 'NOERRORSTR':#make  errorStr == NOERRORSTR for there to be no error strings
		print(errorStr)
		inputScrubber(inputStr, optionTuple, errorStr)

print(' _____     _ _                   _____               ')
print('|  |  |_ _| | |_ _ _ ___ ___ ___|_   _|___ ___ ___ __')
print('|  |  | | | |  _| | |  _| -_|___| | | | -_| . |     |')
print(' \___/|___|_|_| |___|_| |___|     |_| |___|__,|_|_|_|')
print('                    By Jackson Lohman and TJ Reynolds\n')
print('Starting...')
try:
	from picamera import PiCamera
	picam.resolution = (320,320)#run now to give it time to load
	camSupport = True
	print('Pi Camera Enabled')
except ModuleNotFoundError:
	camSupport = False
	print('Pi Camera Disabled')
try:
	import serial
except ModuleNotFoundError:
	arduinoSupport = False
	print('Arduino Disabled')
else:
	serialChoice = inputScrubber('Enable Arduino? [y/n]: ',('y','n'), 'Enter y or n')
	if serialChoice == 'n' or serialChoice == 'N':
		arduinoSupport = False
		print('Arduino Disabled')
	else:
		arduinoSupport = True
		print('Arduino Enabled')
import socket
from PIL import Image
import numpy as np
import pickle
import time
import sys
import os

def piCam(filepath):#filepath = None if it should make a random picture -- Example: piCam('/run/someDirectionForAName') -- (do not add .jpg)
	global imgCounter#to use outside of the program, make a global var 0 
	imgCounter += 1#incraments before the picture. It starts counting with 1
	if filepath != None:
		currentImg = str(filepath)+str(imgCounter)+'.jpg'#adds image number and filepath
		picam.capture(currentImg)
		print('Image :'+str(imgCounter)+' taken.')
		loadImg = Image.open(currentImg)
		cropImg = loadImg.crop((0, 140, 320, 320))
		pixels = np.array(cropImg.getdata(band=2), dtype=np.uint8)#only gets the blue band of the image
		pixels.resize(180,320)#makes it a 2D array
	else:
		print('Using a random image')
		pixels = np.random.rand(180,320)
		time.sleep(.5)#make it act more like the cam in speed
		print('Image :'+str(imgCounter)+' made.')
	return pixels

class NetworkServer:#run on the pi
    def __init__(self, sock=None, port=NetworkPort):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', NetworkPort))#allow any ip
            self.sock.listen(1)#limit connection to one client
            print('Waiting for the ML client')
            self.conn, addr = self.sock.accept()
            print('New connection from: [add later]')#+str(self.sock.getpeername()))
        else:
            self.sock = sock
            print('sock is sock')#is this ever used?

    def send(self, msg):
        self.conn.sendall(msg.encode())

    def listen(self):
        while True:
            data = self.conn.recv(1024)
            data = data.decode()
            if data != '':#if something was received
                return data#only exit of the loop/ function

def arduino(order):#I wand to get everything working, then do the arduino so debuging so problems are simple
	print('Arduino order: '+str(order))#delete later

def trainNN():
	if camSupport == False:
			continueCamQuestion = 'The camera is disabled, this will program use a random picture and will not save.\nContinue? [y,n]: '
			continueCam = inputScrubber(continueCamQuestion,('y','n'),'Invalid Input\n')
			if continueCam == 'n':
				exit()#close the program
			while True:
				piCam(None)#makes a random picture
	else:#if camera support is true
		tdQuestion = 'Select an option:\n  (1) = forward\n  (2) = left\n  (3) = right\n  (4) = stop\n  (5) = other\nEnter [1,2,3,4,5]: '
		trainDirection = inputScrubber(tdQuestion, ('1','2','3','4','5'),'Invalid Input\n')#used a var because str was too long
		if trainDirection == '1':
			filepathEnd = 'forward'
		elif trainDirection == '2':
			filepathEnd = 'turnLeft'
		elif trainDirection == '3':
			filepathEnd = 'turnRight'
		elif trainDirection == '4':
			filepathEnd = 'stop'
		elif trainDirection == '5':
			filepathEnd = 'other'
		trainSaveFilepathPrefix = ''#if prefix is disabled, it is nothing
		trainPrefixQuestion = inputScrubber('Would you like to use an image prefix? [y,n]: ',('y','n'),'InvalidInput\n')
		if trainPrefixQuestion == 'y':
			trainSaveFilepathPrefix = input('Enter a prefix: ')
		input('Press CTRL-C to quit taking pictures\nPress ENTER to continue')
		print('Starting...')
		while True:
			piCam('/'+filepathEnd+'/'+trainSaveFilepathPrefix+filepathEnd)#where and what the file is called

def runNN():
	global NetworkHost
	imageFilepath = '/run'
	tfAddr = input('Is Tensorflow at '+NetworkHost+'?\n  If so, Press ENTER\n  If not, Enter the correct address :')
	if tfAddr != '':#if the user typed a new ip
		NetworkHost = tfAddr
	net = NetworkServer()#Waits for a connection to the ML program
	if camSupport == False:
		runCamQuestion = 'The camera is disabled, this will program use a random picture and will not save.\nContinue? [y,n]: '
		runInput = inputScrubber(runCamQuestion,('y','n'),'Invalid Input\n')
		if runInput == 'n':
			exit()
		imageFilepath = None#uses a random picture and does not save
	input('Press CTRL-C to quit driving\nPress ENTER to continue\n')
	while True:
		img = piCam(imageFilepath)
		net.send(img)
		order = net.listen()
		arduino(order)

def remoteControl():
	print('List of commands:\n(WASD)\n  w-forward\n  a-left\n  d-right\n  s-stop\nUse CTRL-C to exit\n')
	while True:
		RCdirection = inputScrubber('Enter [w,a,s,d]: ', ('w','a','s','d'), 'Invalid Input')
		if RCdirection == 'w':
			arduino(0)#forward
		elif RCdirection == 'a':
			arduino(1)#left
		elif RCdirection == 's':
			arduino(2)#right
		elif RCdirection == 'd':
			arduino(3)#stop

def Main():
	mainMode = inputScrubber('Select an option:\n  (1)Train NN\n  (2)Run NN\n  (3)RC mode\nEnter [1,2,3]: ', ('1','2','3'), 'Invalid Input\n')
	if mainMode == '1':
		trainNN()
	elif mainMode == '2':
		runNN()
	elif mainMode == '3':
		remoteControl()


if __name__ == "__main__":
Main()
