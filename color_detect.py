import cv2 as cv
import numpy as np
framewidth = 640
frameheight = 480
cap = cv.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)
myColors = [[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255]]
myValues = [[51,153,255],[255,0,255],[0,255,0]]
points = []
def findColor(frame,myColors,myValues):
    frameHsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    count = 0
    new = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(frameHsv,lower,upper)
        x,y = getContours(mask)
        cv.circle(frameResult,(x,y),10,myValues[count],cv.FILLED)
        if x!=0 & y!=0:
            new.append([x,y,count])
        count +=1
    return new
def getContours(img):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area>500:
            peri = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv.boundingRect(approx)
    return x+w//2,y+h//2
def draw(points,myValues):
    for point in points:
        cv.circle(frameResult,(point[0],point[1]),10,myValues[point[2]],cv.FILLED)
while True:
    sucess,frame = cap.read()
    frameResult = frame.copy()
    new = findColor(frame,myColors,myValues)
    if len(new) !=0:
        for p in new:
            points.append(p)
    if len(points)!=0:
        draw(points,myValues)
    cv.imshow('result',frameResult)
    if cv.waitKey(1) & 0xff == ord('e'):
        break