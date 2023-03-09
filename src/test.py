import controller
import cv2

# Constant
camera = 0
isDisplay = False

controller = controller.controller(camera, isDisplay)

while True:
    location, gesture = controller.process()

    print(location)
    print("Gesture: " + gesture)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        controller.quit()
        break
