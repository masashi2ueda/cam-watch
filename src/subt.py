# %%
import util
import matplotlib.pyplot as plt
import numpy as np
import cv2
# %%
target_mask_path = "../instance/mask.png"
target_mask = cv2.imread(target_mask_path, cv2.IMREAD_GRAYSCALE)
path = "../instance/20230305080541_1.mp4"
cap = util.ucv.UCapture(video_path=path)
w, h = cap.get_frame_width_height()
cap.set_pos_sec(6*60+20)
prev_frame = None
mask_th = 50
count_th = 400
is_show = False
diff_cnts = []
diff_triggers = []
for i in range(100):
    ret, frame = cap.read()
    # 画像をグレイスケール
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 画像をリサイズ
    frame = util.ucv.resize(frame, f=0.5)
    # 前の画像がないなら今回を
    if prev_frame is None:
        prev_frame = frame.copy()
    if is_show:
        cv2.imshow('frame', frame)
        cv2.imshow('prev_frame', prev_frame)
    diff_trigger, diff_cnt = util.ucv.get_diff(frame, prev_frame, target_mask, mask_th, count_th, is_show=False)
    print(diff_cnt)
    diff_cnts.append(diff_cnt)
    diff_triggers.append(diff_trigger)
    if not ret:
        break
    prev_frame = frame.copy()
    if is_show:
        cv2.waitKey(0)
# %%
plt.plot(diff_cnts)
# %%
#     for i in range(2):
#         cv2.imshow(f'frames[{i}]', frames[i, :, :])
#     cv2.imshow(f'mask1', mask1)
#     # cv2.imshow(f'mask2', mask2)
#     mask2[mask2 < th] = 0
#     mask2[mask2 >= th] = 255
#     cv2.imshow(f'mask1th', mask1)
#     # cv2.imshow(f'mask2th', mask2)
#     cv2.waitKey(0)
# cap.release()  
# cv2.destroyAllWindows()
# # %%
# # for i in range(1000):
# ret, img = cap.read()
# cv2.imshow('mouse_drawing',img)
# time.sleep(slp)
# # cv2.destroyAllWindows()
# %%
