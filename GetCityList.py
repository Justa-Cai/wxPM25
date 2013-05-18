#-*-coding:utf-8-*-
import threading
import urllib2
import urlparse
import sys
import os
import sqlite3
import md5
import httplib,json
#import chardet
from sgmllib import SGMLParser

"""
Useful Function
"""
class SqliteData:
    def __init__(self, datapath='./data/city.db'):
        path = os.getcwd() + datapath
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()
        if datapath == './data/city.db':
            self.curs.execute('CREATE TABLE if not exists pm_data(city_py TEXT  UNIQUE, city_zh TEXT)')
        self.curs.execute('CREATE TABLE if not exists prov_data(id TEXT  UNIQUE, name TEXT)')
        self.conn.commit()
        
    def PushInto(self, city, cityname):
        try:
            self.curs.execute('insert into pm_data values (?,?)', [city, cityname])
            self.conn.commit()
        except sqlite3.IntegrityError:
            #print "same city", city, cityname
            return
    """
    查询键值是否存在
    """    
    def Query(self,  database, key, value):
        retv = False
        try:
            s = 'select * from  %s WHERE %s=%s' %(database, key ,value)
            data = self.curs.execute(s)
            for i in data:
                retv = True
                break
        except sqlite3.IntegrityError:
            return False
        return retv
    
    def TryInsert(self, s):
        try:
            self.curs.execute(s)
        except sqlite3.IntegrityError:
            return False
        except sqlite3.OperationalError:
            print 'Insert Error ', s
            return False
        return True
            
    
    def PushIntoWeather(self, prov, prov_shortcode,  town, town_shortcode, county, county_shortcode, url):
        """
        数据库 存放 以下的ID 都为 shortcode
        省对应一个 shortcode id  prov_id
        self.curs.execute('CREATE TABLE if not exists prov_data(id TEXT  UNIQUE, name TEXT)')
        
        以 prov_id 建表  prov + prov_id
        town_id name
        self.curs.execute('CREATE TABLE if not exists town_${id} (id TEXT  UNIQUE, name TEXT)')
        
        以town_id 建表 town + town_id
        county_id name url
        self.curs.execute('CREATE TABLE if not exists county_${id} (id TEXT  UNIQUE, name TEXT, url TEXT)')
        """
        # 建省级表
        self.curs.execute('CREATE TABLE if not exists prov_data(id TEXT  UNIQUE, name TEXT)')
        s_prov_data = 'insert into prov_data values("%s","%s")' %(prov_shortcode, prov)
        self.TryInsert(s_prov_data)
        
        # 建市级表 插入市级表数据
        s_town = 'CREATE TABLE if not exists town_%s (id TEXT  UNIQUE, name TEXT)' %(prov_shortcode)
        self.curs.execute(s_town)
        s_town_data = 'insert into town_%s values("%s", "%s")' %(prov_shortcode, town_shortcode, town)
        self.TryInsert(s_town_data)
        
        # 建县级地方表  插入县级地方表数据
        s_county = 'CREATE TABLE if not exists county_%s (id TEXT  UNIQUE, name TEXT, url TEXT)' % (town_shortcode)
        self.curs.execute(s_county)
        s_county_data = 'insert into county_%s values("%s", "%s", "%s")' %(town_shortcode, county_shortcode, county, url)
        self.TryInsert(s_county_data)
        
        # 更新 
        #self.conn.commit()
        
    def Commit(self):
        self.conn.commit()
        
class HttplibGetHtml:    
    def __init__(self, url=None):
        self.url = url
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain", 
            "user-agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"}
        self.conn = httplib.HTTPConnection(url)
        
    def GetData(self):
        self.conn.request("GET", "/", None, self.headers)
        response  = self.conn.getresponse()
        print response.status, response.reason
        if (response.status == 200):
            data = response.read()
            self.conn.close()
            return data
    
class FileGetHtml:
    def __init__(self, path='./data/pm25.htm'):
        self.path = path
    def GetData(self):
        data = ""
        f = open(self.path, "r")
        data = f.read()
        f.close();
        return  data           
"""
    转换  json object 到 dict
""" 
def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d

