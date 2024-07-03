import cv2
import time
import numpy as np
import HandTracker as ht
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################
wCam, hCam = 640, 480
######################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]
volume.SetMasterVolumeLevel(0, None)

detector = ht.handDetector()

cTime = 0
pTime = 0
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    cv2.rectangle(img, (50, 150), (80, 400), (0, 255, 0), 3)
    if len(lmList) != 0:
        # print(lmList[4])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand Range from 50 to 270
        # Vol Range from -96 to 0

        vol = np.interp(length, [50, 220], [-50, maxVol])
        volBar = np.interp(length, [50, 220], [400, 150])
        volPer = np.interp(length, [50, 220], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (50, 150), (80, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)),
                      (80, 400), (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, "FPS:"+str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
    cv2.putText(img, str(int(volPer))+"%", (50, 420),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
