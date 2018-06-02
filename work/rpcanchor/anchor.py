# -*- coding: utf-8 -*-

import cv2
import urllib
from settings import logger
import numpy as np


class RetryAnchorRecognize(object):
    """定位点识别失败时的后备方案"""

    def _check_anchor_im(self, anchor_im):
        h, w = anchor_im.shape
        black_count = len(np.where(anchor_im == 0)[0])
        black_ratio = 1.0 * black_count / (h * w)

        if black_ratio >= 0.7:
            return True
        else:
            return False

    def _get_corner_anchor(self, im_h, anchor_list):

        # check FLIP
        init_top = 0
        init_bot = 0
        for anchor in anchor_list:
            x, y, w, h = anchor[0], anchor[1], anchor[2], anchor[3]
            if y <= 0.5 * im_h:
                init_top += 1
            else:
                init_bot += 1

        if init_top > init_bot:
            image_is_flip = 0
        else:
            image_is_flip = 1

        # check corner pts
        list_x_add_y = list()
        list_x_sub_y = list()
        for anchor in anchor_list:
            x, y, w, h = anchor[0], anchor[1], anchor[2], anchor[3]
            list_x_add_y.append((x + y))
            list_x_sub_y.append((x - y))

        bot_left = anchor_list[list_x_sub_y.index(min(list_x_sub_y))]
        bot_right = anchor_list[list_x_add_y.index(max(list_x_add_y))]
        top_left = anchor_list[list_x_add_y.index(min(list_x_add_y))]
        top_right = anchor_list[list_x_sub_y.index(max(list_x_sub_y))]

        result = {
            'imageAnchorPoints': {'topLeft': {"x": float(top_left[0]), "y": float(top_left[1])},
                                  'bottomLeft': {"x": float(bot_left[0]), "y": float(bot_left[1] + bot_left[3])},
                                  'topRight': {"x": float(top_right[0] + top_right[2]), "y": float(top_right[1])},
                                  'bottomRight': {"x": float(bot_right[0] + bot_right[2]), "y": float(bot_right[1] + bot_right[3])}},
            'imageKeyPoints': [[float(top_left[0]), float(top_left[1])], [float(top_right[0] + top_right[2]), float(top_right[1])],
                               [float(bot_right[0] + bot_right[2]), float(bot_right[1] + bot_right[3])], [float(bot_left[0]), float(bot_left[1] + bot_left[3])]],
            'imageIsFlip': image_is_flip,
            'orientationIsValid': 1,
            'imageIsValid': 0
        }

        flag_error = False
        if top_left[1] == bot_left[1] or top_right[1] == bot_right[1]:
            flag_error = True

        cal_keypoints = [top_left, top_right, bot_right, bot_left]
        return result, flag_error, cal_keypoints

    def _pt_dist(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def _anchor_cos(self, p0, p1, p2):
        # p1
        # |  anchor
        # p0 - p2
        vo = (0, 0)
        v1 = (p1[0] - p0[0], p1[1] - p0[1])
        v2 = (p2[0] - p0[0], p2[1] - p0[1])
        return abs(v1[0] * v2[0] + v1[1] * v2[1]) / (self._pt_dist(vo, v1) * self._pt_dist(vo, v2))

    def _compute_image_valid(self, kps):
        anchor_cosines = [
            self._anchor_cos(kps[0], kps[-1], kps[1]),
            self._anchor_cos(kps[1], kps[0], kps[2]),
            self._anchor_cos(kps[2], kps[1], kps[3]),
            self._anchor_cos(kps[3], kps[2], kps[0]),
        ]

        if max(anchor_cosines) > 0.1:
            print 'key points in this image is not rectangle'
            return 1
        return 2

    def _calibrate_image(self, keypoints):
        return self._compute_image_valid(keypoints)

    def _url_to_image(self, url):
        # download the image, convert it to a NumPy array, and then read it into OpenCV format
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        return image

    def detect(self, im):
        """定位点识别函数"""

        if not isinstance(im, np.ndarray):
            # logger.info('INPUT: %s' % im)
            if isinstance(im, (str, unicode)):
                if im.startswith(('http:', 'https:')):
                    im = self._url_to_image(im)
                else:
                    im = cv2.imdecode(np.fromstring(im, np.uint8), 1)
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        (thresh, im_bw) = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        anchor_list = list()
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(255 - im_bw)
        for i, inst in enumerate(stats[1:]):
            x, y, w, h = inst[0], inst[1], inst[2], inst[3]
            ratio = 1.0 * w / h
            if 1.35 <= ratio <= 4.0 and h >= 10 and w >= 15:
                im_crop = im_bw[y: y + h, x: x + w]
                if self._check_anchor_im(im_crop):
                    anchor_list.append(inst)

        result, flag_error, cal_keypoints = self._get_corner_anchor(im.shape[0], anchor_list)
        anchor_check = self._calibrate_image(cal_keypoints)

        if anchor_check == 2 and not flag_error and result['imageAnchorPoints']['topLeft']['x'] <= im.shape[
            1] * 0.25 and result['imageAnchorPoints']['topRight']['x'] >= im.shape[1] * 0.75 and not result['imageIsFlip']:
            result['imageIsValid'] = 2
        else:
            result['imageIsValid'] = 1

        logger.info('OUTPUT: %s' % result)
        return result
