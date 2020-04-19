# _*_ coding: utf-8 _*_
# -------------------------------------------
#  @description: process keypoint 去掉概率
#  @author: hts
#  @data: 2020-03-27
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
# // Result for MPII (16 body parts)
#     {0,  "RAnkle"},012
#     {1,  "Rknee"},345
#     {2,  "RHip"},678
#     {3,  "LHip"},91011
#     {4,  "LKnee"},121314
#     {5,  "LAnkle"},151617
#     {6,  "Pelv"},181920 √
#     {7,  "Thrx"},212223
#     {8,  "Neck"},242526
#     {9,  "Head"},272829
#     {10, "RWrist"},303132
#     {11, "RElbow"},333435
#     {12, "RShoulder"},363738 √
#     {13, "LShoulder"},394041 √
#     {14, "LElbow"},424344
#     {15, "LWrist"},454647

# [{"image_id": "0291_color.jpg", "category_id": 1, "keypoints": [33.17881393432617, 354.4361572265625, 0.7169342637062073, 
# 134.62977600097656, 290.1838684082031, 0.7453361749649048, 215.79054260253906, 229.3132781982422, 0.7909862995147705, 
# 246.225830078125, 263.1302795410156, 0.7648909091949463, 175.2101593017578, 327.382568359375, 0.6899839043617249, 97.43109130859375,
#  405.1616516113281, 0.5119760036468506, 236.0807342529297, 242.84010314941406, 0.7178401350975037, 320.6231994628906, 
#  188.73289489746094, 0.8264297842979431, 327.3865966796875, 181.96949768066406, 0.7865035533905029, 351.0585021972656, 
#  158.29762268066406, 0.7973981499671936, 225.93563842773438, 225.9315948486328, 0.2525416314601898, 246.225830078125, 
#  205.64137268066406, 0.4038618803024292, 286.8062438964844, 168.4427032470703, 0.7751867175102234, 351.0585021972656, 
#  209.02308654785156, 0.8188015222549438, 337.5317077636719, 246.22178649902344, 0.7530956268310547, 310.4781188964844,
#   280.0387878417969, 0.8791655898094177], "score": 2.791717529296875, "box": [10.903332710266113, 142.2208709716797,
#    377.8199157714844, 393.4474182128906], "box_scores": 0.9908271431922913, "kp_box": [33.17881393432617, 158.29762268066406, 
#    351.0585021972656, 405.1616516113281], "kp_box_score": 0.6992118954658508, "fusion_box_score": 0.9960332720754077}, 
#    {"image_id": "0291_color.jpg", "category_id": 1, "keypoints": [500.3224792480469, 166.29916381835938, 0.028613438829779625,
#    507.3797607421875, 143.95118713378906, 0.017942780628800392, 506.2035217285156, 143.95118713378906, 0.006790915969759226, 
#    506.2035217285156, 115.72212982177734, 0.007657214067876339, 506.2035217285156, 142.77496337890625, 0.013821183703839779, 
#    501.4986877441406, 168.65158081054688, 0.031839512288570404, 507.3797607421875, 107.4886474609375, 0.01075571496039629, 
#    508.55596923828125, 147.4798126220703, 0.013604212552309036, 502.6748962402344, 61.616451263427734, 0.008271751925349236, 
#    502.6748962402344, 60.440242767333984, 0.01721283048391342, 507.3797607421875, 103.96002197265625, 0.137115478515625, 
#    506.2035217285156, 108.66486358642578, 0.3466193974018097, 505.0273132324219, 148.65602111816406, 0.007324235048145056, 
#    505.0273132324219, 107.4886474609375, 0.008744829334318638, 507.3797607421875, 111.01728057861328, 0.07110585272312164,
#     508.55596923828125, 106.31243896484375, 0.09871666878461838], "score": 0.5438540577888489, "box": [503.4945068359375, 
#     39.05272674560547, 511.8427734375, 183.81707763671875], "box_scores": 0.05894629657268524, "kp_box": [500.3224792480469, 
#     60.440242767333984, 508.55596923828125, 168.65158081054688], "kp_box_score": 0.06228318810462952, "fusion_box_score": 0.004143221322060488}]
class process_date:
    def __init__(self, folder_path, write_path):
        #/home/hts/Videos/202003result_mpii
        self.folder_path  = folder_path
        self.write_path = write_path
        # self.key_points = [3,4,6,7,9,10,12,13,18,19,24,25,27,28,33,34,36,37,39,40,42,43]
        self.key_points = [18,19,36,37,39,40]
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
                self.json_path = self.folder_dir + '/' + self.name + '/alphapose-results_.json'
                self.output()


    def output(self):
        fileJson = open(self.json_path,'rb')
        fileJson = json.load(fileJson)
        print('\033[1;45m                fileJson length                :%d \033[0m' %len(fileJson))
        for key in fileJson:
            pic = fileJson[key]
            print('\033[0;32m person number in pic: %d \033[0m' %len(pic))
            suc_detect = False
            self.pose_keypoints_2d = np.zeros((1,14),dtype = float)
            my_counter = 0
            for person in pic :
                if my_counter == 0:
                    my_counter = my_counter+1
                    my_kp = []
                    keypoints = person['keypoints']
                    if len(keypoints) != 48:
                        print('\033[0;36m  erro   %s\033[0m' %key)
                    else:
                        suc_detect = True
                        for index in range(len(keypoints)):
                            # print (index)
                            if index in self.key_points: #去掉概率
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
    parser.add_argument("--folder_path", type=str, default='/home/hts/Desktop/kinect_result/',
                        help="path to the folder for the json to be processed (default: None)")
    parser.add_argument("--write_path", type=str, default='/home/hts/Desktop/kinect_keypoints/',
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
