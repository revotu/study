# -*- coding: utf-8 -*-

import os
import json
import time
import urllib
import threading
import Queue

with open(r'D:\Documents\WeChat Files\dltdlt3636\Files\image(1).json') as f:
    content = f.read()

images = json.loads(content)[:200]

q = Queue.Queue()
for image in images:
    q.put(image)


def download(q):
    while not q.empty():
        image = q.get()
        name = os.path.basename(image)
        resp = urllib.urlopen(image).read()
        with open( name, 'wb') as f:
            f.write(resp)


start = time.time()
for i in range(8):
    t = threading.Thread(target=download, args=(q, ), name='child thread %s' % str(i+1))
    t.start()
t.join()
end = time.time()
print '8 threading: %s' % (end - start)

# 1 threading: 207.596999884
# 5 threading: 91.0520000458
# 8 threading: 86.6410000324
# 10 threading: 116.773000002
