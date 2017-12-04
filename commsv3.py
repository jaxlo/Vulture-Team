#Made for Python 3, By Jackson Lohman and TJ Reynolds
#To be run by a Raspberry Pi on an RC car
try:
	from picamera import PiCamera
except ModuleNotFoundError:
	print('PiCamera Disabled')
	camSupport = False
else:
	picam.resolution = (320,320)
from PIL import Image
import numpy as np
import threading
import serial
import socket
import time
import sys

#Global Vars to change when running (change)
tfIpAddress = '192.168.0.11'#Where tensorflow is on the local network


#program  global vars (do not change)
imgCounter = 0#pictures taken

  ###########################
 # sendCamThread functions #
###########################

def bluescale():
	global imgCounter
	currentImg = '/home/pi/Documents/running/run' +str(imgCounter) + '.jpg'
	if camSupport == True:
		picam.capture(currentImg)
		print('Image :'+str(imgCounter)+' taken.')
	else:
		print('Using a local image to send')
		currentImg = 'roadforward90.jpg'#make sure this is in the same file where it is ran
	loadImg = Image.open(currentImg)
	cropImg = loadImg.crop((0, 140, 320, 320))
	pixels = np.array(cropImg.getdata(band=2), dtype=np.uint8)#only gets the blue band of the image
	pixels.reshape(180,320)#makes it a 2D array
	return pixels


def sendImg(image):
	global tfIpAddress
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (tfIpAddress, 10000)#change to the Tensorflow computer's address add a try statement?
	print('Connecting to Tensorflow')# use this for the IP on the tensorflow side
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect(server_address)
	except OSError:
		print('Could not send image to Tensorflow')
	else:
		print('Image sent to Tensorflow')

def sendCamThread():
	while True:
		imgArray = bluescale()
		sendImg(imgArray)

  ###########################
 # getArduThread functions #
###########################

def tfCommand():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (socket.gethostbyname(socket.gethostname()), 10000)
	sock.bind(server_address)
	sock.listen(1)
	print('Waiting for Tensorflow orders...')
	while True:
		connection, client_address = sock.accept()
		#try
		get = connection.recev(999)#TODO run this to see what is wrong and how to fix it
		#connection.close()  except
		#try -- next tab up 
		data = pickle.loads(get)
		#except
		#data = str(get)
		print('Order Received: '+str(get))
		return get

def brain(command, distance):#optimize values when it is working
	global status
	if distance != 0 and distance < 20 or command == 4:#zero is out of range of the sensor
		pwmA = 0
		pwmB = 0
		print('Stopping..')
		return pwmA, pwmB
	elif command == 1:#forward
		pwmA = 255
		pwmB = 255
		print('Moving Forward...')
		return pwmA, pwmB
	elif command == 2:#turn left
		pwmA = 255
		pwmB = -255
		print('Turning Left...')
		return pwmA, pwmB
	elif command == 3:#turn right
		pwmA = -255
		pwmB = 255
		print('Turning Right...')
		return pwmA, pwmB
	else:#this should not run
		print('No valid command in brain()\nExiting...')
		exit()

def arduino(command):
	counter = 0
	while counter <= 10:#loop through possible locations
		try:
			ser = serial.Serial('/dev/ttyACM'+str(counter), 9600)
		except OSError: #OSError:#if it cannot find the filepath
			counter += 1
		else:#runs if there are no exceptions in the try
			time.sleep(1)
			print('Arduino is at: /dev/ttyACM'+str(counter))
			counter = 22#exit out of the loop
	if counter == 21:
		print('Arduino not found\n  Will try again in 3s')#when the while loop is over
		time.sleep(3)
	x = 0
	while x < 5:#get distance
		raw = ser.readline()
		try:#if bits are transmitted incorrectly, it ignores it
			decoded = raw.decode().strip('\r\n')
			print('Received from the Arduino: '+decoded)
			addAdv =+ int(decoded)
			x += 1
		except UnicodeDecodeError:
			print('Arduino decode error. Ignoring...')
	totalAdv = addAdv/5
	speedA, speedB = brain(command,totalAdv)#decide what to do with distance and orders
	pwm = (str(speedA)+'m'+str(speedB))
	pwmmbytes = str.encode(pwm)
	ser.write(pwmmbytes)#send the data to the arduino
	print('Motor PWM sent to the Arduino: '+pwm)

def getArduThread():
	while True:
		command = tfCommand()
		arduino(command)

threading.Thread(target=getArduThread).start()#thread 1
threading.Thread(target=sendCamThread).start()#thread 2