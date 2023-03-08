import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

from matplotlib import pyplot as plt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import tracker
import display
import gesture_recognizer

# Set up drawing capeabilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Joint List
THUMB = [3, 4, 5]
INDEX = [7, 6, 5]
MIDDLE = [9, 10, 11]
RING = [15, 14, 13]
PINKY = [19, 18, 17]
joint_list = [INDEX, MIDDLE, RING, PINKY]
angle_list = []


def isBent(angle):
    return angle < 150.0


# Set up LiveStream
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:

    tracker = tracker.tracker(hands, joint_list)
    recognizer = gesture_recognizer.recognizer()
    display = display.display()

    while cap.isOpened():
        ret, frame = cap.read()

        # Find hand landmarks
        results, angle_list, image = tracker.process(ret, frame)

        # Recognize Gesture
        gesture = recognizer.recognize(angle_list)
        # Set flag to true
        image.flags.writeable = True

        # RGB - BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Render results
        # Gesture placeholder -- replace with detected gesture
        image = display.render(
            results, image, angle_list, gesture)

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
