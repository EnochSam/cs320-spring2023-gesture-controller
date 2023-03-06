import cv2
import mediapipe as mp
import numpy as np

from matplotlib import pyplot as plt


# Joint List
THUMB = [3, 4, 5]
INDEX = [7, 6, 5]
MIDDLE = [9, 10, 11]
RING = [15, 14, 13]
PINKY = [19, 18, 17]
joint_list = [INDEX, MIDDLE, RING, PINKY]
angle_list = []


class display():
    def __init__(self):
        # Set up drawing capeabilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.joint_list = joint_list
        self.angle_list = angle_list

    def render(self, results, image, gesture):
        # Render results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                self.mp_drawing.draw_landmarks(
                    image, hand, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(
                        color=(121, 22, 76), thickness=2, circle_radius=4),
                    self.mp_drawing.DrawingSpec(
                        color=(121, 44, 250), thickness=2, circle_radius=2),
                )

                # Render left or right
                if self.get_label(num, hand, results):
                    text, coord = self.get_label(num, hand, results)
                    # cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX,
                    #             1, (255, 255, 255), 2, cv2.LINE_AA)
            # Draw finger angles
            self.draw_finger_angles(image, results, self.joint_list)

            # print("IS fist")
            # Save Images
            # cv2.imwrite(os.path.join('output_images',
            #             '{}.jpg'.format(uuid.uuid1())), image)

            cv2.putText(image, gesture, tuple(np.multiply(
                np.array((hand.landmark[self.mp_hands.HandLandmark.WRIST].x,
                          hand.landmark[self.mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        return image

    def get_label(self, index, hand, results):
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
                        (hand.landmark[self.mp_hands.HandLandmark.WRIST].x, hand.landmark[self.mp_hands.HandLandmark.WRIST].y)),
                    [640, 480]).astype(int))

                output = text, coords

                return output

    def draw_finger_angles(self, image, results, joint_list):

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

                self.angle_list.append(angle)

        return image
