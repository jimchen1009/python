import argparse
import datetime
import os
import time
from urllib.parse import unquote

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# 时间的格式类型
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# 对应URL的地址差异
LOG_INDEX_SET = {"log": 296, "log_hour": 233, "log_day": 234}
# 对应下拉列表的缩影
LOG_ELEMENT_SELECT = {"log": 0, "log_hour": 3, "log_day": 2}
# 文件的地址
MACHINE_LOG_PATH = "/data1/user00/logs/{}.log"
MACHINE_LOG_NAMES = ["workspace{}_behavior.log"]


def generate_additional():
    file_paths = []
    for zone_id in (101, 102, 103, 201, 202, 301, 302, 401, 402):
        for game_id in range(1, 16):
            workspace_id = zone_id * 1000 + game_id
            for MACHINE_LOG_NAME in MACHINE_LOG_NAMES:
                log_name = str.format(MACHINE_LOG_NAME, workspace_id)
                file_paths.append(str.format(MACHINE_LOG_PATH, log_name))
    return '{"field":"path","operator":"is not one of","value":"#file_paths#"}'.replace("#file_paths#", ','.join(file_paths))


def driver_find_element(driver, by_name, search_name, seconds: float = 10):
    return WebDriverWait(driver, seconds).until(expected_conditions.presence_of_element_located((by_name, search_name)))


def driver_choose_date(driver, by_name, search_name, choose_time: datetime.datetime):
    find_element = driver_find_element(driver, by_name, search_name).find_element(By.CLASS_NAME, "bk-date-picker-header")
    find_element.find_elements(By.CLASS_NAME, "bk-date-picker-header-label")[0].click()
    year_element = driver_find_element(driver, By.CLASS_NAME, "bk-date-picker-cells.bk-date-picker-cells-year")
    # 下面这段代码不知道为何不生效, 就直接换成复杂的方式实现了
    # year_element.find_element(By.XPATH, str.format("//*[text()='{}']", choose_time.year)).find_element(By.XPATH, "..").click()
    year_num_elements = year_element.find_elements(By.XPATH, "./*")
    for year_num_element in year_num_elements:
        element_name = year_num_element.find_elements(By.XPATH, "./*")[0].get_attribute("innerText")
        if element_name == str(choose_time.year):
            year_num_element.click()
            break
    month_num_elements = driver_find_element(driver, By.CLASS_NAME, "bk-date-picker-cells.bk-date-picker-cells-month").find_elements(By.XPATH, "./*")
    for month_num_element in month_num_elements:
        element_name = month_num_element.find_elements(By.XPATH, "./*")[0].get_attribute("innerText")
        if element_name == str(choose_time.month).zfill(2):
            month_num_element.click()
            break
    time.sleep(0.1)


def driver_choose_month(driver, by_name, search_name, choose_time: datetime.datetime):
    search_element = driver_find_element(driver, by_name, search_name)

    find_element = search_element.find_elements(By.XPATH, "./*")[0]
    find_element = find_element.find_elements(By.XPATH, "./*")[2]
    find_element = find_element.find_element(By.CLASS_NAME, "bk-date-picker-header-label")
    find_element.click()
    time.sleep(0.1)
    find_element = search_element.find_element(By.CLASS_NAME, "bk-date-picker-cells.bk-date-picker-cells-year")
    year_num_elements = find_element.find_elements(By.XPATH, "./*")
    for year_num_element in year_num_elements:
        year_name = year_num_element.find_elements(By.XPATH, "./*")[0].get_attribute("innerText")
        if year_name == str(choose_time.year):
            year_num_element.click()
            time.sleep(0.1)
            break
    find_element = search_element.find_element(By.CLASS_NAME, "bk-date-picker-cells.bk-date-picker-cells-month")
    month_num_elements = find_element.find_elements(By.XPATH, "./*")
    for month_num_element in month_num_elements:
        month_name = month_num_element.find_elements(By.XPATH, "./*")[0].get_attribute("innerText")
        if month_name == str(choose_time.month).zfill(2):
            month_num_element.click()
            time.sleep(0.1)
            break


