#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-crawler-set 
@File    ：穷游start.py
@IDE     ：IntelliJ IDEA 
@Author  ：大数据老哥
@Date    ：2020/12/27 12:15 
'''

import pypinyin
import requests
import parsel
import csv
from concurrent.futures import ThreadPoolExecutor
import jieba
from wordcloud import WordCloud

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0' }

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

# 下载中国信息
nameList=[]
def China(num):
  url="https://place.qyer.com/china/citylist-0-0-"+num
  html= requests.get(url,headers=headers)
  text=html.text
  dom=parsel.Selector(text)
  lilist=dom.xpath("//*[@class='plcCitylist']/li")
  print("正在爬取第%s页"%num)
  for list in lilist:
      # 获取name
      travel_name=list.xpath(".//h3/a/text()").get()
      # 获取去过的人数
      travel_number =list.xpath(".//p[@class='beento']/text()").get()
      # 获取图片地址
      travel_image=list.xpath(".//p[@class='pics']/a/img/@src").get()
      # 获取介绍
      travel_hot=list.xpath(".//p[@class='pois']/a/text()").getall()
      # 去掉空格
      travel_hot=[hot.strip() for hot in travel_hot]
      # 转换为字符串
      travel_hot='.'.join(travel_hot)
      # 获取城市url
      travel_url ="https:"+list.xpath(".//h3/a/@href").get()
      # 数据保存
      nameList.append(".".join(travel_name))
      with open('穷游中国数据.csv',mode='a',encoding='utf-8',newline='') as f:
          csv_writer=csv.writer(f)
          csv_writer.writerow([travel_name,travel_number,travel_hot,travel_url,travel_image])
  print("爬取完成第%s页"%num)

def create_wordcloud(comments,name):
    content = ''.join(comments)
    wl = jieba.cut(content,cut_all=True)
    wl_space_split = ' '.join(wl)
    wc = WordCloud('simhei.ttf',
                   background_color='white', # 背景颜色
                   width=1000,
                   height=600,).generate(wl_space_split)
    wc.to_file('%s.png'%name)

def province_id(name):
    url="https://place.qyer.com/%s/sight/"%(pinyin(name))

    html= requests.get(url,headers=headers)
    text=html.text
    dom=parsel.Selector(text)
    return dom.xpath("//p[@class='plcMenuBarAddPlan fontYaHei']/a/@data-pid").get()
def province(name,id,num):
    url="https://place.qyer.com/poi.php?action=list_json"
    data={
      'page':num,
      'type':'city',
      'pid':id,
      'sort':'32',
      'subsort':'all',
      'isnominate':'-1',
      'haslastm':'false',
      'rank':'6',
    }
    list=requests.post(url,headers=headers,data=data).json()
    datas=list['data']['list']
    for data in datas:
        province_image=(data['photo']).strip()
        # 页面地址
        province_url=("https:"+data['url']).strip()
        # 获取名称
        province_name=(data['cnname']).strip()
        # 获取评分
        province_score=(data['grade']).strip()
        # 获取点评人数
        province_comment=(data['commentCount']).strip()

        province_introduce=(data['comments'][0]['text']).strip()
        province_introduce=province_introduce.replace("\n","").replace(" ","")
        nameList.append(province_name)
        with open('穷游%s数据.csv'%name,mode='a',encoding='utf-8',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow([province_name,province_score,province_comment,province_introduce,province_url,province_image])

    print("%s爬取完成第%s页"%(name,num))
def main():

    input_str=input("请求输入要获取的城市名称：比如 北京、上海 默认是中国")
    if input_str=="":
        pool = ThreadPoolExecutor(10)
        for i  in range(1,100):
            pool.submit(China,i.__str__())
        pool.shutdown(wait=True)
        names=[list.strip() for list in nameList]
        create_wordcloud(names,"中国词汇")
    elif input_str=='中国':
        pool = ThreadPoolExecutor(10)
        for i  in range(1,100):
            pool.submit(China,i.__str__())
        pool.shutdown(wait=True)
        names=[list.strip() for list in nameList]
        create_wordcloud(names,"中国词汇")
    else:
        pool = ThreadPoolExecutor(10)
        id=province_id(input_str)
        for i in range(1,100):
            pool.submit(province,input_str,id,i.__str__())
        pool.shutdown(wait=True)
        names=[list.strip() for list in nameList]
        create_wordcloud(names,"%s词汇"%input_str)


if __name__ == '__main__':
    main()