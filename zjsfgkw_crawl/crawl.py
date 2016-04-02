#!/usr/bin/env python3
#encoding=utf-8

url = "http://www.zjsfgkw.cn/RealData/RealData"
url2 = "http://www.zjsfgkw.cn/RealData/GetRealDataHistoryAddress?date={}&selectWhere={}"

import urllib3
import json
import urllib
from bs4 import BeautifulSoup
import datetime
import pdb

http = urllib3.PoolManager()

end_date = datetime.date.today()
begin_date = datetime.date(2014, 7, 29)

city = http.request("GET", url)
page = BeautifulSoup(city.data, 'html.parser')
city_list = page.find_all('div', attrs={'class' : 'courtDistriceName'})
city_list = [p.text for p in city_list]

r = http.urlopen("GET","http://www.zjsfgkw.cn/RealData/GetRealDataHistoryAddress?date={}&selectWhere={}".format(end_date.strftime('%Y%m%d'), urllib.parse.quote("地区_杭州")))
res = json.loads(r.data.decode('utf-8'))
print("date\tplace\t"+"\t".join(res['lineDataTime']))

while (begin_date <= end_date):
    for city in city_list:
        date = begin_date.strftime('%Y%m%d')
        req_params = urllib.parse.urlencode({"date": date,
            "selectWhere": "地区_"+city})
        req_url = "http://www.zjsfgkw.cn/RealData/GetRealDataHistoryAddress"
        r = http.urlopen("GET","http://www.zjsfgkw.cn/RealData/GetRealDataHistoryAddress?date={}&selectWhere={}".format(date, urllib.parse.quote("地区_"+city)))
        res = json.loads(r.data.decode('utf-8'))
        print(date+"\t"+city+"\t"+"\t".join([str(p) for p in res['lineDataReceivecase']]))
        begin_date = begin_date + datetime.timedelta(1)

