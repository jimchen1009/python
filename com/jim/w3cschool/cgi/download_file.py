#!/usr/bin/python3

# HTTP 头部
import urllib.parse
name = urllib.parse.quote("新增区服", encoding="utf-8")  #中文乱码的问题
content = "Content-Disposition: attachment; filename=file.txt".format(name)
print(content)
print()
# 打开文件
fo = open("tmp/新增区服.txt", mode="r", encoding="utf-8")   #使用rb下载文件未空
print(fo.read())
# 关闭文件
fo.close()
