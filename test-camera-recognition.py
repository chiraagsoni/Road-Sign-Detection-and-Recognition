import cv2
import numpy as np
import glob

MIN_MATCH_COUNT=20
FLANN_INDEX_KDTREE = 0
cap = cv2.VideoCapture(0)
checkImages=[cv2.imread(file) for file in glob.glob("C:/Users/ROHIT/Desktop/BEproject/programs/templates/*.jpg")]
circleImage = cv2.imread('circle.jpg')
triangleImage=cv2.imread('tri1.jpg')




##finding contour of circle and triangle for comparison
grayCircle=cv2.cvtColor(circleImage,cv2.COLOR_BGR2GRAY)
grayTriangle=cv2.cvtColor(triangleImage,cv2.COLOR_BGR2GRAY)
ret, thresholdedCircle = cv2.threshold(grayCircle, 127, 255,0)
ret, thresholdedTriangle = cv2.threshold(grayTriangle, 127, 255,0)
circleContour,hierarchy=cv2.findContours(thresholdedCircle,2,1)
triContour,hierarchy=cv2.findContours(thresholdedTriangle,2,1)
circleContour=circleContour[0]
triangleContour=triContour[0]

param1=[0, 0, 0]
param2=[160,160, 255]
lower=np.array(param1)
upper=np.array(param2)
while(1):
    ##creating mask for red region
    ret, img2 = cap.read()
    mask=cv2.inRange(img2,lower,upper)
    output = cv2.bitwise_and(img2, img2, mask = mask)
    cv2.imshow('mask',mask)
    cv2.imshow('output',output)



##finding contours from edged image which support min area
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,1)
##print len(contours) ##number of contours found

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
               ## cv2.drawContours(img2,contours,idx,(0,255,255),2)


    ROIFinalTotalCopy=[]
    ROIFinalTotalCopy.extend(ROIFinalTotal)

    ##removing child contours from shape matched contours
    if len(ROIFinalTotal)>0:
        for x in ROIFinalTotal:
            if hierarchy[0][x][3] in ROIFinalTotal:
                ROIFinalTotalCopy.remove(x)
      

    shapeCategory=[]
    if len(ROIFinalTotalCopy)>0:
        for y in ROIFinalTotalCopy:
            cv2.drawContours(img2,contours,y,(0,255,255),3)
            if y in ROICircle:
                shapeCategory.append('circle')
            if y in ROITriangle:
                shapeCategory.append('triangle')
    print shapeCategory

#########cv2.drawContours(img2,contours,-1,(255,0,0),1)


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
            temp.append(z)
            rectangles.append(temp)
            cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),3)
            

    sift=cv2.SIFT()
    matchesMask=[]


    if len(rectangles)>0:
    
        for i in rectangles:
        
            imageTemp=img2[i[1]:i[1]+i[3] , i[0]:i[0]+i[2] ]
            roiKP,roiDesc=sift.detectAndCompute(imageTemp,None)
        
            index_params=dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params=dict(checks=50)
            flann=cv2.FlannBasedMatcher(index_params,search_params)
            nMatches=[]
            print len(checkImages)
            for checkImage in checkImages:
            
                dbImageKP,dbImageDesc=sift.detectAndCompute(checkImage,None)
                matches=flann.knnMatch(dbImageDesc,roiDesc,k=2)
            
                good=[]
                for m,n in matches:
                
                    if m.distance< 0.7*n.distance:
                          good.append(m)
                nMatches.append(len(good))
                '''
                if(len(good)>MIN_MATCH_COUNT):
                     print ("enough matches are found - %d" %(len(good)))
                     cv2.imshow("matched image",checkImage)
                '''
            t=nMatches.index(max(nMatches))
            print max(nMatches)
            cv2.imshow("matched Image",checkImages[t])
                       
    cv2.imshow('Dected ROI',img2)
    
    if cv2.waitKey(1)==27:
        break
cap.release()
cv2.destroyAllWindows()
