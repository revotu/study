# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText


MAIL_HOST = 'smtp.exmail.qq.com'
MAIL_USER = 'donglongtu@hexin.im'
MAIL_PASS = 'LongTu3636'


class MailRPC(object):

    def send_mail(self, from_addr, to_addrs, subject, text):
        msg = MIMEText(text, _subtype='html', _charset='utf8')
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ";".join(to_addrs)

        try:
            server = smtplib.SMTP_SSL()
            server.connect(MAIL_HOST)
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(from_addr, to_addrs, msg.as_string())
            server.close()
        except Exception, e:
            print str(e)
            return False
        return True

MailRPC().send_mail('donglongtu@hexin.im', ['632624460@qq.com', 'donglongtu@hexin.im'], 'MAIL SUBJECT', 'MAIL CONTENT')