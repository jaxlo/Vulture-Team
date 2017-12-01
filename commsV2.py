#By Jackson Lohman 2017
#To be run by a Raspberry Pi on an RC car
from PIL import Image
import numpy as np
import time
import serial
np.set_printoptions(threshold=np.inf)# to print the entire numpy array when printed

#global vars
usbConnection = False
imgCounter = 0
currentImg = ''
latestArduino = 0

def headlessRun():
	while True:
		ArduinoCom.receive()#get the latest distance from the Arduino
		ArduinoCom.send(243,200)#replace with vars
		takeImage()

def takeImage():
	global imgCounter, currentImg
	currentFilepath = '/home/pi/Documents/running/run' +str(imgCounter) + '.jpg'#make a new directory for this
	picam.capture(currentFilepath)
	print('Picture saved at :'+currentFilepath)
	loadImg = Image.open(currentFilepath)
	cropImg = loadImg.crop((0, 140, 320, 320))
	pixels = np.array(cropImg.getdata(band=2), dtype=np.uint8)#only gets the blue band of the image RGB,012 -- 1D array
	pixels.reshape(180,320)#makes it a 2D array

def sendImage(imageArray):
	pass#python network code goes here

def rcPrompt():
	startRC = input('Start RC mode? (y,n)')
	if startRC.lower() == 'n' or startRC.lower() == 'no':
		headlessRun()
	elif startRC.lower() == 'y' or startRC.lower() == 'yes':
		pass
	else:
		print('  Type "yes" or "no"')
		rcPrompt()
	#TODO rc code goes here

def rcRun():
	print('This feature is not available./nRedirecting you to non-rc mode')
	headlessRun()

class ArduinoCom:
	def connect():#Checks the connection and Connects if not connected
		global usbConnection#uses the global var
		if  usbConnection == False:
			counter = 0
			global ser#adds the global var instead of making a local one with the same name
			while counter <= 20:#loop through possible locations
				try:
					ser = serial.Serial('/dev/ttyACM'+str(counter), 9600)
				except OSError: #OSError:#if it cannot find the filepath
					counter += 1
				else:#runs if there are no exceptions in the try
					time.sleep(1)
					print('Arduino is at: /dev/ttyACM'+str(counter))
					counter = 22#exit out of the loop
					usbConnection = True
			if counter == 21:
				print('Arduino not found\n  Will try again in 3s')#when the while loop is over
				time.sleep(3)
				ArduinoCom.connect()#re-run the loop

	def receive():#called to see what the latest thing the arduino is transmitting to the pi
		ArduinoCom.connect()
		global latestArduino
		while True:
			raw = ser.readline()
			ArduinoCom.connect()
			try:#if bits are transmitted incorrectly, it ignores it
				decoded = raw.decode().strip('\r\n')
				print('Received from the Arduino: '+decoded)
				latestArduino = decoded
			except UnicodeDecodeError:
				print('Arduino decode error. Ignoring...')


	def send(speedA, speedB):#called to send PWM to the arduino from the pi
		ArduinoCom.connect()
		pwm = (str(speedA)+'m'+str(speedB))
		pwmmbytes = str.encode(pwm)
		ser.write(pwmmbytes)
		ArduinoCom.connect()
		print('PWM sent to the Arduino: '+pwm)

def takePicture():
	pass

headlessRun()

#if __name__ == "__main__":#if this program being run bu itself, not imported
#	rcPrompt()#prompts to run in RC mode
#
#if __name__ != "__main__":#If this is imported
#	headlessRun()#runs without prompting for RC mode
