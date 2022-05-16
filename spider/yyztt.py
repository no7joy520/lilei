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
        url = "http://www.yitb.com/category-22"
        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode(res.apparent_encoding)
        html_obj = etree.HTML(html)
        dt = self.dt
        # dt = "2022-05-12"
        dt1 = dt.split("-")
        dt1[1] = dt.split("-")[1].replace("0", "")
        dt = "-".join(dt1)
        node_list1 = html_obj.xpath('//div[@class="hot-jobs-list"]')
        sj_x = './/div[@class="hot-jobs-content"]/ul/li/span/text()'


        lianj = './/div[@class="hot-jobs-content"]/h3/a/@href'
        list_url = []
        try:
            for i in node_list1:
                sj = i.xpath(sj_x)[0].strip()
                if sj == dt:
                    # href = urljoin(url, i.xpath(lianj)[0].strip())
                    list_url.append(urljoin(url, i.xpath(lianj)[0].strip()))
                else:
                    break
        except Exception as e:
            print(e)

        return list(reversed(list_url))


    def get_details(self, url):

        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode('gbk')
        html_obj = etree.HTML(html)

        zw_xp = '//div[@id="article_body"]'
        t_xp = './/div[@class="news-content"]/h1/text()'
        zw = html_obj.xpath(zw_xp)[0]
        zw = etree.tostring(zw,encoding='utf-8').decode('utf8')


        title = html_obj.xpath(t_xp)[0]
        return title, zw


if __name__ == '__main__':
    c = spider(dt="2021-04-20")
    urll = c.get_subsurl()
    # print(urll)
    title, zw = c.get_details('http://www.yitb.com/index.php/viewnews-8707')
    print(title)
    print(zw)