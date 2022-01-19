import cv2
import numpy as np

img1 = cv2.imread('tri1.png')
img2 = cv2.imread('tri5.jpg')

gray1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
gray2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray1, 127, 255,0)
ret, thresh2 = cv2.threshold(gray2, 127, 255,0)

contours,hierarchy = cv2.findContours(thresh,2,1)
cnt1 = contours[0]
cv2.drawContours(img1,contours,0,(200,0,0),2)
cv2.imshow('image1 contour',img1)

contours,hierarchy = cv2.findContours(thresh2,2,1)
cnt2 = contours[0]
cv2.drawContours(img2,contours,-1,(255,0,0),2)
cv2.imshow('image2 contour',img2)

ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
print ret
print hierarchy

cv2.waitKey(0)
cv2.destroyAllWindows()
