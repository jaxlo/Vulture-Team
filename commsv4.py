#Made for Python 3.6, By Jackson Lohman and TJ Reynolds
#To be run by a Raspberry Pi on an RC car

NetworkHost = '192.168.1.103'
NetworkPort = 59281
imgCounter = 0

def inputScrubber(inputStr, optionTuple, errorStr):#optionTuple needs to be a str
	while True:#can only exit the loop if there is a valid input
		responce = input(inputStr)
		for item in optionTuple:
			if item == responce:
				return responce#only exit
		print(errorStr)

print(' _____     _ _                   _____               ')
print('|  |  |_ _| | |_ _ _ ___ ___ ___|_   _|___ ___ ___ __')
print('|  |  | | | |  _| | |  _| -_|___| | | | -_| . |     |')
print(' \___/|___|_|_| |___|_| |___|     |_| |___|__,|_|_|_|')
print('                    By Jackson Lohman and TJ Reynolds\n')
print('Starting...')
try:
	from picamera import PiCamera
	picam = PiCamera()
	picam.resolution = (320,320)#run now to give it time to load
	camSupport = True
	print('Pi Camera Enabled')
except ImportError:
	camSupport = False
	print('Pi Camera Disabled')
try:
	import serial
except ImportError:
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

def network(image):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((NetworkHost, NetworkPort))
		tosend = pickle.dumps(image, protocol = 0)
		sock.sendall(tosend)
		sock.shutdown(socket.SHUT_WR)
		print('Image Sent')
		data = sock.recv(1024)
	print('Received: ', str(data.decode()))
	sock.close()
	return str(data.decode())

class Arduino:
	def __init__(self, ser=None):
		if arduinoSupport == False:
			print('Fake echo Arduino connected')
			return#exits function
		serialConnection = False
		while serialConnection == False:
			counter = 0
			while True:
				try:
					self.ser = serial.Serial('/dev/ttyACM'+str(counter), 9600)
				except OSError:#if it cannot find the filepath
					counter += 1
				else:#runs if there are no exceptions in the try
					serialConnection = True
					print('Arduino is at: /dev/ttyACM'+str(counter))
					time.sleep(2)#Give the arduino time to reset
					break#exits counting loop
				if counter == 11:#where the program stopps looking for the arduino
					counter = 0
					print('Arduino not found\n  Will try again in 3s')#when the while loop is over
					time.sleep(3)

	def sendPwm(self, pwmA, pwmB):
		if arduinoSupport == False:
			print('Echo Arduino PWM_A: '+str(pwmA)+', pwmB: '+str(pwmB))
			return#exits function
		pwm = ('<sd, '+str(pwmA)+', '+str(pwmB)+'>')
		pwmmbytes = str.encode(pwm)
		self.ser.write(pwmmbytes)#send the data to the arduino
		#self.ser.flushOutput() renamed in docs

	def sendOrder(self, order):#converts the order to pwm and uses sendPwm to send it to the Arduino
		order = int(order)
		#pwmA is the left and pwmB is the right
		if order == 0:#forward
			pwmA = 255
			pwmB = 255
			print('Moving Forward...')
		elif order == 1:#turn left
			pwmA = 0
			pwmB = 255
			print('Turning Left...')
		elif order == 2:#turn right
			pwmA = 255
			pwmB = 0
			print('Turning Right...')
		elif order == 3:#stop
			pwmA = 0
			pwmB = 0
			print('Stopping..')
		else:#this should not run
			raise Exception('Not a valid command\nUse int 0-3')
		self.sendPwm(pwmA, pwmB)

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
			piCam('MLtrain'+'/'+filepathEnd+'/'+trainSaveFilepathPrefix+filepathEnd)#where and what the file is called

def runNN():
	ardu = Arduino()#takes 2 seconds to connect (waiting for the arduino to restart with USB connection)
	imageFilepath = 'MLtrain/run'
	if camSupport == False:
		runCamQuestion = 'The camera is disabled, this will program use a random picture and will not save.\nContinue? [y,n]: '
		runInput = inputScrubber(runCamQuestion,('y','n'),'Invalid Input\n')
		if runInput == 'n':
			exit()
		imageFilepath = None#uses a random picture and does not save
	input('Press CTRL-C to quit driving\nPress ENTER to continue\n')
	while True:
		img = piCam(imageFilepath)
		order = network(img)
		ardu.sendOrder(order)

def remoteControl():
	ardu = Arduino()
	print('List of commands:\n(WASD)\n  w-forward\n  a-left\n  d-right\n  s-stop\nUse CTRL-C to exit\n')
	while True:
		try:
			RCdirection = inputScrubber('Enter [w,a,s,d]: ', ('w','a','s','d'), 'Invalid Input')
			if RCdirection == 'w':
				ardu.sendOrder(0)#forward
			elif RCdirection == 'a':
				ardu.sendOrder(1)#left
			elif RCdirection == 'd':
				ardu.sendOrder(2)#right
			elif RCdirection == 's':
				ardu.sendOrder(3)#stop
		except KeyboardInterrupt:#if the user exits
			ardu.sendOrder(3)#stop
			exit()

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
