import socket
import numpy as np
import time

carIpAddress = '192.168.1.14'

def sendOrder(order):#works
	global carIpAddress
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (carIpAddress, 10000)#change to the Tensorflow computer's address add a try statement?
	print('Connecting to the car')# use this for the IP on the tensorflow side
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sendOrder = str(order).encode()
	try:
		sock.connect(server_address)
		sock.send(sendOrder)
	except OSError:
		print('Could not send image to the car')
		time.sleep(.1)
	else:
		print('Image sent to the car')

def getImage():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostbyname(socket.gethostname()), 10000))#port
	sock.listen(1)
	print('Waiting for image...')
	while True:
		connection, carIpAddress = sock.accept()
		get = connection.recev(999)#TODO run this to see what is wrong and how to fix it
		print('Image received from the car')
		return get
