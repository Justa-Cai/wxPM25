#-*-coding:utf-8-*-

import httplib,urllib,json,sys
def GetPM25(city_py):
    params = urllib.urlencode({'city': city_py, 
                               'token': '5j1znBVAsnSf5xQyNQyq', 
                               'stations':'no'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/ "}
    
    conn = httplib.HTTPConnection("pm25.in")
    conn.request("GET", "/api/querys/pm2_5.json", params, headers)
    response = conn.getresponse()
    retv = [] 
    if (response.status == 200):
        data = json.load(response)
        #print data[0]
        #print json.dumps(data, indent = 1)
        #print data[0]['area'], "pm2.5:", data[0]['pm2_5'], "ø’∆¯÷ ¡ø:", data[0]['quality']
        retv = data[0]
    conn.close()
    return retv
