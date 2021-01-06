from FileForm_UI import *

class FileForm(frmFile):
    def __init__(self, parent):        # 创建一个菜单项，这里前面的&和后面的\tCtrl+V只是为了显示有快捷键
        super(FileForm, self).__init__(parent)
        self.cBExt.AppendItems(['.jpg', '.pdf', '.xls,.xlsx,.xlsm'])
        self.gDFiles.setExts('')

    def cBExtOnCombobox(self, event):
        self.setExtension(self.cBExt.GetValue())

    def cBExtOnTextEnter(self, event):
        self.setExtension(self.cBExt.GetValue())

    def setExtension(self, ext):
        # Will finalize later
        self.gDFiles.setExts(ext)

 

    def bnOkOnButtonClick(self, event):
        pass

    def bnCancelOnButtonClick( self, event ):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frm = FileForm(None)
    frm.Show()
    app.MainLoop()
