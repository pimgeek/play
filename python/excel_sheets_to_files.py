# -*- coding:utf-8 -*-
# 把程序直接放入表格所在的文件夹内，双击运行即可

import os, shutil                                                              # 导入文件和文件夹访问相关库函数
import time                                                                    # 导入获取时间戳相关库函数
from decimal import Decimal                                                    # 导入数字处理相关库函数
import xlrd
from xlwt import *
# 删除指定的文件夹
def rmdir(path):
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)                                                # 删除同名文件夹
        except WindowsError:                                                   # 处理文件被占用等异常
            print "请关闭 %s 文件夹中的文件，然后重新运行本程序...".decode('utf-8') % path
            time.sleep(5)                                                      # 停顿 5 秒，让用户看到
            exit()
    else:                                                                      # 如果 output_path 所指定的文件夹不存在，不做任何操作
      return 0
# 创建指定的文件夹
def mkdir(path):
  while 1:
    if os.path.isdir(output_path):
      time.sleep(2)                                                              # 如果文件夹尚未被删除完毕，等待 2 秒后再试
    else:
      time.sleep(2)                                                              # 如果文件夹已被删除完毕，再额外等待 2 秒后创建新文件夹，避免出现文件夹创建错误
      os.makedirs(output_path)                                                   # 根据 output_path 所给定的路径，创建文件夹
      return 0
# 获取当前目录下所有 Excel 文件的处理过程，独立形成一个函数 get_excel_files
# 调用方法 file_list = get_excel_files('.')
def get_excel_files(path):
    file_list = []
    for file in os.listdir(path):                                          # 获取指定目录下的所有文件
        file_extension = file.split('.')[-1]
        if (file_extension == 'xls' or file_extension == 'xlsx'):          # 筛选以 xls 或 xlsx 为后缀的文件
            file_list.append(os.path.join(path, file))
    return file_list
# 把修复 sheet 中单元格格式错误的处理过程，独立形成一个函数 fix_cell_values
# 调用方法 output_sheet = fix_cell_values(input_sheet, output_sheet)
def fix_cell_values(input_sheet, output_sheet):
    nrows = input_sheet.nrows                                              # 获取第 sheet_id 个页签的总行数
    ncols = input_sheet.ncols                                              # 获取第 sheet_id 个页签的总列数
    for row_id in range(nrows):                                            # 针对 sheet 中的每一行逐一做处理，当前行为 row_id 
        for col_id in range(ncols):                                        # 针对 row_id 中的每一列逐一做处理，当前列为 col_id
            number = input_sheet.cell(row_id, col_id).value                # 获得第 row_id 行，第 col_id 列所在单元格的值
            if (input_sheet.cell(row_id, col_id).ctype == 3):              # 如果是日期类型，做日期值相应的处理
                number = xlrd.xldate.xldate_as_datetime(input_sheet.cell(row_id, col_id).value, 1).strftime('%Y/%m/%d %H:%M:%S')
                new_value = str(number).strip(' ?')
            elif (input_sheet.cell(row_id, col_id).ctype == 2):            # 如果是数值类型，做数值相应的处理
                number = Decimal(number)
                new_value = str(number).strip(' ?')
            else:                                                          # 如果是其它类型，做日期值相应的处理
                try:                                                       # 替换 Latin 空格字符为 ASCII 空格，去掉行首行尾的不必要字符
                    number = number.replace(u'\xa0', u' ')
                    new_value = str(number.encode('gbk')).strip(' ?')
                except UnicodeEncodeError:
                    new_value = number
            output_sheet.write(row_id, col_id, new_value)                  # 把处理后的数值写入 sheet 中对应位置
    return output_sheet

# 设定当前工作目录
output_path = os.path.join('.', '分割sheet后的表格').decode('utf-8')       # 定义一个用于存放输出表格的文件夹
# 删除旧的输出目录
rmdir(output_path)
# 创建新的输出目录
mkdir(output_path)
# 获取所有待处理文件
excel_files = get_excel_files('.')
# 逐一处理每个 Excel 文件，提取其中的页签，修复单元格数值，然后保存为单独的文件
for filename in excel_files:
    filename_gbk = unicode(filename, 'gbk')                                # 把文件名从 gbk 格式转换为 unicode 格式，不写也没出错。
    input_wb = xlrd.open_workbook(filename_gbk)                            # 打开一个 xls 文件，并把它的内容读入内存，以变量 input_wb 进行访问
    for sheet_id in range(len(input_wb.sheets())):
        input_sheet = input_wb.sheet_by_index(sheet_id)                    # 把第 sheet_id 个页签的信息赋给变量 input_sheet
        input_sheet_name = input_sheet.name
        output_wb = Workbook(encoding = 'gbk')                             # 在内存中创建一个新表格 output_wb，并定义新表格编码格式为 gbk
        output_sheet = output_wb.add_sheet(input_sheet_name)               # 为新表格 output_wb 创建一个新的页签，并以变量 output_sheet 进行访问
        fix_cell_values(input_sheet, output_sheet)                         # 修复 input_sheet 中每个 cell 的值，并存入 output_sheet
        time_stamp = str(Decimal(1000 * time.time()))                      # 获取当前时间戳
        output_filename = time_stamp + '-' + input_sheet_name + '.xls'     # 在文件名中添加时间戳，避免重名
        output_wb.save(output_filename)
        shutil.move(output_filename, output_path)
