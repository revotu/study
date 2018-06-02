# Image alignment for better rec
# Zhilun Yang
# 2017/10/31

import os, cv2
import scipy as sp
import scipy.misc
import numpy as np


def align_image(im_temp, im_align):
    # align image with temp image using cv2
    p1 = im_align.astype(np.float32)
    p2 = im_temp.astype(np.float32)

    warp_mode = cv2.MOTION_AFFINE  # MOTION_TRANSLATION | MOTION_EUCLIDEAN | MOTION_AFFINE | MOTION_HOMOGRAPHY
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else:
        warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000,  1e-7)
    (cc, warp_matrix) = cv2.findTransformECC(p1, p2,warp_matrix, warp_mode, criteria)
    # print "_align_two_rasters: cc:{}".format(cc)

    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_function = cv2.warpPerspective
    else:
        warp_function = cv2.warpAffine
    im_result = warp_function(im_temp, warp_matrix, (im_align.shape[1], im_align.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    im_result[im_result == 0] = np.average(im_result)
    return im_result


def process(FILE_temp, FILE_input):
    im_temp     = sp.misc.imread(FILE_temp, True)           # the TEMPLATE
    im_align    = sp.misc.imread(FILE_input, True)          # the image to be transformed
    im_result   = align_image(im_temp, im_align)            # aligned result image

    # vis merge result
    merge_result = cv2.addWeighted(im_align, 0.5, im_result, 0.5, 0)
    cv2.imwrite(os.path.join('.', 'affine', 'merge_temp2_test1.png'), merge_result)
    return im_result


basedir = os.path.join('.', 'examples')
FILE_temp = os.path.join(basedir, "temp2.jpg")
FILE_input = os.path.join(basedir, "test1.jpg")
im_result = process(FILE_temp, FILE_input)
