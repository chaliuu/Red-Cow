import cv2

cap = cv2.VideoCapture("outpy.avi")

for i in range(10):
  print(cap.set(4, 600))

for i in range(10):
  print(cap.set(4, 200))
# while cap.isOpened():
#   returnval, frame_i = cap.read()
#   cv2.imshow("Frame i", frame_i)
#
#   cv2.waitKey(1000)


while cap.isOpened():
  returnval, frame = cap.read()
  cv2.imshow("frame", frame)
  cv2.waitKey(1000)

cv2.destroyAllWindows()