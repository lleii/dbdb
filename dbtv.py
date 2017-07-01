#!/usr/bin/env python
# -*- coding:utf-8 -*-

#import urllib2
import requests
import pandas as pd
from pprint import pprint
import json,time,sys
import logging

logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M:%S'
                            )


'''
url = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&sort=rank&page_limit=500&page_start=0"
'''


page_limit = str(1)   #500
#["国产剧","综艺","美剧","英剧","韩剧","日剧","港剧","日本动画","热门"]
for t in [u"综艺",u"美剧",u"英剧",u"韩剧",u"日剧",u"港剧",u"日本动画",u"热门"]:
    o = pd.read_excel('tvdb.xlsx',"tmpl")
    with pd.ExcelWriter("tvdb.xlsx") as writer:
        o.to_excel(writer, sheet_name=t)
    continue

    j = requests.get(url).json()
    url = "https://movie.douban.com/j/search_subjects?type=tv&tag=" + t + "&sort=rank&page_limit=" + page_limit + "&page_start=0"
    print url

    for i in j['subjects']:
        print i["title"]
        b = o["id"].tolist()
        if int(i["id"]) not in b:        
            c = requests.get("http://api.douban.com/v2/movie/subject/" + str(int(i["id"]))).json()
            time.sleep(0.1)#豆瓣:150次/h
            if 'ratings_count' in c: 
                i["ratings_count"] = c["ratings_count"]
                print i["ratings_count"]
                o = o.append(i, ignore_index=True) 
                with pd.ExcelWriter("tvdb.xlsx") as writer:
                    o.to_excel(writer, sheet_name=t)
            else:
                break
