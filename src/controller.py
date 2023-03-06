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

# Set up drawing capeabilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def isBent(angle):
    return angle < 150.0


# Set up LiveStream
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:

    tracker = tracker.tracker(hands)
    display = display.display()

    while cap.isOpened():
        ret, frame = cap.read()

        results, image = tracker.process(ret, frame)

        # Set flag to true
        image.flags.writeable = True

        # RGB - BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Render results
        # Gesture placeholder -- replace with detected gesture
        image = display.render(results, image, "Is fist")

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
