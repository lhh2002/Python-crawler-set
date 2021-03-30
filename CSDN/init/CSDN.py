
import time
from threading import Thread
from queue import Queue
import requests
from lxml import etree


class CSDN_url(object):
    def __init__(self,url):
        if url[:22] == "https://blog.csdn.net/" and len(url) <= 22:
            raise ValueError("你想帮CSDN首页刷访客?")
        elif url[:22] == "https://blog.csdn.net/" and len(url) > 22:
            pass
        else:
            raise ValueError("网址出现错误，请检查后运行")
        self.url = url
        self.q = Queue()
        self.payload = ""
        self.headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Cookie": "l=AurqcPuigwQdnQv7WvAfCoR1OlrRQW7h; isg=BHp6mNB79CHqYXpVEiRteXyyyKNcg8YEwjgLqoRvCI3ddxqxbLtOFUBGwwOrZ3ad; thw=cn; cna=VsJQERAypn0CATrXFEIahcz8; t=0eed37629fe7ef5ec0b8ecb6cd3a3577; tracknick=tb830309_22; _cc_=UtASsssmfA%3D%3D; tg=0; ubn=p; ucn=unzbyun; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=981798063989731689; hng=CN%7Czh-CN%7CCNY%7C156; um=0712F33290AB8A6D01951C8161A2DF2CDC7C5278664EE3E02F8F6195B27229B88A7470FD7B89F7FACD43AD3E795C914CC2A8BEB1FA88729A3A74257D8EE4FBBC; enc=1UeyOeN0l7Fkx0yPu7l6BuiPkT%2BdSxE0EqUM26jcSMdi1LtYaZbjQCMj5dKU3P0qfGwJn8QqYXc6oJugH%2FhFRA%3D%3D; ali_ab=58.215.20.66.1516409089271.6; mt=ci%3D-1_1; cookie2=104f8fc9c13eb24c296768a50cabdd6e; _tb_token_=ee7e1e1e7dbe7; v=0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;` rv:47.0) Gecko/20100101 Firefox/47.0"
            }
    def run(self):
        dicts = self.article()
        p1 = Thread(target=self.Producer,args=(dicts,))
        p1.start()
        c1 = Thread(target=self.Consumer, args=(dicts,))
        c1.start()
    def Producer(self,your_dict):
        self.count = 0
        while your_dict:
            while self.count < 20:
                html = requests.get("https://www.kuaidaili.com/free",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"})
                if html.status_code == 200:
                    text = html.text
                else:
                    continue

                dom = etree.HTML(text)
                ip_ids = dom.xpath('//*[@id="list"]/table/tbody/tr[*]/td[1]/text()')
                port_ids = dom.xpath('//*[@id="list"]/table/tbody/tr[*]/td[2]/text()')
                for a,b in zip(ip_ids,port_ids):
                    ip=a.replace("\n\t\t\t","").replace("\t\t","")
                    port=b.replace("\n\t\t\t","").replace("\t\t","")
                    proxy=ip+":"+port
                    try:
                        proxies = {"http": proxy}
                        response = requests.get('http://www.baidu.com', proxies=proxies)
                        if response.status_code == 200:
                            self.count += 1
                            self.q.put(proxies)
                            print("[Info] 成功获取代理{},现在所存代理数为{}".format(proxies,self.count))
                            break
                    except:
                        pass
            else:
                print("[warning] 当前代理池超过20,请等待消耗")
    def Consumer(self,your_dict):
        print("[Info] 准备代理时间,静默30秒")
        time.sleep(30)
        while your_dict:
            while not self.q.empty():
                proxies = self.q.get()
                print("[Info] 当前使用{}代理".format(proxies))
                for url in your_dict.keys():
                    try:
                        html = requests.get(url, proxies=proxies, timeout=2)
                        if html.status_code == 200:
                            your_dict[url] += 1
                            print("[Info] 访问{}成功,当前访问数为{}".format(url,your_dict[url]))
                            self.frequency_number(your_dict,url)
                            time.sleep(1)
                        else:
                            print("[warning] 代理出现问题,静默2秒")
                            time.sleep(2)
                    except Exception as err:
                        print("[warning] CSDN出现问题,错误原因为{},静默120秒".format(err))
                        time.sleep(120)
                    print("[Info] 此代理{}已使用成功,删除代理".format(proxies))
                self.count -= 1
            else:
                print("[warning] 代理为空,正在使用本地访问CSDN，静默10秒")
                for url in your_dict.keys():
                    html = requests.request("GET", url, data=self.payload, headers=self.headers)
                    if html.status_code == 200:
                        your_dict[url] += 1
                        print("[Info] 访问{}成功,当前访问数为{}".format(url,your_dict[url]))
                        self.frequency_number(your_dict,url)
                        time.sleep(1)
                time.sleep(10)
    def frequency_number(self,your_dict,url):
        your_num = your_dict[url]
        if your_num >= 10000:
            print("[Info] 检测一篇文章访问量过万,删除文章访问")
            your_dict.pop(url)
    def article(self):
        dicts,num = {},0
        resp = requests.request("GET", self.url, data=self.payload, headers=self.headers)
        resp.encoding = resp.apparent_encoding
        html_source = resp.text
        dom = etree.HTML(html_source)
        articles = dom.xpath('//*[@id="articleMeList-blog"]/div[2]/div[*]/h4/a/@href')
        frequency = dom.xpath('//*[@id="articleMeList-blog"]/div[2]/div[*]/div[1]/p/span[2]/text()')

        for a,b in zip(articles,frequency):
            if int(b) < 10000:
                num += 1
                dicts[a] = int(b)
        print("[Info] 该账号剩余{}篇文章未达万访问".format(num))
        return dicts
def main(url):
    # print(url)
    pop = CSDN_url(url)
    pop.run()
