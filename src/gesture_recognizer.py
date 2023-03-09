class recognizer:
    def getGesture(self, joint_angles):
        isFist = True
        angle = 1
        for joint in joint_angles:
            if joint[angle] > 90:
                isFist = False
        if isFist:
            gesture = "Closed Fist"
        else:
            gesture = "Open Hand"
        return gesture
