# -*- coding: utf-8 -*-
# -------------------------------------------
#  @description: change save json name
#  @version: 2.0
#  @data: 2020-03-24
# -------------------------------------------
# -------------------------------------------
#  @description: change 16->16 to achieve mpii keypoint format
#  @version: ２.1
#  @data: 2020-03-24
# -------------------------------------------
# -------------------------------------------
#  @description: 绘制人体框
#  @version: wenbin
#  @data: 2020-04-08
# -------------------------------------------
import torch
import json
import os
import zipfile
import time
from multiprocessing.dummy import Pool as ThreadPool
import numpy as np
from opt import opt
import ntpath


''' Constant Configuration '''
delta1 = 1
mu = 1.7
delta2 = 2.65
gamma = 22.48
scoreThreds = 0.3
matchThreds = 5
areaThres = 0#40 * 40.5
alpha = 0.1
#pool = ThreadPool(4)


def pose_nms(bboxes, bbox_scores, pose_preds, pose_scores):
    '''
    Parametric Pose NMS algorithm
    bboxes:         bbox locations list (n, 4)
    bbox_scores:    bbox scores list (n,) 各个框为人的score
    pose_preds:     pose locations list (n, 16, 2) 各关节点的坐标
    pose_scores:    pose scores list    (n, 16, 1) 各个关节点的score
    '''
    #global ori_pose_preds, ori_pose_scores, ref_dists

    pose_scores[pose_scores == 0] = 1e-5

    final_result = []

    #wenbin
    ori_bboxes = bboxes.clone()
    
    ori_bbox_scores = bbox_scores.clone() # 各个框为人的score，下面要删除，此处先备份
    ori_pose_preds = pose_preds.clone() # 各关节点的坐标，下面要删除，此处先备份
    ori_pose_scores = pose_scores.clone() # 各个关节点的score，下面要删除，此处先备份 [n, 16, 1]
    # 检测到的人在原始图像上的坐标
    xmax = bboxes[:, 2]
    xmin = bboxes[:, 0]
    ymax = bboxes[:, 3]
    ymin = bboxes[:, 1]
    # 检测到的人的宽高
    widths = xmax - xmin
    heights = ymax - ymin
    # alpha=0.1，为论文中的1/10，此处为NMS中当前batch各个人子框的阈值[n,]
    ref_dists = alpha * np.maximum(widths, heights)

    nsamples = bboxes.shape[0]
    # 当前batch各个人骨架的均值 [n, 1]
    human_scores = pose_scores.mean(dim=1)

    human_ids = np.arange(nsamples)
    # Do pPose-NMS
    pick = []
    merge_ids = []
    while(human_scores.shape[0] != 0):
        # Pick the one with highest score
        pick_id = torch.argmax(human_scores)
        pick.append(human_ids[pick_id])
        # num_visPart = torch.sum(pose_scores[pick_id] > 0.2)

        # Get numbers of match keypoints by calling PCK_match
        #当前人NMS子框的阈值
        ref_dist = ref_dists[human_ids[pick_id]]
        # 公式（10）的距离，[n]，由于每次均会删除id，因而n递减
        simi = get_parametric_distance(pick_id, pose_preds, pose_scores, ref_dist)
        # 返回满足条件的点的数量，[n]，由于每次均会删除id，因而n递减
        num_match_keypoints = PCK_match(pose_preds[pick_id], pose_preds, ref_dist)

        # Delete humans who have more than matchThreds keypoints overlap and high similarity
        # gamma = 22.48，matchThreds = 5
        # 迭代删除的索引
        delete_ids = torch.from_numpy(np.arange(human_scores.shape[0]))[(simi > gamma) | (num_match_keypoints >= matchThreds)]

        if delete_ids.shape[0] == 0:
            delete_ids = pick_id
        #else:
        #    delete_ids = torch.from_numpy(delete_ids)
# 选出来得分最高的人，找到与之骨架重合度最高的人，从总人中删除．否则删除得分最高的人．直到没有人了．merge是需要消除的人．一个人可能重复多次出现在ｐｉｃｋ中
        merge_ids.append(human_ids[delete_ids])
        pose_preds = np.delete(pose_preds, delete_ids, axis=0)
        pose_scores = np.delete(pose_scores, delete_ids, axis=0)
        human_ids = np.delete(human_ids, delete_ids)
        human_scores = np.delete(human_scores, delete_ids, axis=0)
        bbox_scores = np.delete(bbox_scores, delete_ids, axis=0)

        # wenbin
        bboxes = np.delete(bboxes, delete_ids, axis=0)
