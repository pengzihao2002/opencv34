import cv2
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread

# 视频路径
video_path = "../video/original/height_shot/person/road.mp4"
# 全局变量，用于视频播放
is_playing = False
cap = None
pause = False
current_frame_pos = 0  # 当前播放的帧位置


# 视频播放函数
def play_video():
    global is_playing, cap , current_frame_pos ,pause
    # 创建一个窗口并设置允许调整大小
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    # 设置窗口大小 (宽度, 高度)
    cv2.resizeWindow('Video', 800, 600)
    # VideoCapture()接受一个参数，可以是整数类型的摄像头索引(0,1...),或视频路径
    cap = cv2.VideoCapture(video_path)
    # 检查视频是否打开成功
    if not cap.isOpened():
        return print("无法打开视频！")
    # 跳转到停止时的帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_pos)

    # 成功打开视频，循环读取视频帧
    while is_playing:
        # 没有按下暂停按钮
        if not pause:
            # 对VideoCapture对象使用read()
            # 返回ret（false或true，表示是否成功读取帧）和 frame（表示捕获的图像帧，一个表示图像的多维数组，如 NumPy 数组）
            ret, frame = cap.read()
            if not ret:
                print("无法读取视频帧")
                break

            # 显示当前帧
            cv2.imshow('Video', frame)
            current_frame_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)  # 保存当前帧位置
            
            # 每帧停留10毫秒，如果按下 'ESC' 键则退出
            if cv2.waitKey(10) & 0xFF == 27:
                is_playing = False
                break
        # 按下暂停按钮
        else:  
            cv2.waitKey(100)  # 保持窗口不关闭，等待下一个动作

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    
# 按下“开始播放”按钮时调用的函数
def start_video():
    global is_playing
    # 只有在没有播放时才能触发play_video()
    if not is_playing :
        is_playing = True
        # 使用线程来播放视频，以避免阻塞主GUI线程
        thread = Thread(target=play_video)
        thread.start()

# 按下“退出播放”按钮时调用的函数
def exit_video():
    # 重置所有设置
    global is_playing , pause ,current_frame_pos , cap
    is_playing = False
    pause = False
    current_frame_pos = 0
    if cap:
        cap.release()
    cv2.destroyAllWindows()


# 暂停播放视频
def pause_video():
    global pause
    # 只有在播放时才能暂停
    if is_playing:
        pause = not pause  # 切换暂停/继续播放

# 创建Tkinter窗口
def create_gui():
    root = tk.Tk()
    root.title("video_player")
    window_width = 250
    window_height = 250

    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的居中位置
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)

    # 设置窗口大小和位置（居中显示）
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.geometry(f"{window_width}x{window_height}")

    # 创建“开始播放”按钮
    start_button = ttk.Button(root, text="开始播放", command=start_video)
    start_button.pack(pady=10)

    # 创建“退出播放”按钮
    stop_button = ttk.Button(root, text="退出播放", command=exit_video)
    stop_button.pack(pady=10)

    # 创建“暂停/继续”按钮
    pause_button = ttk.Button(root, text="暂停/继续", command=pause_video)
    pause_button.pack(pady=10)

    # 启动Tkinter主循环
    root.mainloop()

# 执行程序
create_gui()
# 释放资源
if cap:
    cap.release()
cv2.destroyAllWindows()