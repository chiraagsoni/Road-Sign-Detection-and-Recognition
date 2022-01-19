import numpy as np
import cv2

## Read the image
img = cv2.imread('tri6.jpg')
cv2.imshow('Original image',img)

## Do the processing
i = 3  # Draw contour(i)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # Convert to binary image
##ret,thresh = cv2.threshold(gray,127,255,0)

## Canny edge detectionto find threshold insead of using the above function(cv2.threshold())
thresh=cv2.Canny(img,100,200)
cv2.imshow('Canny Image',thresh)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,i,(255,0,0),3)
print len(contours) # Total number of contours in the image
print "Area = ", cv2.contourArea(contours[i])
print "Perimeter = ", cv2.arcLength(contours[i],True)

## Show the image
cv2.imshow('image',img)

## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
