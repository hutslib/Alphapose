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
        
    img_ori = cv2.imread('/home/hts/Desktop/kinect_pic/b/aaa/0008_color.jpg')
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
    temp = [191.4891815185547, 215.0364227294922, 0.4517185091972351, 218.52777099609375, 226.16993713378906, 0.5216860771179199, 248.7473602294922, 234.1224822998047, 0.36508888006210327, 263.0619201660156, 219.8079376220703, 0.45060425996780396, 231.25181579589844, 221.3984375, 0.3167969882488251, 228.07080078125, 207.08389282226562, 0.34528136253356934, 259.88092041015625, 227.7604522705078, 0.7379199862480164, 296.4625244140625, 262.7515869140625, 0.6079698204994202, 301.23406982421875, 264.34210205078125, 0.5761451125144958, 315.548583984375, 283.42816162109375, 0.5628469586372375, 234.4328155517578, 254.79905700683594, 0.6901631355285645, 251.9283905029297, 265.9325866699219, 0.502133309841156, 271.01446533203125, 273.8851318359375, 0.5307292342185974, 313.95806884765625, 242.0749969482422, 0.6545906662940979, 315.548583984375, 221.3984375, 0.969918429851532, 344.17767333984375, 240.4844970703125, 0.4010535776615143]
    cor_x, cor_y = [], []
    #pick_points = [0,1,2,3,4,5,6,7,8,9]
    pick_points = [6,12,13]
    for j in range(16):
        if j in pick_points:
            cor_x.append(float(temp[j*3]))
            cor_y.append(float(temp[j*3+1]))
            print(float(temp[j*3]),float(temp[j*3+1]))
        
    
    Draw_body(cor_x, cor_y, './test.jpg')
    print('succeed')
