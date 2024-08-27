import cv2
import time
import HandTracker as ht
import keyboard

variable = 1


def press_with_var(variable):
    if variable == 1:
        keyboard.press_and_release('w')
        print('W pressed')
    else:
        keyboard.press_and_release('s')
        print('S pressed')


try:
    while True:
        press_with_var(variable)
        time.sleep(1)  # Delay to avoid spamming, adjust as needed
        # Update the variable for demonstration (you can remove or modify this part)
        variable = 1 if variable == 0 else 0

except KeyboardInterrupt:
    print("Program terminated by user")
