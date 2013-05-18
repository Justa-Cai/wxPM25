# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrameBase
###########################################################################

class MainFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PM2.5", pos = wx.DefaultPosition, size = wx.Size( 480,480 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		m_choiceCityChoices = []
		self.m_choiceCity = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceCityChoices, 0 )
		self.m_choiceCity.SetSelection( 0 )
		bSizer2.Add( self.m_choiceCity, 0, wx.ALL, 5 )
		
		self.m_staticInfo = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticInfo.Wrap( -1 )
		bSizer2.Add( self.m_staticInfo, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrlInfo = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
		bSizer3.Add( self.m_textCtrlInfo, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Weather", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem1 )
		
		self.m_menubar1.Append( self.m_menu1, u"&More" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.m_choiceCity.Bind( wx.EVT_CHOICE, self.OnCityChange )
		self.Bind( wx.EVT_MENU, self.OnWeatherDialog, id = self.m_menuItem1.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnCityChange( self, event ):
		event.Skip()
	
	def OnWeatherDialog( self, event ):
		event.Skip()
	

###########################################################################
## Class MainDailogPM25
###########################################################################

class MainDailogPM25 ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"wxPM2.5", pos = wx.DefaultPosition, size = wx.Size( 302,266 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		m_choice1Choices = []
		self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		bSizer2.Add( self.m_choice1, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
		bSizer3.Add( self.m_textCtrl1, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class WeatherDialogBase
###########################################################################

class WeatherDialogBase ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Weather", pos = wx.DefaultPosition, size = wx.Size( 480,480 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_static = wx.StaticText( self, wx.ID_ANY, u"Province", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_static.Wrap( -1 )
		bSizer2.Add( self.m_static, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choiceProvChoices = []
		self.m_choiceProv = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choiceProvChoices, 0 )
		self.m_choiceProv.SetSelection( 0 )
		bSizer2.Add( self.m_choiceProv, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_static1 = wx.StaticText( self, wx.ID_ANY, u"Town", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_static1.Wrap( -1 )
		bSizer21.Add( self.m_static1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choiceTownChoices = []
		self.m_choiceTown = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choiceTownChoices, 0 )
		self.m_choiceTown.SetSelection( 0 )
		bSizer21.Add( self.m_choiceTown, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_static11 = wx.StaticText( self, wx.ID_ANY, u"County", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.m_static11.Wrap( -1 )
		bSizer211.Add( self.m_static11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choiceCountyChoices = []
		self.m_choiceCounty = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choiceCountyChoices, 0 )
		self.m_choiceCounty.SetSelection( 0 )
		bSizer211.Add( self.m_choiceCounty, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer211, 0, wx.EXPAND, 5 )
		
		bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"GetWeather", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2111.Add( self.m_button1, 1, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2111, 0, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrlInfo = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
		bSizer3.Add( self.m_textCtrlInfo, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDialog )
		self.m_choiceProv.Bind( wx.EVT_CHOICE, self.OnChoiceProv )
		self.m_choiceTown.Bind( wx.EVT_CHOICE, self.OnChoiceTown )
		self.m_choiceCounty.Bind( wx.EVT_CHOICE, self.OnChoiceCounty )
		self.m_button1.Bind( wx.EVT_BUTTON, self.OnGetWeather )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnInitDialog( self, event ):
		event.Skip()
	
	def OnChoiceProv( self, event ):
		event.Skip()
	
	def OnChoiceTown( self, event ):
		event.Skip()
	
	def OnChoiceCounty( self, event ):
		event.Skip()
	
	def OnGetWeather( self, event ):
		event.Skip()
	

