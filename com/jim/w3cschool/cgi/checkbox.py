#!/usr/bin/python3

# coding=utf-8
# 引入 CGI 处理模块
import cgi

# 创建 FieldStorage的实例
form = cgi.FieldStorage()

# 接收字段数据
if form.getvalue('google'):
    google_flag = "是"
else:
    google_flag = "否"

if form.getvalue('youj'):
    youj_flag = "是"
else:
    youj_flag = "否"

print("Content-type:text/html")
print()
print("<html>")
print("<head>")
print("<title>W3Cschool教程 CGI 测试实例</title>")
print("</head>")
print("<body>")
print("<h2> W3Cschool教程是否选择了 : %s</h2>" % youj_flag)
print("<h2> Google 是否选择了 : %s</h2>" % google_flag)
print("</body>")
print("</html>")
