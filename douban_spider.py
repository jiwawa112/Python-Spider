#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import requests

class DoubanSpider:
    def __init__(self):
        self.url_temp_list = [
        {
            "url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?&start=0&count=18&loc_id=108288",
            "country":"US"
        },
        {
            "url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/tv_korean/items?&start=0&count=18&loc_id=108288",
            "country":"UK"
        },
        {
            "url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/tv_domestic/items?&start=0&count=18&loc_id=108288",
            "country":"CN"
        }
        ]
        self.proxies = {"http":"http://117.91.131.225"}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/75.0.3770.142 Safari/537.36",
                        "Referer": "https://m.douban.com/tv/american"
                        }

    def parse_url(self,url): #发送请求，获取响应
        print(url)
        response = requests.get(url,proxies=self.proxies,headers=self.headers)
        print(response.content.decode())
        return response.content.decode()

    def get_content_list(self,json_str): #提取数据
        dict_ret = json.loads(json_str)
        content_list = dict_ret["subject_collection_items"]
        total = dict_ret['total']

        return content_list,total

    def save_content_list(self,content_list,country): #保存
        with open("douban_multiple.txt","a",encoding="utf-8") as f:
            for content in content_list:
                content['country'] = country
                f.write(json.dumps(content,ensure_ascii=False))
                f.write("\n") #写入换行符，进行换行
        print("保存成功")

    def run(self): # 实现主要逻辑
        for url_temp in self.url_temp_list:
            num = 0
            total = 100 #假设有第一页
            while num < total+18:
                # 1.start_url
                url = url_temp['url_temp'].format(num)
                # 2.发送请求，获取相应
                json_str = self.parse_url(url)
                # 3.提取数据
                content_list,total = self.get_content_list(json_str)
                # 4.保存
                self.save_content_list(content_list,url_temp['country'])
                # if len(content_list) < 18:
                #     break
                # 5.构造下一页的url地址,进入循环
                num += 18


if __name__ == '__main__':
    douban_spider = DoubanSpider()
    douban_spider.run()