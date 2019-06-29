# HoG feature for nearest neighbor+ search


import cv2 as cv
import scipy.io as sio
from util.synthetic_util import SyntheticUtil


win_size = (128, 128)
block_size = (32, 32)
block_stride = (32, 32)
cell_size = (32, 32)
n_bins = 9
hog = cv.HOGDescriptor(win_size, block_size, block_stride, cell_size, n_bins)

def gray_to_hog(im, hog):
    """
    An gray image to HoG feature
    :param im:
    :param hog:
    :return:
    """

    return hog.compute(im)

def ut():
    im_name = '../../data/16_edge_image.jpg'
    im = cv.imread(im_name, 0)
    im = cv.resize(im, (320, 180))

    feature = hog.compute(im)
    print('feature shape {}'.format(feature.shape))

# database camera
data = sio.loadmat('../data/worldcup_sampled_cameras.mat')
database_cameras = data['pivot_cameras']

n, _ = database_cameras.shape

# World Cup soccer template
data = sio.loadmat('../data/worldcup2014.mat')
model_points = data['points']
model_line_index = data['line_segment_index']

im_h, im_w = 180, 320
for i in range(1):
    edge_image = SyntheticUtil.camera_to_edge_image(database_cameras[i,:],
                                                    model_points,
                                                    model_line_index,
                                                    im_h=720, im_w=1280,
                                                    line_width=4)
    edge_image = cv.resize(edge_image, (im_w, im_h))
    edge_image = cv.cvtColor(edge_image, cv.COLOR_BGR2GRAY)
    feat = gray_to_hog(edge_image, hog)
    print('feature dimension {}'.format(feat.shape))

#def camera_to_edge_image(camera_data,
#                             model_points, model_line_segment,
#                             im_h=720, im_w=1280, line_width=4):


