# %%
import util
import matplotlib.pyplot as plt
import numpy as np
import cv2
# %%
src_path = "../instance/20230305080541.mp4"
dst_path = "../instance/20230305080541_1.mp4"
util.ucv.change_fps(src_path, dst_path, 1)

# %%
