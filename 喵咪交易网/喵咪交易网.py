#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-crawler-set 
@File    ：喵咪交易网.py
@IDE     ：IntelliJ IDEA 
@Author  ：大数据老哥
@Date    ：2021/4/16 20:31 
'''
import requests
import parsel, csv

f = open('喵咪.csv', mode='a', encoding='utf-8', newline='')

csvHeader = csv.DictWriter(f,
                           fieldnames=['地区', '标签', '价格', '浏览次数', '卖家承诺', '在售只数', '地区', '品种', '预防', '联系人姓名', '电话',
                                       '运费', '是否纯种', '待售数量', '猫咪性别', '猫咪年龄', '驱虫情况', '可视频看猫咪', '详情地址'])

csvHeader.writeheader()
for i in range(1,10):

    url = "http://www.maomijiaoyi.com/index.php?/chanpinliebiao_pinzhong_37_"+str(i)+"--24.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
    }
    data = requests.get(url=url, headers=headers).text
    selector = parsel.Selector(data)
    urls = selector.css('div .content:nth-child(1) a::attr(href)').getall()
    address = selector.css('div .content:nth-child(1) .area .color_333::text').getall()
    address = [i.strip() for i in address]
    regionAndURL = zip(urls, address)
    for s in regionAndURL:
        url = "http://www.maomijiaoyi.com" + s[0]
        address = s[1]
        data = requests.get(url=url, headers=headers).text
        selector = parsel.Selector(data)
        title = selector.css('.detail_text .title::text').get().strip()  ## 标签
        price = selector.css('.info1 span:nth-child(2)::text').get().strip()  ## 价格
        viewsNum = selector.css('.info1 span:nth-child(4)::text  ').get()  ## 浏览次数
        commitment = selector.css('.info1 div:nth-child(2) span::text  ').get().replace("卖家承诺: ", "")  # 卖家承诺
        onlineOnly = selector.css('.info2 div:nth-child(1) .red::text  ').get()  # 在售只数
        variety = selector.css('.info2 div:nth-child(3) .red::text  ').get()  # 品种
        prevention = selector.css('.info2 div:nth-child(4) .red::text  ').get()  # 预防
        contactPerson = selector.css('.user_info div:nth-child(1) .c333::text  ').get()  # 联系人姓名
        phone = selector.css('.user_info div:nth-child(2) .c333::text  ').get()  ## 电话
        shipping = selector.css('.user_info div:nth-child(3) .c333::text  ').get().strip()  # 运费
        purebred = selector.css('.item_neirong div:nth-child(1) .c333::text').get().strip()  # 是否纯种
        quantityForSale = selector.css('.item_neirong div:nth-child(3) .c333::text').get().strip()  # 待售数量
        catSex = selector.css('.item_neirong div:nth-child(4) .c333::text').get().strip()  # 猫咪性别
        catAge = selector.css('div.xinxi_neirong .item:nth-child(2)  div:nth-child(2) .c333::text').get().strip()  # 猫咪年龄
        dewormingSituation = selector.css(
            'div.xinxi_neirong .item:nth-child(2)  div:nth-child(3) .c333::text').get().strip()  # 驱虫情况
        canWatchCatsInVideo = selector.css(
            'div.xinxi_neirong .item:nth-child(2)  div:nth-child(4) .c333::text').get().strip()  # 可视频看猫咪
        print("正在爬取这只喵咪的信息=>"+title)
        dis = {
            '地区': address,
            '标签': title,
            '价格': price,
            '浏览次数': viewsNum,
            '卖家承诺': commitment,
            '在售只数': onlineOnly,
            '品种': variety,
            '预防': prevention,
            '联系人姓名': contactPerson,
            '电话': phone,
            '运费': shipping,
            '是否纯种': purebred,
            '待售数量': quantityForSale,
            '猫咪性别': catSex,
            '猫咪年龄': catAge,
            '驱虫情况': dewormingSituation,
            '可视频看猫咪': canWatchCatsInVideo,
            '详情地址': url
        }
        csvHeader.writerow(dis)
