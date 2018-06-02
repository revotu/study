import zerorpc

client = zerorpc.Client()
client.connect("tcp://127.0.0.1:8190")

origin_image_url = 'http://image.alexwang.cc/sigma/exercise/18841f1608/suduus08q12yekdsp1fc32a9d-origin.jpg'


print client.rec(origin_image_url)
