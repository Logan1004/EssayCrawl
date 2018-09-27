# --*-- coding: utf-8 --*--

import os
import sys

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(to_addr,message):
    from_addr = 'testEmail1004@126.com'
    password = 'l123456'
    smtp_server = 'smtp.126.com'
    # message = 'test'
    msg = MIMEText(message, 'html', 'utf-8')

    server = smtplib.SMTP(smtp_server, 25)
    #server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)

    msg['From'] = _format_addr(u'该修bug了！！<%s>' % from_addr)
    msg['To'] = _format_addr(u'维护 <%s>' % to_addr)
    msg['Subject'] = Header(u'网站监控异常', 'utf-8').encode()
    server.sendmail(from_addr, [to_addr], msg.as_string())

    server.quit()

if __name__ == "__main__":
    try:
        message = " "
        send_mail('1585084146@qq.com',message)
        send_mail('1264160868@qq.com',message)
        send_mail('1228974364@qq.com',message)
    except Exception as e:
        print(str(e))