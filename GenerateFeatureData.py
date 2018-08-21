__author__ = 'Montya'

import cv2
import numpy as np
import sys

MIN_CONTOUR_AREA = 10
RESIZED_IMAGE_WIDTH = 32
RESIZED_IMAGE_HEIGHT = 32
GRID_SIZE = 8
STEP_SIZE = RESIZED_IMAGE_HEIGHT/GRID_SIZE

def main():
    imgTrainingNumbers = cv2.imread("Train.png")

               # read in training numbers image
    height,width,_ = imgTrainingNumbers.shape

    small = cv2.resize(imgTrainingNumbers,(width/4,height/4))
    cv2.imshow("small",small)
    #canny = cv2.Canny(imgTestingNumbers,20,255)
    #cv2.imshow("canny",canny)
    imgTrainingNumbers = small.copy()

    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)          # get grayscale image
    cv2.imshow("gray",imgGray)

    #imgThresh = imgGray.copy()

    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                        # blur
    cv2.imshow("blur",imgBlurred)
                                                        # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # not invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

    print kernel

    erosion = cv2.erode(imgThresh,kernel,iterations = 1)
    dilation = cv2.dilate(imgThresh, kernel, iterations = 1)

    opening = cv2.dilate(erosion, kernel, iterations = 1)
    closing = cv2.erode(dilation, kernel, iterations = 1)

    imgThresh = opening.copy()
    '''
    cv2.imshow("imgThresh", imgThresh)      # show threshold image for reference

    imgThreshCopy = imgThresh.copy()

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,                 # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)           # compress horizontal, vertical, and diagonal segments and leave only their end points

    npaFlattenedImagesVectors =  np.empty((0, GRID_SIZE*GRID_SIZE))
    intClassifications = []
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9')]


    for npaContour in npaContours:                          # for each contour
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:          # if contour is big enough to consider
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)         # get and break out bounding rect

                                                # draw rectangle around each contour as we ask user for input
            cv2.rectangle(imgTrainingNumbers,           # draw rectangle on original training image
                          (intX, intY),                 # upper left corner
                          (intX+intW,intY+intH),        # lower right corner
                          (0, 0, 255),                  # red
                          2)                            # thickness

            imgROI = imgThresh[intY:intY+intH, intX:intX+intW]                                  # crop char out of threshold image
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))     # resize image, this will be more consistent for recognition and storage


            #_,imgROIResized = cv2.threshold(imgROIResized,127,255,cv2.THRESH_BINARY)

            '''cv2.imshow("t",imgROIResized)

            black =0
            white=0
            for i in range(0,19):
                if imgROIResized[10,i] == 255:
                    white = white + 1
                elif imgROIResized[10,i] == 0:
                    black = black + 1
                print(imgROIResized[10,i])
            print(white+black)
            if(white+black == 19):
                count=count+1
                print(count)
            '''

            cv2.imshow("imgROI", imgROI)                    # show cropped out char for reference
            cv2.imshow("imgROIResized", imgROIResized)      # show resized image for reference
            cv2.imshow("training_numbers.png", imgTrainingNumbers)      # show training numbers image, this will now have red rectangles drawn on it

            intChar = cv2.waitKey(0)                     # get key press

            if intChar == 27:                   # if esc key was pressed
                sys.exit()                      # exit program
            elif intChar in intValidChars:      # else if the char is in the list of chars we are looking for . . .

                intClassifications.append(intChar)                                                # append classification char to integer list of chars (we will convert to float later before writing to file)
                featureList = []
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
                        featureList.append(black)
                featureArray = np.array(featureList)
                featureVector = featureArray.reshape((1,GRID_SIZE*GRID_SIZE))
                #print(featureArray)
                npaFlattenedImagesVectors = np.append(npaFlattenedImagesVectors,featureVector,0)

    print "\n\ntraining complete !!\n"
    fltClassifications = np.array(intClassifications)
    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))
    #print(npaClassifications)
    np.savetxt("Classifications.txt", npaClassifications)           # write flattened images to file
    np.savetxt("Feature_vectors.txt", npaFlattenedImagesVectors)          #



                #npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
                #npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                    # add current flattened impage numpy array to list of flattened image numpy arrays
            # end if
        # end if
    # end for
    cv2.waitKey(0)
    return





if __name__ == '__main__':
    main()