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

f=open(r'../douban','r')
cookies={}  
for line in f.read().split(';'):
    name,value=line.strip().split('=',1)
    cookies[name]=value

#all_tags = [u"国产剧"]
#all_sort = ["rank"]
page_limit = str(500)   #500
sleep_time = 37
all_tags = [u"国产剧", u"综艺", u"美剧", u"英剧", u"韩剧", u"日剧", u"港剧", u"日本动画", u"热门"]
all_sort = ["rank", "time", "recommend"]
for t in all_tags:
    all_id=[]
    for s in all_sort:
    #page_limit = str(3)
    #for t in [u"国产剧"]:
        o = pd.read_excel(t+".xlsx","dbdb")
        ll = len(o)
        w=""
        url = "https://movie.douban.com/j/search_subjects?type=tv&tag=" + t + "&sort=" + s + w + "&page_limit=" + page_limit + "&page_start=0"
        j = requests.get(url).json()
        print (w,s,t,ll,url)
        time.sleep(1)

        for i in j['subjects']:
            if int(i["id"]) not in o["id"].tolist():        
                c = requests.get("http://api.douban.com/v2/movie/subject/" + str(int(i["id"]))).json()
                if 'ratings_count' in c: 
                    ll+=1
                    i.update(c)
                    print (w,s,t,ll,i["title"])
                    o = o.append(i, ignore_index=True) 
                    with pd.ExcelWriter(t+".xlsx") as writer:
                        o.to_excel(writer, sheet_name="dbdb")
                else:
                    break
                time.sleep(sleep_time)#豆瓣:150次/h

        w = "&watched=on"
        url = "https://movie.douban.com/j/search_subjects?type=tv&tag=" + t + "&sort=" + s + w + "&page_limit=" + "500" + "&page_start=0"
        j = requests.get(url,cookies=cookies).json()
        print (w,s,t,ll,url)
        time.sleep(1)

        for i in j['subjects']:
            all_id.append(int(i["id"]))
            #pprint (len(all_id))

    for index in o.index:
        if o.ix[index, "id"] not in all_id:
            o.set_value(index, "watched", 1)
        else:
            o.set_value(index, "watched", 0)

    with pd.ExcelWriter(t+".xlsx") as writer:
        o.to_excel(writer, sheet_name="dbdb")

    #    o = pd.read_excel(t+".xlsx","dbdb")
    #    with pd.ExcelWriter(t+".xlsx") as writer:
    #        o.sort_values(['rate'],ascending=0).to_excel(writer, sheet_name="dbdb")
