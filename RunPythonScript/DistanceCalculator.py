import cv2
import numpy as np

def find_marker(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    c = max(contours, key = cv2.contourArea)
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

KNOWN_WIDTH = 8.5  # Width in inches (e.g., A4 paper width)
KNOWN_DISTANCE = 24.0  # Distance in inches

# Initialize webcam
cap = cv2.VideoCapture(0)

# Calibration
ret, frame = cap.read()
if not ret:
    print("Failed to grab frame for calibration.")
    cap.release()
    exit()
marker = find_marker(frame)
if marker is None:
    print("Calibration object not detected.")
    cap.release()
    exit()
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

while True:
    ret, frame = cap.read()
    if not ret:
        break
    marker = find_marker(frame)
    if marker:
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        box = cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv2.putText(frame, f"{inches:.2f}in", (frame.shape[1] - 200, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.imshow("Distance Measurement", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
