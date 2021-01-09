# -*- coding: utf-8 -*-
import pdfplumber  # 为了操作PDF
from openpyxl import Workbook
import os
from sys import argv

def pdf2excel(sourceFile):
    wb = Workbook()  # 创建文件对象
    ws = wb.active  # 获取第一个sheet
    path=sourceFile
    pdf = pdfplumber.open(path)
    print('\n')
    print('开始读取数据')
    print('\n')
    print(pdf.pages[1].extract_tables()[0][0])
    ws.append(pdf.pages[1].extract_tables()[0][0])
    for page in pdf.pages:
        获取当前页面的全部文本信息，包括表格中的文字
        print(page.extract_text())
        for table in page.extract_tables():
            print(table)
            for row in table:
                if ("Part number" not in row) and (row[0] is not None):
                    print(row[0])
                    print(type(row))
                    print(str(row))
                    newRow=[]
                    for s in row:
                        s=str(s).replace(","," ")
                        newRow.append(s)
                    rowlist=str(newRow).replace("[","",).replace("]","").replace("'","").replace("\\n","").split(",")
                    #rowlist=str(row).replace("[","",).replace("]","").replace("'","").replace("\\n","").split(",")
                    print(rowlist)
                    ws.append(rowlist)
            print('---------- 分割线 ----------')
    pdf.close()
    # 保存Excel表
    destFile=os.path.splitext(sourceFile)[0]+'.xlsx'
    # print(destFile)
    wb.save(destFile)
    return True
    print('\n')
    print('写入excel成功')
    print('保存位置：')
    print(destFile)
    print('\n')
   
def convertFiles(files):
    fileList=files.split('\n')
    for pdfFile in fileList:
        pdfFile=pdfFile.strip()
        print(os.path.splitext(pdfFile))
        print(os.path.splitext(pdfFile)[1])
        if os.path.splitext(pdfFile)[1].upper()!='.PDF':
            continue
        elif os.path.exists(pdfFile):
            pdf2excel(pdfFile)
    
if __name__=="__main__":
    print(argv)
    if len(argv)>1:
        fileName=argv[1]
    elif len(getText())>0:
        #print(getText())
        convertFiles(getText())
        exit
    else:
        fileName=input("Please enter file name:")
        if(os.path.exists(fileName)):
            pdf2excel(fileName)
        else:
            print("File not exist!")
