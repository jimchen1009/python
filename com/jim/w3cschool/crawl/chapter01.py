"""
Beautiful Soup 的安装方法和 requests 一样，使用如下指令安装(也是二选一)：
pip install beautifulsoup4
easy_install beautifulsoup4

一个强大的第三方库，都会有一个详细的官方文档。我们很幸运，Beautiful Soup 也是有中文的官方文档：http://beautifulsoup.readthedocs.io/zh_CN/latest/
"""

# -*- coding:UTF-8 -*-
import sys

import requests
from bs4 import BeautifulSoup


class downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数

    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = 'gbk'  # 查看网页的源码发现网页的编码方式gbk
        html = req.text
        div_bf = BeautifulSoup(html, features="html.parser")
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]), features="html.parser")
        a = a_bf.find_all('a')
        self.nums = len(a[13:])  # 剔除不必要的章节，并统计章节数
        for each in a[13:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    @staticmethod
    def get_contents(target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, features="html.parser")
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    @staticmethod
    def writer(name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《一年永恒》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '一念永恒.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" % float(i / dl.nums) + '\r')
        sys.stdout.flush()
    print('《一年永恒》下载完成')
