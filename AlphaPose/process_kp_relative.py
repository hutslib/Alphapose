# _*_ coding: utf-8 _*_
# -------------------------------------------
#  @description: process keypoint and calculate frquency 
#  @author: hts
#  @data: 2020-03-25
#  @version: 1.0
#  @github: hutslib
# -------------------------------------------
import json
import os
import sys
import argparse
import numpy as np



# "picIMG_aaa1120.jpg": [{"keypoints": [133.2736358642578, 204.3765411376953, 0.8725109100341797, 200.28384399414062, 
# 208.84388732910156, 0.7072502970695496, 267.2940673828125, 213.3112335205078, 0.6668407917022705, 262.82672119140625, 
# 249.0500030517578, 0.7156121730804443, 173.47976684570312, 249.0500030517578, 0.7506511211395264, 84.13284301757812, 
# 240.1153106689453, 0.5469750761985779, 267.2940673828125, 231.1806182861328, 0.7646099925041199, 405.78179931640625,
#  235.64796447753906, 0.7208899855613708, 423.65118408203125, 235.64796447753906, 0.787325382232666, 486.1940002441406,
#   235.64796447753906, 0.847907543182373, 325.36956787109375, 186.5071563720703, 0.5204940438270569, 356.6409912109375,
#    208.84388732910156, 0.44285374879837036, 401.314453125, 208.84388732910156, 0.676399827003479, 401.314453125, 
#    262.4520568847656, 0.7071422338485718, 329.8369140625, 266.9194030761719, 0.7833027839660645, 320.9022216796875,
#     208.84388732910156, 0.7903297543525696], "scores": 2.6284847259521484, "idx": 1}], 

class process_date:
    def __init__(self, folder_path, write_path):
        #/home/hts/Videos/202003result_mpii
        self.folder_path  = folder_path
        self.write_path = write_path
        labels = os.listdir(self.folder_path) #label = a
        for self.label in labels: 
            #/home/hts/Videos/202003result_mpii/a
            self.folder_dir = self.folder_path + self.label
            # print(self.folder_dir)
            print('\033[0;32;47m      foldername        :%s \033[0m'  %self.folder_dir)
            self.write_dir = self.write_path + self.label + '/keypoints.txt'
            names = os.listdir(self.folder_dir) # aaa
            # print(names)
            for self.name in names:
                #/home/hts/Videos/202003result_mpii/a/aaa/alphapose-results-forvis-tracked.json
                self.json_path = self.folder_dir + '/' + self.name + '/alphapose-results-forvis-tracked.json'
                self.output()


    def output(self):
        fileJson = open(self.json_path,'rb')
        fileJson = json.load(fileJson)
        print('\033[1;45m                fileJson length                :%d \033[0m' %len(fileJson))
        for key in fileJson:
            pic = fileJson[key]
            print('\033[0;32m person number in pic: %d \033[0m' %len(pic))
            suc_detect = False
            self.pose_keypoints_2d = np.zeros((1,32),dtype = float)
            for person in pic:
                my_kp = []
                keypoints = person['keypoints']
                if len(keypoints) != 48:
                     print('\033[0;36m  erro   %s\033[0m' %key)
                else:
                    suc_detect = True
                    for index in range(len(keypoints)):
                        # print (index)
                        if (index+1)%3 != 0:
                            my_kp.append(keypoints[index])
                            # print(index)
                    self.pose_keypoints_2d = np.insert(self.pose_keypoints_2d, 0, my_kp, axis=0)
                    print('suc   %s' %key)
            self.pose_keypoints_2d = np.delete(self.pose_keypoints_2d, -1, axis=0)
            if suc_detect == True:
                # print(self.pose_keypoints_2d)
                with open(self.write_dir, 'a') as file:
                        for p in range(len(self.pose_keypoints_2d)):
                            for index in range(len(self.pose_keypoints_2d[p])):
                                file.write(str(self.pose_keypoints_2d[p][index]))
                                file.write('\n')
                            file.write(self.name + self.label + '\n')
                file.close()

                
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", type=str, default='/home/hts/Videos/wenbin_result/',
                        help="path to the folder for the json to be processed (default: None)")
    parser.add_argument("--write_path", type=str, default='/home/hts/Videos/wenbin_keypoints/',
                        help="path to the folder for the results to be saved (default: None)")
    parser.add_argument("--label", type=str, default=None,
                        help="label (default: None)")
    args = parser.parse_args()
    folder_path = args.folder_path
    write_path = args.write_path
    label = args.label

    process_date(folder_path, write_path)
    # process_date(r'/home/hts/hts2019/openpose/Res/','/home/hts/hts2019/openpose/keypoints.txt')            
    # path = r'/home/hts/hts2019/openpose/Res/01_keypoints.json'
    # output()