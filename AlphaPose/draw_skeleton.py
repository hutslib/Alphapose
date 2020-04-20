# -------------------------------------------
#  @description: 只绘制骨架去掉背景，图片大小与原始一直。
#  @author: hts
#  @data: 2020-04-13
# -------------------------------------------
import sys
# print(sys.path)
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    # print('!!!!')
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
# print(sys.path)
import cv2
import math
import numpy as np


def Draw_body(cor_x, cor_y, dir_name):
        
    img_ori = cv2.imread('/home/hts/Desktop/kinect_pic/a/aaa/0002_color.jpg')
    sp = img_ori.shape
    print(sp)
    img = np.zeros((sp[0], sp[1]), dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #img = cv2.imread('./30_0.jpg')

    part_line = {}
    # p_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, PURPLE, RED, RED, BLUE, BLUE]
    # line_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, RED, RED, BLUE, BLUE]
    l_pair = [
            (8, 9), (11, 12), (11, 10), (2, 1), (1, 0),
            (13, 14), (14, 15), (3, 4), (4, 5),
            (8, 7), (7, 6), (6, 2), (6, 3), (8, 12), (8, 13)
        ]
    p_color = [ (77,255,127), (77,255,191), (77,255,204),(204,77,255),(191,77,255), (127,77,255), 
                (0, 255, 102), (0, 191, 255),(0, 255, 255),(0, 255, 255),(191, 255, 77),(191, 255, 77), 
                (77, 255, 204),(77,255,255), (77,204,255), (77,191,255)]
    line_color = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), 
                (77,255,222), (77,196,255), (77,135,255), (191,255,77), (77,255,77), 
                (77,222,255), (255,156,127), 
                (0,127,255), (255,127,77), (0,77,255), (255,77,36)]    
    # l_pair = [
    #         (0, 1), (0, 2), (1, 3), (2, 4),  # Head
    #         (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    #         (17, 11), (17, 12),  # Body
    #         (11, 13), (12, 14), (13, 15), (14, 16)
    #     ]

    # p_color = [(0, 255, 255), (0, 191, 255),(0, 255, 102),(0, 77, 255), (0, 255, 0), #Nose, LEye, REye, LEar, REar
    #             (77,255,255), (77, 255, 204), (77,204,255), (191, 255, 77), (77,191,255), (191, 255, 77), #LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
    #             (204,77,255), (77,255,204), (191,77,255), (77,255,191), (127,77,255), (77,255,127), (0, 255, 255)] #LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck

    
    # Draw keypoints
    for n in range(10):
        part_line[n] = (int(cor_x[n]), int(cor_y[n]))
        #bg = img.copy()
        cv2.circle(img, (int(cor_x[n]), int(cor_y[n])), 5, p_color[n], -1)
    
    # Draw limbs
    # for i, (start_p, end_p) in enumerate(l_pair):
    #     if start_p in part_line and end_p in part_line:
    #         start_xy = part_line[start_p]
    #         end_xy = part_line[end_p]
    #         X = (start_xy[0], end_xy[0])
    #         Y = (start_xy[1], end_xy[1])
    #         mX = np.mean(X)
    #         mY = np.mean(Y)
    #         length = ((Y[0] - Y[1]) ** 2 + (X[0] - X[1]) ** 2) ** 0.5
    #         angle = math.degrees(math.atan2(Y[0] - Y[1], X[0] - X[1]))
    #         stickwidth = 5
    #         polygon = cv2.ellipse2Poly((int(mX),int(mY)), (int(length/2), stickwidth), int(angle), 0, 360, 1)
    #         cv2.fillConvexPoly(img, polygon, line_color[i])
    
    cv2.imwrite(dir_name, img)

if __name__ == '__main__':
    temp = [325.0851135253906, 354.8621826171875, 0.6322734951972961, 277.11724853515625, 306.894287109375, 0.8115265965461731, 234.90553283691406, 281.9510192871094, 0.6867309808731079, 259.8488464355469, 274.2761535644531, 0.7372114062309265, 313.57281494140625, 276.19488525390625, 0.8209307789802551, 317.4102478027344, 326.0814208984375, 0.7046723365783691, 244.4990997314453, 274.2761535644531, 0.7050938010215759, 213.79966735839844, 239.7393035888672, 0.7159721255302429, 213.79966735839844, 235.90187072753906, 0.6610541343688965, 219.55581665039062, 216.7147216796875, 0.3590053617954254, 194.61253356933594, 287.7071533203125, 0.8780078887939453, 188.8563995361328, 268.52001953125, 0.7865536212921143, 194.61253356933594, 243.57672119140625, 0.7317582964897156, 232.98681640625, 237.82057189941406, 0.6932752132415771, 263.686279296875, 251.25157165527344, 0.8039182424545288, 292.46697998046875, 249.33287048339844, 0.8424583077430725]
    cor_x, cor_y = [], []
    pick_points = [0,1,2,3,4,5,6,7,8,9]
    for j in range(16):
        if j in pick_points:
            cor_x.append(float(temp[j*3]))
            cor_y.append(float(temp[j*3+1]))
            print(float(temp[j*3]),float(temp[j*3+1]))
        
    
    Draw_body(cor_x, cor_y, './test.jpg')
    print('succeed')
