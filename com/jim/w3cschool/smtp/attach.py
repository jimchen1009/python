#!/usr/bin/python3

import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "chenjingjun@aobi.com"  # 用户名
mail_pass = ""  # 口令[本地TODO.txt保存]、或者密码

sender = 'chenjingjun@aobi.com'
receivers = ['915508287@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("W3Cschool教程", 'utf-8')
message['To'] = Header("测试", 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="https://www.w3cschool.cn">W3Cschool教程链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
# 邮件正文内容
message.attach(MIMEText(mail_msg, 'html', 'utf-8'))

# 构造附件1，传送当前目录下的 attachment.txt 文件。 如果有多个附件，可依次构造
att1 = MIMEApplication(open('attachment.txt', 'rb').read())
att1.add_header('Content-Disposition', 'attachment', filename='附件1.txt')
message.attach(att1)

# 指定图片为当前目录
fp = open('attachment.png', 'rb')
att2 = MIMEImage(fp.read())
fp.close()
# 定义图片 ID，在 HTML 文本中引用
att2.add_header('Content-ID', '<image1>')
message.attach(att2)


try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
