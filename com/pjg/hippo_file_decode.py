import argparse
import json
import os


# 前面的顺序是: IP、报错次数、报错时间、报错日志【不能改变】
from json import JSONDecodeError

LOG_KEY_TUPLES = [["ip", ""], ["cnt", "1"], ["report_time", ""], ["log", ""], ["minTimeInfo", ""], ["raw_log", ""]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='information')
    parser.add_argument('--input_path', dest="input_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn', type=str, help='输入路径')
    parser.add_argument('--output_path', dest="output_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn\decode', type=str, help='输出路径')
    parser.add_argument('--file_suffix', dest="file_suffix", default=r'decode', type=str, help='增加文件后缀')
    parser.add_argument('--new_line', dest="new_line", default=False, type=bool, help='是否增加空格')

    args = parser.parse_args()
    input_path = args.input_path
    input_filenames = os.listdir(input_path)
    for input_filename in input_filenames:
        file_path = str.format("{}\\{}", input_path, input_filename)
        if os.path.isdir(file_path):
            continue
        input_filename_split = input_filename.split('.')
        write_path = str.format("{}\\{}_{}.{}", args.output_path, input_filename_split[0], args.file_suffix, input_filename_split[1])
        write_file = open(write_path, 'a', encoding='UTF-8')
        with open(file_path, 'r', encoding='UTF-8') as file:
            file_lines = file.readlines()
            for file_line in file_lines:
                if len(file_line.strip()) == 0:
                    continue
                decode_line = ""
                try:
                    json_data = json.loads(file_line)
                except JSONDecodeError:
                    print(file_line)
                for LOG_KEY_TUPLE in LOG_KEY_TUPLES:
                    LOG_KEY = LOG_KEY_TUPLE[0]
                    if LOG_KEY in json_data:
                        if len(decode_line) != 0:
                            decode_line = decode_line + "\t"
                        json_value = json_data[LOG_KEY]
                        if isinstance(json_value, str):
                            decode_line = decode_line + json_value.rstrip()
                        else:
                            decode_line = decode_line + str(json_value)
                    elif len(LOG_KEY_TUPLE[1]) > 0:
                        if len(decode_line) != 0:
                            decode_line = decode_line + "\t"
                        decode_line = decode_line + LOG_KEY_TUPLE[1]
                write_file.write(decode_line + "\n")
                if args.new_line:
                    write_file.write("\n")  # 为什么加2个空行才生效？？
                write_file.flush()
        write_file.close()
