import requests
from lxml import etree
import datetime
import re
from urllib.parse import urljoin



class spider():
    def __init__(self,dt):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.dt = dt

    def get_subsurl(self):
        url = "https://www.dstoutiao.com/?page={}"
        dt = self.dt
        # dt = "2021-04-13"
        # sj = './a/span/text()'
        lianj = './a/@href'
        list_url = []

        for i in range(1,3):

            res = requests.get(url=url.format(i), headers=self.headers, timeout=31)
            html = res.content.decode(res.apparent_encoding)
            html_obj = etree.HTML(html)
            node_list1 = html_obj.xpath('//div[@class="index_page_main"]//ul[@class="index_news_list1 fl"]/li')


            try:
                for u in node_list1:
                    list_url.append(urljoin(url, u.xpath(lianj)[0].strip()))

            except Exception as e:
                print(e)

        return list(reversed(list_url))


    def get_details(self, url):

        dt = self.dt
        # dt = "2021-04-22"
        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode(res.apparent_encoding)
        html_obj = etree.HTML(html)

        sj = html_obj.xpath(
            '//div[@class="subpage_main"]//ul[@class="news_neirong"]/li[@class="news_fubiao"]/span[1]/text()')

        content = html_obj.xpath('//div[@class="subpage_main"]//ul[@class="news_neirong"]/li[4]')
        title = html_obj.xpath('//div[@class="subpage_main"]//ul[@class="news_neirong"]/li[1]/h4/text()')

        if sj[0][3:14].strip() != dt:
            return "",""

        return title[0], etree.tostring(content[0]).decode('utf8')


if __name__ == '__main__':
    c = spider(dt="2021-04-20")
    urll = c.get_subsurl()
    # print(urll)
    title, zw = c.get_details("https://www.dstoutiao.com/html/ds/zxfull/2021/0422/98886.html")
    print(title)
    print(zw)
    print("meishuchu")