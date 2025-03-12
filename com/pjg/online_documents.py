import argparse
import datetime
import json
import os
import re
import sys
import time

import pandas
import pyperclip
import xlrd as xlrd
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def driver_find_element(driver, by_name, search_name, seconds: float = 10):
    return WebDriverWait(driver, seconds).until(expected_conditions.presence_of_element_located((by_name, search_name)))


def clear_and_backup(driver, name: str, directory: str):
    action = action_operate_board(driver)
    action_send_keys(action, 500, Keys.ARROW_LEFT)
    action_send_keys(action, 500, Keys.ARROW_UP)
    action.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    # action.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
    action.send_keys(Keys.DELETE).perform()
    return action

def action_operate_board(driver):
    action = ActionChains(driver)
    operate_board = driver_find_element(driver, By.ID, "canvasContainer").find_element(By.CLASS_NAME, "main-board")
    action.click(operate_board).perform()
    return action


def action_move_left_up(driver):
    action = ActionChains(driver)
    action_send_keys(action, 500, Keys.ARROW_LEFT)
    action_send_keys(action, 500, Keys.ARROW_UP)
    return action


def action_send_keys(action: ActionChains, count: int, keys_to_send, do_perform: bool = True):
    for i in range(0, count):
        action.send_keys(keys_to_send)
    if do_perform:
        action.perform()
    return action


def execute_load_data1(config):
    expression = config["expression"]
    file_name = config["filename"]
    title = config["title"]
    pattern = re.compile(expression)
    with open(file_name, encoding="UTF-8") as file:
        read_string = file.read()
    pattern_strings = pattern.findall(read_string)
    return_strings = []
    strings = list(title)
    strings.append(generate_date_message())
    return_strings.append(strings)
    for pattern_string in pattern_strings:
        strings = list(pattern_string)
        strings.append("")
        return_strings.append(strings)
    return return_strings


def execute_load_data2(config):
    file_name = config["filename"]
    sheet_name = config["sheetname"]
    title = config["title"]
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_name(sheet_name)
    return_strings = []
    ids = []
    name_ids = {}
    for rx in range(5, sheet.nrows):
        cells = sheet.row(rx)
        if rx == 5:
            for i in range(0, len(cells)):
                cell = cells[i]
                if cell.value in title:
                    ids.append(i)
                    name_ids[cell.value] = i
        elif rx > 5:
            strings = []
            for name in title:
                if name not in name_ids:
                    continue
                i = name_ids[name]
                cell = cells[i]
                strings.append(cell.value)
            if rx == 6:
                strings.append(generate_date_message())
            else:
                strings.append("")
            return_strings.append(strings)
    return return_strings


def generate_date_message():
    date_string = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    return str.format("【程序全量导出,日期{}】", date_string)