# pick中存放的是全部的筛选出来的得分最高的人
    assert len(merge_ids) == len(pick)
    preds_pick = ori_pose_preds[pick]
    scores_pick = ori_pose_scores[pick]
    bbox_scores_pick = ori_bbox_scores[pick]

    # wenbin
    bboxes_pick = ori_bboxes[pick]

    #final_result = pool.map(filter_result, zip(scores_pick, merge_ids, preds_pick, pick, bbox_scores_pick))
    #final_result = [item for item in final_result if item is not None]

    for j in range(len(pick)):
        ids = np.arange(16)
        max_score = torch.max(scores_pick[j, ids, 0])

        if max_score < scoreThreds:
            continue

        # Merge poses
        merge_id = merge_ids[j]
        # 返回冗余关节点位置和这些关节点对应的score。无冗余姿态的情况下，merge_pose==preds_pick[j]==ori_pose_preds[merge_id]，merge_score==ori_pose_scores[merge_id]
        merge_pose, merge_score = p_merge_fast(
            preds_pick[j], ori_pose_preds[merge_id], ori_pose_scores[merge_id], ref_dists[pick[j]])

        max_score = torch.max(merge_score[ids])

        # wenbin
        # print('---------------------')
        # print(ori_bbox_scores[merge_id])
        # print(bbox_scores_pick[j])
        if torch.max(ori_bbox_scores[merge_id]) > bbox_scores_pick[j]:
            merge_id_max = torch.argmax(ori_bbox_scores[merge_id])
            merge_box = ori_bboxes[merge_id_max]
            merge_box_score = ori_bbox_scores[merge_id_max]
        else:
            merge_box = bboxes_pick[j]
            merge_box_score = bbox_scores_pick[j]

        if max_score < scoreThreds:
            continue

        xmax = max(merge_pose[:, 0])
        xmin = min(merge_pose[:, 0])
        ymax = max(merge_pose[:, 1])
        ymin = min(merge_pose[:, 1])

        if (1.5 ** 2 * (xmax - xmin) * (ymax - ymin) < areaThres):
            continue

        ## wenbin
        # Get boxes after NMS
        # merge_pose_box = merge_pose - 0.3
        # merge_pose_box_xs = merge_pose_box[:,0]
        # merge_pose_box_ys = merge_pose_box[:,1]
        # merge_pose_box_xmin = merge_pose_box_xs.min()
        # merge_pose_box_xmax = merge_pose_box_xs.max()
        # merge_pose_box_ymin = merge_pose_box_ys.min()
        # merge_pose_box_ymax = merge_pose_box_ys.max()
        # boxes_nms = torch.tensor([merge_pose_box_xmin, merge_pose_box_ymin, merge_pose_box_xmax, merge_pose_box_ymax])


        final_result.append({
            'keypoints': merge_pose - 0.3,
            'kp_score': merge_score,
            'proposal_score': torch.mean(merge_score) + bbox_scores_pick[j] + 1.25 * max(merge_score),
            
            # wenbin
            'box': merge_box,
            'box_scores': merge_box_score
            # 'box': boxes_ms
        })
        ##

    return final_result


def filter_result(args):
    score_pick, merge_id, pred_pick, pick, bbox_score_pick = args
    global ori_pose_preds, ori_pose_scores, ref_dists
    ids = np.arange(16)
    max_score = torch.max(score_pick[ids, 0])

    if max_score < scoreThreds:
        return None

    # Merge poses
    merge_pose, merge_score = p_merge_fast(
        pred_pick, ori_pose_preds[merge_id], ori_pose_scores[merge_id], ref_dists[pick])

    max_score = torch.max(merge_score[ids])
    if max_score < scoreThreds:
        return None

    xmax = max(merge_pose[:, 0])
    xmin = min(merge_pose[:, 0])
    ymax = max(merge_pose[:, 1])
    ymin = min(merge_pose[:, 1])

    if (1.5 ** 2 * (xmax - xmin) * (ymax - ymin) < 40 * 40.5):
        return None

    return {
        'keypoints': merge_pose - 0.3,
        'kp_score': merge_score,
        'proposal_score': torch.mean(merge_score) + bbox_score_pick + 1.25 * max(merge_score)
    }


