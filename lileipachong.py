import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
from spider import diyizhixiao,zhixiaozhuanye,zhixiaobaodao,zhixiaotoutiao
import datetime


pattern1 = re.compile('<div class="biu_xw_title">([\s\S]*?)</div>')
pattern2 = re.compile('<div class="biu_xw_body">[\s\S]*?<div class="fx">')
pattern3 = re.compile('<h1>(.*?)</h1>')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}


def login(dr):
    dr.implicitly_wait(100)
    dr.get("http://xiaokenet.cn/admin_login.php?file=login")
    deng = dr.find_element_by_xpath('//*[@id="username"]')
    mi = dr.find_element_by_xpath('//*[@id="password"]')
    dian = dr.find_element_by_xpath('/html/body/table/tbody/tr[1]/td[2]/form/p[5]/input[2]')
    deng.send_keys("zxjzd")
    mi.send_keys("zxjzd")
    dian.click()


def upload_data(dr, title, zw):
    dr.switch_to_default_content()  # 切换回主页面
    dr.find_element_by_xpath('//*[@id="menu_news"]/li[1]/a').click()  # 点击发布信息
    dr.switch_to_frame("main")  # 切换到选择发布配置的子页面

    # driver.switch_to_default_content()
    # dr.switchTo().frame("framename or id")#不过时的方法
    # driver.switchTo().defaultContent()#切回主页面
    dr.find_element_by_xpath(
        "//form[@name='myform']//tbody[@id='tabs0']//span[@id='load_category_1']").click()  # 选择栏目
    dr.find_element_by_xpath(
        "//form[@name='myform']//tbody[@id='tabs0']//span[@id='load_category_1']//option[@value='1']").click()  # 选择栏目
    dr.find_element_by_xpath('//*[@id="title"]').send_keys(title)  # 发送文章的标题
    iframe = dr.find_elements_by_tag_name("iframe")[0]  # 切换到发送文章主体的子页面
    dr.switch_to_frame(iframe)  # 切换到发送文章主体的子页面
    dr.find_element_by_xpath('/html/body').send_keys(zw)  # 发送正文
    dr.switch_to_default_content()  # 切换回主页面
    dr.switch_to_frame("main")  ##切换到选择发布配置的子页面
    dr.find_element_by_xpath('//*[@id="listorder"]').clear()  # 填写排序
    dr.find_element_by_xpath('//*[@id="listorder"]').send_keys("60")  # 填写排序
    dr.find_element_by_xpath('//*[@id="cpcontainer"]/form/table/tbody[3]/tr/td[2]/input[1]').click()  # 提交

    sleep(5)
    dr.find_element_by_xpath("//a[text()='{}']".format(title)).click()  # 再次提交
    dr.switch_to_default_content()  # 再次提交
    dr.switch_to_frame("main")  # 再次提交
    dr.find_element_by_xpath('//*[@id="cpcontainer"]/form/table/tbody[3]/tr/td[2]/input[4]').click()  # 再次提交
    # html = driver.page_source
    dr.find_element_by_xpath("//a[text()='{}']/../preceding-sibling::*[2]".format(title)).click()  # 选中刚才发布的新闻

    dr.find_element_by_xpath('//*[@id="cpcontainer"]/table/tbody/tr[17]/td/div[2]/input[3]').click()  # 选择推荐
    dr.find_element_by_xpath('//*[@id="submit"]').click()  # 提交


if __name__ == '__main__':
    print('start')
    dt = datetime.datetime.now().strftime('%Y-%m-%d')

    chrome_options = Options()

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('blink-settings=imagesEnabled=false')

    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    login(driver)

    spider_list = [
        diyizhixiao,
        # zhixiaozhuanye,
        zhixiaobaodao,
        zhixiaotoutiao,
                   ]
    for i in spider_list:
        c = i.spider(dt)
        url_1 = c.get_subsurl()
        print(i,url_1)
        if url_1:
            for url in url_1:
                try:
                    title, zw = c.get_details(url)
                except Exception as e:
                    print(e)
                    continue
                # print(title,zw)
                if title and zw != "":
                    upload_data(driver, title, zw)

    driver.quit()
    print('end')
