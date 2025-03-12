import os
import openpyxl

def modify_excel_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(directory, filename)
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active  # 获取第一个工作表

            # 修改 A1 单元格，添加前缀 'story.' 如果尚未添加
            current_value = sheet['A1'].value
            if current_value is None:
                current_value = ''
            if not current_value.startswith('story.'):
                sheet['A1'].value = 'story.' + current_value

            # 设置 B1 单元格的值为 'T_story'
            sheet['B1'].value = 'T_story'

            # 设置 A5 单元格的值为 'both'
            sheet['A5'].value = 'both'

            # 设置 C1 单元格的值
            config_value = "{javaConfig:{isGenerateJavaConfigClassFile:false,isGenerateJavaConfigDataClassFile:false}}"
            sheet['C1'].value = config_value

            sheet['V5'].value = 'both'

            # 保存修改
            workbook.save(filepath)
            print(f"Modified: {filepath}")

# 使用示例：修改当前目录中的所有 xlsx 文件
if __name__ == "__main__":
    modify_excel_files("C:/ProjectFamily/Family_Product/0Excel/develop/excel/story")
