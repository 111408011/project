import cv2
import numpy as np
import os
import operator
from Tkinter import *
from tkFileDialog import *

AMOUNT_BOX_X = 0
AMOUNT_BOX_Y = 0
AMOUNT_BOX_WIDTH = 0
AMOUNT_BOX_HEIGHT = 0

MIN_CONTOUR_AREA = 30
MAX_CONTOUR_AREA = 1000
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 20
count=0
countRow=0
countColomn=0
start=0
end=0
nextRow=0
previous=0
current=0
flag= False
index=0

def checkall(width,height):
	global blackhat
	count =0 
	for j in range(height):
		if(blackhat[j][width]!=0):
			count+=1
			
		
	if(count==0):					
		return False
	else:
		return True

def checkallR(height,start,end):
	global blackhat
	countR =0 
	for j in range(start,end):		
		if(blackhat[height][j]!=0):
			countR+=1
			
		
	if(countR==0):					
		return False
	else:
		return True


def finalcontour(height,start,end):
	startR=0
	endR=0
	nextRow=0
	previousR=0
	currentR=0
	flagR= False
	global index
	global blackhat
	for i in range(height):
		result=checkallR(i,start,end)
	
		if (result==True):
			if (previousR == 0):
				startR= i		
				previousR = i
				currentR=i
			elif(currentR !=0 and (currentR == (previousR+1))):
				currentR=i
				previousR+=1
			elif (currentR !=0 and currentR == previousR):
				currentR=i
		else:
			if(previousR !=0):
				endR = i
				flagR=True
				indexName=str(index)+"0.png"
				if((endR-startR)>5):
					print (endR-startR)			
					cv2.imwrite(indexName,blackhat[startR-2:endR+2,start-1:end+1])
					findAmount(blackhat[startR-2:endR+2,start-1:end+1])
					index+=1
				previousR=0
			else:
				flagR=False
				continue  


def findAmount(imgROI):
    	try:
        	npaClassifications = np.loadtxt("classifications.txt", np.float32)
    	except:
		print ("error, unable to open classifications.txt, exiting program\n")
		os.system("pause")
		return
	try:
        	npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
    	except:
		print ("error, unable to open flattened_images.txt, exiting program\n")
		os.system("pause")
		return

	npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train
	kNearest = cv2.ml.KNearest_create()                   # instantiate KNN object
	kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             # resize image, this will be more consi
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array
        npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 9)     # call KNN function find_nearest
        strCurrentChar = str(chr(int(npaResults[0][0])))                                             # get character from results
        print ("\n" + strCurrentChar + "\n")                  # show the full string
        return


img = cv2.imread("Test1.jpg")
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)       # get grayscale image
imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur
                                                        # filter image from grayscale to black and white
imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      4)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
blackhat = cv2.morphologyEx(imgThresh,cv2.MORPH_OPEN,kernel)
#blackhat = cv2.erode(blackhat1,kernel,iterations = 1)
cv2.imwrite("show.png",blackhat)
height,width,_ = img.shape

for i in range(width):
	result=checkall(i,height)
	
	if (result==True):
		if (previous == 0):
			start= i		
			previous = i
			current=i
		elif(current !=0 and (current == (previous+1))):
			current=i
			previous+=1
		elif (current !=0 and current == previous):
			current=i
	else:
		if(previous !=0):
			end = i
			flag=True
#			cv2.imwrite(indexName,blackhat[0:width,start:end])
			finalcontour(height,start,end)
			previous=0
		else:
			flag=False
			continue  

