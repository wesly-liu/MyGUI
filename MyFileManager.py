# -*- coding: utf-8 -*-
from FileForm import *
from ImageResize import *
from pdf2Excel import *
import os

class FileManager(FileForm):
    def __init__(self, parent):        # 创建一个菜单项，这里前面的&和后面的\tCtrl+V只是为了显示有快捷键
        super(FileManager, self).__init__(parent)
        resizeJpgMenu = self.gDFiles.popupmenu.Append(-1, "Resize jpg file")
        self.gDFiles.Bind(wx.EVT_MENU, self.resizeJpg,resizeJpgMenu)  # 将菜单绑定给一个函数
        pdf2ExcelMenu = self.gDFiles.popupmenu.Append(-1, "Converter pdf to excel")
        self.gDFiles.Bind(wx.EVT_MENU, self.pdf2Excel,pdf2ExcelMenu)  # 将菜单绑定给一个函数
        

    def resizeJpg(self, event):
        # will finalize later
        if len(self.gDFiles.GetSelectedRows())>0:
            newSize = wx.GetNumberFromUser('Please enter number', '16-8192', 'ImageResizer', value=1280, min=16, max=8192)
            i=0
            row=self.gDFiles.GetNumberRows()
            # for jpg in self.gDFiles.getColumnValue(0):
            for r in self.gDFiles.GetSelectedRows():
                jpg=self.gDFiles.GetCellValue(r,0)    
                if os.path.splitext(jpg)[1].upper() == '.JPG' and os.path.exists(jpg):
                    newFile=size(jpg,newSize)
                    if os.path.exists(newFile):
                        i+=1
                        self.stStatus.SetStatusText(f'{i}/{row} files have been converted',0)
                    else:
                        self.stStatus.SetStatusText(f"{jpg} don't need to convert",0) 
            self.stStatus.SetStatusText(f"Total {i} files has been convert",0) 
        else:
            wx.MessageBox('Please select at least one file!','MyFileManager')
        
    def resizeImageMenuOnMenuSelection( self, event ):
        self.cBExt.SetValue('.jpg')
        # self.cBExt.SetEditable(False)
        if len(self.gDFiles.GetSelectedRows())>0:
            self.resizeJpg(event)
            
    def pdf2Excel(self,event):
        if len(self.gDFiles.GetSelectedRows())>0:
            i=1
            row=len(self.gDFiles.GetSelectedRows())
            self.stStatus.SetStatusText(f'Start converting, total {row} files',0)
            # for jpg in self.gDFiles.getColumnValue(0):
            for r in self.gDFiles.GetSelectedRows():
                pdf=self.gDFiles.GetCellValue(r,0)    
                if os.path.splitext(pdf)[1].upper() == '.PDF' and os.path.exists(pdf):
                    if pdf2excel(pdf)==True:
                        self.stStatus.SetStatusText(f'{i}/{row} files have been converted',0)
                    i+=1
        else:
            wx.MessageBox('Please select at least one file!','MyFileManager')
            
            
    def pdf2ExcelMenaulOnMenuSelection( self, event ):
        self.cBExt.SetValue('.pdf')
        if len(self.gDFiles.GetSelectedRows())>0:
            self.pdf2Excel(event)
                        

if __name__ == '__main__':
    app=wx.App()
    frm=FileManager(None)
    frm.Show()
    app.MainLoop()
