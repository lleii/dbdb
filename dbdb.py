#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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
#c = requests.get("http://api.douban.com/v2/movie/subject/2210001").json()
page_limit = str(500)   #500
for t in [u"国产剧",u"综艺",u"美剧",u"英剧",u"韩剧",u"日剧",u"港剧",u"日本动画",u"热门"]:
#page_limit = str(3)
#for t in [u"国产剧"]:
    o = pd.read_excel(t+".xlsx","dbdb")

    url = "https://movie.douban.com/j/search_subjects?type=tv&tag=" + t + "&sort=rank&page_limit=" + page_limit + "&page_start=0"
    j = requests.get(url).json()
    pprint (url)
    time.sleep(1)

    for i in j['subjects']:
        if int(i["id"]) not in o["id"].tolist():        
            c = requests.get("http://api.douban.com/v2/movie/subject/" + str(int(i["id"]))).json()
            time.sleep(60)#豆瓣:150次/h
            if 'ratings_count' in c: 
                i.update(c)
                #i["ratings_count"] = c["ratings_count"]
                pprint (i)
                o = o.append(i, ignore_index=True) 
                with pd.ExcelWriter(t+".xlsx") as writer:
                    o.to_excel(writer, sheet_name="dbdb")
            else:
                break

#    o = pd.read_excel(t+".xlsx","dbdb")
#    with pd.ExcelWriter(t+".xlsx") as writer:
#        o.sort_values(['rate'],ascending=0).to_excel(writer, sheet_name="dbdb")
