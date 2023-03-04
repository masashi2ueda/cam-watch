# %%
import util
# %%
filepath = 'test.mp4'
cap = util.ucv.UCapture()
cap.set_fps(10)
writer = util.ucv.UVideoWriter(filepath, cap)
ut = util.utime.Utime()
ut.start()
end_min = 0.5
while(True):
    ret, img = cap.read()
    writer.write(img)
    if end_min < ut.get_now_min():
        break
del cap, writer
# %%
