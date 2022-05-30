#!/usr/bin/python3
# coding=utf-8

# CGI处理模块
import cgi

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取数据, 它也可以处理浏览器提交的 POST 表单数据
site_name = form.getvalue('name')
site_url = form.getvalue('url')

print("Content-type:text/html")
print()
print("<html>")
print("<head>")
print("<title>W3Cschool教程 CGI 测试实例</title>")
print("</head>")
print("<body>")
print("<h2>%s官网：%s</h2>" % (site_name, site_url))
print("</body>")
print("</html>")
