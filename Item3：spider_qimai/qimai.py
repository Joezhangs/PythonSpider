#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/11/15 11:37
# software: PyCharm
import time
from retrying import retry
from selenium.webdriver import ActionChains
import re
from lxml import etree
import hu_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import sys
import os
import logging

path = "log"
if not os.path.exists(path):
    os.mkdir(path)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s -%(levelname)s -%(filename)s -%(funcName)s : %(message)s',
                    filename="{}/{}".format(path, "logging.log"))
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
# $ stream_handler.setLevel(level=logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s -%(levelname)s -%(filename)s -%(funcName)s : %(message)s'))
logger.addHandler(stream_handler)

shibai_num = 0


def action_click(browser, a):
    action = ActionChains(browser)
    action.move_to_element(a).click().perform()


@retry(stop_max_attempt_number=3)
def parse_html_twoC(HTML, HTML_twoC):
    """
    解析获取官网url
    :param HTML:存储的对象
    :param HTML_twoC:需要解析的HTML
    :return:存储的对象
    """
    HTML_twoC = etree.HTML(HTML_twoC)
    try:
        website_url = HTML_twoC.xpath(
            "//div[@class='info-wrap']/div[@class='info']/p[@class='app-info']/span[3]//text()")
    except:
        logger.info("元素不存在")
    if website_url:
        HTML["developer_website"] = "".join(''.join(website_url).split("·"))
    return HTML


@retry(stop_max_attempt_number=3)
def parse_html_twoA1(item1, item2, html):
    """
    采集ios详情页----应用信息
    :param item:存储的对象
    :param html:需要解析的html
    :return:存储的对象
    """
    logger.info("开始解析twoA1")
    html = etree.HTML(html)
    logo_url = html.xpath("//div[@id='app-side-bar']/img/@src")
    # print("logo_url:", "".join(logo_url))
    jietu_divs = html.xpath("//div[@class='screenshot-list'][1]/div/div")
    screenshot_url = ''
    for div in jietu_divs:
        screenshot_url += "".join(div.xpath("img/@src")) + ";\n"  # 应用截图
    app_name = html.xpath("//div[@class='appname']/text()")  # app名字
    app_name = "".join(app_name).split()
    print("app_name:", "".join(app_name))
    app_info = html.xpath("//div[@class='app-info']")[0]
    developer = app_info.xpath("div[@class='auther']//div[@class='value']/text()")  # 开发商
    classz = app_info.xpath("div[@class='genre']//a[@target='_blank']/text()")  # 分类
    price = app_info.xpath("div[@class='price']/div[@class='value']/text()")  # 价格
    app_desc = html.xpath("//div[@class='description']//text()")  # 描述
    ul_lis = html.xpath('//ul[@class="baseinfo-list"]/li')  # 支持网站li
    for ul_li in ul_lis:
        p_type = ul_li.xpath("p[@class='type']/text()")
        p_type = "".join(p_type)
        if "支持网站" in p_type:
            support_website = ul_li.xpath("p[@class='info']//text()")
            item1["support_website"] = "".join(support_website)
        if "内容评级" in p_type:
            content_rating = ul_li.xpath("p[@class='info']//text()")
            item1["content_rating"] = "".join(content_rating)
    item1["app_desc"] = "".join(app_desc)
    item2["app_desc"] = "".join(app_desc)
    item1["price"] = "".join(price)
    item1["classz"] = "".join(classz)
    item2["classz"] = "".join(classz)
    item1["developer"] = "".join(developer)
    item2["developer"] = "".join(developer)
    item1['app_name'] = "".join(app_name)
    item1["screenshot_url"] = screenshot_url
    item2["screenshot_url"] = screenshot_url
    item1["logo_url"] = ''.join(logo_url)
    item2["logo_url"] = ''.join(logo_url)
    item1["app_name"] = "".join(app_name)
    item2["app_name"] = "".join(app_name)
    logger.info("解析twoA1结束")
    return item1, item2


@retry(stop_max_attempt_number=3)
def parse_html_twoA3(item, html):
    """
    解析评论数据
    :param item:存储的对象
    :param html:需要解析的html
    :return:存储的对象
    """
    logger.info("开始解析twoA2")
    html = etree.HTML(html)
    average_rating = html.xpath("//div[@class='score-star'][1]/p[@class='num']/text()")[0]  # 平均评分
    comments_num = html.xpath("//div[@class='score-star'][1]/p[@class='comment-num-item']/text()")[0]  # 评论人数
    item["app_market"] = "App Store"
    item["average_rating"] = "".join(average_rating)
    item["comments_num"] = "".join(comments_num[:-3])
    logger.info("解析twoA2结束")
    return item


