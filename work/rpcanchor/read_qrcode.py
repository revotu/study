# -*-coding:utf-8-*-
# --------------------------------------------
# QRcode enhancement
# Zhilun Yang

import os
import cv2
import glob
import json
import urllib
import numpy as np


def _url_to_image(url):
    # download the image, convert it to a NumPy array, and then read it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def _crop_qrcode_by_image(im, fname):
    # 1. use connected components to filter qrcode image
    # 2. use top/bot position to set page index

    im_h, im_w = im.shape
    (thresh, im_bw) = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_erosion = cv2.erode(cv2.dilate(im_bw, np.ones((3, 3)), iterations=1), np.ones((15, 15)), iterations=1)
    # cv2.imwrite('D:\Desktop\ErrorImage\\' + os.path.basename(fname), img_erosion)

    im_vis = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
    LIST_qrcode = list()
    page_idx = 5
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(255 - img_erosion)
    for inst in stats[1 : ]:
        x, y, w, h = inst[0], inst[1], inst[2], inst[3]
        ratio = w * 1.0 / h    # qrcode is square
        if ratio >= 0.85 and ratio <= 1.15 and h >= 70 and w >= 70 and h <= 160 and w <= 160:
            
            # we can add x, y position to filter more
            # assert image is in the right direction，纸张处于正常位置
            if x <= 0.3 * im_w and y >= 0.7 * im_h:     # left bottom
                page_idx = 1    # maybe more than 2 page
                im_crop = im[y : y + h, x : x + w]
                cv2.rectangle(im_vis, (x, y), (x + w, y + h), (0, 0, 255), 5)
                LIST_qrcode.append((im_crop, page_idx))

            elif x >= 0.7 * im_w and y <= 0.2 * im_h:   # right top
                page_idx = 2
                im_crop = im[y : y + h, x : x + w]
                cv2.rectangle(im_vis, (x, y), (x + w, y + h), (0, 0, 255), 5)
                LIST_qrcode.append((im_crop, page_idx))

            elif x >= 0.7 * im_w and y >= 0.7 * im_h:   # right bottom
                page_idx = 2
                im_crop = im[y : y + h, x : x + w]
                cv2.rectangle(im_vis, (x, y), (x + w, y + h), (0, 0, 255), 5)
                LIST_qrcode.append((im_crop, page_idx))

    # assert there is only one qrcode image
    cv2.imwrite('D:\\Desktop\\ErrorImage\\qr_result_1\\' + str(page_idx) + '-000' + os.path.basename(fname), im_vis)
    if len(LIST_qrcode) != 1: 
        print 'there is more than 1 qrcode image'

        # used for debug vis
        # print fname
        # for inst in stats[1 : ]:
        #     x, y, w, h = inst[0], inst[1], inst[2], inst[3]
        #     ratio = w * 1.0 / h    # qrcode is square
        #     if h >= 50 and w >= 50 and h <= 160 and w <= 160:
        #         if ratio >= 0.85 and ratio <= 1.15:
        #             cv2.rectangle(im_vis, (x, y), (x + w, y + h), (0, 0, 255), 5)
        #             print ratio
        #
        # cv2.imwrite('D:\Desktop\ErrorImage\\' + os.path.basename(fname), im_vis)
        # cv2.imwrite('D:\Desktop\ErrorImage\\' + os.path.basename(fname) + 'sss.jpg', img_erosion)
        return False, False
    else:
        # qrimage is in LIST_qrcode
        return LIST_qrcode[0]


def _crop_qrcode_by_json(image):
    # use sheet json to filter image
    return ''


# download data from http://ai.alexwang.cc/api/data/exercise/error/anchor?exercise_uid=4c8aa82902&type=anchor
# data = json.loads(open('FeHelper-20171121104224.json', 'r').read())
# for inst in data['data']:
#     image = _url_to_image(inst['url'])
#     cv2.imwrite(os.path.basename(inst['url']), image)


# 需查看现有代码是否做了二维码过滤与定位工作，但是 sheet 答题卡应该也是定义了二维码
# 1. use _crop_qrcode to get qrcode image do it again. LOCAL_QRCODE_BIN code
for fname in glob.glob(r'D:\Desktop\ErrorImage\down\**\*.jpg'):
# for fname in glob.glob(r'D:\Desktop\ErrorImage\error-debug\*.jpg'):
    # if '3nazc6lhdprz5zvtw3g59444d-origin.jpg' not in fname: continue
    image, page_idx = _crop_qrcode_by_image(cv2.imread(fname, 0), fname)
