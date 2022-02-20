import cv2
import time
import math
from modules import handtrackingmodule as htm
import numpy as np
import platform

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F')

# remember to remove this information before making commit
login = ['charlesliu688@gmail.com', 'letsgospurs']

email_form = driver.find_element(By.ID, 'login-username')
email_form.send_keys(login[0])

password_form = driver.find_element(By.ID, 'login-password')
password_form.send_keys(login[1])

driver.find_element(By.ID, 'login-button').click()
#
# import urllib.request
# import cv2 as cv # Please install with PIP: pip install cv2
# import numpy as np
#
# frame = None
# key = None
#
# print('START')
# while True:
#   imgResponse = urllib.request.urlopen ('http://192.168.1.68/capture?')
#   imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
#   frame= cv.imdecode (imgNp,-1)
#   cv.imshow('Window',frame)
#   key = cv.waitKey(10)
#   if key == (ord('q')):
#     break
# cv.destroyAllWindows()

# getting the operating system
os_name = platform.system()

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

cap = cv2.VideoCapture(0)
cam_width, cam_height = 640, 480
cap.set(3, cam_width)
cap.set(4, cam_height)

tracker = htm.HandTracker()

def main():
    previous_time = 0
    previous_location = [0, 0]

    action_time = 0
    previous_action = ""
    time_since_action = 0
    action_done_once = False

    action = ""

    while True:
        # get the image from the video capture
        success, image = cap.read()

        cur_time = time.time()
        cv2.imshow("Image", image)
        cv2.waitKey(1)

        if action == "":
            print("No action")
        elif action == "play":
            play_button = driver.find_element(By.CLASS_NAME, 'A8NeSZBojOQuVvK4l1pS')
            if play_button.get_dom_attribute('aria-label') == 'Play':
                play_button.click()
        elif action == "pause":
            play_button = driver.find_element(By.CLASS_NAME, 'A8NeSZBojOQuVvK4l1pS')
            if play_button.get_dom_attribute('aria-label') == 'Pause':
                play_button.click()
        elif action == "next":
            driver.find_element(By.CLASS_NAME, 'ARtnAVxkbmzyEjniZXVO').click()
        elif action == "previous":
            driver.find_element(By.CLASS_NAME, "FKTganvAaWqgK6MUhbkx").click()
        elif action == "like":
            like_button = driver.find_element(By.CLASS_NAME, "Fm7C3gdh5Lsc9qSXrQwO")
            if like_button.get_dom_attribute('aria-checked') == 'false':
                like_button.click()
        elif action == "unlike":
            like_button = driver.find_element(By.CLASS_NAME, "Fm7C3gdh5Lsc9qSXrQwO")
            if like_button.get_dom_attribute('aria-checked') == 'true':
                like_button.click()
        elif action == "repeat":
            driver.find_element(By.CLASS_NAME, "bQY5A9SJfdFiEvBMM6J5").click()
        elif action == "shuffle":
            driver.find_element(By.CLASS_NAME, "d4u88Fc9OM6kXh7FYYRj").click()

        # getting the image from the tracker
        image = tracker.find_hands(image)
        landmarks = tracker.get_landmarks(image)

        # if no hand is detected
        if len(landmarks) == 0: 
            continue

        # getting the finger orientations 
        thumb = tracker.get_finger_orientation(image, 0)
        index_finger = tracker.get_finger_orientation(image, 1)
        middle_finger = tracker.get_finger_orientation(image, 2)
        ring_finger = tracker.get_finger_orientation(image, 3)
        pinky_finger = tracker.get_finger_orientation(image, 4)

        # playing and pausing tracks
        if index_finger == 1 and thumb + middle_finger + ring_finger + pinky_finger == 0:
            if previous_action != "play":
                action = "play"
                previous_action = "play"
                time.sleep(3)
            else:
                action = "pause"
                previous_action = "pause"
                time.sleep(3)
            continue

        # skipping tracks
        # detecting hand motion to right and left while fist closed
        if cur_time - previous_time > 0.4 and thumb + index_finger + middle_finger == 3 and ring_finger + pinky_finger == 0:
            if previous_action == "next" or previous_action == "previous":
                action = ""
                previous_action = ""
                time.sleep(1)
                continue

            # getting the current  location
            x1, y1 = landmarks[5][1], landmarks[5][2]

            if cur_time - previous_time > 1:
                previous_time = cur_time
                previous_location = [x1, y1]
                continue

            delta_x = x1 - previous_location[0]
            delta_y = y1 - previous_location[1]

            action = findAction(cam_width, cam_height, delta_x, delta_y)
            previous_action = action

            # updating the previous locations
            previous_location = [x1, y1]
            previous_time = 0
            continue

        # thumbs up and down
        if thumb == 1 and index_finger + ring_finger == 0:
            if landmarks[4][2] < landmarks[9][2]:
                if previous_action != "like":
                    previous_action = "like"
                    action_done_once = False
                    time_since_action = 0
                    action_time = cur_time

                if cur_time - action_time > 0.5:
                    time_since_action += 0.5
                    action_time = cur_time
                if not action_done_once and time_since_action >= 1:
                    action_done_once = True
                    time_since_action = 0
                    action = "like"
                elif action_done_once and time_since_action >= 3.0:
                    time_since_action = 0
                    action = "like"
                else: 
                    action = ""
            else:
                if previous_action != "unlike":
                    previous_action = "unlike"
                    action_done_once = False
                    time_since_action = 0
                    action_time = cur_time

                if cur_time - action_time > 0.5:
                    time_since_action += 0.5
                    action_time = cur_time
                if not action_done_once and time_since_action >= 1:
                    action_done_once = True
                    time_since_action = 0
                    action = "unlike"
                elif action_done_once and time_since_action >= 3.0:
                    time_since_action = 0
                    action = "unlike"
                else:
                    action = ""
            continue

        # controlling the volume 
        if thumb + index_finger == 2 and middle_finger + ring_finger + pinky_finger == 0:
            # finding the length between the wrist and the fingers to use as reference distance
            referenceLength = tracker.get_distance(0, 5)

            # finding the length of the line between the thumb and index finger tip
            length = tracker.get_distance(4, 8)

            action = "volume"

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
            else:
                action = ""
            continue
        
        # the shuffle gesture
        if thumb + index_finger + pinky_finger == 3 and middle_finger + ring_finger == 0:

            if previous_action != "shuffle":
                previous_action = "shuffle"
                action_done_once = False
                time_since_action = 0
                action_time = cur_time

            if cur_time - action_time > 0.5:
                time_since_action += 0.5
                action_time = cur_time
            if not action_done_once and time_since_action >= 1:
                action_done_once = True
                time_since_action = 0
                action = "shuffle"
            elif action_done_once and time_since_action >= 3.0:
                time_since_action = 0
                action = "shuffle"
            else:
                action = ""

        # the repeat gesture
        if thumb + index_finger + middle_finger + ring_finger + pinky_finger == 5:
            # using the distance between thumb begin and middle finger
            reference_length = tracker.get_distance(2, 5)
            length = tracker.get_distance(4, 12)
            # if the distance is within thirty, then it is the repeat gesture
            if abs(length - reference_length) < 30:

                if previous_action != "repeat":
                    previous_action = "repeat"
                    action_done_once = False
                    time_since_action = 0
                    action_time = cur_time

                if cur_time - action_time > 0.5:
                    time_since_action += 0.5
                    action_time = cur_time
                if not action_done_once and time_since_action >= 1:
                    action_done_once = True
                    time_since_action = 0
                    action = "repeat"
                elif action_done_once and time_since_action >= 3.0:
                    time_since_action = 0
                    action = "repeat"
                else:
                    action = ""



