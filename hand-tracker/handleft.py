import cv2
import time
from modules import handtrackingmodule as htm
import math


def main():
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
                print(knuckles[1], knuckles[2])
                previous_locations.append([knuckles[1], knuckles[2]])
                print(previous_locations)
                if len(previous_locations) > 20:
                    previous_locations.pop(0)
                # delta_x = previous_locations[len(previous_locations) - 1][0] - previous_locations[0][0]
                # delta_y = previous_locations[len(previous_locations) - 1][1] - previous_locations[0][1]
                # print("delta_x: ", delta_x, "delta_y: ", delta_y)
                # print(previous_time)
                previous_time = cur_time

        cur_time = time.time()
        fps = 1 / (cur_time - pr_time)
        pr_time = cur_time

        # displaying the current fps
        cv2.putText(image, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(1)


def findAction(previous_locations_list, cam_w, cam_h):
    """Compute the net change in x and y coords to
    determine which overall direction the motion went in.
    Also, determine which quadrant this delta belongs to, thereby
    finding the associated motion."""

    delta_x = previous_locations_list[len(previous_locations_list) - 1][0] - previous_locations_list[0][0]
    delta_y = previous_locations_list[len(previous_locations_list) - 1][1] - previous_locations_list[0][1]

    theta_a = math.degrees(math.atan(delta_y / delta_x))

    if delta_y > 0:
        theta_ref = math.degrees(math.atan(cam_h / cam_w))
    else:
        theta_ref = math.degrees(math.atan(-cam_h / cam_w))

    print("theta_a: ", theta_a)
    print("theta_ref: ", theta_ref)

    action = ""

    # the action are flipped because the delta x and y are flipped on the camera
    # such that the user get the right coordinates sent to the processing below.

    # quadrant I of the trig circle
    if delta_y > 0 and delta_x > 0:
        print("Q1")
        if 0 < theta_a < theta_ref:
            action = "Play Previous Song"
        elif 0 < theta_ref < theta_a:
            action = "Pause Song"

    # quadrant II of the trig circle
    if delta_y > 0 and delta_x < 0:
        print("Q2")
        if 0 > theta_a > theta_ref:
            action = "Play Next Song"
        elif 0 > theta_ref > theta_a:
            action = "Pause Song"

    # quadrant III of the trig circle
    if delta_y < 0 and delta_x < 0:
        print("Q3")
        if 0 > theta_a > theta_ref:
            action = "Play Next Song"
        elif 0 > theta_ref > theta_a:
            action = "Resume Song"

    # quadrant IV of the trig circle
    if delta_y < 0 and delta_x > 0:
        print("Q4")
        if 0 > theta_a > theta_ref:
            action = "Play Previous Song"
        elif 0 > theta_ref > theta_a:
            action = "Resume Song"

    print("delta_x: ", delta_x, "delta_y: ", delta_y)
    print(action)
    return action

if __name__ == "__main__":
    prev = [[71, 375], [72, 375], [74, 375], [67, 403], [69, 393], [74, 375], [112, 352], [144, 306], [210, 280], [287, 221], [360, 167], [399, 146]]
    findAction(prev, 640, 480)
    # main()
