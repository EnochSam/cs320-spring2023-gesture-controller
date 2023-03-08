import cv2
import mediapipe as mp
import numpy as np

from matplotlib import pyplot as plt


class display():
    def __init__(self):
        # Set up drawing capeabilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def render(self, results, image, angle_list, gesture):
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
            self.draw_finger_angles(image, angle_list)

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

    def draw_finger_angles(self, image, angle_list):
        angle = 1
        location = 0
        for joint in angle_list:
            cv2.putText(image, str(round(joint[angle], 2)), tuple(np.multiply(joint[location], [640, 480]).astype(
                int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        return image
