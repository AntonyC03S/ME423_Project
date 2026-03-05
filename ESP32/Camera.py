import cv2

def open_any_camera(max_index=10):
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ok, frame = cap.read()
            if ok and frame is not None:
                print("Opened camera index:", i, frame.shape)
                return cap
            cap.release()
    raise RuntimeError("No camera opened. On Windows your iPhone won't appear unless you install Camo/EpocCam or similar.")

cap = open_any_camera()
while True:
    ok, frame = cap.read()
    if not ok:
        break
    cv2.imshow("feed", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()