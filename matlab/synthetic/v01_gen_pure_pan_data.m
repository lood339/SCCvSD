clear
close all

% This script generate a sequence of debug data.
% The camera has fixed focal length and tilt angles. Its pan angle changes so that can be used to
% visualize and debug the code in feature extraction (siamese network)

addpath('../util');
addpath('../../data');
addpath('./synthetic_util');

load('worldcup2014_noPenalty_grid_points.mat');
model_points = points;
model_line_segment = line_segment_index;

uot = load('soccer_train_val_fl_cc.mat');
cc_mean = uot.cc_mean;

fl_mean = uot.fl_mean;

pan_min = -35.0;
pan_max =  35.0;
pan_step = 0.8;
pan_angles = [pan_min:pan_step: pan_max];

N = length(pan_angles)

im_h = 720;
im_w = 1280;
dist_h = 180;
dist_w = 320;
edge_maps = zeros(im_h, im_w, 1, N);
distance_maps = zeros(im_h, im_w, 1, N);
cameras = zeros(N, 9);
for i = [1:1:N]
    pan = pan_angles(i);
    tilt = -10.0;
    fl = fl_mean;
    roll = 0;
    cc = cc_mean;
    
    camera = zeros(1, 9);
    camera(1) = 640.000000;
    camera(2) = 360.000000;
    camera(3) = fl;

    base_rotation = rotateY_axis(0)*rotateZ_axis(roll)*rotateX_axis(-90);
    pan_tilt_rotation =  PanYTiltX2matrix(pan, tilt);
    rotation = pan_tilt_rotation * base_rotation;
    rot_vec = rotationMatrixToVector(rotation');    
    camera([4:6]) = rot_vec;
    camera([7:9]) = cc; 
    cameras(i,:) = camera;    
end

%{
n_channel = 1;
[distance_maps] = camera_to_distance_map(cameras, model_points, ...
                    model_line_segment, dist_h, dist_w);

batch_size = 8;

N = size(distance_maps, 4);
h = size(distance_maps, 1);
w = size(distance_maps, 2);

assert(batch_size*10<N);

debug_data = {};
for i = [1:10]
    temp = zeros(h, w, n_channel, batch_size);    
    for j = [1:batch_size]
        temp(:,:,:,j) = distance_maps(:,:, :, (i-1)*batch_size+j);        
    end
    debug_data{i} = single(temp);
end
%}

%save('debug_data_v3.mat', 'debug_data', 'cameras', 'pan_angles');
%save('pure_pan_v2.mat', 'cameras', 'edge_maps', 'pan_angles', 'distance_maps');


