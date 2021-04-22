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
        url = "http://www.cdsp.com.cn/index.php/Zixun/index"
        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode(res.apparent_encoding)
        html_obj = etree.HTML(html)
        # dt = self.dt
        dt = "2021-04-19"
        node_list1 = html_obj.xpath('//div[@id="content"]//ul[@id="xinwenhuizong"]//div[@class="twos_tits2"]')
        sj = './span/text()'
        lianj = './a/@href'
        list_url = []
        try:
            for i in node_list1:
                if i.xpath(sj)[0].strip() == dt:
                    # href = urljoin(url, i.xpath(lianj)[0].strip())
                    list_url.append(urljoin(url, i.xpath(lianj)[0].strip()))
                else:
                    break
        except Exception as e:
            print(e)

        # return list(reversed(list_url))
        return list(reversed(list_url))[0:3]

    def get_details(self, url):

        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode(res.apparent_encoding)
        html_obj = etree.HTML(html)
        zw = etree.tostring(html_obj.xpath('//div[@class="lists"]')[0]).decode('utf8')
        pattern1 = re.compile('src="(.*?)"/>')
        pic_href = pattern1.findall(zw)
        if pic_href:
            for i in pic_href:
                zw = zw.replace(i, urljoin(url, i))
        title = html_obj.xpath('//div[@class="titlest"]/text()')[0]
        return title, zw


if __name__ == '__main__':
    c = spider()
    urll = c.get_subsurl()
    # print(urll)
    for i in urll:
        title, zw = c.get_details(i)
        print(title)
        print(zw)
    #
