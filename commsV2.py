#By Jackson Lohman 2017
#To be run by a Raspberry Pi on an RC car


import time
import serial

carName = 'cobra'#cobra or vulture (Used to identify)
usbConnection = False

def headlessRun():
	while True:
		var1 = ArduinoCom.receive()
		ArduinoCom.send(243,200)#replace with vars

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
	print('This feature is not available./nRedirecting you to non rc mode')
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
		while True:
			raw = ser.readline()
			ArduinoCom.connect()
			try:#if bits are transmitted incorrectly, it ignores it
				decoded = raw.decode().strip('\r\n')
				print('Received from the Arduino: '+decoded)
				return decoded
			except UnicodeDecodeError:
				print('Arduino decode error. Ignoring...')


	def send(speedA, speedB):#called to send PWM to the arduino from the pi
		ArduinoCom.connect()
		pwm = (str(speedA)+'m'+str(speedB))
		pwmmbytes = str.encode(pwm)
		ser.write(pwmmbytes)
		ArduinoCom.connect()
		print('PWM sent to the Arduino: '+pwm)

headlessRun()
