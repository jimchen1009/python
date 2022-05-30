#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"       # 设置服务器
mail_user = "915508287@qq.com"  # 用户名
mail_pass = ""  # 口令[微信保存]、或者密码

sender = '915508287@qq.com'
receivers = ['chenjingjun@aobi.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="https://www.w3cschool.cn">这是一个链接</a></p>
"""

message = MIMEText(_text=mail_msg, _subtype='html', _charset='utf-8')
message['From'] = Header("W3Cschool教程", 'utf-8')
message['To'] = Header("测试", 'utf-8')

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")

"""
Date: Mon, 14 Feb 2022 14:39:33 +0800
Received: from xmbgsz5.mail.qq.com (unknown [113.108.92.46])
    by bizmx39.qq.com (NewMx) with SMTP id 
    for <chenjingjun@aobi.com>; Mon, 14 Feb 2022 14:39:31 +0800
X-QQ-SPAM: none
X-QQ-HITDIVERSE: none
X-QQ-FEAT: 7Lv6dviieSSPx4ecrIOylX04g1ai59oC0an7VoNGxyHpAGvsFfL+U4dk1JjuQ
    rwSKe43p1hbyf3ki61szKuGe5y8j+bghSpblsHd4McvT3PxdB5aQgw3Ttjw/dHqohcuTa3t
    pdTEDvBqVVkuaX9V5n1oAjo+rMZcgWaI5Jdsxb7JFf5P/ErYP9xV64NX3pP4l8T2xLAX4u+
    iFbfZydT8Ihder9x04vnNfkFq4luwg6IdIHjFRvTI94PMx0+YiYYxW1zSbxMbCjKVymAjXs
    dApxTt1bxqx7B7CV/Fk47BebaomllHwDxvxAaLySzd4t7W2HJbATF4tpr/UMcXYedQrf5jF
    E5T2aW5U29HieBiLS7DUY4aLH4tlg==
X-QQ-MAILINFO: MJpDEouUnwTTAj+2jADRg04ym3aCn+yhj8QDv4mtkK8O3jaA4kLTxFVMd
    vFrK1iT3/kZpkZ4I71UXD6KhLipDVVUoO5nOhUkiheGv4XWcaQ8UGPS/d4qo6cx7oJCbdZZ
    LDnCP8uvTvek9S14gfWbGjEWNxGIPZoarg==
X-QQ-mid: bizmx39t1644820771trqsjaezy
X-QQ-CSender: 915508287@qq.com
X-QQ-ORGSender: 915508287@qq.com
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=qq.com; s=s201512;
    t=1644820771; bh=1FMhQhz61/44blVqZ66x6Fqyo9zPGhCz8CqnYcgUCKM=;
    h=From:To:Subject;
    b=V4CVuz+BTha21GLSzEUYT9627SRJPh8ZgmuBCr6XWLYnVst+4F4mXkoPnCyO7aEVV
    p69BD94E8TKMOcBUONDfU+bB3Qp0UnbiDlZnwi5PqQdgw2BhntN7ak22eaVxF/agjd
    zpXj0lOTCk063BmVBvf49HMHr3Q2UOZSE8BCrJE8=
Received: from CHENJINGJUN.rd.com ([221.4.53.36])
    by newxmesmtplogicsvrszb6.qq.com (NewEsmtp) with SMTP
    id 9DEB266A; Mon, 14 Feb 2022 14:39:30 +0800
Message-ID: <tencent_C5ABD5DAC42323F94606ECF02A5C63C61708@qq.com>
    PzlPSPUbdBReQLZFQspdRxpZLFlypKMCH0QD7Yi8dIyLZ+lepN49iDI2g4uAlG9AiIAWK//06reS
    fCvoHzKY7IPXoV38BGHvwnPS7phBcH+jf5pyh2D+HezTxbzQdSOzIAxAXjieeRSvta+gWwK6YTsk
    czVI4y0ugbaewkkvJid19hQK8ns6uhKuOTu/LllTWpXNaLKZ/5GX56vSJRtPNLle/G7Yqkeh/Ssd
    b9MGrJzAlrLIpPZxwWFSozDSC9Fx3CPIzpLpv0gfYkY5Cy4FWgR61IYJN+PCD+h+DRGJihVp3VNE
    gQTJF6xNehnoaDa8r1q6gmPwyhF3RSkDk86VwwZKRK0DO3UrikpMSbqg8kWbuNqsk7UgWOJXZHfH
    fVYFxvV9/OFey65IoSeef0RzJV3f7bT87Ann32WLnOMq1PcZ5oB4jNMyr7xQq93v7F5LEDqHa8pq
    BUV2eEpH+XWRFgOUmN1HsUjL1LW+vgukivddm7nVkDqt4dNpC3jwRBr+DzQtM0xHKqKzubnXxRJl
    vQQ4Qdv2NZZrb8svrQgfcrehRa0DUPJMPuizFjlIIY3g26I5L4W3xDQH5Wx7c1NtHgTV0hfVOVom
    ag0NPJbHsxKLJxpA0ldB1Sa/K+t8s9Y9BWVt5hT0AFXUxpGiqNna+Pf9XXwlzDIWDl1by/hqeWvm
    wD71KTYpkH4xx2GATSN/irruyFl28jzJgKJ68PTOhBC57YsbrYyamp7GG3A06XmiRcu81L6noTsv
    a+3U18Q3wf+Zm6uc3UJMjTTEhKFMTytEySUe2EyQvXUukK1uzbKZFyIV4XYszWDq49wAdFTSOyfx
    nWvN3LIAB+oYqLirYquD8e6gx/GJyJ1BkeBgWzlpKG
Sender: 915508287@qq.com
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: base64
From: =?utf-8?b?VzNDc2Nob29s5pWZ56iL?=
To: =?utf-8?b?5rWL6K+V?=
Subject: =?utf-8?b?UHl0aG9uIFNNVFAg6YKu5Lu25rWL6K+V?=
"""
