#-*-coding:utf-8-*-
import wx
import uibase
app = wx.App()

#frame = uibase.MainFrameBase(None)
#frame.Show()

dlg = uibase.MainDailogPM25(None)
dlg.Show()

app.MainLoop()