def driver_choose_date(driver, by_name, search_name, choose_time: datetime.datetime):
    search_element = driver_find_element(driver, by_name, search_name)
    find_element = search_element.find_element(By.CLASS_NAME, "bk-date-picker-cells")
    day_num_elements = find_element.find_elements(By.XPATH, "./*")
    for day_num_element in day_num_elements:
        day_name = day_num_element.find_elements(By.XPATH, "./*")[0].get_attribute("innerText")
        if day_name == str(choose_time.day):
            day_num_element.click()
            break
    time.sleep(0.1)


def driver_choose_time(driver, time_element, choose_time: datetime.datetime):
    find_element = time_element.find_element(By.CLASS_NAME, "bk-time-picker-cells.bk-time-picker-cells-with-seconds")
    find_elements = find_element.find_elements(By.CLASS_NAME, "bk-time-picker-cells-list")
    for i in range(0, 3):
        if i == 0:
            num = choose_time.hour
        elif i == 1:
            num = choose_time.minute
        elif i == 2:
            num = choose_time.second
        else:
            num = 0
        scroll_element = find_elements[i].find_element(By.CLASS_NAME, "bk-time-picker-cells-ul")
        driver.execute_script("arguments[0].scrollIntoView()", scroll_element)
        time.sleep(0.1)
        num_elements = scroll_element.find_elements(By.XPATH, "./*")
        for num_element in num_elements:
            if num_element.get_attribute("innerText") == str(num).zfill(2):
                driver.execute_script("arguments[0].click()", num_element)
                break
        time.sleep(0.1)


