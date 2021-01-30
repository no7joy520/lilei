import requests
from lxml import etree
import datetime
import re

class diyi():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    def get_subsurl(self):
        url = "http://www.zhixiao001.com/html/rd/index.html"
        html = requests.get(url=url, headers=self.headers, timeout=31).text
        html_obj = etree.HTML(html)
        dt = datetime.datetime.now().strftime('%Y-%m-%d')
        # dt = "2021-01-15"
        node_list1 = html_obj.xpath('//*[@id="post-data"]/div')
        list_url = []
        for i in node_list1:
            if str(i.xpath("string(./ div[2] / div[1] / div / span[2])"))[0:10] == dt:
                list_url.append(i.xpath("./div[2]/h2/a/@href")[0])
            else:
                break
        return list_url
    def get_details(self,url):
        base_url = "http://www.zhixiao001.com"
        pattern1 = re.compile('<div class="biu_xw_title">([\s\S]*?)</div>')
        pattern2 = re.compile('<div class="biu_xw_body">[\s\S]*?<div class="fx">')
        pattern3 = re.compile('<h1>(.*?)</h1>')
        pattern4 = re.compile('(【.*?】)([\s\S]*)(【.*?】)')

        html = requests.get(url=base_url+url, headers=self.headers,
                            timeout=31).content.decode('utf8')

        title = pattern3.findall(pattern1.findall(html)[0])[0]
        zw = pattern2.findall(html)[0]
        zw = pattern4.sub(r'【直销界】\2', zw)
        return title,zw

if __name__ == '__main__':
    c =diyi()
    urll = c.get_subsurl()
    title,zw = c.get_details(urll[0])
    print(title)
    print(zw)
	#蓝冰
