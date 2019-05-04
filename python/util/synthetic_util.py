import numpy as np
import cv2 as cv

import random
from rotation_util import RotationUtil

class SyntheticUtil:
    @staticmethod
    def camera_to_edge_image(cameras, model_points, model_line_segment, dist_h=72, dist_w=128):
        """
        1. project (line) model images using cameras
        2. compute distance map
        :param cameras: N * 9
        :param model_points: N * 2
        :param model_line_segment: index
        :param dist_h: image resolution
        :param dist_w:
        :return: N * 1 * H * W
        """
        assert cameras.shape[1] == 9

        n = cameras.shape[0]
        pass

    @staticmethod
    def generate_ptz_cameras(cc_statistics,
                             fl_statistics,
                             roll_statistics,
                             pan_range, tilt_range,
                             u, v,
                             camera_num):
        """
        :param cc_statistics:
        :param fl_statistics:
        :param roll_statistics:
        :param pan_range:
        :param tilt_range:
        :param u:
        :param v:
        :param camera_num:
        :return: N * 9 cameras
        """

        cc_mean, cc_std, cc_min, cc_max = cc_statistics
        fl_mean, fl_std, fl_min, fl_max = fl_statistics
        roll_mean, roll_std, roll_min, roll_max = roll_statistics
        pan_min, pan_max = pan_range
        tilt_min, tilt_max = tilt_range

        camera_centers = np.random.normal(cc_mean, cc_std, camera_num)
        focal_lengths = np.random.normal(fl_mean, fl_std, camera_num)
        rolls = np.random.normal(roll_mean, roll_std, camera_num)
        pans = np.random.uniform(pan_min, pan_max, camera_num)
        tilts = np.random.uniform(tilt_min, tilt_max, camera_num)

        cameras = np.zeros((camera_num, 9))
        for i in range(camera_num):
            base_rotation = RotationUtil.rotate_y_axis(0) @ RotationUtil.rotate_x_axis(rolls[i]) @\
                RotationUtil.rotate_x_axis(-90)
            pan_tilt_rotation = RotationUtil.pan_y_tilt_x(pans[i], tilts[i])
            rotation = pan_tilt_rotation @ base_rotation
            rot_vec = cv.Rodrigues(rotation)

            cameras[i][0] = focal_lengths[i]
            cameras[i][1], cameras[i][2] = u, v
            cameras[i][3], cameras[i][4], cameras[i][5] = rot_vec[0], rot_vec[1], rot_vec[2]
            cameras[i][6], cameras[i][7], cameras[i][8] = camera_centers[i][0], camera_centers[i][1], camera_centers[i][2]
        return cameras





"""
function [im] = project_model_bw_fast(camera, model_points, model_line_segment)
% [im] = project_model_bw_fast(camera, model_points, model_line_segment)
% project a 2D field model to the image space (black and white)
% It is faster as using OpenCV, output one-channel edge image
% assume image size is 1280 x 720, line thickness 4
% im: rgb_image with overlaied lines
% camera: 9 camera parameters, (u, v, focal_length, Rx, Rx, Rz, Cx, Cy, Cz)
%         (Rx, Rx, Rz): is Rodrigues angle, (Cx, Cy, Cz) unit in meter
% model_points: N x 2 matrix, model world coordinate in meter
% model_line_segment: line segment index, start from 1
% example: 
% camera = [640.000000	 360.000000	 2986.943295	 1.367497	 -1.082443	 0.980122	 -16.431519	 14.086604	 5.580546];
% load('soccer_field_model.mat');
% model_points = points;
% model_line_segment = line_segment_index + 1;
% project_model(camera, model_points, model_line_segment);
assert(length(camera) == 9);
assert(size(model_points, 2) == 2);
assert(size(model_line_segment, 2) == 2);


% 
u = camera(1);
v = camera(2);
f = camera(3);
rod = camera(4:6); % Rodrigues angle
c = camera(7:9)';

K = [f, 0, u; 0, f, v; 0, 0, 1];
rotation = rotationVectorToMatrix(rod)'; % camera rotation to world point rotation

N = size(model_points, 1);
image_points = zeros(N, 2);

for i = [1:N]
    p = [model_points(i, 1), model_points(i, 2), 0.0]';
    % translate, rotate, then project
    p = K*rotation*(p - c);
    x = p(1)/p(3);
    y = p(2)/p(3);  % p(3) may be zero
    image_points(i, :) = [x, y];    
end

im_w = 1280;
im_h = 720;
% remove part of linesegment
model_line_segment = in_image_linesegment(image_points, model_line_segment, im_w, im_h);
im = drawLineSegment(image_points, model_line_segment, im_w, im_h, 4);
end
"""

"""
function [dist_map] = camera_to_distance_map(cameras, ...
                        model_points, model_line_segment, ...
                        dist_h, dist_w)
%[dist_map] = camera_to_distance_map(cameras, n_channel, ...
%    model_points, model_line_segment)
% default resolution [72, 128]

assert(size(cameras, 2) == 9);


N = size(cameras, 1);

dist_map = zeros(dist_h, dist_w, 1, N);

for i = [1:N]
    im = project_model_bw_fast(cameras(i, :), model_points, model_line_segment);
    im = imresize(im, [dist_h, dist_w]);
    dist_map(:,:,:,i) = distanceTransform(im);
    if mod(i, 5000) == 0
        i/N
    end
end

end
"""
