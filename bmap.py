#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Channing Wong
#
# @mail: channing.wong@yahoo.com
# @home: http://blog.3363.me/
# @date: Mar 3, 2012
#

import json
import sys
import time,datetime
import types
import urllib
import urllib2
import torndb
from util.poi import PoiConvert

reload(sys)
sys.setdefaultencoding('utf-8')


class BaiduMap:
    """
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.query = [
                ('b', '(-1599062.039999999,811604.75;24779177.96,8168020.75)'),
                ('c', '1'), #city code
                ('from', 'webmap'),
                ('ie', 'utf-8'),
                ('l', '4'),
                ('newmap', '1'),
                ('qt', 's'),
                ('src', '0'),
                ('sug', '0'),
                ('t', time.time().__int__()),
                ('tn', 'B_NORMAL_MAP'),
                ('wd', keyword),
                ('wd2', '')
                 ]
        self.mapurl = 'http://map.baidu.com/'
        #self.file = open('%s.txt' % keyword, 'w')
        self.count = 0
        self.count_c = 0
        self.total_num = 0

        self._get_city()

    def _fetch(self, query=None, json=True):
        res = None
        try:
            data = urllib.urlencode(query)
            url = self.mapurl + '?' + data
            req = urllib2.Request(url)
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            req.add_header('Accept-Charset', 'utf-8;q=0.7,*;q=0.3')
            req.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
            req.add_header('host', 'map.baidu.com')
            req.add_header("Cookie", 'BAIDUID=113B438FD487DA48E0E1FA0755B465F3:FG=1; showgrtip=1; Maptodowntip=2; SSUDBTSP=1373332699; SSUDB=2Q5aGVtVjlsbm1ZbDQ3b3NKNEtQR21waFdoWU40aTNrZzdqbmV0bnRkamE4UUpTQVFBQUFBJCQAAAAAAAAAAAEAAACzzjYNUkFORkkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANpk21HaZNtRN; BDUSS=JVV01WMHJPd2lEV3pHZWFvOXNGM2N4SXB2LXY4NVVZM3ViQ05RLWhwMkNieHhTQVFBQUFBJCQAAAAAAAAAAAEAAACzzjYNUkFORkkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAILi9FGC4vRReV; cflag=32767; bdshare_firstime=1375418801906; BDSFRCVID=QaKEJL0CkFnRZnV6YREs2eBt_XLK0gscB-Tpychi3ovYymswJeC6Ex5; H_BDCLCKID_SF=JRKD_Dt2JKvbfP0kh46M-JD8hxLX2tQJfK3Gsl5FMRrSMb_G0xJjy5kwMaQQttoUKKjCslkM5-OUEJcX0p6xMxkX-HoWtqQTJgQ-5KQNMIK0hC06D5Lae5PW5ptX24Ra2CJ-LPoq2Ru_DPoTenrhQMLpDhtL3jQnLev2aUQ42IjSMRj5-PcNqfnQbpbRbqO2bK5AB-TvMpFaVhQu0x6qLTKk2a_Et6F8tnF8_Kv5b-0_fPnm-J5qh4oHhxoJqM6MWmTZhPL55CQcVl0Cyn7YK6KPXPThJfcw3g0j0-OgJq3JDI52MMQ2y-IB2aO7BMT-0bc4XIKLJCtbMK_wD6Rb5nbHMqOK2JFXKKAs2bcg3lFKjpne245CQTKUbtcHtfc9BDFHalrgWKJJqpb8hMTDbbO-5-AH5MK83237aJ5nJq5lMDFGejL-D53WepJf-K6X2jnKQJ58K6r_et-rWM5mQfI-Mnou--JN3bcibh6-JqTc8RL4yfTUyT8sKPOj0lRILCopX4onBbkBfnbEy4oTjxLbjHCeqTDjtnFjV--8KR3KHJrmKPoVq4tehH4tW6vdWDvmKC8-bfobElklM476bJ_vjMnAajcqQRKDQIOFfDK-bKLljT835n-Wqlbq--vXHD7yWCvd3x7pO4TKX-jWjljWqtR--nDjaCoKKJRjMfJvhb3RbtQDW5oyMnQMhUKebecWaPQF5l8-stPGe6D5D6jQjHRf-b-XaI58BCIXHJOoDDvj0fRpyRFljxDt2qj0LbvK24_KWl7FeR6mj4RvD--yQMv8BxCfMJvB0CLa2Mtbf4b_bf--QJv0eGKjt5-DtJKsL-35Htn8jPbpK4o_-DCShUFsQ4oi3mQropOo3JrCoRrKjlrCQJJXbt5JyhvrWbRMQbOPHxb2JJOdMjbo5lF-hqbfBtQmJeTO_CcJ-J8XMD0mjTbP; H_PS_PSSID=2777_1447_2975_3058_2980_3062_2939_2249_2701; IM_old=0|hjyalokr; MCITY=-%3A')
            res = urllib2.urlopen(req, timeout=10)
            data = res.read()
            if json:
                return self._tojson(data)
            else:
                return data
        except urllib2.HTTPError, e:
            print e;
            msg = "crawler a page has an exception" % url
            logger.error(msg)

        finally:
            if res != None:
                res.close()

    def _tojson(self, data):
        try:
            js = json.loads(data, 'utf-8')
        except:
            js = None

        return js

    def _get_city(self):
        data = self._fetch(self.query)

        if type(data['content']) is not types.ListType:
            print 'keyword error.'
            sys.exit()

        self.city = data['content']

        if data.has_key('more_city'):
            for c in data['more_city']:
                self.city.extend(c['city'])

        for city in self.city:
            self.total_num += city['num']

    def _get_data(self, city, page=0):
        query = [
                ('addr', '0'),
                ('b', '(%s)' % city['geo'].split('|')[1]),
                ('c', city['code']),
                ('db', '0'),
                ('gr', '3'),
                ('ie', 'utf-8'),
                ('l', '9'),
                ('newmap', '1'),
                ('on_gel', '1'),
                ('pn', page), #当前分页页码
                ('qt', 'con'),
                ('src', '7'),
                ('sug', '0'),
                ('t', time.time().__int__()),
                ('tn', 'B_NORMAL_MAP'),
                ('wd', self.keyword),
                ('wd2', ''),
                 ]
        data = self._fetch(query)
        return data

    def _save(self, content, city):
        for c in content:
            self.count += 1
            self.count_c += 1
            if c.has_key('tel'):
                tel = c['tel']
            else:
                tel = ''

            if c.has_key('geo'):
                geo = c['geo']
            if geo is not None and geo !='':
                lnglat = geo.split(";")[0].split("|")[1]
                arr = lnglat.split(",")
                lng,lat = PoiConvert.convertor(float(arr[0]),float(arr[1]))

            
            _data = '%s\t%s\t%s\t%s\t%s\t%s\n' % (city['name'], c['name'], c['addr'], tel, lng, lat)
            self.file.write(_data)
            print '(%s/%s) %s[%s/%s]' % (self.count, self.total_num, city['name'], self.count_c, city['num'])

    def get(self, city):
        self.count_c = 0
        pages = abs(-city['num'] / 10)
        for page in range(0, pages):
            data = self._get_data(city, page)
            if data.has_key('content'):
                self._save(data['content'], city)

    def get_all(self):
        for city in self.city:
            self.get(city)

        self.file.close()

    def migrate2db(self,keyword):
        #db = torndb.Connection("127.0.0.1", "sales_help", "root", "123456")
        db = torndb.Connection("58.211.114.118", "ec_food", "food", "food")
        f = open(keyword + ".txt","r")
        line = f.readline()
        while('' != line and line is not None):
            cityName,name,address,phone,lng,lat = line.split("\t")
            #id = db.execute_lastrowid(
            #"insert into sales_service_point(sp_name,phone,address,lng_baidu,lat_baidu,createtime,product_category_ids) values(%s,%s,%s,%s,%s,%s,%s)",
            #name,phone,address,lng,lat,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"0")
            id = db.execute_lastrowid(
            "insert into biz_corp_shop(shop_name,phone,address,lng_baidu,lat_baidu,create_time,pid) values(%s,%s,%s,%s,%s,%s,%s)",
            name,phone,address,lng,lat,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"0")
            line = f.readline()


if __name__ == '__main__':
    if sys.argv.__len__() == 2:
        keyword = sys.argv[1]
    if sys.argv.__len__() == 3:
        keyword = sys.argv[1]
        sync2db = sys.argv[2]
    else:
        keyword = '钻石'

    baidumap = BaiduMap(keyword)
    print '_' * 20
    print 'CITY: %s' % baidumap.city.__len__()
    print 'DATA: %s' % baidumap.total_num
    #baidumap.get_all()
    if sync2db == 'true' and sync2db is not None:
        baidumap.migrate2db(keyword)
    







