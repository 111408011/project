__author__ = 'Montya'

import cv2
import numpy as np
import os
import operator
import sys

MIN_CONTOUR_AREA = 30
RESIZED_IMAGE_WIDTH = 32
RESIZED_IMAGE_HEIGHT = 32
GRID_SIZE = 8
STEP_SIZE = RESIZED_IMAGE_HEIGHT/GRID_SIZE
ERROR = 1#2
SECTION_MATCH_THRESHOLD = 22#22



class ContourWithData():

    # member variables ############################################################################
    npaContour = None           # contour
    boundingRect = None         # bounding rect for contour
    intRectX = 0                # bounding rect top left corner x location
    intRectY = 0                # bounding rect top left corner y location
    intRectWidth = 0            # bounding rect width
    intRectHeight = 0           # bounding rect height
    fltArea = 0.0               # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):                            # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False        # much better validity checking would be necessary
        return True

###################################################################################################


def main():

    allContoursWithData = []                # declare empty lists,
    validContoursWithData = []              # we will fill these shortly
    total = 0.0
    totalCorrect = 0.0

    try:
        npaClassifications = np.loadtxt("Classifications.txt", np.int)                  # read in training classifications
    except:
        print "error, unable to open classifications.txt, exiting program\n"
        os.system("pause")
        return


    try:
        npaFlattenedImagesVectors = np.loadtxt("Feature_vectors.txt", np.int)                 # read in training images
    except:
        print "error, unable to open flattened_images.txt, exiting program\n"
        os.system("pause")
        return

    #print(npaClassifications[0])
    #print(npaFlattenedImagesVectors[0][0])
    print (npaClassifications.size)
    print (npaFlattenedImagesVectors.size)

    imgTestingNumbers = cv2.imread("Slip.jpg")          # read in testing numbers image

    height,width,_ = imgTestingNumbers.shape

    small = cv2.resize(imgTestingNumbers,(width/4,height/4))
    cv2.imshow("small",small)
    #canny = cv2.Canny(imgTestingNumbers,20,255)
    #cv2.imshow("canny",canny)
    imgTestingNumbers = small.copy()

    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)       # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur

                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean
    '''kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

    print kernel

    erosion = cv2.erode(imgThresh,kernel,iterations = 1)
    dilation = cv2.dilate(imgThresh, kernel, iterations = 1)

    opening = cv2.dilate(erosion, kernel, iterations = 1)
    closing = cv2.erode(dilation, kernel, iterations = 1)

    imgThresh = opening.copy()
'''
    cv2.imshow("imgThresh", imgThresh)      # show threshold image for reference

    imgThreshCopy = imgThresh.copy()        # make a copy of the thresh image, this in necessary b/c findContours modifies the image

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,             # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,         # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)   # compress horizontal, vertical, and diagonal segments and leave only their end points

    for npaContour in npaContours:                             # for each contour
        contourWithData = ContourWithData()                                             # instantiate a contour with data object
        contourWithData.npaContour = npaContour                                         # assign contour to contour with data
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
        allContoursWithData.append(contourWithData)                                     # add contour with data object to list of all contours with data
    # end for

    for contourWithData in allContoursWithData:                 # for all contours
        if contourWithData.checkIfContourIsValid():             # check if valid
            validContoursWithData.append(contourWithData)       # if so, append to valid contour list
        # end if
    # end for

    validContoursWithData.sort(key = operator.attrgetter("intRectX"))         # sort contours from left to right

    strFinalString = ""         # declare final string, this will have the final number sequence by the end of the program

    for contourWithData in validContoursWithData:            # for each contour

        cnt = np.zeros((10,), dtype=np.int)
                                                # draw a green rect around the current char
        cv2.rectangle(imgTestingNumbers,                                        # draw rectangle on original testing image
                      (contourWithData.intRectX, contourWithData.intRectY),     # upper left corner
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),      # lower right corner
                      (0, 255, 0),              # green
                      2)                        # thickness

        cv2.imshow("imgTestingNumbers", imgTestingNumbers)
        cn = imgTestingNumbers[contourWithData.intRectY:contourWithData.intRectY+contourWithData.intRectHeight,contourWithData.intRectX:contourWithData.intRectX+contourWithData.intRectWidth]
        cn = cv2.resize(cn,(32,32))
        cv2.imshow("digit",cn)


        imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,     # crop char out of threshold image
                           contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             # resize image, this will be more consistent for recognition and storage
        print("Test1")
        for arrayRow in range(0,292,1):
            sectionNumber = 0
            sectionPass = np.zeros((GRID_SIZE*GRID_SIZE,), dtype=np.int)
            for row in range(0,GRID_SIZE,1):
                for col in range(0,GRID_SIZE,1):
                    black=0
                    white=0
                    sectY = row*STEP_SIZE
                    sectX = col*STEP_SIZE
                    imgSection = imgROIResized[sectY:sectY+STEP_SIZE, sectX:sectX+STEP_SIZE]
                    #imgName = "Section "+str(row)+str(col)
                    #cv2.imshow(imgName,imgSection)
                    #print(imgName)
                    for i in range(0,STEP_SIZE):
                        for j in range(0,STEP_SIZE):
                            if imgSection[i,j] == 255:
                                white = white + 1
                            elif imgSection[i,j] == 0:
                                black = black + 1
                    #print(black)
                    if(abs(black - npaFlattenedImagesVectors[arrayRow][sectionNumber])< ERROR):
                        sectionPass[sectionNumber] = 1

                    #featureList.append(black)
                    sectionNumber = sectionNumber + 1

            sectionMatched = 0
            for s in sectionPass:
                if(s==1):
                    sectionMatched = sectionMatched + 1

            if(sectionMatched>SECTION_MATCH_THRESHOLD):

                num = npaClassifications[arrayRow]
                num = num - 48
                cnt[num] = cnt[num] + 1

        maxIndex=cnt.argmax()
        print(cnt)
        maxIndex = maxIndex + 48
        c=maxIndex

        key = cv2.waitKey(0)
        if key==27:
            sys.exit()

        if(key == c):
            totalCorrect = totalCorrect + 1

        total = total + 1

                                                     # get character from results

        #strFinalString = strFinalString + strCurrentChar            # append current char to full string
    # end for
    print("total = " + str(total))
    print("total correct = " + str(totalCorrect))
    percentage = totalCorrect/total*100.0
    print("Percentage = " + str(percentage))

    # end for
    '''
    cv2.imshow("imgTestingNumbers", imgTestingNumbers)
    print(strFinalString)'''
    cv2.waitKey(0)
    return

if __name__ == '__main__':
    main()