# -*- coding: utf-8 -*-

import os
import json
import time
import urllib
from multiprocessing import Process, Queue

with open(r'D:\Documents\WeChat Files\dltdlt3636\Files\image(1).json') as f:
    content = f.read()

images = json.loads(content)[:200]

q = Queue()
for image in images:
    q.put(image)


def download(q):
    while not q.empty():
        image = q.get()
        name = os.path.basename(image)
        resp = urllib.urlopen(image).read()
        with open( name, 'wb') as f:
            f.write(resp)


if __name__ == "__main__":
    start = time.time()
    for i in range(10):
        p = Process(target=download, args=(q, ), name='child process %s' % str(i+1))
        p.start()
    p.join()
    end = time.time()
    print '8 processing: %s' % (end - start)

# 8 processing: 99.5850000381