#-*-coding:utf-8-*-
import httplib, json

"""
从网站获取 天气预报信息
"""
def GetInfo(url, site='m.weather.com.cn'):
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
    return None