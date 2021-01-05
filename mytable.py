# -*- coding: utf-8 -*-
import wx
import wx.grid

class MyTable(wx.grid.Grid):
    def __init__(self,parent):
        super(MyTable,self).__init__(parent)
        
    def setList(self,target):
        '''把一个二维List写入到表格,清空原来的数据'''
        self.SetTable(None)        
        if len(target)==0:
            return
        row=len(target)
        col=len(target[0])
        self.CreateGrid(row,col)
        for i in range(0,row):
            for j in range(0,col):
                self.SetCellValue(i,j,target[i][j])
    
    def getList(self):
        '''读取表格并将内容写入到一个二维List里面'''
        result=[]
        row=self.GetNumberRows()
        col=self.GetNumberCols()
        for i in range(0,row):
            ls=[]
            for j in range(0,col):
                ls.append(self.GetCellValue(i,j))
            result.append(ls)
        return result
    
    def setRowCount(self,row):
        c=self.GetNumberCols()
        self.SetTable(None)
        self.CreateGrid(row,c)
        
    def setColumnCount(self,col):
        r=self.GetNumberRows()
        self.SetTable(None)
        self.CreateGrid(r,col)
        
    def clearRows(self):
        c=self.GetNumberCols()
        self.SetTable(None)
        self.CreateGrid(0,c)

    def appendList(self,target):
        '''把一个二维List追加到表格,保留原来的数据'''       
        if len(target)==0:
            return
        row=len(target)
        col=len(target[0])
        currentRow=self.GetNumberRows()
        self.AppendRows(row)
        for i in range(0,row):
            for j in range(0,col):
                self.SetCellValue(currentRow+i,j,target[i][j])

#below are sample class and main        
class MyFrame(wx.Frame):
    #This class is testing only
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target",size=(500,300))
        p = wx.Panel(self)

        grid=MyTable( p )
        
        ls=[['1','2','3'],['4','5','6']]
        grid.setList(ls)

        ls1=[['12','22','32'],['42','52','62']]
        returnList=grid.appendList(ls1)
        print(returnList)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND|wx.ALL, 5)
        p.SetSizer(sizer)
      
            
if __name__=='__main__':
    app = wx.App()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()