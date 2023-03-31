import controller
import cv2

# Constant

FIST = 0
HAND = 1


CAMERA = 0
ISDISPLAY = True
QUIT = HAND

SCREEN_SIZE = [640, 800]


controller = controller.controller(CAMERA, ISDISPLAY, SCREEN_SIZE)


def quit():
    if cv2.waitKey(10) & 0xFF == ord('q'):
        controller.quit()


while True:
    location, gesture = controller.process()

    print(location)
    print("Gesture: ", gesture)

    if gesture == QUIT:
        quit()
        break
