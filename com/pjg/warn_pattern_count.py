import argparse
import datetime
import getpass
import os
import re
from re import Pattern

import demjson

PATTERN_REPLACE_PATTERNS = [
    [re.compile(r'at com\.sun\.proxy\.\$Proxy\d+\.'), r'com.sun.proxy.\\$Proxy\\d+.'],
    [re.compile(r'sun\.reflect\.GeneratedMethodAccessor\d+\.invoke'), r'sun.reflect.GeneratedMethodAccessor\\d+.invoke'],
    [re.compile(r'\.java:\d+\)'), r'.java:\\d+)']
]


OTHER_WARN_CHARACTERS_LIST = [
    "503 Service Unavailable",
    "com.linecorp.armeria.client.ResponseTimeoutException"
]


class MessageBatch:
    def __init__(self, message: str, count: int):
        self.message = message
        self.count = count

    def __str__(self):
        return str.format("{}\t{}", self.count, self.message.strip())


class WarnPattern:
    def __init__(self, pattern_str: str, parameter: dict):
        self.pattern_str = pattern_str
        self.pattern = re.compile(pattern_str)
        self.parameter = parameter
        self.count = 0

    def get_warn_count(self):
        return self.parameter["warnCount"]

    def __str__(self):
        return str.format("currentCount:{}\t\twarnCount:{}\n{}", self.count, self.get_warn_count(), self.pattern_str.strip())


def read_path_message_batch(input_path: str, line_pattern_str: str, count_pattern_str: str, name_like: str = ""):
    message_batch_list = []
    input_filenames = os.listdir(input_path)
    for input_filename in input_filenames:
        if len(name_like) > 0 and re.search(name_like, input_filename) is None:
            continue
        file_path = str.format("{}\\{}", input_path, input_filename)
        if os.path.isdir(file_path):
            continue
        line_batch_list0 = read_file_line_batch(file_path, line_pattern_str, count_pattern_str)
        for line_batch0 in line_batch_list0:
            message_batch_list.append(line_batch0)
    return message_batch_list


def read_file_line_batch(file_path: str, line_pattern_str: str, count_pattern_str: str):
    message_batch_list = []
    if line_pattern_str is None or len(line_pattern_str.strip()) == 0:
        line_pattern = None
    else:
        line_pattern = re.compile(line_pattern_str, re.M | re.I)
    if count_pattern_str is None or len(count_pattern_str.strip()) == 0:
        count_pattern = None
    else:
        count_pattern = re.compile(count_pattern_str, re.M | re.I)
    read_line = MessageBatch("", 1)
    with open(file_path, 'r', encoding="UTF-8") as file:
        file_lines = file.readlines()
        for file_line in file_lines:
            file_line = file_line.rstrip()
            if len(file_line) == 0:
                append_line_batch(read_line, message_batch_list)
                continue
            if line_pattern is not None and line_pattern.search(file_line):
                append_line_batch(read_line, message_batch_list)
                if count_pattern is not None:
                    matcher = count_pattern.match(file_line.strip())
                if matcher:
                    count = matcher.group("count")
                    read_line.count = int(count)
                line_batch_join_string(read_line, file_line, count_pattern)
            else:
                line_batch_join_string(read_line, file_line, count_pattern)
    append_line_batch(read_line, message_batch_list)
    return message_batch_list


def append_line_batch(read_line: MessageBatch, line_batch_list: list):
    if len(read_line.message) != 0:
        line_batch_list.append(MessageBatch(read_line.message, read_line.count))
    read_line.message = ""
    read_line.count = 1


def line_batch_join_string(read_line: MessageBatch, file_line: str, remove_pattern: Pattern):
    if remove_pattern is not None:
        file_line = remove_pattern.sub("", file_line, count=10)
    if len(read_line.message) > 0:
        read_line.message = read_line.message + "\n"
    read_line.message = read_line.message + file_line


def prepare_warn_pattern(pattern_batch_list: list):
    warn_pattern_list = []
    for pattern_batch in pattern_batch_list:
        line_batch = pattern_batch.message
        splits = line_batch.split("\n", 1)
        # 字符串的key值没有引号，用 demjson.decode(）
        # 正则表达式要按照 ACII顺序排列: [-\d_\w+]
        parameter = demjson.decode(splits[0])
        line_splits = splits[1].split("\n", 1)
        if len(line_splits) > 1:
            line_batch1 = line_splits[0]
            line_batch2 = line_splits[1]
            for ch in "[]()$":
                line_batch2 = line_batch2.replace(ch, "\\" + ch)
            line_batch = line_batch1 + "\n" + line_batch2
        else:
            line_batch = line_splits[0]
        for PATTERN_REPLACE_PATTERN in PATTERN_REPLACE_PATTERNS:
            pattern = PATTERN_REPLACE_PATTERN[0]
            replace = PATTERN_REPLACE_PATTERN[1]
            matcher = pattern.search(line_batch)
            if matcher:
                line_batch = pattern.sub(replace, line_batch)
        warn_pattern_list.append(WarnPattern(line_batch, parameter))
    return warn_pattern_list


