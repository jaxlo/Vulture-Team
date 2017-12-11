from time import sleep
from picamera import PiCamera


picam = PiCamera()
picam.resolution = (320,320)
picam.start_preview()
#camera warm-up
sleep(2)
print('1 = forward\n2 = left\n3 = right\n4 = stop\n5 = random')
y = input('option number 1,2,3,4, or 5:  ')
x = int(y)

capnum = 0
if x == 1:
	while True:
		picam.capture('/home/pi/Documents/forward/roadforward' +str(capnum) + '.jpg')
		print('Picture: '+str(capnum) +' taken')
		capnum += 1

elif x == 2:
	while True:
		picam.capture('/home/pi/Documents/turnLeft/roadleft' +str(capnum) + '.jpg')
		print('Picture: '+str(capnum) +' taken')
		capnum += 1

elif x == 3:
	while True:
		picam.capture('/home/pi/Documents/turnRight/roadright' + str(capnum) + '.jpg')
		print('Picture: '+str(capnum) +' taken')
		capnum += 1

elif x == 4:
	while True:
		picam.capture('/home/pi/Documents/stop/roadstop' + str(capnum) + '.jpg')
		print('Picture: '+str(capnum) +' taken')
		capnum += 1

elif x == 5:
        while True:
                picam.capture('/home/pi/Documents/random/testRandom' + str(capnum) + '.jpg')
                print('Picture: '+str(capnum) +' taken')
                capnum += 1
