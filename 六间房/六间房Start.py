#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-crawler-set 
@File    ：六间房Start.py
@IDE     ：IntelliJ IDEA 
@Author  ：大数据老哥
@Date    ：2020/12/19 15:21 
'''

# 导入所需要的依赖
import requests
import re


# 过滤掉特殊字符
def match(title):
    compile= re.compile(r'[\\\/:\*\?\"><\|]')
    match = re.sub(compile, "_",title)
    return match

# 设置请求头等参数，防止被反爬
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}

def  main(num):
    url="https://v.6.cn/minivideo/getMiniVideoList.php?act=recommend&page=%s&pagesize=50" %(num)
    print("开始下载第%s页" %(num))
    # 发送请求
    data=requests.get(url,headers=headers)
    # 解析数据
    json=data.json()
    # 解析出我们想要的数据来
    datalist=json["content"]["list"]
    # 循环遍历数据
    for data in datalist:
      #获取title
      title=data["alias"]+'.mp4'
      newTitle=match(title)
      # 获取视频url
      playurl=data["playurl"]
      # 在次发一次请求 来请求视频数据
      video=requests.get(playurl,headers=headers)
      with open("video\\"+newTitle,'ab') as output:
           # 以二进制的形式写入到本地
           output.write(video.content)
      print("下载成功: ",newTitle)
if __name__ == '__main__':
    for i in range(1,10):
        main(i)