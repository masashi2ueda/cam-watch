# %%
import cv2

cap = cv2.VideoCapture(0)
filepath = 'test.mp4'

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS)) # フレームレート

codec = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(filepath, codec, fps, (w, h))


for i in range(100):
# while(True):
    # カメラから映像を１枚読込む
    ret, img = cap.read()

    # カメラから読込んだ映像をファイルに書き込む
    video.write(img)

    # カメラから読み込んだ映像を画面に表示する
    cv2.imshow('frame', img)

    # # エスケープキーが押されたら処理終了
    # if cv2.waitKey(1) & 0xFF == 27:
    #     break

# Videoを作成時には、開放処理が必要
video.release()
# カメラを使った処理には開放粗利が必要
cap.release()
# Windowを開いた場合は閉じる処理が必要
cv2.destroyAllWindows()

# %%
