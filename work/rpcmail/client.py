# -*- coding: utf-8 -*-

import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
c.send_mail('donglongtu@hexin.im', ['donglongtu@163.com', 'donglongtu@hexin.im'], '测试邮件主题', '测试邮件正文')