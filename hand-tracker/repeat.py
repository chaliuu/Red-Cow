import cv2
import time
from modules import handtrackingmodule as htm

cam_width, cam_height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

tracker = htm.HandTracker()
pr_time = 0
cur_time = 0

while True:
    # get the image from the video capture
    success, image = cap.read()

    # getting the image from the tracker
    image = tracker.find_hands(image, True)
    landmarks = tracker.get_landmarks(image)

    if len(landmarks) > 0:

        thumb = tracker.get_finger_orientation(image, 0)
        index_finger = tracker.get_finger_orientation(image, 1)
        middle_finger = tracker.get_finger_orientation(image, 2)
        ring_finger = tracker.get_finger_orientation(image, 3)
        pinky_finger = tracker.get_finger_orientation((image, 4))

        if thumb + index_finger + middle_finger + ring_finger + pinky_finger == 5:

            reference_length = tracker.get_distance(image, 2, 5)
            length = tracker.get_distance(image, 4, 12)

            if abs(length - reference_length) < 30:
                print('repeat shown')
            else: print('repeat not shown')
        else: print('repeat not shown')

    cur_time = time.time()
    fps = 1 / (cur_time - pr_time)
    pr_time = cur_time

    # displaying the current fps
    cv2.putText(image, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)