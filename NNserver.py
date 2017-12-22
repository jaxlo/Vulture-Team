import socket
import numpy as np
import time
import pickle

carIpAddress = '192.168.1.100'

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
		print('Could not send image to the car')
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

print('Starting...')

while True:
	image = getImage()
