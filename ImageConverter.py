from PIL import Image
import numpy as np
import glob
import os

filepathToConvert = '/run/media/jax/DualOS/CompSci/finalCar/mlTrain11-4-17/all/turnLeft/'
filepathEnd = '/home/jax/Documents/BluescaleImages/turnLeft/'


os.chdir("/run/media/jax/DualOS/CompSci/finalCar/mlTrain11-4-17/all/turnLeft/")
for file in glob.glob('*.jpg'):
	print(file)
	currentImg = (str(filepathToConvert)+str(file))
	loadImg = Image.open(currentImg)
	cropImg = loadImg.crop((0, 140, 320, 320))
	pixels = np.array(cropImg.getdata(band=2), dtype=np.uint8)#only gets the blue band of the image
	pixels.resize(180,320)#makes it a 2D array
	im = Image.fromarray(pixels)
	im.save(filepathEnd+'blue'+file)
	print('One image converted')
