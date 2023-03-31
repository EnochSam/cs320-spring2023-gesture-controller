import webbrowser
import time
# Gestures
FIST = "Closed Fist"
HAND = "Open Hand"


def getTime():
    return time.perf_counter()


def elapsed_time(initial):
    return time.perf_counter() - initial


class recognizer:
    def __init__(self) -> None:
        self.gestures = [FIST, HAND]
        self.Cooldown = 5
        self.lastCall = getTime()

    def getGesture(self, joint_angles):
        isFist = True
        angle = 1
        for joint in joint_angles:
            if joint[angle] > 90:
                isFist = False
        if isFist:
            gesture = self.getIndex(FIST)
        elif self.testGesture(joint_angles):
            gesture = self.getIndex(HAND)
            if (elapsed_time(self.lastCall) >= self.Cooldown):
                webbrowser.open("https://www.youtube.com/watch?v=iQwTTRLuEyU")
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

    def testGesture(self, angle_list):
        return (angle_list[0][1] >= 90 and angle_list[1][1] < 90 and angle_list[2][1] < 90 and angle_list[3][1] < 90)

    def isBent(self, angle):
        return angle < 90
