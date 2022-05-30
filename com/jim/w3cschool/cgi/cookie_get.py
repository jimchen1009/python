#!/usr/bin/python3
# coding=utf-8

# 导入模块

import os

import http.cookies

print("Content-type: text/html")
print()
print("""
<html>
<head>
<meta charset="gbk">
<title>W3Cschool教程(w3cschool.cn)</title>
</head>
<body>
<h1>读取cookie信息</h1>
""")

if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ.get('HTTP_COOKIE')
    c = http.cookies.SimpleCookie()
    c.load(cookie_string)
    try:
        data = c['name'].value
        print("cookie data: " + data + "<br>")
    except KeyError:
        print("cookie 没有设置或者已过去<br>")

print("""
</body>
</html>
""")
