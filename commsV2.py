#By Jackson Lohman 2017
#To be run by a Raspberry Pi

import time
import serial

'''List of known problems/bugs
-The arduino is not hot swappable there is a strange input bug with the loop
-Encoding and decoding the data from the arduino is in a garbled format
'''
carName = 'cobra'#cobra or vulture (Used to identify)

def headlessRun():
	while True:
		arduConnect()
		arduTx()
		if newSpeed == True:
			arduTx(1,2)

def rcRun():
	startRC = imput('Start RC mode? (y,n)')
	if startRC.lower() == n or startRC.lower() == no:
		headlessRun()
	elif startRC.lower() == y or startRC.lower() == yes:
		pass
	else:
		print('  Type "yes" or "no"')

def arduConnect():#checks the arduino connection
	counter = 0
	while counter <= 20:#loop through possible locations
		try:
			ser = serial.Serial('/dev/ttyACM'+str(counter), 9600)
		except: #OSError:#if it cannot find the filepath
			counter += 1
		else:#runs if there are no exceptions in the try
			time.sleep(1)
			print('Arduino is at: /dev/ttyACM'+str(counter))
			return ser#if it finds a location exits here
	print('Arduino not found\n  Will try again in 3s')#when the while loop is over
	time.sleep(3)
	arduConnect()#re-run the loop

def arduTx():#called to see what the latest thing the arduino is transmitting to the pi w/ error checking
	while True:
		ser = arduConnect()
		raw = ser.readline()#read the newest output from the Arduino
		type(raw)
		decoded = raw.decode('ascii')#.decode("utf-8").encode("windows-1252").decode("utf-8")#remove unwanted characters
		#if decoded[:1] == 'a' or decoded[:-1] == 'z':#makes sure it gets the full message (inspired by how DNA works)
		#	takeFirst = decoded[1]#remove the first character
		#	takeLast = takeFirst[-1]#remove the last character #TODO make it remove the first and last char before returning
		return decoded

def arduRx(speedA, speedB):#called to send PWM to the arduino from the pi
	ser = arduConnect()
	pwm = ('a'+str(speedA)+'m'+str(speedB)+'z')
	print(pwm)
	pwmmbytes = str.encode(pwm)
	ser.write(pwmmbytes)

#while True:#test
#	arduRx(1,1)
#	var = arduTx()
#	print('Var: '+var)

print('Name: '+__name__)
print('Main: '+__main__)

if __name__ == "__main__":#if this program being run bu itself, not imported
	rcRun()

if __name__ != "__main__":#If this is imported
	headlessRun()