#-*-coding:utf-8-*-
import wx
import uibase
import os
import sqlite3
import inspect
import pm25,weather
from threading import Thread
from wx.lib.pubsub import Publisher

class SqliteData:
    def __init__(self, datapath='./data/city.db'):
        path = os.getcwd() + datapath
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()
        #self.curs.execute('CREATE TABLE if not exists pm_data(city_py TEXT  UNIQUE, city_zh TEXT)')
        #self.conn.commit()
        
    def PushInto(self, city, cityname):
        try:
            self.curs.execute('insert into pm_data values (?,?)', [city, cityname])
            self.conn.commit()
        except sqlite3.IntegrityError:
            #print "same city", city, cityname
            return
        
    def GetCityList(self):
        rs = self.curs.execute("select * from pm_data")
        city_py = []
        city_zh = []
        for r in rs:
            city_py.append(r[0])
            city_zh.append(r[1])
           
        return city_py, city_zh 
    
    def WeatherGetProv(self):
        rs = self.curs.execute("select * from prov_data")
        id = []
        name = []
        for r in rs:
            id.append(r[0])
            name.append(r[1])
        return id, name 
    
    def WeatherGetTown(self, prov_id):
        s = 'select * from town_%s'  % prov_id
        rs = self.curs.execute(s)
        id = []
        name = []
        for r in rs:
            id.append(r[0])
            name.append(r[1])
        return id, name 
    
    def WeatherGetCounty(self, prov_id):
        s = 'select * from county_%s'  % prov_id
        rs = self.curs.execute(s)
        id = []
        name = []
        urls = []
        for r in rs:
            id.append(r[0])
            name.append(r[1])
            urls.append(r[2])
        return id, name , urls
    
"""
Weather Dialog
"""    
        
class WeatherThread(Thread): 
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        
    def run(self):
        data = weather.GetInfo(self.url)
        Publisher().sendMessage("weather", data)
             
class WeatherDialog(uibase.WeatherDialogBase):    
    def __init__(self, parent):
        uibase.WeatherDialogBase.__init__(self, parent)
        self.sq = SqliteData('./data/weather.db')
        self.initdata()
        
        Publisher().subscribe(self.OnWeatherThread, "weather")
        
    def initdata(self):
        # 省级列表
        self.prov_id, self.prov = self.sq.WeatherGetProv()
        for i in range(0, len(self.prov)):
            self.m_choiceProv.Append(self.prov[i])
            
        self.m_choiceProv.SetSelection(0)
        self.UpdateTownData()
    
    def UpdateTownData(self):
        # clear first
        self.m_choiceTown.Clear()
        prov_pos = self.m_choiceProv.GetSelection()
        self.town_id, self.town = self.sq.WeatherGetTown(self.prov_id[prov_pos])
        for i in range(0, len(self.town)):
            self.m_choiceTown.Append(self.town[i])
            
        self.m_choiceTown.SetSelection(0)
        self.UpdateCountyData()
        
    def UpdateCountyData(self):
        # clear first
        self.m_choiceCounty.Clear()
        
        town_pos = self.m_choiceTown.GetSelection()
        self.county_id, self.county, self.county_urls= self.sq.WeatherGetCounty(self.town_id[town_pos])
        for i in range(0, len(self.county_id)):
            self.m_choiceCounty.Append(self.county[i])
            
        self.m_choiceCounty.SetSelection(0)
            
    def OnChoiceProv(self, event):
        self.UpdateTownData()
        #print inspect.stack()[0][3]
        
    def OnChoiceTown(self, event):
        self.UpdateCountyData()
        #print inspect.stack()[0][3]
        
    def OnChoiceCounty(self, event):
        self.OnGetWeather(None)
        
    def OnGetWeather(self, event):
        #print inspect.stack()[0][3]
        prov_pos = self.m_choiceProv.GetSelection()
        town_pos = self.m_choiceTown.GetSelection()
        county_pos = self.m_choiceCounty.GetSelection()
        # 直辖市 prov_id + county_id + town_id
        # 非直辖市 prov_id + town_id + county_id
        if len(self.town) == 1:
            county_id = self.county_id[county_pos]
            county_id = county_id.replace(self.town_id[town_pos], "")
            url = '/data/'  + self.prov_id[prov_pos] + county_id + "00.html"
        else:
            url = self.county_urls[county_pos]
        t = WeatherThread(url)
        t.start()
        
    def OnWeatherThread(self, msg):
        data = msg.data
        if data == None:
            return None
        self.m_textCtrlInfo.Clear()
        
        info = data['weatherinfo']     
        s = "" 
        s += info['city'] + '\n'
        s += info['date_y']  + '  '
        s += info['week'] + '\n'
        s += "今天: "
        s += info['temp1'] + ' '
        s += info['weather1'] + ' ' 
        s += "\n"
        
        s += "明天: "
        s += info['temp2'] + ' '
        s += info['weather2'] + ' ' 
        s += "\n"
        
        s += "后天: "
        s += info['temp2'] + ' '
        s += info['weather2'] + ' ' 
        s += "\n"
        
        s += "\n\n\n\n"
        self.m_textCtrlInfo.AppendText(s)
        
        return 
    
        s = ""
        for i in info:
            s_tmp  = "%s:%s" %(i, info[i])
            s += s_tmp + "\n"
        self.m_textCtrlInfo.AppendText(s)
    
        
"""
PM 25 Dialog
"""
        
class PM25Thread(Thread): 
    def __init__(self, city):
        Thread.__init__(self)
        self.city_py = city
        
    def run(self):
        data = pm25.GetPM25(self.city_py)
        Publisher().sendMessage("pm25", data)
        
class MainFrame(uibase.MainFrameBase):
    def __init__(self, parent):
        uibase.MainFrameBase.__init__(self, parent)
        self.sq = SqliteData()
        self.city_py,self.city_zh = self.sq.GetCityList()
       
        for i in  range(0, len(self.city_py)):
            self.m_choiceCity.Append(self.city_zh[i])
            
        self.m_choiceCity.Select(0)
        Publisher().subscribe(self.OnPm25Thread, "pm25")
        
    def OnCityChange( self, event ):
        self.m_staticInfo.SetLabel("Fetch PM2.5 ing...")
        t = PM25Thread(self.city_py[self.m_choiceCity.GetSelection()])
        t.start()
        
    def OnPm25Thread(self, msg):
        self.m_staticInfo.SetLabel("Fetch PM2.5 finished...")
        data = msg.data
        s = data['area']
        s += str("\n  pm2.5: ")
        s += str(data['pm2_5'])
        s += str("\n  空气质量: ")
        s += str(data['quality'])
        s += str('\n')
        self.m_textCtrlInfo.AppendText(s)
        
    def OnWeatherDialog(self, event):
        dlg = WeatherDialog(self)
        dlg.ShowModal()
        
    def OnClose( self, event ):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    
    frame = MainFrame(None)
    frame.Show()
    
#     dlg = WeatherDialog(None)
#     dlg.ShowModal()
    
    app.MainLoop()