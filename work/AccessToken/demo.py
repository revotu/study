import time
import random
import hashlib
access_key = "99fc83d8"
access_secret = "46bdd2070dd5"
# timestamp = str(int(time.time()))
# nonce = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5))
timestamp = '1478511151'
nonce = 'bsdew'
print ''.join(sorted([access_key, timestamp, nonce, access_secret ]))
signature = hashlib.sha1(''.join(sorted([access_key, timestamp, nonce, access_secret ]))).hexdigest()

print timestamp, nonce, signature