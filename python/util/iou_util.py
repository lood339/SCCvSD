import cv2 as cv
import numpy as np
from projective_camera import ProjectiveCamera

class IouUtil:
    @staticmethod
    def homography_warp(h, image, dst_size, background_color):
        """
        :param h:
        :param image:
        :param dst_size:
        :param background_color:
        :return:
        """
        assert h.shape == (3, 3)
        im_dst = cv.warpPerspective(image, h, dst_size, borderMode=cv.BORDER_CONSTANT, borderValue=background_color)
        return im_dst



def ut_homography_warp():
    camera_data = np.asarray([640, 360, 3081.976880,
                              1.746393, -0.321347, 0.266827,
                              52.816224, -54.753716, 19.960425])

    u, v, fl = camera_data[0:3]
    rod_rot = camera_data[3:6]
    cc = camera_data[6:9]

    camera = ProjectiveCamera(fl, u, v, cc, rod_rot)
    h = camera.get_homography()
    inv_h = np.linalg.inv(h)
    im = cv.imread('../../data/16.jpg')
    assert im is not None


    #homography_warp(h, image, dst_size, background_color):
    template_size = (115, 74);
    warped_im = IouUtil.homography_warp(inv_h, im, (115, 74), (0, 0, 0))
    cv.imwrite('warped_image.jpg', warped_im)




if __name__ == '__main__':
    ut_homography_warp()
