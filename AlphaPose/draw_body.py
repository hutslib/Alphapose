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
    for i in range(len(cor_x)):
        cor_x[i] = int(cor_x[i])
        cor_y[i] = int(cor_y[i])
    cor_x_min = min(cor_x)
    cor_y_min = min(cor_y)

    if cor_x_min < 0:
        for i in range(len(cor_x)):
            cor_x[i] = cor_x[i] - cor_x_min + 5
    if cor_y_min < 0:
        for i in range(len(cor_y)):
            cor_y[i] = cor_y[i] - cor_y_min + 5


    cor_x.append((cor_x[5]+cor_x[6])/2)
    cor_y.append((cor_y[5]+cor_y[6])/2)

    cor_x_min = min(cor_x)
    cor_x_max = max(cor_x)
    cor_y_min = min(cor_y)
    cor_y_max = max(cor_y)

    img = np.zeros((cor_y_max+10, cor_x_max+10), dtype=np.uint8)
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
    for n in range(16):
        part_line[n] = (int(cor_x[n]), int(cor_y[n]))
        #bg = img.copy()
        cv2.circle(img, (int(cor_x[n]), int(cor_y[n])), 5, p_color[n], -1)
    
    # Draw limbs
    for i, (start_p, end_p) in enumerate(l_pair):
        if start_p in part_line and end_p in part_line:
            start_xy = part_line[start_p]
            end_xy = part_line[end_p]
            X = (start_xy[0], end_xy[0])
            Y = (start_xy[1], end_xy[1])
            mX = np.mean(X)
            mY = np.mean(Y)
            length = ((Y[0] - Y[1]) ** 2 + (X[0] - X[1]) ** 2) ** 0.5
            angle = math.degrees(math.atan2(Y[0] - Y[1], X[0] - X[1]))
            stickwidth = 5
            polygon = cv2.ellipse2Poly((int(mX),int(mY)), (int(length/2), stickwidth), int(angle), 0, 360, 1)
            cv2.fillConvexPoly(img, polygon, line_color[i])
    
    cv2.imwrite(dir_name, img)

if __name__ == '__main__':
    temp = [33.17881393432617, 354.4361572265625, 0.7169342637062073, 134.62977600097656, 290.1838684082031, 0.7453361749649048, 215.79054260253906, 229.3132781982422, 0.7909862995147705, 246.225830078125, 263.1302795410156, 0.7648909091949463, 175.2101593017578, 327.382568359375, 0.6899839043617249, 97.43109130859375, 405.1616516113281, 0.5119760036468506, 236.0807342529297, 242.84010314941406, 0.7178401350975037, 320.6231994628906, 188.73289489746094, 0.8264297842979431, 327.3865966796875, 181.96949768066406, 0.7865035533905029, 351.0585021972656, 158.29762268066406, 0.7973981499671936, 225.93563842773438, 225.9315948486328, 0.2525416314601898, 246.225830078125, 205.64137268066406, 0.4038618803024292, 286.8062438964844, 168.4427032470703, 0.7751867175102234, 351.0585021972656, 209.02308654785156, 0.8188015222549438, 337.5317077636719, 246.22178649902344, 0.7530956268310547, 310.4781188964844, 280.0387878417969, 0.8791655898094177]

    cor_x, cor_y = [], []
    
    for j in range(16):
        cor_x.append(float(temp[j*3]))
        cor_y.append(float(temp[j*3+1]))

    cor_x = (cor_x - np.mean(cor_x))
    cor_y = (cor_y - np.mean(cor_y))
    cor_x = cor_x.tolist()
    cor_y = cor_y.tolist()
        
    
    Draw_body(cor_x, cor_y, './test.jpg')
    print('succeed')