def findAction(cam_w, cam_h, delta_x_, delta_y_):
    """Compute the net change in x and y coords to
    determine which overall direction the motion went in.
    Also, determine which quadrant this delta belongs to, thereby
    finding the associated motion."""

    if delta_x_ != 0:
        theta_a = math.degrees(math.atan(delta_y_ / delta_x_))

    if delta_y_ > 0 and delta_x_ != 0:
        theta_ref = math.degrees(math.atan(cam_h / cam_w))
    else:
        theta_ref = math.degrees(math.atan(-cam_h / cam_w))

    if delta_x_ != 0:
        print("theta_a: ", theta_a)
        print("theta_ref: ", theta_ref)

    action = ""

    # the action are flipped because the delta x and y are flipped on the camera
    # such that the user get the right coordinates sent to the processing below.

    if abs(delta_x_) < 200 and abs(delta_y_) < 200:
        return action
    
    if delta_x_ > 0:
        action = "next" 
    elif delta_x_ < 0:
        action = "previous"

    # # quadrant I of the trig circle
    # if delta_y_ > 0 and delta_x_ > 0:
    #     if 0 < theta_a < theta_ref:
    #         action = "Play Next Song"
    #     elif 0 < theta_ref < theta_a:
    #         action = "Pause Song"

    # # quadrant II of the trig circle
    # if delta_y_ > 0 and delta_x_ < 0:
    #     if 0 > theta_a > theta_ref:
    #         action = "Play Previous Song"
    #     elif 0 > theta_ref > theta_a or theta_ref > 0 > theta_a:
    #         action = "Pause Song"

    # # quadrant III of the trig circle
    # if delta_y_ < 0 and delta_x_ < 0:
    #     if 0 > theta_a > theta_ref or (theta_a > 0 and theta_ref < 0):
    #         action = "Play Previous Song"
    #     elif 0 > theta_ref > theta_a:
    #         action = "Resume Song"

    # # quadrant IV of the trig circle
    # if delta_y_ < 0 and delta_x_ > 0:
    #     if 0 > theta_a > theta_ref:
    #         action = "Play Next Song"
    #     elif 0 > theta_ref > theta_a:
    #         action = "Resume Song"

    return action

if __name__ == "__main__": 
    main()