@retry(stop_max_attempt_number=3)
def parse_html_twoA7(item, html, ios_id):
    """
    解析排名数据
    :param item: 存储的对象
    :param html: 需要解析的页面
    :param ios_id:软件ios版本的id
    :return:存储的对象
    """
    logger.info("开始解析twoA7")
    html = etree.HTML(html)
    trs = html.xpath("//table[@class='data-table']//tr")
    list = []
    r = 0
    for tr in trs:
        r += 1
        if r >= len(trs):
            break
        if r == 1:
            has = tr.xpath("th/text()")
            list.append(has)
        if r == 2 or r == 3:
            d = 0
            tds = tr.xpath("td")
            li1s = []
            for td in tds:
                d += 1
                if d == 1:
                    li1 = td.xpath("text()")
                    li1 = "".join(li1)
                    # print(li1)
                    li1s.append(li1)
                if d == 2 or d == 3 or d == 4:
                    li1 = td.xpath("div/p[1]/text()")
                    li1 = "".join(li1)
                    # print(li1)
                    li1s.append(li1)
            # print(li1s)
            list.append(li1s)
    lzs = li_shuju(list)
    for lz in lzs:
        ios_Leaderboardl = {}
        ios_Leaderboardl["ios_id"] = ios_id
        ios_Leaderboardl["leaderboartl"] = ''.join(lz.split()).replace("（", "(").replace("）", ")")
        item.append(ios_Leaderboardl)
    logger.info("结束解析twoA7")
    return item


@retry(stop_max_attempt_number=3)
def li_shuju(list):
    """
    处理表数据
    :param list:传入一个列表
    :return: 处理过的表数据
    """
    # print(list)
    lzs = []
    list_ha = len(list)
    list_li = len(list[0])
    for i in range(1, list_ha):
        for z in range(1, list_li):
            a = list[i][0] + "-" + list[0][z] + ":" + list[i][z]
            lzs.append(a)
    # print("lzs", lzs)
    return lzs


@retry(stop_max_attempt_number=3)
def parse_html_twoB1(item, html):
    """
    解析
    :param item:
    :param html:
    :return:
    """
    logger.info("开始解析twoB1")
    html = etree.HTML(html)
    ul_lis = html.xpath('//ul[@class="baseinfo-list"]/li')  # 基本信息
    for ul_li in ul_lis:
        p_type = ul_li.xpath("p[@class='type']/text()")
        p_type = "".join(p_type)
        if "Bundle" in p_type:
            bundle = ul_li.xpath("p[@class='info']//text()")  # Bundle id
            item["Bundle_id"] = "".join(bundle)
    logger.info("结束解析twoB1")
    return item


@retry(stop_max_attempt_number=3)
def parse_html_twoB3(items, html, android_id):
    """
    解析评论
    :param items:
    :param html:
    :param android_id:
    :return:
    """
    logger.info("开始解析twoB3")
    html = etree.HTML(html)
    html = html.xpath("//div[@class='ivu-table']")[0]
    body_trs = html.xpath("div[@class='ivu-table-body']//tbody/tr")
    for body_tr in body_trs:
        item = {}
        tr = body_tr.xpath("td//span/text()")
        item["android_id"] = android_id
        item["app_market"] = tr[0]
        item["average_rating"] = tr[1]
        item["comments_num"] = tr[2]
        items.append(item)
    logger.info("结束解析twoB3")
    return items


@retry(stop_max_attempt_number=3)
def parse_html_twoB5(item, html, android_id):
    """
    解析排名数据
    :param item:
    :param html: 一个字典
    :param android_id: 软件安卓版本的id
    :return:
    """
    logger.info("开始解析twoB5")
    keys = html.keys()
    for key in keys:
        text = etree.HTML(html[key])
        trs = text.xpath("//tr[@class='ivu-table-row']")
        for tr in trs:
            itemz = {}
            span = tr.xpath("td//span/text()")
            itemz["leaderboardl"] = key + "-" + span[0] + ":" + span[1]
            itemz["android_id"] = android_id
            item.append(itemz)
    logger.info("结束解析twoB5")
    return item


