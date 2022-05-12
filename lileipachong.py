import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# from time import sleep
import time
import re
from spider import diyizhixiao,zhixiaozhuanye,zhixiaobaodao,zhixiaotoutiao
import datetime
import os


pattern1 = re.compile('<div class="biu_xw_title">([\s\S]*?)</div>')
pattern2 = re.compile('<div class="biu_xw_body">[\s\S]*?<div class="fx">')
pattern3 = re.compile('<h1>(.*?)</h1>')
overtime = 1000
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

def init_dr():
    chrome_options = Options()

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('blink-settings=imagesEnabled=false')

    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    return driver


def login(dr):
    dr.implicitly_wait(10)
    # dr.get("https://www.xiaokenet.cn/admin_login.php")
    dr.get("https://www.zhixiaojie.cn/admin_login.php")
    deng = dr.find_element_by_xpath('//*[@id="username"]')
    mi = dr.find_element_by_xpath('//*[@id="password"]')
    dian = dr.find_element_by_xpath('/html/body/table/tbody/tr[1]/td[2]/form/p[5]/input[2]')
    deng.send_keys("admin")
    mi.send_keys("bjtxj0987")
    dian.click()







def upload_data(dr, title, zw):

    dr.switch_to_default_content()  # 切换回主页面
    dr.find_element_by_xpath('//*[@id="header_news"]').click()  # 点击信息资讯
    dr.find_element_by_xpath('//*[@id="menu_news"]/li[2]/a').click()  # 点击发布信息
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

    time.sleep(5)
    dr.find_element_by_xpath("//a[text()='{}']".format(title)).click()  # 再次提交
    dr.switch_to_default_content()  # 再次提交
    dr.switch_to_frame("main")  # 再次提交
    dr.find_element_by_xpath('//*[@id="cpcontainer"]/form/table/tbody[3]/tr/td[2]/input[4]').click()  # 再次提交
    # html = driver.page_source
    # locator = dr.find_element_by_xpath("//a[text()='{}']/../preceding-sibling::*[2]".format(title))
    locator = (By.XPATH, "//a[text()='{}']/../preceding-sibling::*[2]".format(title))
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable(locator))
    dr.find_element(*locator).click()# 选中刚才发布的新闻


    dr.find_element_by_xpath('//*[@id="cpcontainer"]/table/tbody/tr[17]/td/div[2]/input[3]').click()  # 选择推荐
    dr.find_element_by_xpath('//*[@id="submit"]').click()  # 提交




if __name__ == '__main__':
    start_now = datetime.datetime.now()
    print(start_now.strftime('%Y-%m-%d %H:%M:%S'),'start')
    dt = start_now.strftime('%Y-%m-%d')

    driver = init_dr()
    login(driver)
    upload_data(driver, "tesy", "testyjjjj")

    # spider_list = [
    #     diyizhixiao,
    #     # zhixiaozhuanye,
    #     zhixiaobaodao,
    #     zhixiaotoutiao,
    #                ]
    # for i in spider_list:
    #     c = i.spider(dt)
    #     url_1 = c.get_subsurl()
    #     print(i,url_1)
    #     if url_1:
    #         for url in url_1:
    #             try:
    #                 title, zw = c.get_details(url)
    #             except Exception as e:
    #                 print(e)
    #                 continue
    #             # print(title,zw)
    #
    #             if title and zw != "":
    #                 print(title, "即将上传")
    #                 try:
    #                     upload_data(driver, title, zw)
    #                 except Exception as e:
    #                     print(e)
    #                     driver.quit()
    #                     # os.system("ps -ef | grep 'chromedriver' | grep -v grep | awk '{print $2}' | xargs kill -s SIGINT")
    #                     driver = init_dr()
    #                     login(driver)
    #                     continue



    driver.quit()
    print(datetime.datetime.now(),'end')
    print("耗时",datetime.datetime.now()-start_now)
