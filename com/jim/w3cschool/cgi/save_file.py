#!/usr/bin/python3
# coding=utf-8

import cgi
import cgitb
import os

"""
激活这个模块之后，如果发生了未被捕获的异常，将会显示详细的已格式化的报告。 
报告显示内容包括每个层级的源代码摘录，还有当前正在运行的函数的参数和局部变量值，以帮助你调试问题。 
你也可以选择将此信息保存至文件而不是将其发送至浏览器。
此函数可通过设置 sys.excepthook 的值以使 cgitb 模块接管解释器默认的异常处理机制。
"""
cgitb.enable()

form = cgi.FieldStorage()

# 获取文件名
fileitem = form['filename']

# 检测文件是否上传
if fileitem.filename:
    # 设置文件路径
    # 如果你使用的系统是 Unix/Linux，你必须替换文件分隔符，在 window 下只需要使用open() 语句即可：
    fn = os.path.basename(fileitem.filename.replace("\\", "/"))
    filename = os.getcwd() + '/tmp/' + fn
    open(filename, 'wb').write(fileitem.file.read())
    message = '文件 "' + filename + '" 上传成功'
else:
    message = '文件没有上传'

print("Content-type: text/html")
print()
print("""
<html>
<head>
<meta charset="gbk">
<title>W3Cschool教程(w3cschool.cn)</title>
</head>
<body>
   <p>%s</p>
</body>
</html>
""" % (message,))