def p_merge(ref_pose, cluster_preds, cluster_scores, ref_dist):
    '''
    Score-weighted pose merging
    INPUT:
        ref_pose:       reference pose          -- [16, 2]
        cluster_preds:  redundant poses         -- [n, 16, 2]
        cluster_scores: redundant poses score   -- [n, 16, 1]
        ref_dist:       reference scale         -- Constant
    OUTPUT:
        final_pose:     merged pose             -- [16, 2]
        final_score:    merged score            -- [16]
    '''
    dist = torch.sqrt(torch.sum(
        torch.pow(ref_pose[np.newaxis, :] - cluster_preds, 2),
        dim=2
    ))  # [n, 16]

    kp_num = 16
    ref_dist = min(ref_dist, 15)

    mask = (dist <= ref_dist)
    final_pose = torch.zeros(kp_num, 2)
    final_score = torch.zeros(kp_num)

    if cluster_preds.dim() == 2:
        cluster_preds.unsqueeze_(0)
        cluster_scores.unsqueeze_(0)
    if mask.dim() == 1:
        mask.unsqueeze_(0)

    for i in range(kp_num):
        cluster_joint_scores = cluster_scores[:, i][mask[:, i]]  # [k, 1]
        cluster_joint_location = cluster_preds[:, i, :][mask[:, i].unsqueeze(
            -1).repeat(1, 2)].view((torch.sum(mask[:, i]), -1))

        # Get an normalized score
        normed_scores = cluster_joint_scores / torch.sum(cluster_joint_scores)

        # Merge poses by a weighted sum
        final_pose[i, 0] = torch.dot(cluster_joint_location[:, 0], normed_scores.squeeze(-1))
        final_pose[i, 1] = torch.dot(cluster_joint_location[:, 1], normed_scores.squeeze(-1))

        final_score[i] = torch.dot(cluster_joint_scores.transpose(0, 1).squeeze(0), normed_scores.squeeze(-1))

    return final_pose, final_score


def p_merge_fast(ref_pose, cluster_preds, cluster_scores, ref_dist):
    '''
    Score-weighted pose merging
    INPUT:
        ref_pose:       reference pose          -- [16, 2]
        cluster_preds:  redundant poses         -- [n, 16, 2]
        cluster_scores: redundant poses score   -- [n, 16, 1]
        ref_dist:       reference scale         -- Constant
    OUTPUT:
        final_pose:     merged pose             -- [16, 2]
        final_score:    merged score            -- [16]
    '''
    dist = torch.sqrt(torch.sum(
        torch.pow(ref_pose[np.newaxis, :] - cluster_preds, 2),
        dim=2
    ))

    kp_num = 16
    ref_dist = min(ref_dist, 15)

    mask = (dist <= ref_dist)
    final_pose = torch.zeros(kp_num, 2)
    final_score = torch.zeros(kp_num)

    if cluster_preds.dim() == 2:
        cluster_preds.unsqueeze_(0)
        cluster_scores.unsqueeze_(0)
    if mask.dim() == 1:
        mask.unsqueeze_(0)

    # Weighted Merge
    masked_scores = cluster_scores.mul(mask.float().unsqueeze(-1))
    normed_scores = masked_scores / torch.sum(masked_scores, dim=0)

    final_pose = torch.mul(cluster_preds, normed_scores.repeat(1, 1, 2)).sum(dim=0)
    final_score = torch.mul(masked_scores, normed_scores).sum(dim=0)
    return final_pose, final_score


def get_parametric_distance(i, all_preds, keypoint_scores, ref_dist):
    pick_preds = all_preds[i]
    pred_scores = keypoint_scores[i]
    dist = torch.sqrt(torch.sum(
        torch.pow(pick_preds[np.newaxis, :] - all_preds, 2),
        dim=2
    ))
    mask = (dist <= 1)

    # Define a keypoints distance
    score_dists = torch.zeros(all_preds.shape[0], 16)
    keypoint_scores.squeeze_()
    if keypoint_scores.dim() == 1:
        keypoint_scores.unsqueeze_(0)
    if pred_scores.dim() == 1:
        pred_scores.unsqueeze_(1)
    # The predicted scores are repeated up to do broadcast
    pred_scores = pred_scores.repeat(1, all_preds.shape[0]).transpose(0, 1)

    score_dists[mask] = torch.tanh(pred_scores[mask] / delta1) * torch.tanh(keypoint_scores[mask] / delta1)

    point_dist = torch.exp((-1) * dist / delta2)
    final_dist = torch.sum(score_dists, dim=1) + mu * torch.sum(point_dist, dim=1)

    return final_dist


def PCK_match(pick_pred, all_preds, ref_dist):
    dist = torch.sqrt(torch.sum(
        torch.pow(pick_pred[np.newaxis, :] - all_preds, 2),
        dim=2
    ))
    ref_dist = min(ref_dist, 7)
    num_match_keypoints = torch.sum(
        dist / ref_dist <= 1,
        dim=1
    )

    return num_match_keypoints


