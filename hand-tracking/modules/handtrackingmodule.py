import time
import cv2
import mediapipe as mp

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
        landmarks = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_num]
            # iterating through the landmarks in each hand
            for id, lm in enumerate(hand.landmark):
                # getting the dimensions of the image capture
                height, width, channel = image.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                landmarks.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

        return landmarks
