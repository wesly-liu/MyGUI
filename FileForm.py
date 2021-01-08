from FileForm_UI import *
import Everything
import timer
import socket

class FileForm(frmFile):
    def __init__(self, parent):        # 创建一个菜单项，这里前面的&和后面的\tCtrl+V只是为了显示有快捷键
        super(FileForm, self).__init__(parent)
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
        self.everything=Everything.Everything()
        self.baseEverythingSearch=''        
        self.timer = wx.Timer(self)#创建定时器
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)#绑定一个定时器事件


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
    
    def OnTimer(self,event):
        d=self.everything.getResult(self.tCEverythingSearch.GetValue()+' '+self.cBExt.GetValue().replace(',','|') +self.baseEverythingSearch)
        self.gDFiles.clearRows()
        self.gDFiles.appendList(d)
        self.stStatus.SetStatusText(f'Total {len(d)} files')
 

    def bnOkOnButtonClick(self, event):
        pass

    def bnCancelOnButtonClick( self, event ):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frm = FileForm(None)
    frm.Show()
    app.MainLoop()
