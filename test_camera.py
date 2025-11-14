# test_camera.py
import cv2

print("Test 1: VideoCapture(0)")
cap = cv2.VideoCapture(0)
print(f"  isOpened: {cap.isOpened()}")
ret, frame = cap.read()
print(f"  read: ret={ret}, frame={'OK' if frame is not None else 'None'}")
cap.release()

print("\nTest 2: VideoCapture(0, cv2.CAP_V4L2)")
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
print(f"  isOpened: {cap.isOpened()}")
ret, frame = cap.read()
print(f"  read: ret={ret}, frame={'OK' if frame is not None else 'None'}")
cap.release()

print("\nTest 3: VideoCapture('/dev/video0', cv2.CAP_V4L2)")
cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
print(f"  isOpened: {cap.isOpened()}")
ret, frame = cap.read()
print(f"  read: ret={ret}, frame={'OK' if frame is not None else 'None'}")
cap.release()