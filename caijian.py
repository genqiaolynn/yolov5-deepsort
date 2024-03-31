import cv2

# 打开视频文件
cap = cv2.VideoCapture('video/1.mp4')

# 设置视频的起始时间（以秒为单位）
start_time = 2

# 设置需要截取的视频长度（以秒为单位）
duration = 8

# 将视频的帧率设置为每秒25帧
fps = 25

# 计算需要读取的帧数
frame_count = int(duration * fps)

# 设置视频的当前帧数
cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_time * fps))

# 逐帧读取视频，并将每一帧写入一个新的视频文件
out = cv2.VideoWriter('output_file.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))
for i in range(frame_count):
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)

# 释放资源
cap.release()
out.release()