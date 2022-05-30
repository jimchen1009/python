#!/usr/bin/python3
# coding=utf-8

print('Content-Type: text/html')
# Cookie 的设置非常简单，cookie 会在 http 头部单独发送。
print('Set-Cookie: name="W3Cschool";expires=Thu 02 Dec 2023 18:30:00 GMT')
print()
print("""
<html>
  <head>
    <meta charset="gbk">
    <title>W3Cschool教程(w3cschool.cn)</title>
  </head>
    <body>
        <h1>Cookie set OK!</h1>
    </body>
</html>
""")
