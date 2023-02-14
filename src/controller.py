import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Set up drawing capeabilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# Set up LiveStream
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        # BGR - RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB - BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Flip image
        # image = cv2.flip(image, 1)

        # Detections
        print(results)
        print(results.multi_hand_landmarks)

        # Render results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image, hand, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(
                        color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(
                        color=(121, 44, 250), thickness=2, circle_radius=2),
                )

        # Save Images
        # cv2.imwrite(os.path.join('output_images',
        #             '{}.jpg'.format(uuid.uuid1())), image)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


# #Base Options
# BaseOptions = mp.tasks.BaseOptions
# GestureRecognizer = mp.tasks.vision.GestureRecognizer
# GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
# GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
# VisionRunningMode = mp.tasks.vision.VisionRunningMode

# #Create a gesture recognizer instance with live stream mode
# def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#     print('gesture recognition result {}'.format(result))

# options = GestureRecognizerOptions(
#     base_options=BaseOptions(model_asset_path='C:\\Users\\samen\\cs320-spring2023-gesture-controller\\src\\gesture_recognizer.task'),
#     running_mode=VisionRunningMode.LIVE_STREAM,
#     result_callback=print_result)
# with GestureRecognizer.create_from_options(options) as recognizer:


# model_path = 'C:\\Users\\samen\\cs320-spring2023-gesture-controller\\src\\gesture_recognizer.task'
# base_options = BaseOptions(model_asset_path=model_path)