def write_json(all_results, outputpath, for_eval=False):
    '''
    all_result: result dict of predictions
    outputpath: output directory
    '''
    form = opt.format
    json_results = []
    json_results_cmu = {}
    filename = opt.video
    #print(all_results)
    for im_res in all_results:
        im_name = im_res['imgname']
        for human in im_res['result']:
            keypoints = []
            result = {}
            if for_eval:
                result['image_id'] = int(im_name.split('/')[-1].split('.')[0].split('_')[-1])
            else:
                result['image_id'] = im_name.split('/')[-1]
            result['category_id'] = 1

            kp_preds = human['keypoints']
            kp_scores = human['kp_score']
            pro_scores = human['proposal_score']

            # wenbin
            human_box = human['box']
            box= []
            for n in range(4):
                box.append(float(human_box[n]))
            box_scores = float(human['box_scores'])
            #######

            for n in range(kp_scores.shape[0]):
                keypoints.append(float(kp_preds[n, 0]))
                keypoints.append(float(kp_preds[n, 1]))
                keypoints.append(float(kp_scores[n]))
            result['keypoints'] = keypoints
            result['score'] = float(pro_scores)

            # wenbin
            result['box'] = box
            result['box_scores'] = float(box_scores)
            result['kp_box'] = human['kp_box']
            kp_box_score = human['kp_box_score'][0]
            result['kp_box_score'] = kp_box_score
            fusion_box_score = (box_scores * kp_box_score) / (box_scores * kp_box_score + (1-box_scores) * (1-kp_box_score))
            result['fusion_box_score'] = fusion_box_score
            #####

            if form == 'cmu': # the form of CMU-Pose
                if result['image_id'] not in json_results_cmu.keys():
                    json_results_cmu[result['image_id']]={}
                    json_results_cmu[result['image_id']]['version']="AlphaPose v0.2"
                    json_results_cmu[result['image_id']]['bodies']=[]
                tmp={'joints':[]}
                result['keypoints'].append((result['keypoints'][15]+result['keypoints'][18])/2)
                result['keypoints'].append((result['keypoints'][16]+result['keypoints'][19])/2)
                result['keypoints'].append((result['keypoints'][17]+result['keypoints'][20])/2)
                indexarr=[0,51,18,24,30,15,21,27,36,42,48,33,39,45,6,3,12,9]
                for i in indexarr:
                    tmp['joints'].append(result['keypoints'][i])
                    tmp['joints'].append(result['keypoints'][i+1])
                    tmp['joints'].append(result['keypoints'][i+2])
                json_results_cmu[result['image_id']]['bodies'].append(tmp)
            elif form == 'open': # the form of OpenPose
                if result['image_id'] not in json_results_cmu.keys():
                    json_results_cmu[result['image_id']]={}
                    json_results_cmu[result['image_id']]['version']="AlphaPose v0.2"
                    json_results_cmu[result['image_id']]['people']=[]
                tmp={'pose_keypoints_2d':[]}
                result['keypoints'].append((result['keypoints'][15]+result['keypoints'][18])/2)
                result['keypoints'].append((result['keypoints'][16]+result['keypoints'][19])/2)
                result['keypoints'].append((result['keypoints'][17]+result['keypoints'][20])/2)
                indexarr=[0,51,18,24,30,15,21,27,36,42,48,33,39,45,6,3,12,9]
                for i in indexarr:
                    tmp['pose_keypoints_2d'].append(result['keypoints'][i])
                    tmp['pose_keypoints_2d'].append(result['keypoints'][i+1])
                    tmp['pose_keypoints_2d'].append(result['keypoints'][i+2])
                json_results_cmu[result['image_id']]['people'].append(tmp)
            else:
                json_results.append(result)
##version 2.0
    if form == 'cmu': # the form of CMU-Pose
        with open(os.path.join(outputpath,'alphapose-results_'+ntpath.basename(filename).split('.')[0]+'.json'), 'w') as json_file:
            json_file.write(json.dumps(json_results_cmu))
            if not os.path.exists(os.path.join(outputpath,'sep-json_'+ntpath.basename(filename).split('.')[0])):
                os.mkdir(os.path.join(outputpath,'sep-json_'+ntpath.basename(filename).split('.')[0]))
            for name in json_results_cmu.keys():
                with open(os.path.join(outputpath,'sep-json_'+ntpath.basename(filename).split('.')[0],name.split('.')[0]+'.json'),'w') as json_file:
                    json_file.write(json.dumps(json_results_cmu[name]))
    elif form == 'open': # the form of OpenPose
        with open(os.path.join(outputpath,'alphapose-results_'+ntpath.basename(filename).split('.')[0]+'.json'), 'w') as json_file:
            json_file.write(json.dumps(json_results_cmu))
            if not os.path.exists(os.path.join(outputpath,'sep-json_'+ntpath.basename(filename).split('.')[0])):
                os.mkdir(os.path.join(outputpath,'sep-json_'+ntpath.basename(filename).split('.')[0]))
            for name in json_results_cmu.keys():
                with open(os.path.join(outputpath,'sep-json_'+ntpath.basename(filename).split('.')[0],name.split('.')[0]+'.json'),'w') as json_file:
                    json_file.write(json.dumps(json_results_cmu[name]))
    else:
        with open(os.path.join(outputpath,'alphapose-results_'+ntpath.basename(filename).split('.')[0]+'.json'), 'w') as json_file:
            json_file.write(json.dumps(json_results))

