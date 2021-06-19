import cv2
import numpy as np
import mediapipe as mp
import time
import os
import HandTrackingModule as htp

brushthickness=25
eraserthickness=100
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlaylist = []
for inPath in myList:
    image = cv2.imread(f'{folderPath}/{inPath}')
    overlaylist.append(image)
print(len(overlaylist))
header = overlaylist[0]
drawColor=(255,0,255)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector=htp.handDetector(detectionCon=0.85)

while True:
    success, img = cap.read()
    img=cv2.flip(img,1)

    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)

    if len(lmlist)!=0:

        print(lmlist)
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]

        fingers=detector.fingersUp()
        print(fingers)

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
            print("Selection")
            if y1<125:
                if 250<x1<450:
                    header=overlaylist[0]
                    drawColor=(255,0,255)
                elif 550<x1<750:
                    header=overlaylist[1]
                    drawColor = (255, 0, 0)
                elif 800<x1<950:
                    header=overlaylist[2]
                    drawColor = (0, 255, 0)
                elif 1050<x1<1200:
                    header=overlaylist[3]
                    drawColor = (0, 0, 0)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),25,drawColor,cv2.FILLED)
            print("Drawing")
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserthickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushthickness)

            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    # cv2.resize(img, (1200, 720))
    # cv2.resize(imgInv, (1200, 720))
    # cv2.resize(imgCanvas, (1200, 720))
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    img[0:125,0:1280]=header
    # img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Canvas",imgCanvas)
    cv2.imshow("Image", img)
    cv2.waitKey(1)



cv2.destroyAllWindows()
