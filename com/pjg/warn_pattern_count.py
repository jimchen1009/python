import argparse
import os
import re
from re import Pattern


class LineBatch:
    def __init__(self, line_batch: str, count: int):
        self.line_batch = line_batch
        self.count = count

    def __str__(self):
        return str.format("{}\t{}", self.count, self.line_batch)


def read_path_line_batch(input_path: str, line_pattern_str: str, count_pattern_str: str):
    line_batch_list = []
    input_filenames = os.listdir(input_path)
    for input_filename in input_filenames:
        file_path = str.format("{}\\{}", input_path, input_filename)
        if os.path.isdir(file_path):
            continue
        line_batch_list0 = read_file_line_batch(file_path, line_pattern_str, count_pattern_str)
        for line_batch0 in line_batch_list0:
            line_batch_list.append(line_batch0)
    return line_batch_list


def read_file_line_batch(file_path: str, line_pattern_str: str, count_pattern_str: str):
    line_batch_list = []
    line_pattern = re.compile(line_pattern_str, re.M | re.I)
    count_pattern = re.compile(count_pattern_str, re.M | re.I)
    read_line = LineBatch("", 1)
    with open(file_path, 'r', encoding="UTF-8") as file:
        file_lines = file.readlines()
        for file_line in file_lines:
            file_line = file_line.rstrip()
            if len(file_line) == 0:
                append_line_batch(read_line, line_batch_list)
                continue
            if line_pattern.search(file_line):
                append_line_batch(read_line, line_batch_list)
                matcher = count_pattern.match(file_line.strip())
                if matcher:
                    count = matcher.group("count")
                    read_line.count = int(count)
                line_batch_join_string(read_line, file_line, count_pattern)
            else:
                line_batch_join_string(read_line, file_line, count_pattern)
    append_line_batch(read_line, line_batch_list)
    return line_batch_list


def append_line_batch(read_line: LineBatch, line_batch_list: list):
    if len(read_line.line_batch) != 0:
        line_batch_list.append(LineBatch(read_line.line_batch, read_line.count))
    read_line.line_batch = ""
    read_line.count = 1


def line_batch_join_string(read_line: LineBatch, file_line: str, remove_pattern: Pattern):
    if remove_pattern is not None:
        file_line = remove_pattern.sub("", file_line, count=1)
    if len(read_line.line_batch) > 0:
        read_line.line_batch = read_line.line_batch + "\n"
    read_line.line_batch = read_line.line_batch + file_line


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='information')
    parser.add_argument('--input_path', dest="input_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn\decode', type=str, help='输入路径')
    parser.add_argument('--output_path', dest="output_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn\count', type=str, help='输出路径')

    args = parser.parse_args()
    line_pattern_str = r"(?P<time>\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\])"
    count_pattern_str = r"(?P<ip>\d+.\d+.\d+.\d+)\t(?P<count>\d+)\t(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\t"
    line_batch_list = read_path_line_batch(args.input_path, line_pattern_str, count_pattern_str)
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    write_path = str.format("{}\\{}", args.output_path, "汇总报错.txt")
    if os.path.exists(write_path):
        os.remove(write_path)
    write_file = open(write_path, 'a', encoding="UTF-8")
    for line_batch in line_batch_list:
        write_file.write(str(line_batch))
        write_file.write("\n")
    write_file.close()
