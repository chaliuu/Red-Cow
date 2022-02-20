import cv2
import mediapipe as mp
import math


class HandTracker():
    def __init__(self, static_image_mode=False, max_num_hands=2, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.num_hands = max_num_hands
        self.complexity = model_complexity
        self.detection_confidence = min_detection_confidence
        self.tracking_confidence = min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.num_hands, self.complexity, self.detection_confidence, self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, image, draw=False):
        # get the rgb image for processing
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get the result from the image
        self.results = self.hands.process(rgb_image)

        if self.results.multi_hand_landmarks:
            # iterating through the hands detected
            for hand in self.results.multi_hand_landmarks:
                # if draw is true, display the hand tracking for the hand
                if draw:
                    self.mp_draw.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS)
        return image

    def get_landmarks(self, image, hand_num=0, draw=False):
        self.landmarks = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_num]
            # iterating through the landmarks in each hand
            for id, lm in enumerate(hand.landmark):
                # getting the dimensions of the image capture
                height, width, channel = image.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                self.landmarks.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

        return self.landmarks

    def get_distance(self, image, p1, p2, hand_num=0, draw=False):
        if len(self.landmarks) == 0: 
            return 0

        # getting the x and y of the landmarks 
        x1, y1 = self.landmarks[p1][1], self.landmarks[p1][2]
        x2, y2 = self.landmarks[p2][1], self.landmarks[p2][2]

        # use math to find the distance 
        return math.hypot(x2 - x1, y2 - y1)

    # returns 1 if the finger is up and 0 if the finger is down
    def get_finger_orientation(self, image, finger=0, hand_num=0):
        
        if len(self.landmarks) == 0: 
            return -1

        # finger must be from 0 - 4
        if finger >= 0 and finger < 5:
            # get the y value of the finger landmarks
            if finger == 0:
                finger_middle = 5
            else:
                finger_middle = finger * 4 + 2
            finger_tip = finger * 4 + 4

            wrist = 0

            if self.get_distance(image, finger_tip, wrist) < self.get_distance(image, finger_middle, wrist):
                return 0
            else:
                return 1


    def draw_landmark(self, image, p1):
        cv2.circle(image, (self.landmarks[p1][1], self.landmarks[p1][2]), 15, (255, 255, 255), cv2.FILLED)