#! /usr/bin/env python

from SimpleCV import Camera, Image
import numpy as np
import time

# setup()

## initialize image
baseImg = Image("../images/baseImage.jpg")

## initialize camera
## cam = Camera(0, {'width':320, 'height':240})
cam = Camera()

## arguments area
imgCropCoorList = [(0,0),(320,0),(0,240),(320,240)]
imgCropWidth, imgCropHeight = 320,240

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
		currentImg = cam.getImage()
		
		imgCropList=[]
		
		imgCropList = cropImg(currentImg, imgCropCoorList)
    
		print "=========================="

		for index,imgCrop in enumerate(imgCropList):
			print "-------------------"

			if isOn(imgCrop, baseImg, 0.1):
				print ("find something in :  "+ str(index))
			else:
				print ("nothing changed in : "+ str(index))
 
		time.sleep(1)


