# %%
import cv2

# %%
class UCapture:
    def __init__(self, video_path = None):
        self.cap = None
        if video_path is None:
            self.cap = cv2.VideoCapture(0)
    def get_frame_width_height(self):
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (w, h)
    def get_fps(self):
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        return fps
    def set_fps(self, fps):
        self.cap.set(cv2.CAP_PROP_FPS, fps)
    def read(self):
        ret, img = self.cap.read()
        return ret, img
    def __del__(self):
        self.cap.release()
class UVideoWriter:
    def __init__(self, path, cap: UCapture=None):
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = None
        if cap is not None:
            fps = cap.get_fps()
            (w, h) = cap.get_frame_width_height()
            self.writer = cv2.VideoWriter(path, codec, fps, (w, h))
    def write(self, img):
        self.writer.write(img)
    def __del__(self):
        self.writer.release()


# %%
if __name__ == "__main__":
    filepath = 'test.mp4'
    cap = UCapture()
    writer = UVideoWriter(filepath, cap)
    for i in range(100):
        print(i)
        ret, img = cap.read()
        writer.write(img)
    del cap, writer
# %%
