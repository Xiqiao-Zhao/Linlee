import math

import cv2
import numpy as np
import win32api
import win32con
# 图片路径
file_path = './test/片1 左正10V_000007.jpg'  #修改为本次实验的中的任意一张图像路径，从而获得这次实验的pixelDistance
img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
a = []
b = []


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)
        # print(x, y)
    if len(a)==2:
        win32api.keybd_event(16, 0, 0, 0)  # shift
        win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(81, 0, 0, 0)  # Q
        win32api.keybd_event(81, 0, win32con.KEYEVENTF_KEYUP, 0)


cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)

length = math.sqrt((a[0]-a[1])**2+(b[0]-b[1])**2)
print(length)
