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
        
    img_ori = cv2.imread('/home/hts/kinect_pic_1/0000_color.jpg')
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
    for n in range(3):
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
    temp = [237.73190307617188, 261.40020751953125, 0.9030706882476807, 233.74618530273438, 219.5502166748047, 0.8321270942687988, 227.7676239013672, 171.72166442871094, 0.797931969165802, 253.6747589111328, 173.71450805664062, 0.7851492762565613, 249.6890411376953, 219.5502166748047, 0.8359363079071045, 249.6890411376953, 261.40020751953125, 0.8275410532951355, 239.72476196289062, 171.72166442871094, 0.8245024681091309, 237.73190307617188, 95.99311828613281, 0.8439276814460754, 237.73190307617188, 84.03596496582031, 0.8713452816009521, 237.73190307617188, 38.20026779174805, 0.8569822907447815, 211.82476806640625, 169.7288055419922, 0.8430814743041992, 205.84620666503906, 139.83596801757812, 0.7678086757659912, 213.81761169433594, 95.99311828613281, 0.8916050791740417, 263.6390686035156, 95.99311828613281, 0.8505486845970154, 269.61761474609375, 135.85025024414062, 0.8407207727432251, 269.61761474609375, 169.7288055419922, 0.8784126043319702]
    cor_x, cor_y = [], []
    pick_points = [6,12,13]
    for j in range(16):
        if j in pick_points:
            cor_x.append(float(temp[j*3]))
            cor_y.append(float(temp[j*3+1]))
            print(float(temp[j*3]),float(temp[j*3+1]))
        
    
    Draw_body(cor_x, cor_y, './test.jpg')
    print('succeed')
