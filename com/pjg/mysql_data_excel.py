import argparse
import os

from xlwt import Workbook

TABLE_ITEMS = {
    "month_card": [["大类", 1], ["道具ID", 10000212], ["数量", 1], ["邮件标题", ""], ["邮件内容", ""]],
    "player": [["大类", 1], ["道具ID", 10000232], ["数量", 1], ["邮件标题", ""], ["邮件内容", ""]],
    "weekly_card": [["大类", 1], ["道具ID", 10000240], ["数量", 1], ["邮件标题", ""], ["邮件内容", ""]]
}

SERVER_ITEMS = {
    "aqq": [["服务器(手Q、微信)", 2], ["平台(iOS、安卓)", 1]],
    "awx": [["服务器(手Q、微信)", 1], ["平台(iOS、安卓)", 1]],
    "iqq": [["服务器(手Q、微信)", 2], ["平台(iOS、安卓)", 0]],
    "iwx": [["服务器(手Q、微信)", 1], ["平台(iOS、安卓)", 0]]
}

USE_NAMES = {
    "UserId": "角色ID",
    "ZoneId": "区服ID",
    "AccountId": "OpenId"
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='information')
    parser.add_argument('--input_path', dest="input_path", default="C:/Users/chenjingjun/Desktop/20221206_mysql_dump", type=str, help='文件路径')
    parser.add_argument('--excel_name', dest="excel_name", default='1206补发.xls', type=str, help='导出文件xls')
    args = parser.parse_args()

    input_path = args.input_path
    if not os.path.exists(input_path):
        exit(1)
    excel_path = input_path + "/" + args.excel_name
    if os.path.exists(excel_path):
        os.remove(excel_path)
    input_filenames = os.listdir(input_path)
    work_book = Workbook(encoding="UTF-8")
    for input_filename in input_filenames:
        if not input_filename.__contains__("db"):
            continue
        sheet_name = input_filename.replace("db_swy_user_", "")
        sheet = work_book.add_sheet(sheet_name)
        server_name = sheet_name.split("_", maxsplit=1)[0]
        table_name = sheet_name.split("_", maxsplit=1)[1]
        file_path = input_path + "/" + input_filename
        with open(file_path, 'r', encoding='UTF-8') as file:
            file_lines = file.readlines()
            indexes = {}
            for i in range(len(file_lines)):
                file_line = file_lines[i]
                splits = file_line.split("\t")
                index = 0
                for j in range(len(splits)):
                    split = splits[j]
                    if i == 0:
                        if split in USE_NAMES:
                            indexes[j] = len(indexes)
                            sheet.write(i,  indexes[j], USE_NAMES[split])
                    else:
                        if j in indexes:
                            sheet.write(i, indexes[j], split)
            width = len(indexes)
            server_items = SERVER_ITEMS[server_name]
            for i in range(len(file_lines)):
                for j in range(len(server_items)):
                    server_item = server_items[j]
                    if i == 0:
                        sheet.write(0, width + j, server_item[0])
                    else:
                        sheet.write(i, width + j, server_item[1])
            width = width + len(server_items)
            table_items = TABLE_ITEMS[table_name]
            for i in range(len(file_lines)):
                for j in range(len(table_items)):
                    table_item = table_items[j]
                    if i == 0:
                        sheet.write(0, width + j, table_item[0])
                    else:
                        sheet.write(i, width + j, table_item[1])
    work_book.save(excel_path)
