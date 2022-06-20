import cv2
import numpy as np
import pandas as pd
import win32api
import win32con
import os
import math

file_path = './test/片1 左正10V_000007.jpg'   #这行不用管
img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
a = []
b = []
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        # print(a)
        # print(b)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)

        # print(x, y)
    if event == cv2.EVENT_LBUTTONUP:
        if len(a)==1:
            win32api.keybd_event(16, 0, 0, 0)  # shift
            win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(81, 0, 0, 0)  # Q
        win32api.keybd_event(81, 0, win32con.KEYEVENTF_KEYUP, 0)

def key(path2img):
    imgLists = os.listdir(path2img)
    for imgList in imgLists:
        file_path = path2img+'/'+imgList+''
        img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
        cv2.imshow("image", img)
        cv2.waitKey(0)

def calculate(realWorldDistance,pixelDistance):
    result = []
    singlePixelLength = realWorldDistance/pixelDistance
    for i in range(1,len(a)):
        length = math.sqrt((a[i] - a[i-1]) ** 2 + (b[i] - b[i-1]) ** 2)
        result.append(length*singlePixelLength)
    return result
if __name__ == '__main__':

    imgPath = './test'  #图像所在的文件夹
    realWorldDistance = 40 #真实世界距离，单位为微米μm
    pixelDistance = 100 #由init.py计算的得到的像素距离
    pointNum = 5 #一次需要标记几个点
    finalResult = []

    for i in range(pointNum):
        a = []
        b = []
        key(imgPath)
        print(a)
        print(b)
        result = calculate(realWorldDistance,pixelDistance)
        win32api.keybd_event(16, 0, 0, 0)  # shift
        win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
        print(result)
        finalResult.append(result)
    print(finalResult)
    finalResultArray = np.array(finalResult)
    finalResultArrayT = np.transpose(finalResultArray)
    data = pd.DataFrame(finalResultArrayT)
    writer = pd.ExcelWriter('./result/' + imgPath + '.xlsx')  # 写入Excel文件
    data.to_excel(writer, 'page_1', float_format='%.5f')  # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()
    # print(a)
    # print(b)
