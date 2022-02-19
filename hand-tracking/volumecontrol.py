import sys
sys.path.append('/Users/yug/Documents/Red-Cow/hand-tracking/venv/lib/python3.8/site-packages')
import cv2
import time
import numpy as np

cam_width, cam_height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

pr_time = 0

while True:
    success, image = cap.read()

    cur_time = time.time()
    fps = 1/(cur_time - pr_time)
    pr_time = cur_time

    # displaying the current fps
    cv2.putText(image, f'fps: {str(int(fps))}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)