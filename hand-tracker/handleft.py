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

previous_time = 0
previous_locations = []

while True:
    # get the image from the video capture
    success, image = cap.read()

    # getting the image from the tracker
    image = tracker.find_hands(image, True)
    landmarks = tracker.get_landmarks(image)

    if len(landmarks) > 0:
        # detect hand movement to the left
        tracker.draw_landmark(image, 5)
        if cur_time - previous_time > 0.1:
            knuckles = landmarks[5]
            previous_locations.append([previous_time, knuckles[1], knuckles[2]])
            if len(previous_locations) > 20:
                previous_locations.pop(0)
            print(previous_time)
            previous_time = cur_time


    cur_time = time.time()
    fps = 1 / (cur_time - pr_time)
    pr_time = cur_time

    # displaying the current fps
    cv2.putText(image, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)