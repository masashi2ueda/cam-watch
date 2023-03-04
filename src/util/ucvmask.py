import cv2
import numpy as np
import matplotlib.pyplot as plt
class MaskView:
    def __init__(
            self,
            dst_path,
            src_img_path=None,
            src_img=None) -> None:
        self.dst_path = dst_path
        self.points = np.array([[0, 0], [10, 0], [10, 10], [0, 10]])
        self.view_img = None
        if src_img is not None:
            self.view_img = src_img.copy()
        self.org_img = self.view_img.copy()
        self.pi = 0
        self.draw_polygon()
    def draw_polygon(self):
        self.view_img[:, :, :] = self.org_img
        cv2.polylines(self.view_img, [self.points], True, color=(255, 0, 0))
    def save_mask(self):
        w, h, _ = self.view_img.shape
        dst_img = np.zeros((w, h))
        cv2.fillConvexPoly(dst_img, self.points, color=(255))
        plt.imshow(dst_img, cmap="gray")
        plt.pause(0.1)
        plt.close()
        cv2.imwrite(self.dst_path, dst_img)

    def update_points(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points[self.pi] = [x, y]
            self.draw_polygon()
            self.pi+=1
            if self.pi == 4:
                self.pi = 0
    def start_draw(self):
        cv2.namedWindow(winname='mouse_drawing')
        cv2.setMouseCallback('mouse_drawing',self.update_points)
        while True:
            cv2.imshow('mouse_drawing',self.view_img)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        self.save_mask()