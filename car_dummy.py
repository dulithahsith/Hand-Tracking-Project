import cv2
import os
import time
import numpy as np
import HandTracker as ht
import math
from pynput.keyboard import Controller, Key

keyboard = Controller()

######################
wCam, hCam = 640, 480
######################

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

detector = ht.handDetector()

cTime = 0
pTime = 0
volPer = 0

# Track the state of each key
keys_pressed = {
    's': False,
    'w': False,
    'a': False,
    'd': False,
    Key.shift_l: False,
    Key.ctrl_l: False
}


folderPath = "F:\Projects\Computer Vision\Hand Tracking Project\CarPartImages"
myList = os.listdir(folderPath)


img_accl = cv2.imread(f'{folderPath}/accelerator.png')
img_accl = cv2.resize(img_accl, (100, 250))

img_break = cv2.imread(f'{folderPath}/break.png')
img_break = cv2.resize(img_break, (100, 200))

img_upshift = cv2.imread(f'{folderPath}/upshift.png')
img_upshift = cv2.resize(img_upshift, (60, 280))

img_downshift = cv2.imread(f'{folderPath}/downshift.png')
img_downshift = cv2.resize(img_downshift, (60, 280))


# Function to press a key if not already pressed


def press_key(key):
    if not keys_pressed[key]:
        keyboard.press(key)
        keys_pressed[key] = True

# Function to release a key if currently pressed


def release_key(key):
    if keys_pressed[key]:
        keyboard.release(key)
        keys_pressed[key] = False


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList1, lmList2 = detector.findPosition(img)

    if len(lmList1) != 0 and len(lmList2) != 0:
        # print(lmList[4])
        a1, a2 = lmList1[4][2], lmList1[5][2]
        b1, b2 = lmList2[4][2], lmList2[5][2]
        c1, c2 = lmList1[12][1], lmList1[11][1]
        d1, d2 = lmList2[12][1], lmList2[11][1]
        if (a2 - a1 < 20):
            press_key('s')
        else:
            release_key('s')

        if (b2 - b1 < 20):
            press_key('w')
            img[195:445, 370:470] = img_accl
        else:
            release_key('w')

        if (a2 - b2 > 40):
            keyboard.press('a')
            if (a2 - b2 > 50):
                press_key('w')
                time.sleep(0.04)
            elif (a2 - b2 > 70):
                press_key('w')
                time.sleep(0.07)
            else:
                time.sleep(0.03)
            keyboard.release('a')

        if (a2 - b2 < -40):
            keyboard.press('d')
            if (a2 - b2 < -50):
                press_key('w')
                time.sleep(0.04)
            elif (a2 - b2 < -70):
                press_key('w')
                time.sleep(0.07)
            else:
                time.sleep(0.03)
            keyboard.release('d')
        if (d1 < d2):
            press_key(Key.shift_l)
        else:
            release_key(Key.shift_l)
        if (c1 > c2):
            press_key(Key.ctrl_l)
        else:
            release_key(Key.ctrl_l)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, "FPS:"+str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
