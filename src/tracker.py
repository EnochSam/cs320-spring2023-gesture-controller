import mediapipe as mp
from mediapipe.tasks import python
import cv2


class tracker():

    def __init__(self, hands):
        self.hands = hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def process(self, ret, frame):
        # BGR - RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set flag
        image.flags.writeable = False

        # Flip image
        image = cv2.flip(image, 1)

        # Detections
        results = self.hands.process(image)

        tracking = results, image

        return tracking
