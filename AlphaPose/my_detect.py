# _*_ coding: utf-8 _*_
# -------------------------------------------
#  @description:  pose detect implement (video detect for test )
#  @author: hts
#  @data: 2020-03-23
#  @version: 1.0
#  @github: hutslib
# -------------------------------------------

import sys
# print(sys.path)
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    # print('!!!!')
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
# print(sys.path)
import os
import argparse
import cv2
from dataloader import VideoLoader
# import opt

# from opt import opt
# import video_demo

parser = argparse.ArgumentParser()
parser.add_argument('--folder_path', default='/home/hts/Videos/202003video/', type=str,
                    help='video folder')
# parser.add_argument('--folder_path', default='/home/hts/Videos/test/', type=str,
#                     help='video folder')                   
parser.add_argument('--pic_path', default='/home/hts/Pictures/04pic/',type=str,
                    help='pic save path')
parser.add_argument('--result_folder', default='/home/hts/Videos/04result/', type=str,
                    help='video folder')
parser.add_argument('--flow_folder', default='/home/hts/Videos/04flow/', type=str,
                    help='flow folder')
args = parser.parse_args()
folder_path = args.folder_path #/home/hts/Videos/test
pic_path = args.pic_path #/home/hts/Pictures/202003pic_Alphapose/
result_folder = args.result_folder #/home/hts/Videos/202003result_mpii/
flow_folder = args.flow_folder #/home/hts/Videos/202003flow/
folders = os.listdir(folder_path)
#print(folders)
for foldername in folders:
    video_folder = folder_path + foldername #/home/hts/Videos/test/a
    result_path = result_folder + foldername + '/' #/home/hts/Videos/202003result_mpii/a/
    flow_path = flow_folder + foldername + '/' #/home/hts/Videos/202003flow/a/
    print('\033[0;32;47m-------video_folder---------: %s \033[0m'  %video_folder)
    videos = os.listdir(video_folder)
    for video in videos:
        video_dir = video_folder + '/' + video #/home/hts/Videos/test/a/aaa
        videonames = os.listdir(video_dir)
        print(video_dir)
        for videoname in videonames:
            print(videoname) #/home/hts/Videos/test/a/aaa/IMG_aaa.avi
            # data_loader = VideoLoader(video_dir, batchSize=opt.detbatch).start()
            # (fourcc,fps,frameSize) = data_loader.videoinfo()
            cap = cv2.VideoCapture(video_dir + '/' + videoname)#函数创建一个对象cap
            # fps=cap.get(cv2.CAP_PROP_FPS)
            # print(fps)
            num = 0
            while True:
                success, frame = cap.read() # 按帧读取捕获的视频，第一个返回值为布尔值，表示帧读取是否正确，如果视频读取到结尾则返回False，第二个元素为读取到的帧。
                if success:
                    num += 1
                    if (num%10 ==0):
                        # print(num)
                        # print('suc')
                        # cv2.imshow('frame%d' %num, frame)
                        # print(video.split('.')[0])
                        # print(pic_path + foldername + '/pic%s%d.jpg' %(video.split('.')[0], num)) 
                        cv2.imwrite(pic_path + foldername + '/' + video + '/pic%s%d.jpg' %(videoname.split('.')[0], num), frame)
                        # print(pic_path + foldername + '/' + video + '/pic%s%d.jpg' %(videoname.split('.')[0], num))
                        #/home/hts/Pictures/202003pic_Alphapose/a/aaa/picIMG_aaa1.jpg
                else: 
                    break
                # if cv2.waitKey(5) == 27:
                    # break
            print('finish')
            cap.release() # 释放cap对象
            # cv2.destroyAllWindows() # 关闭所有窗口
#python3 demo.py --indir /home/hts/Desktop/kinect_test/a/aaa --outdir /home/hts/Desktop/kinect_result/a/aaa --save_img  --dataset mpii

        #/home/hts/Pictures/202003pic_Alphapose/a/aaa #/home/hts/Videos/202003result_mpii/a/aaa 
        cmd = 'python3 demo.py --indir ' +  pic_path + foldername + '/' + video  + ' --outdir ' + result_path  + video + ' --dataset mpii --expID 1 --save_img'
        print('\033[0;32m start detect! %s \033[0m' %cmd)
        os.chdir('/home/hts/AlphaPose')
        os.system(cmd)
        # print(cmd)
        os.chdir('PoseFlow')
          #/home/hts/Pictures/202003pic_Alphapose/a/aaa #/home/hts/Videos/202003result_mpii/a/aaa/alphapose-results_.json #/home/hts/Videos/202003result_mpii/a/aaa/alphapose-results-forvis-tracked.json  #/home/hts/Videos/202003flow/a/aaa
        cmd = 'python tracker-general.py --imgdir ' + pic_path + foldername + '/' + video + ' --in_json ' + result_path  + video + '/alphapose-results_.json' + ' --out_json ' + result_path + video + '/alphapose-results-forvis-tracked.json' + ' --visdir ' + flow_path + video
        # print(cmd)
        print('\033[0;32m start pose flow! %s \033[0m' %cmd)
        os.system(cmd)
        



