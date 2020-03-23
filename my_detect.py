# _*_ coding: utf-8 _*_
# -------------------------------------------
#  @description:  pose detect implement (video detect for test )
#  @author: hts
#  @data: 2020-03-23
#  @version: 1.0
#  @github: hutslib
# -------------------------------------------

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import os
import argparse
# from opt import opt
# import video_demo

parser = argparse.ArgumentParser()
parser.add_argument('--folder_path', default='/home/hts/Videos/202003video/', type=str,
                    help='video folder')
parser.add_argument('--result_folder', default='/home/hts/Videos/202003result_mpii/', type=str,
                    help='video folder')
args = parser.parse_args()
folder_path = args.folder_path
result_folder = args.result_folder
folders = os.listdir(folder_path)
#print(folders)
for foldername in folders:
    video_folder = folder_path + foldername
    result_path = result_folder + foldername
    print('\033[0;32;47m-------video_folder---------: %s \033[0m'  %video_folder)
    videos = os.listdir(video_folder)
    for video in videos:
        video_dir = video_folder + '/' + video
        print(video_dir)
        cmd = 'python3 video_demo.py --video ' +  video_dir + ' --outdir ' + result_path  + ' --save_video --dataset mpii --expID 1'
        # print(cmd)
        print('\033[0;32m start detect! %s \033[0m' %cmd)
        os.system(cmd)
        



