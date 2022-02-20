import cv2
import time
import math
from modules import handtrackingmodule as htm
import platform
import numpy as np

# getting the operating system
os_name = platform.system()

# default
min_volume = 0
max_volume = 100 

# for changing volume in mac os
if os_name == 'Darwin':
    import osascript
    min_volume = 0
    max_volume = 100

# for changing volume in windows
if os_name == 'Windows':
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volume_range = volume.GetVolumeRange()
    min_volume = volume_range[0] + 10
    max_volume = volume_range[1]


cam_width, cam_height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

# instantiating the hand tracker
tracker = htm.HandTracker(min_detection_confidence=0.7)
pr_time = 0

while True:
    # getting the image capture
    success, image = cap.read()
    # finding the hand from the image
    tracker.find_hands(image, True)
    # getting the positions of the different landmarks
    landmarks = tracker.get_landmarks(image)

    if len(landmarks) > 0:
        # getting the positions of thumb and the index finger tips
        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]

        wrist_x, wrist_y = landmarks[0][1], landmarks[0][2]
        finger_begin_x, finger_begin_y = landmarks[5][1], landmarks[5][2]

        # finding the length between the wrist and the fingers to use as reference distance
        referenceLength = math.hypot(finger_begin_x - wrist_x, finger_begin_y - wrist_y)

        # finding the length of the line between the thumb and index finger tip
        length = math.hypot(x2 - x1, y2 - y1)
        # the maximum length is determined relative to the reference length
        min_length = 0.4 * referenceLength
        max_length = 1.3 * referenceLength

        print(min_length, max_length)

        # getting the volume by interpolating
        vol = np.interp(length, [min_length, max_length], [min_volume, max_volume])

        # set the volume by the os system
        if os_name == 'Darwin':
            code, out, error = osascript.osascript(f'set volume output volume {int(vol)}')

        if os_name == 'Windows':
            volume.SetMasterVolumeLevel(vol, None)

        cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 3)

    cur_time = time.time()
    fps = 1/(cur_time - pr_time)
    pr_time = cur_time

    # displaying the current fps
    cv2.putText(image, f'fps: {str(int(fps))}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow("Image", image)
    cv2.waitKey(1)