"""
PM25 Html Data Fetch
"""    
class ParseHtmlDataHerf(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        self.city = []
        self.bv = False
        
    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            #print href
            if href[0].startswith('http://www.pm25.in/'):
                self.bv = True
                self.urls.append(href)
            
    def end_a(self):
        self.bv = False
        
    def handle_data(self, data):
        if (self.bv):
            d = data.decode('utf8')
            #print d
            self.city.append(d)
            
    def GetData(self):
        return self.urls, self.city


def PM25GetCityList():
    url = FileGetHtml()
    data = url.GetData()
    parse = ParseHtmlDataHerf()
    parse.feed(data)
    parse.GetData()
    href, city = parse.GetData()
    
    sq = SqliteData()
    
    l = len(city)
    city_filter=['about', 'rank', 'api', '#'] 
    for i in range(0, l):
       s = href[i][0]
       s = s.replace('http://www.pm25.in/', '')
       bAdd = True
       for j in city_filter:
           if s.find(j) != -1:
               bAdd = False
       if bAdd:
           print city[i], s
           sq.PushInto(s, city[i])


"""
Weather CityList Featch
"""    
class ParseHtmlDataWeatherCityList(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        #self.baseurl = 'http://hlj.weather.com.cn/data/city3jdata/provshi/'
        self.baseurl = '/data/city3jdata/provshi/'
        self.urls = []
        self.city = []
        self.city_shortcode = []
        self.bv = False
        self.tick = 0
        self.bInprov = False
        
    def start_select(self, attrs):
        #self.tick += 1
        if attrs[0][0] == 'id' and attrs[0][1] == 'prov':
            self.bInprov = True
                       
    def end_select(self):
        self.bInprov = False
    
    def start_option(self, attrs):
        if self.bInprov:
            shortcode = attrs[0][1] 
            if attrs[0][1] == 'selected':
                shortcode = attrs[1][1] 
                url = self.baseurl + attrs[1][1] + ".html"
            else:
                url = self.baseurl + attrs[0][1] + ".html"
                
            self.urls.append(url)
            self.city_shortcode.append(shortcode)
            #print attrs[0][1]
        
    def handle_data(self, data):
        if self.bInprov:
            d = data.decode('utf8')
            #print d
            self.city.append(d)
            
    def GetData(self):
        return self.urls, self.city, self.city_shortcode
    
"""
获取市级城市列表
返回  下属城市请求地址 市级城市名称 城市短代码(包括省份)
"""
def WeatherProvGetDetail(url, city_shortcode, baseurl='/data/city3jdata/station/'):
    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/",
            "user-agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"}
    conn = httplib.HTTPConnection("hlj.weather.com.cn")
    conn.request("GET", url, None, headers)
    response = conn.getresponse()
    town_urls = []
    town_names = []
    town_shortcode = []
    if response.status == 200:
        data = json.load(response)
        for i in data:
            #print i, data[i]
            town_names.append(data[i])
            town_shortcode.append(city_shortcode + i)
            town_urls.append(baseurl + city_shortcode + i + ".html")
    conn.close()
    return town_urls, town_names, town_shortcode

"""
从网站获取 天气预报信息
"""
def WeatherGetInfo(url, site='m.weather.com.cn'):
    headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/",
            "user-agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"}
    conn = httplib.HTTPConnection(site)
    conn.request("GET", url, None, headers)
    response = conn.getresponse()
    if response.status == 200:
        data = json.load(response)
        conn.close()
        return data
    conn.close() 
    
    
"""
从HTML 解析省份数据
"""
def WeatherGetCityList():
    # http://hlj.weather.com.cn/
    url = FileGetHtml("./data/weather.htm")
    data = url.GetData()
    parse = ParseHtmlDataWeatherCityList()
    parse.feed(data)
    parse.GetData()
    prov_urls, prov_names, prov_shortcode = parse.GetData()
#     print "len:", len(prov_urls)
#     for i in range(0, len(prov_urls)) :
#         print prov_shortcode[i], prov_names[i]
#     return
    #town_urls, town_names, town_shortcode = WeatherProvGetDetail(prov_urls[4], prov_shortcode[4])
    #county_urls, county_names, county_shortcode = WeatherProvGetDetail(town_urls[0], town_shortcode[0], '/data/')
    #weather_data =  WeatherGetInfo(county_urls[0])
    sq = SqliteData('./data/weather.db')
    # print sq.Query('prov_data', 'id',  '123')
    
    tick = 0
    for i in range(0, len(prov_urls)):  
        # 获取省下属 市列表
        town_urls, town_names, town_shortcode = WeatherProvGetDetail(prov_urls[i], prov_shortcode[i])
        for j in range(0, len(town_urls)):
             # 获取市下属 县地方列表
            county_urls, county_names, county_shortcode = WeatherProvGetDetail(town_urls[j], town_shortcode[j], '/data/') 
            for k in range(0, len(county_urls)):
                tick+=1
                print "Tick:", tick
                sq.PushIntoWeather(prov_names[i], prov_shortcode[i],
                                       town_names[j], town_shortcode[j],
                                       county_names[k], county_shortcode[k], county_urls[k])
    print "end..."            
    sq.Commit()
    
    # print weather_data

if __name__ == '__main__':
    #PM25GetCityList()
    WeatherGetCityList()
