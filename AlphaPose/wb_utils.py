from munkres import Munkres, print_matrix
import numpy as np

# 计算两个人体框的IoU
def cal_bbox_iou(boxA, boxB): 

    xA = max(boxA[0], boxB[0]) #xmin
    yA = max(boxA[2], boxB[2]) #ymin
    xB = min(boxA[1], boxB[1]) #xmax
    yB = min(boxA[3], boxB[3]) #ymax

    if xA < xB and yA < yB: 
        interArea = (xB - xA + 1) * (yB - yA + 1) 
        boxAArea = (boxA[1] - boxA[0] + 1) * (boxA[3] - boxA[2] + 1) 
        boxBArea = (boxB[1] - boxB[0] + 1) * (boxB[3] - boxB[2] + 1) 
        iou = interArea / float(boxAArea + boxBArea - interArea+0.00001) 
    else: 
        iou=0.0

    return iou

# 计算两个人体框的前一个框中的特征点数
def find_region_cors_last(box_pos, all_cors):
    
    x1, y1, x2, y2 = [all_cors[:, col] for col in range(4)]
    x_min, y_min, x_max, y_max = box_pos
    x1_region_ids = set(np.where((x1 >= x_min) & (x1 <= x_max))[0].tolist())
    y1_region_ids = set(np.where((y1 >= y_min) & (y1 <= y_max))[0].tolist())
    region_ids = x1_region_ids & y1_region_ids

    return region_ids

# 计算两个人体框的后一个框中的特征点数
def find_region_cors_next(box_pos, all_cors):
    
    x1, y1, x2, y2 = [all_cors[:, col] for col in range(4)]
    x_min, y_min, x_max, y_max = box_pos
    x2_region_ids = set(np.where((x2 >= x_min) & (x2 <= x_max))[0].tolist())
    y2_region_ids = set(np.where((y2 >= y_min) & (y2 <= y_max))[0].tolist())
    region_ids = x2_region_ids & y2_region_ids

    return region_ids

# 计算加权得分
def cal_grade(l, w):
    return sum(np.array(l)*np.array(w))

# 匈牙利算法获取最佳匹配
def best_matching_hungarian(all_cors, last_boxes, last_box_scores, last_boxes_fff, now_boxes, now_box_scores, weights, weights_fff):
    # all_cors表示图像特征匹配结果
    x1, y1, x2, y2 = [all_cors[:, col] for col in range(4)]
    
    box1_num = len(last_boxes)
    box2_num = len(now_boxes)
    # 匹配得分矩阵
    cost_matrix = np.zeros((box1_num, box2_num))
    print('box1_num: ', box1_num)
    print('box2_num: ', box2_num)
    for pid1 in range(box1_num):
        box1_pos = last_boxes[pid1]
        # 选出在人体框中的orb特征点
        box1_region_ids = find_region_cors_last(box1_pos, all_cors)
        box1_score = last_box_scores[pid1]
        #box1_fff = all_pids_fff[pid1]

        for pid2 in range(box2_num):
            box2_pos = now_boxes[pid2]
            box2_region_ids = find_region_cors_next(box2_pos, all_cors)
            box2_score = now_box_scores[pid2]
                        
            inter = box1_region_ids & box2_region_ids
            union = box1_region_ids | box2_region_ids
            dm_iou = len(inter) / (len(union) + 0.00001)
            #print('dm_iou: ', dm_iou)
            box_iou = cal_bbox_iou(box1_pos, box2_pos)
            # if box1_fff:
            #     grade = cal_grade([dm_iou, box_iou, box1_score, box2_score], weights)
            # else:
            #     grade = cal_grade([dm_iou, box_iou, box1_score, box2_score], weights_fff)
            grade = cal_grade([dm_iou, box_iou, box1_score, box2_score], weights)
                
            cost_matrix[pid1, pid2] = grade
    m = Munkres()
    indexes = m.compute((-np.array(cost_matrix)).tolist())

    return indexes, cost_matrix