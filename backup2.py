import cv2
import numpy as np

circleImage = cv2.imread('circle.jpg')
triangleImage=cv2.imread('tri1.jpg')
img = cv2.imread('s2.jpg')
width=len(img[0])
height=len(img)

if width>=600:
    width=int(width/2)
if height>=400:
    height=int(height/2)
img2=cv2.resize(img,(width,height))


##finding contour of circle and triangle for comparison
grayCircle=cv2.cvtColor(circleImage,cv2.COLOR_BGR2GRAY)
grayTriangle=cv2.cvtColor(triangleImage,cv2.COLOR_BGR2GRAY)
ret, thresholdedCircle = cv2.threshold(grayCircle, 127, 255,0)
ret, thresholdedTriangle = cv2.threshold(grayTriangle, 127, 255,0)
circleContour,hierarchy=cv2.findContours(thresholdedCircle,2,1)
triContour,hierarchy=cv2.findContours(thresholdedTriangle,2,1)
circleContour=circleContour[0]
triangleContour=triContour[0]
##creating mask for red region
param1=[0, 0, 0]
param2=[120 ,65, 255]
lower=np.array(param1)
upper=np.array(param2)
mask=cv2.inRange(img2,lower,upper)
output = cv2.bitwise_and(img2, img2, mask = mask)
cv2.imshow('mask',mask)
cv2.imshow('output',output)



##finding contours from edged image which support min area
contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,1)
print len(contours) ##number of contours found

minAreaSupportedIndex=[]
ROICircle=[]
ROITriangle=[]
for index,cnt in enumerate(contours):
    area=cv2.contourArea(cnt)

    if area>=2200:##min area of sign is assumed to be 2200
        minAreaSupportedIndex.append(index)
        



##matching shapes and removing non matched shapes
if len(minAreaSupportedIndex)>0:
    for idx in minAreaSupportedIndex:
        value1=cv2.matchShapes(contours[idx],circleContour,1,0.0)
        value2=cv2.matchShapes(contours[idx],triangleContour,1,0.0)
        if value1<=0.09999:
            ROICircle.append(idx)
            cv2.drawContours(img2,contours,idx,(255,0,0),2)
        if value2<=0.09999:
            ROITriangle.append(idx)
            cv2.drawContours(img2,contours,idx,(255,0,0),2)


ROICircleFinal=[]
ROITriangleFinal=[]
ROICircleFinal.extend(ROICircle)
ROITriangleFinal.extend(ROITriangle)

ROIFinalTotal=[]
ROIFinalTotal=ROICircleFinal+ROITriangleFinal

##removing child contours from shape matched contours
if len(ROICircle)>0:
    for x in ROICircle:
    
        if hierarchy[0][x][3] in ROIFinalTotal:
            ROICircleFinal.remove(x)
            ROIFinalTotal.remove(x)
    for y in ROICircleFinal:
        cv2.drawContours(img2,contours,y,(0,255,255),2)


if len(ROITriangle)>0:
    for x in ROITriangle:
    
        if hierarchy[0][x][3] in ROIFinalTotal:
            ROITriangleFinal.remove(x)
            ROIFinalTotal.remove(x)
    for y in ROITriangleFinal:
        cv2.drawContours(img2,contours,y,(0,255,255),2)

'''
print 'tiangular ROI',ROITriangleFinal
print 'circular ROI',ROICircleFinal



cv2.drawContours(img2,contours,-1,(255,0,0),1)

print ROIFinalTotal
##drawing rectangles around ROIs
if len(ROIFinalTotal)>0:
    for z in ROIFinalTotal:
        x,y,w,h=cv2.boundingRect(contours[z])    
        cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),3)
    
'''

cv2.imshow(' contours',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
