import cv2
import numpy as np

circleImage = cv2.imread('circle.jpg')
triangleImage=cv2.imread('tri1.jpg')
img = cv2.imread('t5.jpg')
width=len(img[0])
height=len(img)

if width>=850 and width<1100:
    width=int(width/2)
elif width>=1100:
        width=int(width/2)

if height>=600 and height<700:
    height=int(height/2)
elif height>=700:
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
param2=[160,160, 255]
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
        


ROIFinalTotal=[]
##matching shapes and removing non matched shapes
if len(minAreaSupportedIndex)>0:
    for idx in minAreaSupportedIndex:
        value1=cv2.matchShapes(contours[idx],circleContour,1,0.0)
        value2=cv2.matchShapes(contours[idx],triangleContour,1,0.0)
        if value1<=0.03555:
            print 'circle',value1
            ROICircle.append(idx)
            ROIFinalTotal.append(idx)
            
        if value2<=0.03555:
            ROITriangle.append(idx)
            print 'triangle',value2
            ROIFinalTotal.append(idx)
            


ROIFinalTotalCopy=[]
ROIFinalTotalCopy.extend(ROIFinalTotal)

##removing child contours from shape matched contours
if len(ROIFinalTotal)>0:
    for x in ROIFinalTotal:
        print hierarchy[0][x]
        if hierarchy[0][x][3] in ROIFinalTotal:
            ROIFinalTotalCopy.remove(x)
        if hierarchy[0][hierarchy[0][x][3]][3] in ROIFinalTotal:
            ROIFinalTotalCopy.remove(x)
           

shapeCategory=[]
if len(ROIFinalTotalCopy)>0:
    for y in ROIFinalTotalCopy:
        cv2.drawContours(img2,contours,y,(255,0,0),3)
        if y in ROICircle:
            shapeCategory.append('circle')
        if y in ROITriangle:
            shapeCategory.append('triangle')
print shapeCategory

cv2.drawContours(img2,contours,-1,(255,0,0),1)

print ROIFinalTotalCopy
rectangles=[]
##drawing rectangles around ROIs
if len(ROIFinalTotalCopy)>0:
    for z in ROIFinalTotalCopy:
        x,y,w,h=cv2.boundingRect(contours[z])
        temp=[]
        temp.append(x)
        temp.append(y)
        temp.append(w)
        temp.append(h)
        rectangles.append(temp)
        cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),3)
        #imageTemp=img2[y:y+h,x:x+w]
        #cv2.imshow("Extracted ROI",imageTemp)
for i in rectangles:
    imageTemp=img2[i[1]:i[1]+i[3] , i[0]:i[0]+i[2] ]
    cv2.imshow("ROI",imageTemp)
    
cv2.imshow('Dected ROI',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