def get_suffix_filenames(idc_path: str, suffix: str):
    file_names = os.listdir(idc_path)
    suffix_names = set()
    for file_name in file_names:
        if file_name.endswith(suffix):
            suffix_names.add(file_name)
    return suffix_names


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='information')
    parser.add_argument('--url', dest="url", default='https://apps.o.tencent.com/tencent-bkapp-hippogriff-4-prod/api/v1/search/index_set/#INDEX_SET#/export/', type=str, help='下载地址[废弃]')
    parser.add_argument('--qq', dest="qq", default='771129369', type=str, help='QQ账号')
    parser.add_argument('--log_warn', dest="log_warn", default='log_hour', type=str, help='日志汇总类型:log,log_day,log_hour')
    parser.add_argument('--start_time', dest="start_time", default='2022-09-22 0:00:00', type=str, help='开始时间')
    parser.add_argument('--end_time', dest="end_time", default='', type=str, help='结算时间')
    parser.add_argument('--days', dest="days", default=1, type=int, help='天数')
    parser.add_argument('--hours', dest="hours", default='1', type=int, help='小时')
    parser.add_argument('--range_hours', dest="range_hours", default='120', type=int, help='间隔小时')
    parser.add_argument('--range_minutes', dest="range_minutes", default='0', type=int, help='间隔分钟')
    parser.add_argument('--range_seconds', dest="range_seconds", default='0', type=int, help='间隔秒')
    parser.add_argument('--download_path', dest="download_path", default=r'C:\Users\chenjingjun\Desktop\hippo_warn', type=str, help='文件保存地址')

    # 路径/c/projectG window会变成 C:/projectG (如果拼接路径会报错)
    args = parser.parse_args()
    if len(args.end_time) == 0:
        end_time = datetime.datetime.now()
    else:
        end_time = datetime.datetime.strptime(args.end_time, TIME_FORMAT)
    if len(args.start_time) == 0:
        start_time = end_time - datetime.timedelta(hours=args.hours) - datetime.timedelta(days=args.days)
    else:
        start_time = datetime.datetime.strptime(args.start_time, TIME_FORMAT)

    url_params = '?export_dict={"bk_biz_id":"100445","keyword":"*","time_range":"customized","start_time":"#start_time#}","end_time":"#end_time#}","host_scopes":{"modules":[],"ips":""},"addition":[#addition#],"begin":0,"size":100000}'
    log_index = LOG_INDEX_SET[args.log_warn]
    url_params = str.replace(url_params, "#start_time#", datetime.datetime.strftime(start_time, TIME_FORMAT))
    url_params = str.replace(url_params, "#end_time#", datetime.datetime.strftime(end_time, TIME_FORMAT))
    url_params = str.replace(url_params, "#addition#", "")
    download_url = str.replace(args.url, "#INDEX_SET#", str(log_index)) + url_params
    unquote(download_url)

    download_path = args.download_path
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    options = Options()
    # 下载路径的设置一定要\才生效, 否则下载失败
    options.add_experimental_option("prefs", {'download.default_directory':  download_path.replace("/", "\\")})
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://o.tencent.com/console/")
        driver.maximize_window()
        # QQ登录
        try:
            driver_find_element(driver, By.ID, "img_" + args.qq, 5).find_element(By.XPATH, "..").click()
        except TimeoutException:
            # 检测在线QQ失败, 找对应的二维码
            driver_find_element(driver, By.ID, "qr_area", 5)
        # APP图标
        app_elements = driver_find_element(driver, By.CLASS_NAME, "appbtn", 120).find_elements(By.XPATH, "../*")
        for app_element in app_elements:
            name = app_element.find_elements(By.XPATH, "./*")[1].get_attribute("innerText")
            if name == "HippoGriffV4":
                app_element.click()
                break
        # 休息2s等待新的页签加载
        time.sleep(2)
        window_handles = driver.window_handles
        index = len(window_handles) - 1
        # 切换新的页签（似乎不切换driver数据是停留在上一个页签）
        driver.switch_to.window(window_handles[index])
        # 搜索按钮
        driver_find_element(driver, By.CLASS_NAME, "control-icon.right-icon").click()
        # 日志类型列表选择(因为不是列表类型不能用Select)
        driver_find_element(driver, By.CLASS_NAME, "bk-tab-content.data-search").find_element(By.CLASS_NAME, "bk-select.is-default-trigger").click()
        select_elements = driver_find_element(driver, By.CLASS_NAME, "bk-tooltip-content").find_element(By.CLASS_NAME, "bk-options.bk-options-single").find_elements(By.XPATH, "./*")
        select_element = select_elements[LOG_ELEMENT_SELECT[args.log_warn]]
        time.sleep(0.5)
        select_element.click()
        while_start_time = start_time
        while while_start_time < end_time:
            range_seconds = (args.range_hours * 60 + args.range_minutes) * 60 + args.range_seconds
            while_end_time = while_start_time + datetime.timedelta(seconds=range_seconds)
            if while_end_time > end_time:
                while_end_time = end_time
            start_time_str = datetime.datetime.strftime(while_start_time, TIME_FORMAT)
            end_time_str = datetime.datetime.strftime(while_end_time, TIME_FORMAT)
            # 时间的元素,修改显示的时间(但是不会生效)
            # time_ui_element = driver_find_element(driver, By.CLASS_NAME, "bk-date-picker-rel").find_element(By.CLASS_NAME, "trigger").find_elements(By.XPATH, "./*")[1]
            # driver.execute_script(str.format("arguments[0].innerText = '{} - {}'", start_time_str, end_time_str), time_ui_element)
            # 点击显示的时间控件
            driver_find_element(driver, By.CLASS_NAME, "bk-date-picker.long.king-date-picker.is-retrieve-detail").click()
            # 选择时间区间
            if while_start_time.month == while_end_time.month:
                # 月期相同只在第一个面板选择
                driver_choose_month(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-left", while_start_time)
                driver_choose_date(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-left", while_start_time)
                # 在2022-06-29号，08点到21点的日志，第二次driver_choose_date之后自动跳到05-09号开始
                # 验证在其他日志27 28号都不会，暂时同一天的情况就不点击第二次了
                if while_start_time.day != while_end_time.day:
                    driver_choose_date(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-left", while_end_time)
            else:
                driver_choose_month(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-left", while_start_time)
                driver_choose_date(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-left", while_start_time)
                driver_choose_month(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-right", while_end_time)
                driver_choose_date(driver, By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-right", while_end_time)
            # 点击确认开始搜索
            confirm_elements = driver_find_element(driver, By.CLASS_NAME, "bk-date-picker-dropdown").find_element(By.CLASS_NAME, "bk-picker-confirm").find_elements(By.XPATH, "./*")
            for confirm_element in confirm_elements:
                name = confirm_element.get_attribute("innerText")
                if name == "选择时间":
                    confirm_element.click()
                    time_element = driver_find_element(driver, By.CLASS_NAME, "bk-picker-panel-body-wrapper.bk-time-picker-with-range.bk-time-picker-with-seconds").find_element(By.CLASS_NAME, "bk-picker-panel-body")
                    time_element_left = time_element.find_element(By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-left")
                    time_element_right = time_element.find_element(By.CLASS_NAME, "bk-picker-panel-content.bk-picker-panel-content-right")
                    driver_choose_time(driver, time_element_left, while_start_time)
                    driver_choose_time(driver, time_element_right, while_end_time)
                elif name == "确定":
                    confirm_element.click()
                    break
                # 默认空间是按照顺序来的~

            suffix_filenames0 = get_suffix_filenames(download_path, "txt")
            # 查询按钮, 下载文件
            sleep_seconds = range_seconds / (60 * 60 * 24 * 2) + 3
            time.sleep(sleep_seconds)
            operation_icons = driver_find_element(driver, By.CLASS_NAME, "result-table-container").find_element(By.CLASS_NAME, "operation-icons")
            bk_tooltip = operation_icons.find_elements(By.XPATH, "./*")[1]
            action = ActionChains(driver)
            action.move_to_element(bk_tooltip).perform()
            download_dialog = driver_find_element(driver, By.CLASS_NAME, "download-box").find_elements(By.XPATH, "./*")[0]
            download_dialog.click()
            download_element = driver_find_element(driver, By.CLASS_NAME, "bk-dialog-wrapper.async-export-dialog").find_element(By.CLASS_NAME, "bk-primary.bk-button-normal.bk-button")
            time.sleep(0.5) #停留0.5s看看面板，不闪现
            driver.execute_script("arguments[0].click()", download_element)  # 第二或者第三次，点击按钮就没反应, 所以用js实现
            try:
                driver_find_element(driver, By.CLASS_NAME, "bk-table-empty-text", seconds=2)
                print(str.format("[{}, {}] file download error.", start_time_str, end_time_str))
                time.sleep(3.5)  # 等待3s让提示框自动关闭
            except TimeoutException:
                suffix_filenames1 = suffix_filenames0
                while len(suffix_filenames0) == len(suffix_filenames1):
                    time.sleep(0.1)
                    suffix_filenames1 = get_suffix_filenames(download_path, "txt")
                print(str.format("[{}, {}] file download success, change{}", start_time_str, end_time_str, suffix_filenames1 - suffix_filenames0))
            while_start_time = while_end_time

        # 以下是废弃的代码
        # driver.execute_script(str.format("window.open('{}')", download_url))
        # response = requests.get(download_url)
        # download_name = str.format("{}\\{}", download_path, "download.html")
        # with open(download_name, "wb") as code:
        #     code.write(response.content)
        print(str.format("[{}, {}] all files download success, path:{}", datetime.datetime.strftime(start_time, TIME_FORMAT), datetime.datetime.strftime(end_time, TIME_FORMAT), download_path))
    finally:
        driver.quit()