@retry(stop_max_attempt_number=3)
def get_chrome(headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    if headless:
        options.add_argument("--headless")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def sele_app_id():
    conn = hu_utils.open_local_db("app_info")
    ress = hu_utils.select_one(conn)
    ids = []
    for res in ress:
        ids.append(res[0])
    return ids


def main():
    ids = sele_app_id()
    browser = get_chrome()
    browser.maximize_window()
    url = "https://www.qimai.cn/rank/index/brand/free/device/iphone/country/cn/genre/5000"
    browser.get(url)
    browser.implicitly_wait(10)
    wait = WebDriverWait(browser, 10)
    browser.get_screenshot_as_file('1.png')
    wait.until(EC.presence_of_element_located(('xpath', "//tr/td/div")))  # 等待
    time.sleep(1)
    global shibai_num
    shibai_num += 1
    if shibai_num == 1:
        shibai = browser.find_element("xpath", "//span[contains(@class,'icon-shibai')]")
        shibai.click()
        time.sleep(1)
    try:
        a = 0
        while True:
            if a > 24:
                break
            ul = browser.find_element("xpath", '//ul[contains(@class,"more-item-list")]')
            lis = ul.find_elements('xpath', "li")
            # print(len(lis))
            li = lis[a]
            aa = 0
            a += 1
            time.sleep(2)
            logger.info("开始爬取第{}页排行榜".format(a))
            browser.execute_script('window.scrollTo(0,0)')  # 上拉进度条
            li.click()  # 一级页面点击更换排行榜
            time.sleep(3)
            browser.refresh()
            wait.until(EC.presence_of_element_located(('xpath', "//tr/td/div")))  # 等待
            time.sleep(3.1)
            for i in range(3):  # 加载之后的第50到200的数据
                browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 下拉进度条
                time.sleep(5)
            browser.execute_script('window.scrollTo(0,0)')  # 上拉进度条
            time.sleep(5)
            trs = browser.find_elements("xpath", "//table/tbody/tr")
            # if a < 2:
            #     continue
            for tr in trs:
                aa += 1
                if aa > 200:
                    continue
                logger.info("开始爬取第{}条数据".format(aa))
                ios_android_ID = {}
                android_main = {}
                ios_main = {}
                ios_Leaderboardls = []
                android_Leaderboardls = []
                android_rating = []
                android_id = 0
                try:
                    browser.execute_script('window.scrollBy(0,67)')  # 进度条移动
                    time.sleep(0.3)
                    # if aa <= 198:
                    #     continue
                    # ios——info
                    tds = tr.find_elements("xpath", "td")
                    app_name = tds[1].find_element("xpath", 'div/div/a')
                    ios_url = app_name.get_attribute("href")  # ios 的url
                    ios_id = re.search("\/app\/rank\/appid\/(\d+)\/country\/cn", ios_url).group(1)  # ios的id
                    print("ios_id:", ios_id)
                    if int(ios_id) in ids:
                        logger.info("{}已存储到数据库".format(ios_id))
                        continue
                    try:
                        company_ulsz = tds[7].find_element("xpath", "a")
                        company_ulsz.click()
                        time.sleep(5)
                        browser.switch_to.window(browser.window_handles[1])  # 公司页面
                        HTML_twoC = browser.find_element("xpath", "//body").get_attribute("innerHTML")
                        ios_main = parse_html_twoC(ios_main, HTML_twoC)
                        browser.close()
                        time.sleep(2)
                        browser.switch_to.window(browser.window_handles[0])  # 初始页面
                    except:
                        logger.debug("获取元素出错，没有找到公司页面")
                    action_click(browser, app_name)
                    # action
                    time.sleep(5)
                    browser.switch_to.window(browser.window_handles[1])  # app详情页
                    try:
                        HTML_twoA7 = browser.find_element("xpath", "//body").get_attribute("innerHTML")
                        ios_Leaderboardls = parse_html_twoA7(ios_Leaderboardls, HTML_twoA7, ios_id)
                    except:
                        logger.info("parse_html_twoA7解析失败")
                    uls = browser.find_elements("xpath", "//ul[@class='select-list']")
                    lis0 = uls[0].find_elements("xpath", 'li')
                    li1 = lis0[1].find_element("xpath", 'a')
                    li3 = lis0[3].find_element("xpath", 'a')
                    li1.click()
                    time.sleep(5)
                    try:
                        HTML_twoA1 = browser.find_element("xpath", "//body").get_attribute("innerHTML")
                        ios_main, android_main = parse_html_twoA1(ios_main, android_main, HTML_twoA1)
                    except:
                        logger.info("解析失败")
                    li3.click()
                    time.sleep(5)
                    HTML_twoA3 = browser.find_element("xpath", "//body").get_attribute("innerHTML")
                    ios_main = parse_html_twoA3(ios_main, HTML_twoA3)

                    # 安卓--info
                    button_a = browser.find_element("xpath", '//button[contains(@class,"btn-android")]')
                    button_text = button_a.text
                    # print(button_text)
                    if "发现安卓版" not in button_text:
                        button_a.click()
                        time.sleep(5)
                        android_url = browser.current_url  # 获取的是安卓页面的url
                        android_main["caiji_url"] = android_url
                        # print(android_url)
                        android_id = re.search("\/andapp\/baseinfo\/appid\/(\d+)", android_url).group(1)  # 安卓的id
                        android_main["android_id"] = android_id
                        uls = browser.find_elements("xpath", "//ul[@class='select-list']")
                        lis1 = uls[0].find_elements("xpath", 'li')
                        lis2 = uls[1].find_elements("xpath", 'li')
                        li1 = lis1[1].find_element("xpath", 'a')
                        li3 = lis1[3].find_element("xpath", 'a')
                        li5 = lis2[1].find_element("xpath", 'a')
                        li1.click()
                        time.sleep(5)
                        HTML_twoB1 = browser.find_element("xpath", "//body").get_attribute("innerHTML")
                        android_main = parse_html_twoB1(android_main, HTML_twoB1)
                        li3.click()
                        time.sleep(5)
                        try:
                            HTML_twoB3 = browser.find_element("xpath", "//body").get_attribute("innerHTML")
                            android_rating = parse_html_twoB3(android_rating, HTML_twoB3, android_id)
                        except:
                            logger.info("解析失败")
                        li5.click()
                        time.sleep(5)
                        HTML_twoB5 = {}
                        try:
                            towB5 = browser.find_element("xpath", "//div[contains(@class,'ivu-tabs-tab-active')]").text
                            # print("towB5:",towB5)
                            HTML_twoB5[towB5] = browser.find_element("xpath", "//div[@id='rank-info']").get_attribute(
                                "innerHTML")
                            ivu_tabs = browser.find_elements("xpath", "//div[@class='ivu-tabs-tab']")
                            z = 0
                            for ivu_tab in ivu_tabs:
                                z += 1
                                if (z % 2) == 0:
                                    # print(ivu_tab.text)
                                    ivu_tab.click()
                                    time.sleep(4)
                                    azz = ""
                                    azz = browser.find_element("xpath",
                                                               "//div[contains(@class,'ivu-tabs-tab-active')]").text
                                    HTML_twoB5[azz] = browser.find_element("xpath",
                                                                           "//div[@id='rank-info']").get_attribute(
                                        "innerHTML")
                            android_Leaderboardls = parse_html_twoB5(android_Leaderboardls, HTML_twoB5, android_id)
                        except:
                            logger.debug("无排名数据")
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()  # 关闭一个多余页面
                    time.sleep(1)
                    browser.switch_to.window(browser.window_handles[0])  # 更换页面
                    # info
                    ios_main["ios_id"] = ios_id
                    ios_main["caiji_url"] = ios_url
                    ios_android_ID["ios_id"] = ios_id
                    ios_android_ID["android_id"] = android_id
                    logger.info("解析结束，开始存储数据")
                except:
                    logger.info("-----第{}条数据获取失败-----".format(aa))
                    while len(browser.window_handles) > 1:
                        logger.info('关闭一个多余窗口！')
                        browser.switch_to.window(browser.window_handles[1])
                        browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                finally:
                    logger.info("开始数据存储")
                    if ios_main:
                        conn = hu_utils.open_local_db("app_info")
                        hu_utils.insert_update_one(conn, ios_main, "ios_main")
                    else:
                        logger.info("ios_main 无数据")
                    if "android_id" in android_main.keys():
                        conn = hu_utils.open_local_db("app_info")
                        hu_utils.insert_update_one(conn, android_main, "android_main")
                    if ios_android_ID:
                        conn = hu_utils.open_local_db("app_info")
                        hu_utils.insert_update_one(conn, ios_android_ID, "ios_android_ID")
                    else:
                        logger.info("ios_android_ID 无数据")
                    if ios_Leaderboardls:
                        conn = hu_utils.open_local_db("app_info")
                        hu_utils.insert_update_many(conn, ios_Leaderboardls, "ios_Leaderboardls")
                    else:
                        logger.info("ios_Leaderboardls 无数据")
                    if android_Leaderboardls:
                        conn = hu_utils.open_local_db("app_info")
                        hu_utils.insert_update_many(conn, android_Leaderboardls, "android_Leaderboardls")
                    else:
                        logger.info("android_Leaderboardls 无数据")
                    if android_rating:
                        conn = hu_utils.open_local_db("app_info")
                        hu_utils.insert_update_many(conn, android_rating, "android_rating")
                    else:
                        logger.info("android_rating 无数据")
    finally:
        logger.info("关闭浏览器")
        browser.quit()


if __name__ == "__main__":
    main()
