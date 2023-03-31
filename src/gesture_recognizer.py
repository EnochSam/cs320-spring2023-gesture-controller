# Gestures
FIST = "Closed Fist"
HAND = "Open Hand"


class recognizer:
    def __init__(self) -> None:
        self.gestures = [FIST, HAND]

    def getGesture(self, joint_angles):
        isFist = True
        angle = 1
        for joint in joint_angles:
            if joint[angle] > 90:
                isFist = False
        if isFist:
            gesture = self.getIndex(FIST)
        else:
            gesture = self.getIndex(HAND)

        return gesture

    def getIndex(self, gesture):
        index = 0
        for g in self.gestures:
            if g == gesture:
                break
            else:
                index += 1
        return index
