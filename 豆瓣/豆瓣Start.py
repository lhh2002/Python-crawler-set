#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-crawler-set 
@File    ：豆瓣Start.py
@IDE     ：IntelliJ IDEA 
@Author  ：大数据老哥
@Date    ：2020/12/29 23:31 
'''
import requests
import json
import string
import urllib.parse
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def douban(name, count):
    #  请求地址
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&"
    #  请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}
    cookies = {}

    # 携带的参数sort=time&page_limit=20&page_start=0
    parm = {
        'sort': 'time',
        'page_limit': 20,
        'page_start': count,
    }
    # 拼接请求参数
    ajax_url = url + urlencode(parm)
    print(ajax_url)
    # 发送请求
    data_json = requests.get(ajax_url, headers=headers,cookies=cookies).json()

    with open('豆瓣数据.txt', 'a') as output:
        for index, data in enumerate(data_json['subjects']):
            # 评分
            rate = data['rate']
            # 标题
            title = data['title']
            # 图片
            cover = data['cover']
            # 发送下一次请求
            data_ = requests.get(data['url'], headers=headers).content.decode()
            print("正在准备下文件写入："+title)
            # 格式转换
            soupData = BeautifulSoup(data_, 'lxml')
            #  解析数据
            aa = soupData.find(class_='subjectwrap clearfix')
            info = aa.find(attrs={'id': 'info'})
            try:
                if (len(info.find_all(class_='pl')) == 10 ):
                    #写入文件
                    output.write(ten(rate, title, cover, info) + "\n")
                    output.flush()
                if (len(info.find_all(class_='pl')) == 7):
                    # 写入文件
                    output.write(seven(rate, title, cover, info) + "\n")
                    output.flush()
                print("成功向文件写入：" + title)
            except Exception:
                print("格式解析异常：" + title)

        output.close()
def seven(rate, title, cover, info):
    # 导演
    directors = []
    for s in info.find_all(attrs={'rel': 'v:directedBy'}):
        directors.append(s.string)
    # 主演
    protagonists = []
    for s in info.find_all(attrs={'rel': 'v:starring'}):
        protagonists.append(s.string)
    # 类型
    types = []
    for s in info.find_all(attrs={'property': 'v:genre'}):
        types.append(s.string)
    # 解析 制片国家
    ProductsCountry = info.find_all(class_='pl')[3].next_sibling
    # 语言
    language = info.find_all(class_='pl')[4].next_sibling
    # 上映日期
    date = info.find(attrs={'property': 'v:initialReleaseDate'}).string
    # 片长
    runtime = info.find(attrs={'property': 'v:runtime'}).string
    # 将数据保存到集合中
    list = {'rate': rate, 'title': title, 'cover': cover, 'directors': directors, 'protagonists': protagonists,
            'types': types, 'ProductsCountry': ProductsCountry,
            'language': language, 'date': date, 'runtime': runtime}
    # 返回集合
    return json.dumps(list)
def ten(rate, title, cover, info):
    # 导演
    directors = []
    for s in info.find_all(attrs={'rel': 'v:directedBy'}):
        directors.append(s.string)
    # 主演
    protagonists = []
    for s in info.find_all(attrs={'rel': 'v:starring'}):
        protagonists.append(s.string)
    # 类型
    types = []
    for s in info.find_all(attrs={'property': 'v:genre'}):
        types.append(s.string)
        # 解析 制片国家
    ProductsCountry = info.find_all(class_='pl')[4].next_sibling
    # 语言
    language = info.find_all(class_='pl')[5].next_sibling
    # 上映日期
    date = info.find(attrs={'property': 'v:initialReleaseDate'}).string
    # 片长
    runtime = info.find(attrs={'property': 'v:runtime'}).string
    alternateName = info.find_all(class_='pl')[8].next_sibling
    # 将数据保存到集合中
    list = {'rate': rate, 'title': title, 'cover': cover, 'directors': directors, 'protagonists': protagonists,
            'types': types, 'ProductsCountry': ProductsCountry,
            'language': language, 'date': date, 'runtime': runtime, 'alternateName': alternateName}
    # 返回集合
    return json.dumps(list)

if __name__ == '__main__':
    name = urllib.parse.quote("热门", safe=string.ascii_letters)
    for i in range(0, 10):
        douban(name=name, count=i *20)
