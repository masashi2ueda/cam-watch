# %%
import numpy as np
import util
dst_path = "../instance/mask.png"
src_img = np.zeros((600,600,3), np.uint8)
src_img[:, :, 1] = 100
mv = util.ucvmask.MaskView(dst_path=dst_path, src_img=src_img)
mv.start_draw()
