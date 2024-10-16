# 导入opencv模块
import cv2
import sys
import numpy as np
import time

# 加载图片 imread(src , [默认为1表示彩色图，0表示灰度图，-1表示Alpha通道])
img = cv2.imread('../images/original/logo.png', 1)
if img is None:
    sys.exit("图片读取失败")

# 创建窗口 imshow(窗口名，图片)
cv2.imshow('image', img)
# 0xFF 按位与，两个二进制都是1才是1，否则0，可以保留低8位，忽略高位信息
k = cv2.waitKey(0) & 0xFF
if k == 27:  # 按下ESC键
    cv2.destroyAllWindows()
elif k == ord('s'):  # 按下s键，保存在运行路径并退出
    #  Windows系统不允许在文件名中使用特殊字符，如 : 、/ 或 \等
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    cv2.imwrite(f"../images/processed/{timestamp}.png" , img)
    cv2.destroyAllWindows()
