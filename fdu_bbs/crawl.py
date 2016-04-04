#!/usr/bin/env python3
#encoding=utf-8


root_url = "http://bbs.fudan.edu.cn/bbs"

import sys
import traceback
import urllib3
import urllib
import time
import re
import pdb
from bs4 import BeautifulSoup


http = urllib3.PoolManager()
res = http.request("GET", root_url)
url_queue = ['http://bbs.fudan.edu.cn/bbs/0an?path=/groups/ccu.faq/FDU_Base/D544CAA9B']

article_pattern = re.compile("/M.*")

while url_queue:
    base_url = url_queue.pop(0)
    res = http.request("GET", base_url)
    p = BeautifulSoup(res.data, "lxml").find_all('ent')
    for q in p:
        time.sleep(1)
        if not article_pattern.match(q['path']):
            url_queue.append(base_url + q['path'])
        else:
            article_name = q.text
            out_file = open(article_name, 'w')
            art_url = base_url + q['path']
            art_url = art_url.replace("0an?", "anc?")
            art_res = http.request("GET", art_url)
            art_page = BeautifulSoup(art_res.data, 'lxml')
            try:
                out_file.write(urllib.parse.unquote(art_page.bbsanc.text))
            except:
                print(art_url)
            finally:
                out_file.close()
