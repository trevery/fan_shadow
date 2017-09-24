#! /usr/bin/env python

from SimpleCV import Camera, Image
import numpy as np
import time
import serial 
import RPi.GPIO as GPIO

# setup()

## arguments area

imgCropCoorList = [ (21,453),(16,240),(11,13),
					(311,457),(312,241),(313,18),
					(587,459),(593,242),(603,18)]
imgCropWidth, imgCropHeight = 15,15

gpioList= [ 29,31,32,
			33,35,36,
			37,38,40]

threshold = 0.2

## initialize GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpioList, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(38, GPIO.OUT)
#GPIO.setup(40, GPIO.OUT)

'''
GPIO.output(16, GPIO.HIGH)
GPIO.output(20, GPIO.HIGH)
GPIO.output(21, GPIO.HIGH)
'''

## initialize serial
#ser = serial.Serial("/dev/ttyAMA0",9600)

## initialize Image
baseImg = Image("/home/pi/Desktop/fan_shadow/images/baseImage.jpeg")

## initialize camera
## cam = Camera(0, {'width':320, 'height':240})
cam = Camera()



## functions area
def isOn(currentImg, baseImg, threshold):
    '''
    threshold is between(0, 1)
    if percent_change > threshold,
    return True
    '''
    diff = baseImg - currentImg
    matrix = diff.getNumpy()
    flat = matrix.flatten()
    
    # find how much changed
    num_change = np.count_nonzero(flat)
    percent_change = float(num_change)/float(len(flat))
    if percent_change > threshold:
        return True
    else:
        return False



def cropImg(img,imgCropCoorList):
    '''
    return a image list, contain 9 images
    which cropped from the current image.
    '''
    for imgCropCoor in imgCropCoorList:
        ## get x,y coordinate
        xCoor, yCoor = imgCropCoor
        
        ## crop image
        imgCrop = img.crop(xCoor, yCoor, imgCropWidth, imgCropHeight)
        imgCropList.append(imgCrop)

    return imgCropList

# loop()


if __name__ == '__main__':
	
	while True:
		## initialize gpio output to GPIO.HIGH
		GPIO.output(gpioList, GPIO.HIGH)
		#time.sleep(1)
		currentImg = cam.getImage()
		imgCropList=[]
		serialList=[]
		imgCropList = cropImg(currentImg, imgCropCoorList)
    	
    	##buttonList=[36,38,40]
    	
		print ("==========================")
		for index,imgCrop in enumerate(imgCropList):
			print ("-------------------")
			
			if isOn(imgCrop, baseImg, threshold):
				#print("index is : "+str(index))
				GPIO.output(gpioList[index], GPIO.LOW)
				#print(gpioList[index])
				print ("find something in :  "+ str(gpioList[index]))
				#serialList.append(1)
			else:
				GPIO.output(gpioList[index], GPIO.HIGH)
				print ("nothing changed in : "+ str(gpioList[index]))
				#serialList.append(0)
				#ser.write(str(serialList))
				#print(str(serialList))
		time.sleep(0.3)


