import time
import hashlib
import random

access_key = "439e0de9"
access_secret = "0d248280a338"
timestamp = str(int(time.time()))
nonce = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5))
signature = hashlib.sha1(''.join(sorted([access_key, timestamp, nonce, access_secret ]))).hexdigest()
print nonce
print timestamp
print signature
