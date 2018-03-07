# -*- coding:utf-8 -*-
# 把程序直接放入表格所在的文件夹内，双击运行即可
import os, shutil                                            # 引入文件和文件夹访问相关库函数
import xlrd
from xlwt import *

pathx=os.path.join('.','分割sheet后的表格').decode('utf-8')  # 定义一个用于存放输出表格的文件夹

try:
    shutil.rmtree(pathx)                                     # 删除同名文件夹
except WindowsError:                                         # 如果 pathx 所指定的文件夹不存在，不要退出脚本，只抛出异常信息。
    print "dir is not exist"

os.makedirs(pathx)                                           # 根据 pathx 所给定的路径，创建文件夹
dir=os.listdir('.')                                          # 获取当前目录下的所有文件

for i in dir:
    if 'xls' in i[-4:]:                                      # 筛选以 xls 或 xlsx 为后缀的文件（有漏洞 xlst，xlsm 也符合条件）
        filename=unicode(i,'gbk')                            # 把文件名从 gbk 格式转换为 unicode 格式，不写也没出错。
        data=xlrd.open_workbook(filename)                    # 打开一个 xls 文件，并把它的内容读入内存，以变量 data 进行访问
        for q in range(len(data.sheets())):
            w=Workbook(encoding='gbk')                       # 在内存中创建一个新表格 w，并定义新表格编码格式为 gbk
            a=data.sheet_by_index(q)                         # 把第 q 个页签的信息付给变量 a
            name=data.sheets()[q].name                       # 获取第 q 个页签的名称
            nrows=a.nrows                                    # 获取第 q 个页签的总行数
            ncols=a.ncols                                    # 获取第 q 个页签的总列数
            ws=w.add_sheet(name)                             # 为新表格 w 创建一个新的页签，并以变量 ws 进行访问
            for s in range(nrows):                           # 针对 ws 中的每一行逐一做处理，当前行为 s 
                for x in range(ncols):                       # 针对 s 中的每一列逐一做处理，当前列为 x
                    number = a.cell(s,x).value               # 获得第 s 行，第 x 列所在单元格的值
                    if (a.cell(s,x).ctype == 3):             # 如果是日期类型，做日期值相应的处理
                        number=xlrd.xldate.xldate_as_datetime(a.cell(s,x).value, 1).strftime('%Y/%m/%d %H:%M:%S')
                        p=str(number).strip('   ?')
                    elif (a.cell(s,x).ctype == 2):           # 如果是数值类型，做数值相应的处理
                        number_l=list(str(number))
                        if number_l[-1]=='0' and number_l[-2]=='.':
                            number=int(number)
                        p=str(number).strip('   ?')
                    else:                                    # 如果是其它类型，做日期值相应的处理
                        try:                                 # 替换 Latin 空格字符为 ASCII 空格，去掉行首行尾的无效字符
                            number=number.replace(u'\xa0', u' ')
                            p=str(number.encode('gbk')).strip('   ?')
                        except UnicodeEncodeError :
                            p=number
                    ws.write(s,x,p)                          # 写入单元格内容
            filename=name+'.xls'
            w.save(filename)
            shutil.move(filename,pathx)
