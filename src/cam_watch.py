# %%
import util
import cv2

# %%
def save_video(cap, cap_min, cap_fps, dst_path):
    # 録画する場所
    writer = util.ucv.UVideoWriter(dst_path, cap, fps=cap_fps)
    # 撮影開始
    ut = util.utime.Utime()
    while True:
        # 画像を取得
        ret, frame = cap.read(cap_fps)
        writer.write(frame)
        # 録画終了
        if cap_min < ut.get_now_min():
            break
    del writer

# %%
# 動画を再生するかどうか
is_play = False
# 差分用のマスク画像を取得
mask_size = (320, 240)
target_mask_path = "../instance/mask.png"
target_mask = cv2.imread(target_mask_path, cv2.IMREAD_GRAYSCALE)
target_mask = util.ucv.resize(target_mask, sizewh=mask_size)
# カメラを準備
if is_play:
    cap = util.ucv.UCapture(video_path="../instance/20230305080541.mp4")
else:
    cap = util.ucv.UCapture(camera_id=0)
# 差分用の画像
prev_frame = None
# 途中を表示するかどうか
is_show = False
# 差分取得用のパラメータ
mask_th = 50
count_th = 50
# 差分の大きさはiirで常にとっている
iir_diff_cnt = 0
prev_iir_diff_cnt = 0
iir_a = 0.3
# トリガーの閾値
diff_trigger_th = 50
scale_trigger_th = 2
# 次のトリガーまでの時間
# next_trigger_wait_sec = 60 * 1
next_trigger_wait_sec = 5 * 1
trigget_ut = util.utime.Utime()
# 録画のパラメータ
rec_fps = 30
rec_fps = None
rec_min = 30 / 60
# 処理のfps
mask_fps = 3
if is_play:
    src_fps = cap.get_fps()
    next_frame_w = int(src_fps / mask_fps)
    now_frame = 11500
    is_show = True
# 各画像に対して
# while True:
for i in range(100):
    if is_play:
        now_frame += next_frame_w
        cap.set_pos_frame(now_frame)
    print("----------------", i)
    # 画像を取得
    ret, frame = cap.read(mask_fps)
    # 画像をグレイスケール
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 画像をリサイズ
    frame = util.ucv.resize(frame, sizewh=mask_size)
    # 前の画像がないなら今回をコピー
    if prev_frame is None:
        prev_frame = frame.copy()
    if is_show:
        cv2.imshow('frame', frame)
        cv2.imshow('prev_frame', prev_frame)
        if is_play:
            cv2.waitKey(0)
    # 差分を取得
    _, diff_cnt = util.ucv.get_diff(frame, prev_frame, target_mask, mask_th, count_th, is_show=False)
    iir_diff_cnt = iir_diff_cnt * (1-iir_a) + iir_a * diff_cnt
    diff_trigger = iir_diff_cnt - prev_iir_diff_cnt
    scale_trigger = 0 if prev_iir_diff_cnt == 0 else iir_diff_cnt / prev_iir_diff_cnt
    sec_from_last_trigger = trigget_ut.get_now_sec()
    print("diff_cnt:", diff_cnt)
    print("prev_iir_diff_cnt:", prev_iir_diff_cnt)
    print("iir_diff_cnt:", iir_diff_cnt)
    print("diff_trigger:", diff_trigger)
    print("diff_trigger_th:", diff_trigger_th)
    print("scale_trigger:", scale_trigger)
    print("scale_trigger_th:", scale_trigger_th)
    print("sec_from_last_trigger:", sec_from_last_trigger)
    print("next_trigger_wait_sec:", next_trigger_wait_sec)
    is_triggered = False
    if diff_trigger_th < diff_trigger and\
       scale_trigger_th < scale_trigger and \
       next_trigger_wait_sec < sec_from_last_trigger:
        print("---------------capture start"+util.utime.get_nowdt_forfile())
        rec_dst_path = f'../instance/{util.utime.get_nowdt_forfile()}.mp4'
        save_video(cap, rec_min, rec_fps, rec_dst_path)
        print("---------------capture end"+util.utime.get_nowdt_forfile())

        trigget_ut.start()
        is_triggered = True
    # 差分用画像を更新
    prev_frame = frame.copy()
    # iirを更新
    prev_iir_diff_cnt = max(iir_diff_cnt, 1)
    if is_triggered:
        prev_frame = None

# %%
