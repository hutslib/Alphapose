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
                # print(self.folder_dir)
                # print(self.name)
                # print(self.json_path)
                # self.write_path = self.write_path + self.name
                # array2 = np.zeros((1,33))
                # self.person_num = 0
                self.output()
            #     if self.output() == True:
            #         print ('ture')
            #         with open(self.write_path, 'a') as file:
            #             for index in range(len(self.pose_keypoints_2d)):
            #                 file.write(str(self.pose_keypoints_2d[index]))
            #                 file.write('\n')
            #             file.write(name + self.label + '\n')
            #         file.close()
            #         # self.person_id = -2  
            # print(self.counter)   
        



    def output(self):
        fileJson = open(self.json_path,'rb')
        fileJson = json.load(fileJson)
        print('\033[1;45m                fileJson length                :%d \033[0m' %len(fileJson))
        for key in fileJson:
            pic = fileJson[key]
        #     print(pic)
        # for i in range (len(fileJson)):
            # pic = fileJson['picIMG_%s%d.jpg' %(self.name, (i+1)*10)]
            # print(pic)
            print('\033[0;32m person number in pic: %d \033[0m' %len(pic))
            suc_detect = False
            self.pose_keypoints_2d = np.zeros((1,48))
            for person in pic:
                # print(person)
                keypoints = person['keypoints']
                # print(keypoints)
                # if suc_detect: 
                # print('pose_keypoints_2d length %d' %len(keypoints))            
                if len(keypoints) != 48:
                     print('\033[0;36m erro   %s\033[0m' %key)
                else:
                    suc_detect = True
                    self.pose_keypoints_2d = np.insert(self.pose_keypoints_2d, 0, keypoints, axis=0)
                    print('suc   %s' %key)
                # else:
                #     # print(self.pose_keypoints_2d)
                #     self.pose_keypoints_2d = np.insert(self.pose_keypoints_2d, 0, keypoints, axis=0)
                #     print('suc%s%d' %(self.name, i))
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

                
            


    # def resolveJson(self, pic_id):
    #     fileJson = open(self.json_path,'rb')
    #     #print(self.json_path)
    #     fileJson = json.load(fileJson)
    #     pic = fileJson[pic_id]
    #     # people = fileJson["people"]
    # #    person_id = fileJson["person_id"]
    # #    pose_keypoints_2d = fileJson["pose_keypoints_2d"]
    #     return (fileJson)

    # def output(self):
    #     fileJson = open(self.json_path,'rb')
    #     fileJson = json.load(fileJson)
    #     print(len(fileJson))
    #     count = 0
    #     for i in range (len(filejson)):
    #         count = count + 1 
    #         if count % 10 == 0 :
    #         pic = fileJson["picIMG_aaa%d.jpg" %(i=1)*10]
    #         for person in len(pic)


    #     # pic = self.resolveJson()
    #     # print(result)
    #     for person in People:
            
            
    #         # print(type(person))
    #         # self.person_id = person['person_id']
    #         #self.person_num += 1
    #         count = 0
    #         self.pose_keypoints_2d = person['pose_keypoints_2d']
    #         print(self.pose_keypoints_2d)
    #         for index in range(len(self.pose_keypoints_2d)):
    #             if self.pose_keypoints_2d[index] == 0:
    #                 self.counter[index] += 1
    #         self.pose_keypoints_2d = [self.pose_keypoints_2d[index] for index in range(len(self.pose_keypoints_2d)) if self.pose_keypoints_2d[index] != 0 and index in self.key_point]
    #         print(self.pose_keypoints_2d)
    #         print(len(self.pose_keypoints_2d))
    #         if len(self.pose_keypoints_2d) == 33:
    #             return True
    #         # for items, index in  self.pose_keypoints_2d:
    #         #     print (items, index)
    #         # #     if self.pose_keypoints_2d[items] parser.add_argument("-folder_path", type=str, default=None,
    #         # #         count += 1
    #         # #         self.pose_keypoints_2d.remove(0)
    #         # # print(count)
    #         # # print(len(self.pose_keypoints_2d))
    #         # # print(len(self.pose_keypoints_2d))
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", type=str, default='/home/hts/Videos/202003result_mpii/',
                        help="path to the folder for the json to be processed (default: None)")
    parser.add_argument("--write_path", type=str, default='/home/hts/Videos/202003keypoints/',
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