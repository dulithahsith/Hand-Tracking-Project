import cv2
import os
import time
import numpy as np
import HandTracker as ht
import math

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = ht.handDetector()

folderPath = "FingerCounterImages"
myList = os.listdir(folderPath)

overLayList = []
for path in myList:
    image = cv2.imread(f'{folderPath}/{path}')
    image = cv2.resize(image, (150, 150))
    overLayList.append(image)

cTime = 0
pTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    fingerTips = [8, 12, 16, 20]
    fingers = [0, 0, 0, 0, 0]
    img[0:150, 0:150] = overLayList[0]

    if len(lmList) != 0:
        if lmList[4][1] > lmList[3][1]:
            fingers[0] = 1
        for i in range(0, 4):
            if lmList[fingerTips[i]][2] < lmList[fingerTips[i]-2][2]:
                fingers[i+1] = 1
        totFingers = fingers.count(1)
        img[0:150, 0:150] = overLayList[totFingers]
    print(fingers)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, "FPS:"+str(int(fps)), (300, 70),
                cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
