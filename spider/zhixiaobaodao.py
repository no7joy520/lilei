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
        url = "http://www.chndsnews.com/toutiao/"
        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode(res.apparent_encoding)
        html_obj = etree.HTML(html)
        dt = self.dt
        # dt = "2021-04-20"
        node_list1 = html_obj.xpath('//div[@class="listbox"]/ul/li')
        sj = './span/text()'
        lianj = './a/@href'
        list_url = []
        try:
            for i in node_list1:
                if i.xpath(sj)[1].strip()[0:10] == dt:
                    # href = urljoin(url, i.xpath(lianj)[0].strip())
                    list_url.append(urljoin(url, i.xpath(lianj)[0].strip()))
                else:
                    break
        except Exception as e:
            print(e)

        return list(reversed(list_url))


    def get_details(self, url):

        res = requests.get(url=url, headers=self.headers, timeout=31)
        html = res.content.decode(res.apparent_encoding)
        html_obj = etree.HTML(html)

        page_rule = '//ul[@class="pagelist"]/li'
        dpattern = re.compile(r'(lmth\..*?)/')#请求页尾
        srcpattern = re.compile(r'src="(.*?)"')
        durl = url[::-1]
        zw = ""
        zhixiaopattren = re.compile(r'&#12304;&#30452;&#25253;.*?&#12305;')
        zerenpattren = re.compile(r'<p>&#13;\s*?&#36131;&#20219;&#32534;&#36753;[\S\s]*</strong></p>')
        zhixiaojie = '&#12304;直销界&#12305;'

        zw += etree.tostring(html_obj.xpath('//div[@class="content"]')[0]).decode('utf8')

        if html_obj.xpath(page_rule):
            page_l = html_obj.xpath(page_rule)[3:len(html_obj.xpath(page_rule))-1]

            for i in page_l:

                res1 = requests.get(url=url.replace(dpattern.findall(durl)[0][::-1],i.xpath("./a/@href")[0]),headers=self.headers)
                html_obj1 = etree.HTML(res1.content.decode(res.apparent_encoding))
                zw += etree.tostring(html_obj1.xpath('//div[@class="content"]')[0]).decode('utf8')

        for i in srcpattern.findall(zw):
            zw = zw.replace(i, urljoin(url, i))

        try:
            zw = zw.replace(zerenpattren.findall(zw)[0], "")
        except Exception as e:
            pass
        zw = zw.replace(zhixiaopattren.findall(zw)[0], zhixiaojie)

        title = html_obj.xpath('//div[@class="title"]/h2/text()')[0]
        return title, zw


if __name__ == '__main__':
    c = spider(dt="2021-04-20")
    urll = c.get_subsurl()
    # print(urll)
    title, zw = c.get_details("http://www.chndsnews.com/toutiao/2021/0416/116351.html")
    print(title)
    print(zw)