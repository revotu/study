# -*- coding: utf-8 -*-

import os
import json
import urllib

with open(r'D:\Documents\WeChat Files\dltdlt3636\Files\image(3).json') as f:
    content = f.read()

images = json.loads(content)

index = 1
for image in images:
    name = os.path.basename(image)
    print index
    index += 1
    resp = urllib.urlopen(image).read()

    with open(name, 'wb') as f:
        f.write(resp)