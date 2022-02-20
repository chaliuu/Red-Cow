import cv2
import time
import math
from modules import handtrackingmodule as htm
import numpy as np
import platform

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

        # checking if the middle, ring, and pinky fingers are down for volume control
        fingersdown = tracker.get_finger_orientation(image, 2) + tracker.get_finger_orientation(image, 3) + tracker.get_finger_orientation(image, 4)
        if fingersdown == 0:
            # finding the length between the wrist and the fingers to use as reference distance
            referenceLength = tracker.get_distance(image, 0, 5)

            # finding the length of the line between the thumb and index finger tip
            length = tracker.get_distance(image, 4, 8)

            if os_name == 'Darwin':
                # the maximum length is determined relative to the reference length
                min_length = 0.4 * referenceLength
                max_length = 1.3 * referenceLength

                # getting the volume by interpolating
                vol = np.interp(length, [min_length, max_length], [min_volume, max_volume])

                # set the volume on macOS system
                code, out, error = osascript.osascript(f'set volume output volume {int(vol)}')

            elif os_name == 'Windows':
                # the maximum length is determined relative to the reference length
                min_length = 0.2 * referenceLength
                max_length = 1.2 * referenceLength

                # getting the volume by interpolating
                vol = np.interp(length, [min_length, max_length], [min_volume, max_volume])

                # set the volume on Windows system
                volume.SetMasterVolumeLevel(vol, None)

    cur_time = time.time()
    fps = 1/(cur_time - pr_time)
    pr_time = cur_time

    # displaying the current fps
    cv2.putText(image, f'fps: {str(int(fps))}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow("Image", image)
    cv2.waitKey(1)