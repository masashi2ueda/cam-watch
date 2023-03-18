# %%
import cv2
import time
import numpy as np
from . import utime
# %%
def imshow(name, img):
    cv2.imshow(name, img)
def waitKey(msec):
    cv2.waitKey(msec)
def resize(img, sizewh=None, f=None, fx=None, fy=None):
    if sizewh is not None:
        dst_img = cv2.resize(img, sizewh)
    if f is not None:
        dst_img = cv2.resize(img, None, None, f, f)
    return dst_img
def destroyAllWindows():
    cv2.destroyAllWindows()
def get_diff(frame1, frame2, target_mask, mask_th, count_th, is_show=False):
    # マスクを生成
    mask = cv2.absdiff(frame1, frame2)
    if is_show:
        cv2.imshow('mask', mask)
    mask[mask < mask_th] = 0
    mask[mask >= mask_th] = 255
    if is_show:
        cv2.imshow('abs_mask', mask)
    mask[target_mask == 0] = 0
    if is_show:
        cv2.imshow('mask_abs_mask', mask)
    diff_cnt = len(np.where(mask == 255)[0])
    diff_trigger = count_th < diff_cnt
    return diff_trigger, diff_cnt
# %%
class UCapture:
    def __init__(self, video_path=None, camera_id=0):
        self.cap = None
        if video_path is None:
            self.cap = cv2.VideoCapture(camera_id)
        if video_path is not None:
            self.cap = cv2.VideoCapture(video_path)
        self.each_ut = utime.Utime()
        self.each_ut.start()
    def get_frame_width_height(self):
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (w, h)
    def get_fps(self):
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        return fps
    def set_fps(self, fps):
        self.cap.set(cv2.CAP_PROP_FPS, fps)
    def read(self, fps=None):
        # fpsが指定してあるなら、その分待つ
        if fps is not None:
            wait_sec = 1.0 / fps - self.each_ut.get_now_sec()
            if 0 < wait_sec:
                time.sleep(wait_sec)
        # 画像を読み込む
        ret, img = self.cap.read()
        # 次の画像への待ち時間
        self.each_ut.start()
        return ret, img
    def __del__(self):
        self.cap.release()
    def isOpened(self):
        return self.cap.isOpened()
    def release(self):
        self.cap.release()
    def set_pos_frame(self, frame):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame) 
    def set_pos_sec(self, sec):
        frame = int(sec*self.get_fps())
        self.set_pos_frame(frame)
    def get_total_frames(self):
        frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return frames
    def get_now_frame(self):
        frame_Num = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        return frame_Num

class UVideoWriter:
    def __init__(self, path, cap: UCapture=None, fps=None):
        if ".mp4" in path:
            codec = cv2.VideoWriter_fourcc(*'mp4v')
        if ".avi" in path:
            codec = cv2.VideoWriter_fourcc('H', '2', '6', '4')
        self.writer = None
        if cap is not None:
            fps = cap.get_fps() if fps is None else fps
            (w, h) = cap.get_frame_width_height()
            self.writer = cv2.VideoWriter(path, codec, fps, (w, h))
    def write(self, img):
        self.writer.write(img)
    def __del__(self):
        self.writer.release()

def change_fps(src_path, dst_path, dst_fps):
#     src_path = "../instance/20230305080541.mp4"
# dst_path = "../instance/20230305080541_10.mp4"
    cap = UCapture(video_path=src_path)
    writer = UVideoWriter(dst_path, cap, dst_fps)
    pos_frame = 0
    add_frame = cap.get_fps() / dst_fps
    while(True):
        cap.set_pos_frame(int(pos_frame))
        ret, frame = cap.read()
        if not ret:
            break
        pos_frame += add_frame
        writer.write(frame)
        # cv2.imshow(f'frame', frame)
        # cv2.waitKey(0)
    del writer, cap
    # cv2.destroyAllWindows()
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
