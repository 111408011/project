__author__ = 'Montya'

import cv2
import numpy as np
import os
import operator

AMOUNT_BOX_X = 0
AMOUNT_BOX_Y = 0
AMOUNT_BOX_WIDTH = 0
AMOUNT_BOX_HEIGHT = 0

MIN_CONTOUR_AREA = 50
MAX_CONTOUR_AREA = 1000
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 20

def findBox():

    global AMOUNT_BOX_X
    global AMOUNT_BOX_Y
    global AMOUNT_BOX_WIDTH
    global AMOUNT_BOX_HEIGHT

    img = cv2.imread("44.jpg")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur

                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean

    cv2.imshow("th",imgThresh)
    imgThreshCopy = imgThresh.copy()

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,             # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,         # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)   # compress horizontal, vertical, and diagonal segments and leave only their end points

    for npaContour in npaContours:


        area = cv2.contourArea(npaContour)
        print(area)
        if(area > 13000 and area < 20000):
            #print(area)
            [intX, intY, intWidth, intHeight] = cv2.boundingRect(npaContour)

                              # thickness
            AMOUNT_BOX_X = intX + 50
            AMOUNT_BOX_Y = intY
            AMOUNT_BOX_WIDTH = intWidth - 50
            AMOUNT_BOX_HEIGHT = intHeight

            cv2.rectangle(img,           # draw rectangle on original training image
                          (AMOUNT_BOX_X, AMOUNT_BOX_Y),                 # upper left corner
                          (AMOUNT_BOX_X+AMOUNT_BOX_WIDTH,AMOUNT_BOX_Y+AMOUNT_BOX_HEIGHT),        # lower right corner
                          (0, 0, 255),                  # red
                          2)
    cv2.imshow("box",img)
    return

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
        elif self.fltArea > MAX_CONTOUR_AREA: return False
        return True

###################################################################################################



def findAmount():

    imgSlip = cv2.imread("44.jpg")
    imgAmountBox = imgSlip[AMOUNT_BOX_Y:AMOUNT_BOX_Y+AMOUNT_BOX_HEIGHT, AMOUNT_BOX_X:AMOUNT_BOX_X+AMOUNT_BOX_WIDTH]

    cv2.imshow("AmountBox",imgAmountBox)

    allContoursWithData = []                # declare empty lists,
    validContoursWithData = []              # we will fill these shortly
    total = 0.0
    totalCorrect = 0.0

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
    except:
        print "error, unable to open classifications.txt, exiting program\n"
        os.system("pause")
        return


    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
    except:
        print "error, unable to open flattened_images.txt, exiting program\n"
        os.system("pause")
        return

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

    kNearest = cv2.ml.KNearest_create()                   # instantiate KNN object

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)


    height,width,_ = imgAmountBox.shape

    #small = cv2.resize(imgAmountBox,(width/4,height/4))
    #cv2.imshow("small",small)
    #imgTestingNumbers = small.copy()
    if imgAmountBox is None:                           # if image was not read successfully
        print "error: image not read from file \n\n"        # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit function (which exits program)
    # end if

    imgGray = cv2.cvtColor(imgAmountBox, cv2.COLOR_BGR2GRAY)       # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur

                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean

    imgThreshCopy = imgThresh.copy()       # make a copy of the thresh image, this in necessary b/c findContours modifies the image

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
                                                # draw a green rect around the current char
        cv2.rectangle(imgAmountBox,                                        # draw rectangle on original testing image
                      (contourWithData.intRectX, contourWithData.intRectY),     # upper left corner
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),      # lower right corner
                      (0, 255, 0),              # green
                      2)
                                          # thickness
        cv2.imshow("imgTestingNumbers", imgAmountBox)

        imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,     # crop char out of threshold image
                           contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             # resize image, this will be more consistent for recognition and storage

        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array

        npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 9)     # call KNN function find_nearest

        strCurrentChar = str(chr(int(npaResults[0][0])))                                             # get character from results

        strFinalString = strFinalString + strCurrentChar            # append current char to full string
    # end for

    print "\n" + strFinalString + "\n"                  # show the full string

    cv2.imshow("imgAmountBox", imgAmountBox)      # show input image with green boxes drawn around found digits
    cv2.waitKey(0)                                          # wait for user key press

    cv2.destroyAllWindows()


    return



def main():

    findBox()       #finds the coordinates of box

    print(AMOUNT_BOX_X)
    print(AMOUNT_BOX_WIDTH)
    print(AMOUNT_BOX_Y)
    print(AMOUNT_BOX_HEIGHT)

    findAmount()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()