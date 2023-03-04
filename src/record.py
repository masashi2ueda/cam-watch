# %%
import util
import os
# %%
end_min = 10 / 60
print("cap...")
cap = util.ucv.UCapture()
print("ok")
print("set fps...")
cap.set_fps(30)
print("ok")
for i in range(3):
    filepath = f'../instance/{util.utime.get_nowdt_forfile()}.mp4'
    print(filepath)
    dir_name = os.path.dirname(filepath)
    os.makedirs(dir_name, exist_ok=True)
    print("set writer...")
    writer = util.ucv.UVideoWriter(filepath, cap)
    print("ok")
    ut = util.utime.Utime()
    ut.start()
    print("recording...")
    while(True):
        ret, img = cap.read()
        writer.write(img)
        if end_min < ut.get_now_min():
            break
    print("ok")
    del writer
    print("end")
del cap
# %%
