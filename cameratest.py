import cv2

cap = cv2.VideoCapture(0, cv2.CAP_VFW)


cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    ret, frame = cap.read()
    print("RET:", ret, "| FRAME:", None if frame is None else frame.shape)
