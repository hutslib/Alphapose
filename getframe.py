# -*- coding:UTF-8 -*-
import cv2
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--video_path', type = str, default = None,
                        help = "path to video (default: None)")
parser.add_argument('--save_path', type = str, default = '~/darknet/training/image',
                        help = 'path to save the picture (default:~/darknet/training/image)')
args = parser.parse_args()
video_path = args.video_path
save_path = args.save_path                       
cap = cv2.VideoCapture(video_path)#函数创建一个对象cap
num = 0
while True:
    success, frame = cap.read() # 按帧读取捕获的视频，第一个返回值为布尔值，表示帧读取是否正确，如果视频读取到结尾则返回False，第二个元素为读取到的帧。
    if success:
        num += 1
        #cv2.imshow('frame%d' %num, frame)
        cv2.imwrite(save_path + '/pic%d.jpg' % num, frame)
    else: 
        break
    if cv2.waitKey(5) == 27:
        break
print 'finish'
cap.release() # 释放cap对象
cv2.destroyAllWindows() # 关闭所有窗口