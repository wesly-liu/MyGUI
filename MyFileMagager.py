# -*- coding: utf-8 -*-
from FileForm import *
from ImageResize import *
import os

class FileManager(FileForm):
    def __init__(self, parent):        # 创建一个菜单项，这里前面的&和后面的\tCtrl+V只是为了显示有快捷键
        super(FileManager, self).__init__(parent)
        resizeJpgMenu = self.gDFiles.popupmenu.Append(-1, "Resize jpg file")
        self.gDFiles.Bind(wx.EVT_MENU, self.resizeJpg,
                          resizeJpgMenu)  # 将菜单绑定给一个函数
        

    def resizeJpg(self, event):
        # will finalize later
        newSize = wx.GetNumberFromUser('Please enter number', '16-8192', 'ImageResizer', value=1280, min=16, max=8192)
        i=0
        row=self.gDFiles.GetNumberRows()
        for jpg in self.gDFiles.getColumnValue(0):
            if os.path.splitext(jpg)[1].upper() == '.JPG':
                if size(jpg,newSize)==True:
                    i+=1
                    self.stStatus.SetStatusText(f'{i}/{row} files have been converted',0)
                else:
                    self.stStatus.SetStatusText(f"{jpg} don't need to convert",0) 
        self.stStatus.SetStatusText(f"Total {i} files has been convert",0) 

if __name__ == '__main__':
    app=wx.App()
    frm=FileManager(None)
    frm.Show()
    app.MainLoop()
