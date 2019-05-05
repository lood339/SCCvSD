import numpy as np
import cv2 as cv

import random
from rotation_util import RotationUtil
from projective_camera import ProjectiveCamera

class SyntheticUtil:
    @staticmethod
    def camera_to_edge_image(camera_data,
                             model_points, model_line_segment,
                             im_h, im_w, line_width=4):
        """
         Project (line) model images using the camera
        :param camera_data: 9 numbers
        :param model_points:
        :param model_line_segment:
        :param im_h:
        :param im_w:
        :return: H * W * 3 OpenCV image
        """
        assert camera_data.shape[0] == 9

        u, v, fl = camera_data[0:3]
        rod_rot = camera_data[3:6]
        cc = camera_data[6:9]

        camera = ProjectiveCamera(fl, u, v, cc, rod_rot)
        im = np.zeros((im_h, im_w, 3), dtype=np.uint8)
        n = model_line_segment.shape[0]
        color = (255,255,255)
        for i in range(n):
            idx1, idx2 = model_line_segment[i][0], model_line_segment[i][1]
            p1, p2 = model_points[idx1], model_points[idx2]
            q1 = camera.project_3d(p1[0], p1[1], 0.0, 1.0)
            q2 = camera.project_3d(p2[0], p2[1], 0.0, 1.0)
            q1 = np.rint(q1).astype(np.int)
            q2 = np.rint(q2).astype(np.int)
            cv.line(im, tuple(q1), tuple(q2), color, thickness=line_width)
        return im

    @staticmethod
    def generate_ptz_cameras(cc_statistics,
                             fl_statistics,
                             roll_statistics,
                             pan_range, tilt_range,
                             u, v,
                             camera_num):
        """
        Input: PTZ camera base information
        Output: randomly sampled camera parameters
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


def ut_camera_to_edge_image():
    import scipy.io as sio
    # this camera is from UoT world cup dataset, train, index 16
    camera_data = np.asarray([640,	360, 3081.976880,
                              1.746393,	 -0.321347,	 0.266827,
                              52.816224,	 -54.753716, 19.960425])
    data = sio.loadmat('../../data/worldcup2014.mat')
    model_points = data['points']
    model_line_index = data['line_segment_index']
    im = SyntheticUtil.camera_to_edge_image(camera_data, model_points, model_line_index, 720, 1280, line_width=4)
    cv.imwrite('debug_train_16.jpg', im)

def ut_generate_ptz_cameras():
    import scipy.io as sio
    data = sio.loadmat('../../data/soccer_camera_center_focal_length.mat')
    print(data.keys())

    """
    cc_mean, cc_std, cc_min, cc_max = cc_statistics
    fl_mean, fl_std, fl_min, fl_max = fl_statistics
    roll_mean, roll_std, roll_min, roll_max = roll_statistics
    pan_min, pan_max = pan_range
    tilt_min, tilt_max = tilt_range
    """
    


if __name__ == '__main__':
    #ut_camera_to_edge_image()
    ut_generate_ptz_cameras()
