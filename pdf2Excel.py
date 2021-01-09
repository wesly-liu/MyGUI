# -*- coding: utf-8 -*-
import pdfplumber  # 为了操作PDF
from openpyxl import Workbook
import os
from sys import argv
from threading import Thread
from wx.lib.pubsub.core import Publisher
import wx

class pdf2Excel(Thread):
    def __init__(self,window):
        self.window=window
        
    def setStatusBar(self,text):
        try:
            wx.CallAfter(self.window.setStatusbar,text)#这句是调用父进程的setStatusbar函数
        except Exception as e:
            print(str(e))
            
    def appendMsg(self,text):
        try:
            wx.CallAfter(self.window.appendMsg,text)#这句是调用父进程的setStatusbar函数
            # wx.CallAfter(Publisher().sendMessage,text)#这句是调用父进程的setStatusbar函数
        except Exception as e:
            print(str(e))
        
    def convert(self,sourceFile):
        wb = Workbook()  # 创建文件对象
        ws = wb.active  # 获取第一个sheet
        path=sourceFile
        pdf = pdfplumber.open(path)
        s='\n'
        s+='开始读取数据'
        s+='\n'
        s+=str(pdf.pages[1].extract_tables()[0][0])
        self.appendMsg(s)
        ws.append(pdf.pages[1].extract_tables()[0][0])
        for page in pdf.pages:
            #获取当前页面的全部文本信息，包括表格中的文字
            self.appendMsg(str(page.extract_text()))
            for table in page.extract_tables():
                self.appendMsg(str(table))
                for row in table:
                    if ("Part number" not in row) and (row[0] is not None):
                        self.appendMsg(str(row[0]))
                        self.appendMsg(str(type(row)))
                        self.appendMsg(str(row))
                        newRow=[]
                        for s in row:
                            s=str(s).replace(","," ")
                            newRow.append(s)
                        rowlist=str(newRow).replace("[","",).replace("]","").replace("'","").replace("\\n","").split(",")
                        #rowlist=str(row).replace("[","",).replace("]","").replace("'","").replace("\\n","").split(",")
                        self.appendMsg(str(rowlist))
                        ws.append(rowlist)
                self.appendMsg('---------- 分割线 ----------')
        pdf.close()
        # 保存Excel表
        destFile=os.path.splitext(sourceFile)[0]+'.xlsx'
        # print(destFile)
        wb.save(destFile)
        return True
        self.appendMsg(str('\n'))
        self.appendMsg(str('写入excel成功'))
        self.appendMsg(str('保存位置：'))
        self.appendMsg(str(destFile))
        # print('\n'))
    
    # def convertFiles(self,files):
    #     fileList=files.split('\n')
    #     for pdfFile in fileList:
    #         pdfFile=pdfFile.strip()
    #         print(os.path.splitext(pdfFile))
    #         print(os.path.splitext(pdfFile)[1])
    #         if os.path.splitext(pdfFile)[1].upper()!='.PDF':
    #             continue
    #         elif os.path.exists(pdfFile):
    #             pdf2excel(pdfFile)
    
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
