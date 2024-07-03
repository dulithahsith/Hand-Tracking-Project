import cv2
import mediapipe as mp
import time


class handDetector:
    def __init__(self, img_mode=False, maxhands=2, minDetectionConfidence=0.7, minTrackingConfidence=0.7):
        self.img_mode = img_mode
        self.maxhands = maxhands
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(img_mode)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
                # h, w, c = img.shape
                # for id, lm in enumerate(handLms.landmark):
                #     print(id, int(lm.x*w), int(lm.y*h))
                #     if id == 0:
                #         cv2.circle(img, (int(lm.x*w), int(lm.y*h)), 5,
                #                 (255, 0, 255), 4, cv2.FILLED)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int((lm.x*w)), int((lm.y*h))
                lmList.append([id, cx, cy])
                # if draw:
                #     cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    cTime = 0
    pTime = 0
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
