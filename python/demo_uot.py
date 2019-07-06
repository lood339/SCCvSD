import pyflann
import scipy.io as sio
import numpy as np
import cv2 as cv
import time

from util.synthetic_util import SyntheticUtil
from util.iou_util import IouUtil
from util.projective_camera import ProjectiveCamera

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--feature-type', required=True, type=str, default='deep', help='deep or HoG')

args = parser.parse_args()
feature_type = args.feature_type
assert feature_type == 'deep' or feature_type == 'HoG'

"""
Estimate an homogrpahy using edge images 
"""
iou_1_list = []
iou_2_list = []
for query_index in range(186):
    # Step 1: load data
    # database
    if feature_type == 'deep':
        data = sio.loadmat('../data/features/database_camera_feature.mat')
        database_features = data['features']
        database_cameras = data['cameras']
    else:
        data = sio.loadmat('../data/features/database_camera_feature_HoG.mat')
        database_features = data['features']
        database_cameras = data['cameras']

    # testing edge image from two-GAN
    if feature_type == 'deep':
        data = sio.loadmat('../data/features/testset_feature.mat')
        edge_map = data['edge_map']
        test_features = data['features']
        test_features = np.transpose(test_features)
    else:
        data = sio.loadmat('../data/features/testset_feature_HoG.mat')
        edge_map = data['edge_map']
        test_features = data['features']

    # World Cup soccer template
    data = sio.loadmat('../data/worldcup2014.mat')
    model_points = data['points']
    model_line_index = data['line_segment_index']

    template_h = 74  # yard, soccer template
    template_w = 115


    # ground truth homography
    data = sio.loadmat('../data/UoT_soccer/test.mat')
    annotation = data['annotation']
    gt_h = annotation[0][query_index][1]  # ground truth


    state_time = time.time()
    # Step 2: retrieve a camera using deep features
    flann = pyflann.FLANN()
    result, _ = flann.nn(database_features, test_features[query_index], 1, algorithm="kdtree", trees=8, checks=64)
    retrieved_index = result[0]


    """
    Retrieval camera: get the nearest-neighbor camera from database
    """
    retrieved_camera_data = database_cameras[retrieved_index]

    u, v, fl = retrieved_camera_data[0:3]
    rod_rot = retrieved_camera_data[3:6]
    cc = retrieved_camera_data[6:9]

    retrieved_camera = ProjectiveCamera(fl, u, v, cc, rod_rot)

    retrieved_h = IouUtil.template_to_image_homography_uot(retrieved_camera, template_h, template_w)

    iou_1 = IouUtil.iou_on_template_uot(gt_h, retrieved_h)
    print('retrieved homogrpahy IoU {:.3f}'.format(iou_1))

    retrieved_image = SyntheticUtil.camera_to_edge_image(retrieved_camera_data, model_points, model_line_index,
                                                im_h=720, im_w=1280, line_width=4)

    query_image = edge_map[:,:,:,query_index]
    #cv.imshow('Edge image of query image', query_image)
    #cv.imshow('Edge image of retrieved camera', retrieved_image)
    #cv.waitKey(10000)

    """
    Refine camera: refine camera pose using Lucas-Kanade algorithm 
    """
    dist_threshold = 50
    query_dist = SyntheticUtil.distance_transform(query_image)
    retrieved_dist = SyntheticUtil.distance_transform(retrieved_image)

    query_dist[query_dist > dist_threshold] = dist_threshold
    retrieved_dist[retrieved_dist > dist_threshold] = dist_threshold

    #cv.imshow('Distance image of query image', query_dist.astype(np.uint8))
    #cv.imshow('Distance image of retrieved camera', retrieved_dist.astype(np.uint8))
    #cv.waitKey(10000)

    h_retrieved_to_query = SyntheticUtil.find_transform(retrieved_dist, query_dist)

    refined_h = h_retrieved_to_query@retrieved_h
    iou_2 = IouUtil.iou_on_template_uot(gt_h, refined_h)
    print('refined homogrpahy IoU {:.3f}'.format(iou_2))
    print('takes time {:.3f} seconds'.format(time.time()-state_time))
    iou_1_list.append(iou_1)
    iou_2_list.append(iou_2)
iou_1_list = np.array(iou_1_list)
iou_2_list = np.array(iou_2_list)
print('---------- Direct retrival performance ----------')
print('mean IoU for retrived homogrpahy {0}'.format(iou_1_list.mean()))
print('median IoU for retrived homogrpahy {0}'.format(np.median(iou_1_list)))
print('numer of failed cases for retrived homogrpahy {0}'.format((iou_1_list<0.01).sum()))
print('--------------------')
print('---------- Refined retrival performance ----------')
print('mean IoU for refined homogrpahy {0}'.format(iou_2_list.mean()))
print('median IoU for refined homogrpahy {0}'.format(np.median(iou_2_list)))
print('numer of failed cases for refined homogrpahy {0}'.format((iou_2_list<0.01).sum()))
print('--------------------')
