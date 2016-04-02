#!/usr/bin/env python3
#encoding=utf-8


root_url = "http://bbs.fudan.edu.cn/bbs/"

import sys
import urllib3
import re
from bs4 import BeautifulSoup


http = urllib3.PoolManager()
res = http.request("GET", root_url)
url_queue = ['/0an?path=/groups/ccu.faq/FDU_Base/D544CAA9B']

article_pattern = re.compile("/anc?path=*")

while url_queue:
    res = http.request("GET", root_url + url_queue.pop())
    p = BeautifulSoup(res.data, "html.parser").find_all('a', attrs = {'class' :'ptitle'})
    for q in p:
        if not article_pattern.match(q.href):
            url_queue.append(q.href)
        else:
            article_name = q.text
            out_file = open(article_name, 'w')
            art_res = http.request("GET", root_url + q.href)
            art_page = BeautifulSoup(art_res.data).find_all('div', attrs = {'class' : 'pmain'})
            out_file.write(art_page[0].text)
            out_file.close()


