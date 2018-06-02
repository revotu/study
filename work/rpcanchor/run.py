import zerorpc
from settings import logger, DEFAULT_SERVER_PORT
from anchor import RetryAnchorRecognize
import sys

port = DEFAULT_SERVER_PORT


class MainRpc(object):
    def rec(self, img):
        res = {
            'data': None,
            'code': 102,
            'msg': ''
        }
        try:
            data = RetryAnchorRecognize().detect(img)
            res['msg'] = 'ok'
            res['code'] = 0
            res['data'] = data
        except Exception, e:
            res['msg'] = 'error'
            res['code'] = 103
            logger.error(str(e))

        return res


if len(sys.argv) >= 2:
    port = sys.argv[1]

server = zerorpc.Server(MainRpc())
server.bind('tcp://0.0.0.0:%s' % port)
logger.info('start port %s ok!' % port)

server.run()
