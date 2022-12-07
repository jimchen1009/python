import argparse
import os

from xlwt import Workbook

TABLE_ITEMS = {
    "month_card": [["大类", 1], ["道具ID", 10000212], ["数量", 1], ["邮件标题", ""], ["邮件内容", ""]],
    "player": [["大类", 1], ["道具ID", 10000232], ["数量", 1], ["邮件标题", ""], ["邮件内容", ""]],
    "weekly_card": [["大类", 1], ["道具ID", 10000240], ["数量", 1], ["邮件标题", ""], ["邮件内容", ""]]
}

SERVER_ITEMS = {
    "aqq": [["服务器(手Q2、微信1)", 2], ["平台(安卓1、iOS0)", 1]],
    "awx": [["服务器(手Q2、微信1)", 1], ["平台(安卓1、iOS0)", 1]],
    "iqq": [["服务器(手Q2、微信1)", 2], ["平台(安卓1、iOS0)", 0]],
    "iwx": [["服务器(手Q2、微信1)", 1], ["平台(安卓1、iOS0)", 0]]
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
    add_sheets = {}
    for input_filename in input_filenames:
        if not input_filename.__contains__("db"):
            continue
        split_name = input_filename.replace("db_swy_user_", "").split("_", maxsplit=1)
        server_name = split_name[0]
        table_name = split_name[1]
        if table_name not in add_sheets:
            sheet = work_book.add_sheet(table_name)
            add_sheets[table_name] = {"sheet": sheet, "length": 0, "indexes": None}
        add_sheet = add_sheets[table_name]
        sheet = add_sheet["sheet"]
        file_path = input_path + "/" + input_filename
        with open(file_path, 'r', encoding='UTF-8') as file:
            file_lines = file.readlines()
            indexes = add_sheet["indexes"]
            item_list = []
            item_list.extend(SERVER_ITEMS[server_name])
            item_list.extend(TABLE_ITEMS[table_name])
            if indexes is None:
                file_line = file_lines[0]
                splits = file_line.split("\t")
                indexes = {}
                for j in range(len(splits)):
                    split = splits[j]
                    if split in USE_NAMES:
                        indexes[j] = len(indexes)
                        sheet.write(0, indexes[j], USE_NAMES[split])
                add_sheet["indexes"] = indexes
                length = 1
                for j in range(len(item_list)):
                    sheet.write(0, len(indexes) + j, item_list[j][0])
            else:
                length = add_sheet["length"]
            for i in range(1, len(file_lines)):
                file_line = file_lines[i]
                splits = file_line.split("\t")
                for j in range(len(splits)):
                    split = splits[j]
                    if j in indexes:
                        sheet.write(length, indexes[j], split)
                for j in range(len(item_list)):
                    sheet.write(length, len(indexes) + j, item_list[j][1])
                length = length + 1
            add_sheet["length"] = length
    work_book.save(excel_path)
