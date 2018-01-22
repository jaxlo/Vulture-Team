#Made for Python 3, By Jackson Lohman and TJ Reynolds
#To be run by a Raspberry Pi on an RC car

tfIpAddress = '192.168.1.101'#Where the ML server is on the local network
#change to MLipAddress


#global variables
camSupport, arduinoSupport, serverSupport, currentImg = None, None, None, None
imgCounter = 0

def importAll():
	global camSupport, arduinoSupport, serverSupport
	print(' _____     _ _                   _____               ')
	print('|  |  |_ _| | |_ _ _ ___ ___ ___|_   _|___ ___ ___ __')
	print('|  |  | | | |  _| | |  _| -_|___| | | | -_| . |     |')
	print(' \___/|___|_|_| |___|_| |___|     |_| |___|__,|_|_|_|')
	print('                    By Jackson Lohman and TJ Reynolds\n')
	print('Starting...')
	try:
		from picamera import PiCamera
		picam.resolution = (320,320)
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
		serialChoice = inputScrubber('Enable Arduino? (y/n): ',('y','n'), 'Enter y or n')
		if serialChoice == 'n' or serialChoice == 'N':
			arduinoSupport = False
			print('Arduino Disabled')
		else:
			arduinoSupport = True
			print('Arduino Enabled')
	try:
			import socket
	except ModuleNotFoundError:
		serverSupport = False
		print('ML Server Disabled')
	else:
		serverChoice = inputScrubber('Enable ML Server? (y/n): ',('y','n'), 'Enter y or n')
		if serverChoice == 'n' or serverChoice == 'N':
			serverSupport = False
			print('ML Server Disabled')
		else:
			serverSupport = True
			print('ML Server Enabled')
	from PIL import Image
	import numpy as np
	import pickle
	import time
	import sys
	import os

def inputScrubber(inputStr, optionTuple, errorStr):#make sure optionTuple is str, not int
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

def piCam(filepath):#filepath = None if it should make a random picture -- Example: piCam('/run/someDirectionForAName') -- (do not add .jpg)
	global imgCounter
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
		print('Image :'+str(imgCounter)+' made.')
	currentImg = pixels#moves the array to a global var