#国内镜像地址 https://registry.npmmirror.com/binary.html?path=chromedriver/


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='information')
    parser.add_argument('--url', dest="url",
                        default='https://docs.qq.com/sheet/DTmV5S3NSZ0lVeWVE?u=dc9cc03838d140308acf748eb3441920&tab=a1imkx',
                        type=str, help='在线文档地址')
    parser.add_argument('--qq', dest="qq", default='771129369', type=str, help='QQ账号')
    parser.add_argument('--config', dest="config", default='configs/online_documents.json', type=str, help='配置文件')
    parser.add_argument('--backup_path', dest="backup_path", default='C:/ProjectG/备份/在线文档', type=str, help='备份文件路径')
    parser.add_argument('--speed', dest="speed", default=1, type=int, help='切换页签的速度(秒)')
    parser.add_argument('--clipboard', dest="clipboard", default=True, type=bool, help='是否用剪切板模式')
    parser.add_argument('--tabs_only', dest="tabs_only", default="", type=str, help='指定特定的页签')

    # 路径/c/projectG window会变成 C:/projectG (如果拼接路径会报错)
    args = parser.parse_args()
    with open(args.config, 'r', encoding="UTF-8") as file:
        main_config = json.load(file, strict=False)
    options = Options()
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(args.url)
        wait = WebDriverWait(driver, 5)
        driver.maximize_window()
        # driver_find_element(driver, By.ID, "blankpage-button-pc").click()
        # login_tabs = driver_find_element(driver, By.ID, "id-login-tabs")
        # login_tabs.find_element(By.ID, "qq-tabs-title").click()
        # driver.implicitly_wait(2000)
        # login_frame = driver_find_element(driver, By.ID, "login_frame")
        # driver.switch_to.frame(login_frame)
        # driver_find_element(driver, By.ID, "img_" + args.qq).find_element(By.XPATH, "..").click()
        # time.sleep(args.speed)  # 简单处理,每个页签都切换就可以
        sheet_tabs = driver_find_element(driver, By.ID, "sheetbarContainer", 60).find_elements(By.CLASS_NAME, "sheet-box.sheet.sheet-tab-blur")

        directory = args.backup_path + "/" + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M')
        if not os.path.exists(directory):
            os.makedirs(directory)
        action = ActionChains(driver)
        sheet_tab_List = []
        tabs_only = []
        if len(args.tabs_only) > 0 :
            tabs_only = args.tabs_only.split(",")
        for sheet_tab in sheet_tabs:
            sheet_tab_List.append(sheet_tab)
        while len(sheet_tab_List) > 0:
            sheet_tab = sheet_tab_List[0]
            del sheet_tab_List[0]
            x = sheet_tab.location.get("x")
            y = sheet_tab.location.get("y")
            text = sheet_tab.get_attribute("innerText")
            print(str.format("{}({}, {})", text, x, y))
            if x == 0 and y == 0:
                continue
            # 修复 Element is not clickable at point (XXX, XXX), 设定点击位置
            time.sleep(args.speed)  # 简单处理,每个页签都切换就可以
            action.move_to_element(sheet_tab).click().perform()
            match_strings = []
            if text not in main_config:
                continue
            if len(tabs_only) > 0 and text not in tabs_only:
                continue
            sheet_focus = driver_find_element(driver, By.ID, "sheetbarContainer").find_element(By.CLASS_NAME, "sheet-box.sheet.sheet-tab-focus")
            text_focus = sheet_focus.get_attribute("innerText")
            if text_focus != text:
                print(str.format("页签[{}]不是选中页签[{}],错误跳过.", text, text_focus))
                sheet_tab_List.insert(0, sheet_tab)
                continue
            config = main_config[text]
            seconds = args.speed
            if "seconds" in config:
                seconds = config["typeId"]
            clear_and_backup(driver, text, directory)
            typeId = config["typeId"]
            if typeId == 1:
                match_strings = execute_load_data1(config)
            elif typeId == 2:
                match_strings = execute_load_data2(config)
            length = len(match_strings)
            if length == 0:
                continue
            print(str.format("页签[{}]开始导出{}行数据...", text, length - 1))
            if args.clipboard:
                columns = match_strings[0]
                df = pandas.DataFrame(match_strings[1:], columns=columns)
                df.to_clipboard(index=False)
                action_send_keys(action, 100, Keys.ARROW_LEFT)
                action_send_keys(action, 100, Keys.ARROW_UP)
                action.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
            else:
                for match_string in match_strings:
                    length = len(match_string)
                    for index in range(0, length):
                        action_send_keys(action, 1, match_string[index], False)
                        action_send_keys(action, 1, Keys.ARROW_RIGHT, False)
                    action_send_keys(action, 1, Keys.ARROW_DOWN, False)
                    action_send_keys(action, length, Keys.ARROW_LEFT, True)
            print(str.format("页签[{}]完成导出{}行数据!", text, length - 1))
            time.sleep(seconds)  # 简单处理,每个页签都切换就可以
    finally:
        driver.quit()
