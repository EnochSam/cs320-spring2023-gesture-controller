import mediapipe as mp
import cv2

import gesture_recognizer
# import tracker

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


class controller:

    def __init__(self, camera, isDisplay, screen_size):
        # Set up LiveStream
        self.isDisplay = isDisplay
        self.tracker = __import__("tracker")
        self.display = __import__("display")
        self.screen_size = screen_size

        self.cap = cv2.VideoCapture(camera)

        self.hands = mp_hands.Hands(min_detection_confidence=0.8,
                                    min_tracking_confidence=0.5)

    def process(self):
        # with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:

        tracker = self.tracker.tracker(self.hands, joint_list)
        recognizer = gesture_recognizer.recognizer()
        display = self.display.display()

        if self.cap.isOpened():
            ret, frame = self.cap.read()

            # Find hand landmarks
            results, angle_list, image = tracker.process(ret, frame)

            # Find palm position
            location = tracker.getLocation(results, self.screen_size)
            # Recognize Gesture
            gesture = recognizer.getGesture(angle_list)
            # Set flag to true
            image.flags.writeable = True

            # RGB - BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Render results
            if self.isDisplay:
                image = display.render(
                    results, image, angle_list, recognizer.gestures[gesture])
                cv2.imshow('Hand Tracking', image)

        input = location, gesture

        return input

    def quit(self):
        self.cap.release()
        cv2.destroyAllWindows()
