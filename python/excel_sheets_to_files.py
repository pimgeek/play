# -*- coding:utf-8 -*-
#把程序直接放入表格所在的文件夹内，双击运行即可
import os,shutil
import xlrd
from xlwt import *
pathx=os.path.join('.','分割sheet后的表格').decode('utf-8')  #处理后用于存放表格的文件夹
try:
    shutil.rmtree(pathx)  #删除同名文件夹
except WindowsError:
    print "dir is not exist"
os.makedirs(pathx)    #创建文件夹
dir=os.listdir('.')  #获取当前目录下的所有文件
for i in dir:
    if 'xls' in i[-4:]:  #筛选以xls或xlsx为后缀的文件
        filename=unicode(i,'gbk')
        data=xlrd.open_workbook(filename)  #打开文件
        for q in range(len(data.sheets())):
            w=Workbook(encoding='gbk')   #定义新建表格文件的编码格式
            a=data.sheet_by_index(q)  #把第q个页的信息付给变量a
            name=data.sheets()[q].name
            nrows=a.nrows  #行数
            ncols=a.ncols  #列数
            ws=w.add_sheet(name)     #给文件添加sheet页
            for s in range(nrows):   #遍历所有的单元格内容
                for x in range(ncols):
                    number = a.cell(s,x).value
                    if (a.cell(s,x).ctype == 3):
                        number=xlrd.xldate.xldate_as_datetime(a.cell(s,x).value, 1).strftime('%Y/%m/%d %H:%M:%S')
                        p=str(number).strip('   ?')
                    elif (a.cell(s,x).ctype == 2):
                        number_l=list(str(number))
                        if number_l[-1]=='0' and number_l[-2]=='.':
                            number=int(number)
                        p=str(number).strip('   ?')
                    else:
                        try:
                            number=number.replace(u'\xa0', u' ')
                            p=str(number.encode('gbk')).strip('   ?')
                        except UnicodeEncodeError :
                            p=number
                    ws.write(s,x,p)  #写入单元格内容
            filename=name+'.xls'
            w.save(filename)
            shutil.move(filename,pathx)
