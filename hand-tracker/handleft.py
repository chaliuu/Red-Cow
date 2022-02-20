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
            if (cur_time - previous_time) > 0.1:
                knuckles = landmarks[5]
                print(knuckles[1], knuckles[2])
                previous_locations.append([knuckles[1], knuckles[2]])
                print(previous_locations)
                if len(previous_locations) > 15:
                    previous_locations.pop(0)
                delta_x = previous_locations[len(previous_locations) - 1][0] - previous_locations[0][0]
                delta_y = previous_locations[len(previous_locations) - 1][1] - previous_locations[0][1]
                findAction(previous_locations, cam_width, cam_height, delta_x, delta_y)

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


def findAction(previous_locations_list, cam_w, cam_h, delta_x_, delta_y_):
    """Compute the net change in x and y coords to
    determine which overall direction the motion went in.
    Also, determine which quadrant this delta belongs to, thereby
    finding the associated motion."""

    # delta_x_ = previous_locations_list[len(previous_locations_list) - 1][0] - previous_locations_list[0][0]
    # delta_y_ = previous_locations_list[len(previous_locations_list) - 1][1] - previous_locations_list[0][1]

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

    # quadrant I of the trig circle
    if delta_y_ > 0 and delta_x_ > 0:
        print("Q1")
        if 0 < theta_a < theta_ref:
            action = "Play Next Song"
        elif 0 < theta_ref < theta_a:
            action = "Pause Song"

    # quadrant II of the trig circle
    if delta_y_ > 0 and delta_x_ < 0:
        print("Q2")
        if 0 > theta_a > theta_ref:
            action = "Play Previous Song"
        elif 0 > theta_ref > theta_a or theta_ref > 0 > theta_a:
            action = "Pause Song"

    # quadrant III of the trig circle
    if delta_y_ < 0 and delta_x_ < 0:
        print("Q3")
        if 0 > theta_a > theta_ref or (theta_a > 0 and theta_ref < 0):
            action = "Play Previous Song"
        elif 0 > theta_ref > theta_a:
            action = "Resume Song"

    # quadrant IV of the trig circle
    if delta_y_ < 0 and delta_x_ > 0:
        print("Q4")
        if 0 > theta_a > theta_ref:
            action = "Play Next Song"
        elif 0 > theta_ref > theta_a:
            action = "Resume Song"

    print("delta_x: ", delta_x_, "delta_y: ", delta_y_)
    print(action)
    # return action

if __name__ == "__main__":
    # downward motion – pause
    # prev = [[367, 29], [387, 80], [400, 192], [203, 8], [177, 6], [206, 115], [207, 229], [198, 270], [188, 322], [196, 465], [131, 78], [135, 133], [120, 239], [100, 278], [364, 183], [362, 324], [373, 352], [382, 427], [446, 240], [447, 274], [451, 348]]


    # rightward motion – play next
    # prev = [[336, 301], [382, 257], [390, 250], [409, 233], [422, 224], [446, 212], [450, 215], [451, 214], [457, 210], [467, 212], [9, 214], [36, 242], [134, 262], [203, 265], [355, 277], [535, 270], [620, 272], [101, 176], [265, 241], [405, 253], [479, 260]]


    # upward motion – resume
    # prev = [[407, 421], [283, 255], [286, 180], [302, 39], [189, 55], [141, 252], [368, 396], [372, 276], [391, 195], [398, 116], [397, 76], [380, 3], [339, 423], [337, 361], [372, 93], [375, 32]]

    # leftward motion – play previous song
    # prev = [[444, 369], [444, 369], [444, 370], [446, 370], [445, 367], [447, 369], [448, 368], [447, 368], [446, 367], [506, 223], [419, 222], [354, 234], [305, 245], [209, 246], [135, 234], [565, 297], [510, 281], [437, 279], [343, 270], [200, 250], [16, 239]]


    # findAction(prev, 640, 480)

    main()
