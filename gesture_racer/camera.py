import cv2


class Camera:
    def __init__(self, index: int = 0, flip: bool = True):
        self.index = index
        self.flip = flip
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")

    def read(self):
        success, frame = self.cap.read()
        if not success:
            raise RuntimeError("Error: Camera read failed.")
        if self.flip:
            frame = cv2.flip(frame, 1)
        return frame

    def release(self):
        if self.cap:
            self.cap.release()