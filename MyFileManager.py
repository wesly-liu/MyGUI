# -*- coding: utf-8 -*-
from FileForm import *
from ImageResize import *
from pdf2Excel import *
import os
from threading import Thread
from wx.lib.pubsub.core import Publisher

class FileManager(wx.Frame):
    def __init__(self, parent): 
        super().__init__(parent=None,title="FileManager",size=(1600,1024),pos=(100,100))   #继承wx.Frame类
        self.Center()
        
        splitter = wx.SplitterWindow(self,-1)
        topPanel = wx.Panel(splitter)
        bottomPanel = wx.Panel(splitter)
        splitter.SplitHorizontally(topPanel,bottomPanel,300)
        splitter.SetMinimumPaneSize(80)
        
        self.fileForm=FilePanel(topPanel,self)#这里加了self，即子类中的window，这样子类就可以调用父类的函数了
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.fileForm,1,flag=wx.ALL | wx.EXPAND,border=5)
        topPanel.SetSizer(vbox1)
        
        self.tCMessage=wx.TextCtrl(bottomPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.tCMessage,1,flag=wx.ALL | wx.EXPAND,border=5)
        bottomPanel.SetSizer(vbox2)
        
        # bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        # bSizer4.SetMinSize( wx.Size( -1,25 ) ) 
        # self.bnOk = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.bnOk.SetMinSize( wx.Size( -1,25 ) )
        # bSizer4.Add( self.bnOk, 0, wx.ALL, 5 )
        # self.bnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.bnCancel.SetMinSize( wx.Size( -1,25 ) )
        # bSizer4.Add( self.bnCancel, 0, wx.ALL, 5 )
        # bSizer1.Add( bSizer4, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.mainMenu = wx.MenuBar( 0 ) # 创建一个菜单
        self.functionMenu = wx.Menu()
        self.resizeImageMenu = wx.MenuItem( self.functionMenu, wx.ID_ANY, u"ResizeImage", wx.EmptyString, wx.ITEM_NORMAL )
        self.functionMenu.Append( self.resizeImageMenu )
        self.pdf2ExcelMenu = wx.MenuItem( self.functionMenu, wx.ID_ANY, u"Pdf2Excel", wx.EmptyString, wx.ITEM_NORMAL )
        self.functionMenu.Append( self.pdf2ExcelMenu )
        self.searchExcelMenu = wx.MenuItem( self.functionMenu, wx.ID_ANY, u"SearchExcel", wx.EmptyString, wx.ITEM_NORMAL )
        self.functionMenu.Append( self.searchExcelMenu )
        self.batchRenameFunction = wx.MenuItem( self.functionMenu, wx.ID_ANY, u"batchRename", wx.EmptyString, wx.ITEM_NORMAL )
        self.functionMenu.Append( self.batchRenameFunction )
        self.mainMenu.Append( self.functionMenu, u"Function" ) 
        self.SetMenuBar( self.mainMenu )

        self.stStatus=self.CreateStatusBar()#自动生成的Statusbar不好使，所以在这里创建了一个
        
        # self.bnOk.Bind( wx.EVT_BUTTON, self.bnOkOnButtonClick )
        # self.bnCancel.Bind( wx.EVT_BUTTON, self.bnCancelOnButtonClick )

        self.Bind( wx.EVT_MENU, self.resizeImageMenuOnMenuSelection, id = self.resizeImageMenu.GetId() )
        self.Bind( wx.EVT_MENU, self.pdf2ExcelMenuOnMenuSelection, id = self.pdf2ExcelMenu.GetId() )
        self.Bind( wx.EVT_MENU, self.searchExcelMenuOnMenuSelection, id = self.searchExcelMenu.GetId() )
        self.Bind( wx.EVT_MENU, self.batchRenameFunctionOnMenuSelection, id = self.batchRenameFunction.GetId() )
        
        resizeJpgMenu = self.fileForm.gDFiles.popupmenu.Append(-1, "Resize jpg file")
        self.fileForm.gDFiles.Bind(wx.EVT_MENU, self.resizeJpg,resizeJpgMenu)  # 将菜单绑定给一个函数
        pdf2ExcelMenu = self.fileForm.gDFiles.popupmenu.Append(-1, "Converter pdf to excel")
        self.fileForm.gDFiles.Bind(wx.EVT_MENU, self.pdf2Excel,pdf2ExcelMenu)  # 将菜单绑定给一个函数
        
        # Publisher().subscribe(self.appendMsg, "update")


        
    def setStatusbar(self,text):
        self.stStatus.SetStatusText(text)
        
    def appendMsg(self,text):
        self.tCMessage.AppendText(text)

    def resizeJpg(self, event):
        # will finalize later
        if len(self.fileForm.gDFiles.GetSelectedRows())>0:
            newSize = wx.GetNumberFromUser('Please enter number', '16-8192', 'ImageResizer', value=1280, min=16, max=8192)
            i=0
            row=self.fileForm.gDFiles.GetNumberRows()
            # for jpg in self.fileForm.gDFiles.getColumnValue(0):
            for r in self.fileForm.gDFiles.GetSelectedRows():
                jpg=self.fileForm.gDFiles.GetCellValue(r,0)    
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
        self.fileForm.cBExt.SetValue('.jpg')
        # self.cBExt.SetEditable(False)
        if len(self.fileForm.gDFiles.GetSelectedRows())>0:
            self.resizeJpg(event)
            
    def pdf2Excel(self,event):
        p2e=pdf2Excel(self)
        if len(self.fileForm.gDFiles.GetSelectedRows())>0:
            i=1
            row=len(self.fileForm.gDFiles.GetSelectedRows())
            self.stStatus.SetStatusText(f'Start converting, total {row} files',0)
            # for jpg in self.fileForm.gDFiles.getColumnValue(0):
            for r in self.fileForm.gDFiles.GetSelectedRows():
                pdf=self.fileForm.gDFiles.GetCellValue(r,0)    
                if os.path.splitext(pdf)[1].upper() == '.PDF' and os.path.exists(pdf):
                    if p2e.convert(pdf)==True:
                        self.stStatus.SetStatusText(f'{i}/{row} files have been converted',0)
                    i+=1
        else:
            wx.MessageBox('Please select at least one file!','MyFileManager')
            
            
    def pdf2ExcelMenuOnMenuSelection( self, event ):
        self.fileForm.cBExt.SetValue('.pdf')
        if len(self.fileForm.gDFiles.GetSelectedRows())>0:
            self.pdf2Excel(event)
                        
    # def bnOkOnButtonClick( self, event ):
    #     event.Skip()

    # def bnCancelOnButtonClick( self, event ):
    #     event.Skip()


    def pdf2ExcelMenaulOnMenuSelection( self, event ):
        self.cBExt.SetValue('.pdf')
        if len(self.fileForm.gDFiles.GetSelectedRows())>0:
            self.pdf2Excel(event)

    def searchExcelMenuOnMenuSelection( self, event ):
        event.Skip()

    def batchRenameFunctionOnMenuSelection( self, event ):
        event.Skip()

if __name__ == '__main__':
    app=wx.App()
    frm=FileManager(None)
    frm.Show()
    app.MainLoop()
