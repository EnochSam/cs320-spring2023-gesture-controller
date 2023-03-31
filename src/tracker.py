import mediapipe as mp
from mediapipe.tasks import python
import cv2
import numpy as np

# Constants
location_marker = 0


class tracker():

    def __init__(self, hands, joint_list):
        self.hands = hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.joint_list = joint_list
        self.angle_list = []

    def process(self, ret, frame):
        # BGR - RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set flag
        image.flags.writeable = False

        # Flip image
        image = cv2.flip(image, 1)

        # Detections
        results = self.hands.process(image)

        self.draw_finger_angles(results, self.joint_list)

        tracking = results, self.angle_list, image

        return tracking

    def draw_finger_angles(self, results, joint_list):

        self.angle_list = []
        # Loop through hands
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                # Loop through joint sets
                for joint in joint_list:
                    # First Coord
                    a = np.array([hand.landmark[joint[0]].x,
                                  hand.landmark[joint[0]].y])
                    # Second Coord
                    b = np.array([hand.landmark[joint[1]].x,
                                  hand.landmark[joint[1]].y])
                    # Third Coord
                    c = np.array([hand.landmark[joint[2]].x,
                                  hand.landmark[joint[2]].y])

                    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
                        np.arctan2(a[1] - b[1], a[0] - b[0])
                    angle = np.abs(radians*180.0/np.pi)\

                    self.angle_list.append([b, angle])

    def getLocation(self, results, screen_size):
        if results.multi_hand_landmarks:
            location = []
            for hand in results.multi_hand_landmarks:
                location.append(tuple(np.multiply(
                    np.array((hand.landmark[location_marker].x,
                              hand.landmark[location_marker].y)),
                    screen_size).astype(int)))
        else:
            location = "None"
        return location
