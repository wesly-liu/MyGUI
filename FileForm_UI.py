# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

from filetable import *

###########################################################################
## Class frmFile
###########################################################################

class frmFile ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FileForm", pos = wx.DefaultPosition, size = wx.Size( 1280,648 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer2.SetMinSize( wx.Size( -1,1 ) ) 
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"EverythingSearch", wx.DefaultPosition, wx.Size( -1,25 ), 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.tCEverythingSearch = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PROCESS_ENTER )
		bSizer2.Add( self.tCEverythingSearch, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer21.SetMinSize( wx.Size( -1,1 ) ) 
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"SetExtension", wx.DefaultPosition, wx.Size( -1,25 ), 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer21.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		cBExtChoices = []
		self.cBExt = wx.ComboBox( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, cBExtChoices, wx.TE_PROCESS_ENTER )
		bSizer21.Add( self.cBExt, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		self.gDFiles = FileTable( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		#self.gDFiles.CreateGrid( 0, 3 )
		self.gDFiles.EnableEditing( False )
		self.gDFiles.EnableGridLines( True )
		self.gDFiles.EnableDragGridSize( False )
		self.gDFiles.SetMargins( 0, 0 )
		
		# Columns
		self.gDFiles.EnableDragColMove( False )
		self.gDFiles.EnableDragColSize( True )
		self.gDFiles.SetColLabelSize( 30 )
		self.gDFiles.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.gDFiles.EnableDragRowSize( True )
		self.gDFiles.SetRowLabelSize( 80 )
		self.gDFiles.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.gDFiles.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer3.Add( self.gDFiles, 10, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer3, 100, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4.SetMinSize( wx.Size( -1,25 ) ) 
		self.bnOk = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bnOk.SetMinSize( wx.Size( -1,25 ) )
		
		bSizer4.Add( self.bnOk, 0, wx.ALL, 5 )
		
		self.bnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bnCancel.SetMinSize( wx.Size( -1,25 ) )
		
		bSizer4.Add( self.bnCancel, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer4, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.stStatus=self.CreateStatusBar()#自动生成的Statusbar不好使，所以在这里创建了一个
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_ACTIVATE_APP, self.frmFileOnActivateApp )
		self.tCEverythingSearch.Bind( wx.EVT_TEXT, self.tCEverythingSearchOnText )
		self.cBExt.Bind( wx.EVT_COMBOBOX, self.cBExtOnCombobox )
		self.cBExt.Bind( wx.EVT_TEXT_ENTER, self.cBExtOnTextEnter )
		self.bnOk.Bind( wx.EVT_BUTTON, self.bnOkOnButtonClick )
		self.bnCancel.Bind( wx.EVT_BUTTON, self.bnCancelOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def frmFileOnActivateApp( self, event ):
		event.Skip()
	
	def tCEverythingSearchOnText( self, event ):
		event.Skip()
	
	def cBExtOnCombobox( self, event ):
		event.Skip()
	
	def cBExtOnTextEnter( self, event ):
		event.Skip()
	
	def bnOkOnButtonClick( self, event ):
		event.Skip()
	
	def bnCancelOnButtonClick( self, event ):
		event.Skip()
	