def write_message_with_title(output_path: str, filename: str, title: str, message_list: list):
    if len(message_list) == 0:
        return
    file_path = output_path + "\\" + filename
    if os.path.exists(file_path):
        os.remove(file_path)
    file = open(file_path, 'w', encoding="UTF-8")
    file.write("\n")
    file.write("|=======================================================================================================================================|\n\n")
    file.write("\t\t" + title + "\n\n")
    file.write("|=======================================================================================================================================|\n\n")
    file.write("\n")
    for message in message_list:
        file.write(str(message).strip() + "\n\n")
    file.flush()
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='information')
    parser.add_argument('--input_path', dest="input_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn\decode', type=str, help='输入路径')
    parser.add_argument('--output_path', dest="output_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn\count', type=str, help='输出路径')
    parser.add_argument('--pattern_path', dest="pattern_path", default=r'C:\ProjectG\pjg-server\src\test\resources\tencent', type=str, help='报错模板路径')
    parser.add_argument('--filter_count', dest="filter_count", default=True, type=bool, help='是否检测报错数量')
    args = parser.parse_args()

    user_name = getpass.getuser()
    output_path = args.output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    line_pattern_str = r"(?P<time>\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\])"
    count_pattern_str = r"(?P<ip>\d+.\d+.\d+.\d+)\t(?P<count>\d+)\t(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\t"
    message_batch_list = read_path_message_batch(args.input_path, line_pattern_str, count_pattern_str)
    pattern_batch_list = read_path_message_batch(args.pattern_path, "", "", r"warn_pattern\d+\.txt")
    warn_pattern_list = prepare_warn_pattern(pattern_batch_list)
    # 没有匹配到的报错数据
    no_match_message_batch_list = []
    # 匹配搭配到忽略的报错
    ignore_message_batch_list = []
    # 其他报错数据
    other_message_batch_list = []
    for message_batch in message_batch_list:
        is_other_warn = False
        for OTHER_WARN_CHARACTERS in OTHER_WARN_CHARACTERS_LIST:
            if message_batch.message.find(OTHER_WARN_CHARACTERS) != -1:
                is_other_warn = True
        if is_other_warn:
            other_message_batch_list.append(message_batch)
            continue
        match_success = False
        for warn_pattern in warn_pattern_list:
            matcher = warn_pattern.pattern.search(message_batch.message)
            if matcher:
                warn_pattern.count = warn_pattern.count + message_batch.count
                match_success = True
        if not match_success:
            no_match_message_batch_list.append(message_batch)
    pattern_count = len(warn_pattern_list)
    warn_pattern_list = list(filter(lambda e: e.count > 0, warn_pattern_list))
    warn_pattern_list.sort(key=lambda e: e.count, reverse=True)
    no_match_message_batch_list.sort(key=lambda e: e.count, reverse=True)
    other_message_batch_list.sort(key=lambda e: e.count, reverse=True)
    message_list = []
    for warn_pattern in warn_pattern_list:
        if args.filter_count and warn_pattern.count < warn_pattern.get_warn_count():
            if warn_pattern.get_warn_count() < 9999999:
                ignore_message_batch_list.append(warn_pattern)
        else:
            message_list.append(warn_pattern)
            message_list.append("\n")
    message_list.append("|==========================================================================================================================================================|\n\n")
    message_list.append("\n\n\n**************************************************************** 未收录的报错信息 **********************************************************************\n")
    message_list.append("|==========================================================================================================================================================|\n\n")

    for no_match_message_batch in no_match_message_batch_list:
        message_list.append(no_match_message_batch)
    message_list.append("\n\n\n\n\n\n\n\n")
    message_list.append("|==========================================================================================================================================================|\n\n")
    message_list.append("\n\n\n**************************************************************** 可忽略的报错信息 **********************************************************************\n")
    message_list.append("|==========================================================================================================================================================|\n\n")
    message_list.append("\n")
    for ignore_message_batch in ignore_message_batch_list:
        message_list.append(ignore_message_batch)

    current_time_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    title = "操作:【{}】, 时间:【{}】, 报错匹配:【{}】, 忽略:【{}】, 模板总数:【{}】, 检测数量:【{}】".format(user_name, current_time_str, len(warn_pattern_list), len(ignore_message_batch_list), pattern_count, args.filter_count)
    # cur 脚本发送文件是中文,后缀名被自动去掉了, 所以忽略
    write_message_with_title(output_path, "warn.log", title, message_list)
    write_message_with_title(output_path, "other.log", title, other_message_batch_list)
    # write_message_with_title(output_path, "模板报错.txt", title, message_list)
    # write_message_with_title(output_path, "忽略报错.txt", title, ignore_message_batch_list)
    # write_message_with_title(output_path, "其他报错.txt", title, other_message_batch_list)
