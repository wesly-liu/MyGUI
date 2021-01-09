from FileForm_UI import *
import Everything
import timer
import socket
from threading import Thread

class FilePanel(panFile,Thread):#继承Thread是为了在子进程调用父进程
    def __init__(self,parent,window):        # 这里的window是父进程
        super(FilePanel, self).__init__(parent)
        self.window=window#self是为了在类内调用
        self.baseEverythingSearch='' 
        #获取本机IP
        hostname=socket.gethostname()
        ip=socket.gethostbyname(hostname)
        if ip[:5]=='10.86':
            self.cBSearchLANFiles.SetValue(True)
            self.baseEverythingSearch=''
        else:
            self.cBSearchLANFiles.SetValue(False)
            self.baseEverythingSearch=' !10.86'
        self.cBExt.AppendItems(['.jpg', '.pdf', '.xls,.xlsx,.xlsm'])
        self.gDFiles.setExts('')
        self.everything=Everything.Everything(self)
        self.everything.everything_dll.Everything_SetSort(14)
               
        self.timer = wx.Timer(self)#创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)#绑定一个定时器事件
        self.orderByDateDesc=False
        self.orderBySizeDesc=False
        self.col=0
        self.desc=True
        

    def cBExtOnCombobox(self, event):
        self.setExtension(self.cBExt.GetValue())

    def cBExtOnTextEnter(self, event):
        self.setExtension(self.cBExt.GetValue())

    def setExtension(self, ext):
        # Will finalize later
        self.gDFiles.setExts(ext)
        if len(self.tCEverythingSearch.GetValue())>0:
            self.timer.StartOnce(100)
        else:
            self.gDFiles.filterExts()
            

    def tCEverythingSearchOnText( self, event ):
        # print(len(self.tCEverythingSearch.GetValue()))
        if len(self.tCEverythingSearch.GetValue())<3:
            self.timer.Stop()
            return
        self.timer.Stop()
        self.timer.StartOnce(1000)

    def cBSearchLANFilesOnCheckBox(self, event ):
        if self.cBSearchLANFiles.IsChecked()==False:
            self.baseEverythingSearch=' !10.86.' 
        else:
            self.baseEverythingSearch=''
        if len(self.tCEverythingSearch.GetValue())>=3:
            self.timer.StartOnce(100)
            
    def setStatusbar(self,text):
        try:
            wx.CallAfter(self.window.setStatusbar(text))#这句是调用父进程的setStatusbar函数
        except Exception as e:
            print(str(e))
    
    def OnTimer(self,event):
        d=self.everything.getResult(self.tCEverythingSearch.GetValue()+' '+self.cBExt.GetValue().replace(',','|') +self.baseEverythingSearch)
        self.gDFiles.clearRows()
        self.gDFiles.appendList(d)
        self.gDFiles.SetOrderBy(self.col, self.desc , orderBy=self.col)#Because column 0 is filename, 1 is size and it is number, 1 is datetime so it is 2
        self.desc = not self.desc 
        # self.setStatusbar(f'Total {len(d)} files')
        # self.stStatus.SetStatusText(f'Total {len(d)} files')
        
    def gDFilesOnGridLabelLeftClick(self, event ):
        col = event.GetCol()
        if len(self.tCEverythingSearch.GetValue())>=3:
            if col==1:
                self.orderBySizeDesc=not self.orderBySizeDesc
                if self.orderBySizeDesc==True:
                    order=6
                    self.desc=0
                else:
                    order=5
                    self.desc=1
            elif col==2:                
                self.orderByDateDesc=not self.orderByDateDesc
                if self.orderByDateDesc==True:
                    order=14
                    self.desc=1
                else:
                    order=13
                    self.desc=0
            self.everything.everything_dll.Everything_SetSort(order)
            self.col=col
            self.timer.StartOnce(100)

 

    # def bnOkOnButtonClick(self, event):
    #     pass

    # def bnCancelOnButtonClick( self, event ):
    #     self.Close()

if __name__ == '__main__':
    app = wx.App()
    frm=wx.Frame(None)
    panel = FilePanel(frm,None)
    sizer=wx.BoxSizer( wx.VERTICAL )
    sizer.Add(panel, 1, wx.ALL|wx.EXPAND, 5 )
    frm.SetSizer(sizer)
    frm.Show()
    app.MainLoop()
