import time
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

pr_time = 0
cur_time = 0

while True:
    # get the image from the video capture
    success, image = cap.read()

    # get the rgb image for processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # get the result from the image
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        # iterate through the hands detected
        for hand in results.multi_hand_landmarks:
            # display the hand tracking for one hand
            mp_draw.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

    cur_time = time.time()
    fps = 1/(cur_time - pr_time)
    pr_time = cur_time

    # displaying the current fps
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)