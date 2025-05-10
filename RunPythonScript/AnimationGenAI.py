import cv2

cap = cv2.VideoCapture("VID_20241208_173007.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("abru_output.mp4", fourcc, cap.get(cv2.CAP_PROP_FPS),
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cartoon_frame = cv2.stylization(frame, sigma_s=150, sigma_r=0.25)
    out.write(cartoon_frame)

cap.release()
out.release()