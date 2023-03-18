# %%
import numpy as np
import util
dst_path = "../instance/mask.png"
path = "../instance/20230305080541_1.mp4"
cap = util.ucv.UCapture(video_path=path)
ret, src_img = cap.read()
# 画像をリサイズ
src_img = util.ucv.resize(src_img, f=0.5)
mv = util.ucvmask.MaskView(dst_path=dst_path, src_img=src_img)
mv.start_draw()

# %%
