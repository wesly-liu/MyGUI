# -*- coding: utf-8 -*-
from mytable import *
from dropFiles import *
from datetime import datetime


class FileTable(MyTable):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.WANTS_CHARS, name=wx.grid.GridNameStr):
        super(FileTable, self).__init__(parent)
        self.CreateGrid(0, 3)
        self.EnableEditing(False)
        self.EnableGridLines(True)
        self.EnableDragGridSize(True)
        self.SetMargins(0, 0)

        # Columns
        self.SetColSize(0, 757)
        self.SetColSize(1, 96)
        self.SetColSize(2, 196)
        self.EnableDragColMove(False)
        self.EnableDragColSize(True)
        self.SetColLabelSize(30)
        self.SetColLabelValue(0, r"File Name")
        self.SetColLabelValue(1, r"Size")
        self.SetColLabelValue(2, r"ModifiedDate")
        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)

        # Rows
        self.AutoSizeRows()
        self.EnableDragRowSize(True)
        self.SetRowLabelSize(80)
        self.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # 设置行为按行选，开始觉得没用，后来设置gird为只读后看出效果了
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.popupmenu = wx.Menu()  # 创建一个菜单
        # 创建一个菜单项，这里前面的&和后面的\tCtrl+V只是为了显示有快捷键
        pasteMenu = self.popupmenu.Append(-1, "&Paste from clipboard\tCtrl+V")
        openFolderMenu = self.popupmenu.Append(-1, "Open folder")
        self.Bind(wx.EVT_MENU, self.openFolder, openFolderMenu)  # 将菜单绑定给一个函数
        openFileMenu = self.popupmenu.Append(-1, "Open selected file")
        self.Bind(wx.EVT_MENU, self.openFile, openFileMenu)  # 将菜单绑定给一个函数
        self.Bind(wx.EVT_MENU, self.pasteFromClipboard, pasteMenu)
        removeSelectedMenu = self.popupmenu.Append(
            -1, "&Remove selected items\tDel")
        self.Bind(wx.EVT_MENU, self.removeSelected, removeSelectedMenu)
        clearMenu = self.popupmenu.Append(-1, "Clear")
        self.Bind(wx.EVT_MENU, self.clearContents, clearMenu)
        selectAllMenu = self.popupmenu.Append(-1, "&Select All\tCtrl+A")
        self.Bind(wx.EVT_MENU, self.selectALL, selectAllMenu)
        accels = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, removeSelectedMenu.GetId()),
            (wx.ACCEL_CTRL, ord('V'), pasteMenu.GetId()),
            (wx.ACCEL_CTRL, ord('A'), selectAllMenu.GetId())
        ])  # 这里将所有的快捷键加入到一个list里
        self.SetAcceleratorTable(accels)  # 设置整个app使用这些快捷键
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnGridLabelLeftClick)
        self.desc = True
        self.exts = ''

    def OnShowPopup(self, event):
        '''有了这断程序，配合前面的添加菜单，才能将空间和右键菜单绑定起来'''
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnGridLabelLeftClick(self, event):
        col = event.GetCol()
        if col == 1:
            num = True
        else:
            num = False
        self.SetOrderBy(col, self.desc, num)
        self.desc = not self.desc

    def pasteFromClipboard(self, event):
        currentList = []
        for i in range(self.GetNumberRows()):
            currentList.append(self.GetCellValue(i, 0))
        result = paste2List(currentList, self.exts)
        try:
            self.DeleteRows(0, self.GetNumberRows())
        except:
            print('Error')
        self.AppendRows(len(result))
        for i in range(len(result)):
            self.SetCellValue(i, 0, result[i])
            self.SetCellValue(i, 1, str(os.path.getsize(result[i])))
            self.SetCellValue(
                i, 2, str(datetime.fromtimestamp(os.path.getmtime(result[i]))))

    def clearContents(self, event):
        # self.ClearGrid()
        self.DeleteRows(0, self.GetNumberRows())

    def selectALL(self, event):
        for i in range(0, self.GetNumberRows()):
            self.SelectRow(i, True)

    def removeSelected(self, event):
        ls = self.GetSelectedRows()
        ls.sort(reverse=True)
        for i in ls:
            self.DeleteRows(i)

    def openFolder(self, event):
        i = self.GetSelectedRows()[0]
        path = self.GetCellValue(i, 0)
        path = os.path.split(path)[0].strip()
        if os.path.exists(path):
            os.startfile(path)

    def openFile(self, event):
        i = self.GetSelectedRows()[0]
        path = self.GetCellValue(i, 0)
        if os.path.exists(path):
            os.startfile(path)

    def setDrop(self, extension=''):
        dtGrid = gridFileDropTarget(self)  # 将控件作为文件释放到的目标
        dtGrid.setExts(extension)  # 限定扩展名
        self.SetDropTarget(dtGrid)  # 绑定拖拽

    def setExts(self, extension):
        self.setDrop(extension)
        self.exts = extension

    # below are sample class and main


class MyFrame(wx.Frame):
    # This class is testing only
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target", size=(800, 300))
        p = wx.Panel(self)
        grid = FileTable(p)
        grid.setExts('.xls,.c,.cpp,.html')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        p.SetSizer(sizer)


if __name__ == '__main__':
    app = wx.App()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()
