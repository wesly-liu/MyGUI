# -*- encoding:UTF-8 -*-
import wx
import wx.grid  # 直接import wx不行
import os
from datetime import datetime


def filterFiles(fileList, result=[], exts=''):
    """
    按扩展名筛选文件或文件夹列表，判断文件是否存在
        fileList包含文件或文件夹的字符串列表
        result,extFilterList-函数本身用于递归的结果
        exts文件扩展名，以“，”分隔，如“.xls、.xlsx、.xlsm”，默认值为空，即任何文件都可以
    """
    extFilterList = []
    if len(exts) > 0:
        extFilterList = exts.upper().split(',')
    for file in fileList:
        file = file.strip()
        if not os.path.exists(file):
            continue
        if os.path.isdir(file):
            list = os.listdir(file)  # 列出文件夹下所有的目录与文件
            for i in range(0, len(list)):
                fullPath = os.path.join(file, list[i])
                if os.path.isdir(fullPath):
                    ls = []
                    ls.append(fullPath)
                    filterFiles(ls, result, exts=exts)
                elif len(extFilterList) == 0 or os.path.splitext(fullPath)[1].upper() in extFilterList:
                    result.append(fullPath)
        elif len(extFilterList) == 0 or os.path.splitext(file)[1].upper() in extFilterList:
            result.append(file)
    # print(result)
    return result


def getClipboardText():
    """从剪贴板获取文件清单，可以是资源管理器的文件或者直接字符串形式的文件名，这里并不判断文件是否存在"""
    text_data = wx.TextDataObject()
    if wx.TheClipboard.Open():
        success = wx.TheClipboard.GetData(text_data)
        wx.TheClipboard.Close()
    if success:
        return text_data.GetText()
    else:
        text_data = wx.FileDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
        if success:
            ls = text_data.GetFilenames()
            str = ''
            for s in ls:
                str += s+'\n'
            return str


def paste2List(currentList=[], exts=''):
    '''从剪贴板粘贴文件到一个list, 可以是文件或者是\n分割的文件名字符串, 如果指定了currentList, 则最终结果取粘贴结果和currentList的交集，exts为逗号分割的扩展名'''
    result = []
    filenames = getClipboardText().split('\n')
    result = filterFiles(filenames, exts=exts)
    return list(set(currentList+result))


class textFileDropTarget(wx.FileDropTarget):  # 声明释放到的目标
    '''拖放文件到文本的类'''

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.exts = []

    def OnDropFiles(self, x, y, filenames):  # 释放文件处理函数数据
        '''释放文件处理函数数据'''
        filenames = filterFiles(filenames, exts=self.exts)
        for file in filenames:
            if file not in self.window.GetValue():
                self.window.AppendText("%s\n" % file)
        filenames.clear()

    def setExts(self, exts):
        '''设置文件扩展名'''
        self.exts = exts


class listFileDropTarget(wx.FileDropTarget):  # 声明释放到的目标
    '''拖放文件到List的类'''

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.exts = []

    def OnDropFiles(self, x, y, filenames):  # 释放文件处理函数数据
        '''释放文件处理函数数据'''
        filenames = filterFiles(filenames, exts=self.exts)
        for file in filenames:
            if file not in self.window.GetStrings():
                self.window.AppendItems("%s" % file)
        filenames.clear()
        return

    def setExts(self, exts):
        '''设置文件扩展名'''
        self.exts = exts


class gridFileDropTarget(wx.FileDropTarget):  # 声明释放到的目标
    '''拖放文件到grid的类，文件名在第一列'''

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.exts = []

    def OnDropFiles(self, x, y, filenames):  # 释放文件处理函数数据
        '''释放文件处理函数数据'''
        filenames = filterFiles(filenames, exts=self.exts)
        for file in filenames:
            ls = []
            for i in range(self.window.GetNumberRows()):
                ls.append(self.window.GetCellValue(i, 0))
            if file not in ls:
                self.window.AppendRows(1)
                row = self.window.GetNumberRows()-1
                self.window.SetCellValue(row, 0, "%s" % file)
                self.window.SetCellValue(row, 1, str(os.path.getsize(file)))
                self.window.SetCellValue(row, 2, str(
                    datetime.fromtimestamp(int(os.path.getmtime(file)))))
                row += 1
        filenames.clear()
        return 0

    def setExts(self, exts):
        '''设置文件扩展名'''
        self.exts = exts

# below are sample class and main


class MyFrame(wx.Frame):
    # This class is testing only
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target", size=(500, 300))
        p = wx.Panel(self)
        # create the controls
        label = wx.StaticText(p, -1, "Drop some files here:")
        text = wx.TextCtrl(p, -1, "", style=wx.TE_MULTILINE | wx.HSCROLL)
        listBox = wx.ListBox(p, -1)
        grid = wx.grid.Grid(p, -1, wx.DefaultPosition, wx.DefaultSize, 0)
        grid.CreateGrid(0, 2)
        # setup the layout with sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 5)
        sizer.Add(text, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(listBox, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        p.SetSizer(sizer)
        # make the text control be a drop target
        dtText = textFileDropTarget(text)  # 将文本控件作为释放到的目标
        dtText.setExts('.jpg')
        text.SetDropTarget(dtText)
        dt = listFileDropTarget(listBox)  # 将文本控件作为释放到的目标
        dt.setExts('.jpg')
        listBox.SetDropTarget(dt)
        dtGrid = gridFileDropTarget(grid)  # 将文本控件作为释放到的目标
        dtGrid.setExts('.jpg')
        grid.SetDropTarget(dtGrid)


if __name__ == '__main__':
    app = wx.App()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()
