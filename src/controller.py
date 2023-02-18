import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

from matplotlib import pyplot as plt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Set up drawing capeabilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:

            # Process Results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Extract Coordinates
            coords = tuple(np.multiply(
                           np.array(
                               (hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                           [640, 480]).astype(int))

            output = text, coords

            return output


def draw_finger_angles(image, results, joint_list):

    # Loop through hands
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

            if angle > 180.0:
                angle = 360-angle

            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(
                int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # if isBent(angle):
            #     print("joint {} is bent".format(joint))

            angle_list.append(angle)

    return image


def isBent(angle):
    return angle < 150.0


# Joint List
THUMB = [3, 4, 5]
INDEX = [7, 6, 5]
MIDDLE = [9, 10, 11]
RING = [15, 14, 13]
PINKY = [19, 18, 17]
joint_list = [INDEX, MIDDLE, RING, PINKY]
angle_list = []
isFist = False

# Set up LiveStream
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        # BGR - RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set flag
        image.flags.writeable = False

        # Flip image
        image = cv2.flip(image, 1)

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB - BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detections
        # print(results)
        # print(results.multi_hand_landmarks)
        # print(results.multi_handedness)

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

                # Render left or right
                if get_label(num, hand, results):
                    text, coord = get_label(num, hand, results)
                    cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 255, 255), 2, cv2.LINE_AA)

            # Draw finger angles
            draw_finger_angles(image, results, joint_list)

        for angle in angle_list:
            isFist = isBent(angle)

        if isFist:
            print("IS fist")
        # Save Images
        # cv2.imwrite(os.path.join('output_images',
        #             '{}.jpg'.format(uuid.uuid1())), image)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
