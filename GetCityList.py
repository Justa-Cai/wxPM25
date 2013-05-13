#-*-coding:utf-8-*-
import threading
import urllib2
import urlparse
import sys
import os
import sqlite3
import md5
import httplib
#import chardet
from sgmllib import SGMLParser

class SqliteData:
    def __init__(self):
        path = os.getcwd() + "./data/city.db"
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()
        self.curs.execute('CREATE TABLE if not exists pm_data(city_py TEXT  UNIQUE, city_zh TEXT)')
        self.conn.commit()
        
    def PushInto(self, city, cityname):
        try:
            self.curs.execute('insert into pm_data values (?,?)', [city, cityname])
            self.conn.commit()
        except sqlite3.IntegrityError:
            #print "same city", city, cityname
            return
            

        
    
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
    

    
class HttplibGetHtml:    
    def __init__(self, url=None):
        self.url = url
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain", "user-agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"}
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

if __name__ == '__main__':
    url = FileGetHtml()
    data = url.GetData()
    parse = ParseHtmlDataHerf()
    parse.feed(data)
    parse.GetData()
    href, city = parse.GetData()\
    
    sq = SqliteData()
    
    l = len(city)
    city_filter=['about', 'rank', 'api', '#'] 
    for i in range(0, l):
       s = href[i][0]
       s = s.replace('http://www.pm25.in/', '')
       bAdd = True
       for j in city_filter:
           if s.find(j)!=-1:
               bAdd = False
       if bAdd:
           print city[i], s
           sq.PushInto(s, city[i])
