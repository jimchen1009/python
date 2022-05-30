#!/usr/bin/python3
# 请注意第一行代码，在linux中需要在py文件中正确指定python解释器的路径才能运行
# 在Windows中使用Python CGI文件也需要正确指定python解释器的路径才能运行

import os

"""
文件保存后修改 hello.py，修改文件权限为 755（linux和macos需要在webpy文件夹下使用下面的命令来修改文件读写权限，在Windows环境下需要修改文件的读写权限）：
chmod 755 hello.py
"""

# coding=utf-8
print("Content-type:text/html")  # 指定返回的类型，没有这行代码会报错
print()  # 空行，告诉服务器结束头部
# 以下是要返回的HTML正文
print('<html>')
print('<head>')
print('<title>Hello Word - 我的第一个 CGI 程序！</title>')
print('</head>')
print('<body>')
print('<h2>Hello Word! 我的第一CGI程序</h2>')
print('</body>')
print('</html>')

"""
所有的 CGI 程序都接收以下的环境变量，这些变量在 CGI 程序中发挥了重要的作用：

变量名	描述
CONTENT_TYPE	这个环境变量的值指示所传递来的信息的 MIME 类型。目前，环境变量 CONTENT_TYPE 一般都是：application/x-www-form-urlencoded,他表示数据来自于 HTML 表单。
CONTENT_LENGTH	如果服务器与 CGI 程序信息的传递方式是 POST，这个环境变量即使从标准输入 STDIN 中可以读到的有效数据的字节数。这个环境变量在读取所输入的数据时必须使用。
HTTP_COOKIE	客户机内的 COOKIE 内容。
HTTP_USER_AGENT	提供包含了版本数或其他专有数据的客户浏览器信息。
PATH_INFO	这个环境变量的值表示紧接在 CGI 程序名之后的其他路径信息。它常常作为 CGI 程序的参数出现。
QUERY_STRING	如果服务器与 CGI 程序信息的传递方式是 GET，这个环境变量的值即使所传递的信息。这个信息经跟在 CGI 程序名的后面，两者中间用一个问号'?'分隔。
REMOTE_ADDR	这个环境变量的值是发送请求的客户机的IP地址，例如上面的192.168.1.67。这个值总是存在的。而且它是 Web 客户机需要提供给Web服务器的唯一标识，可以在 CGI 程序中用它来区分不同的 Web 客户机。
REMOTE_HOST	这个环境变量的值包含发送 CGI 请求的客户机的主机名。如果不支持你想查询，则无需定义此环境变量。
REQUEST_METHOD	提供脚本被调用的方法。对于使用 HTTP/1.0 协议的脚本，仅 GET 和 POST 有意义。
SCRIPT_FILENAME	CGI 脚本的完整路径
SCRIPT_NAME	CGI 脚本的的名称
SERVER_NAME	这是你的 WEB 服务器的主机名、别名或IP地址。
SERVER_SOFTWARE	这个环境变量的值包含了调用 CGI 程序的 HTTP 服务器的名称和版本号。例如，上面的值为 Apache/2.2.14(Unix)
"""

print()
print("<b>环境变量</b><br>")
print("<ul>")
for key in os.environ.keys():
    print("<li><span style='color:green'>%30s </span> : %s </li>" % (key, os.environ[key]))
print("</ul>")
