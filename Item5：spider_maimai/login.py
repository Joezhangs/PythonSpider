# -*- coding: UTF-8 -*-
# author:吉祥鸟
# datetime:2018/12/6 13:48
# software: PyCharm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
import re
import random
import hu_utils3
import logging
from logging.handlers import RotatingFileHandler
import os

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
# 定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大1K
rHandler = RotatingFileHandler("log.txt", maxBytes=10 * 1024, backupCount=3)
rHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rHandler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(rHandler)
logger.addHandler(console)


def random_steep():
    """
    防止封号，随机暂停
    :return:
    """
    a = random.randint(2, 8)
    logger.info("暂停{}秒".format(a))
    time.sleep(a)


def get_cookies():
    """
    使用selenium获取cookies的值，将其存在文件中
    :return:
    """
    logger.info("使用selenium获取cookies")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-gpu')  # 谷歌文件提到需要加这个属性来规避bug
    chrome_options.add_argument('--headless')  # 无界面设置
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    login_url = "https://acc.maimai.cn/login"
    chrome.get(login_url)
    wait = WebDriverWait(chrome, 10)
    wait.until(EC.element_to_be_clickable(('xpath', "//input[@class='loginBtn']")))
    time.sleep(1)
    user_name = "15755656557"  # 你的手机号
    password = "199618hu"  # 你的密码
    chrome.find_element("xpath", "//input[@class='loginPhoneInput']").send_keys(user_name)
    time.sleep(1)
    chrome.find_element("xpath", "//input[@id='login_pw']").send_keys(password)
    chrome.find_element('xpath', "//input[@class='loginBtn']").click()
    cookies = chrome.get_cookies()
    with open("cookie.json", "w+")as f:
        f.write(json.dumps(cookies))
        f.close()
    logger.info("cookies获取成功")
    chrome.close()


def get_req():
    """
    打开cookies文件获取cookie，进行requests请求
    :return:
    """
    logger.info("打开cookie文件获取cookies")
    with open("cookie.json", "r")as f:
        cookies = json.loads(f.readline())
    req = requests.Session()
    for cookie in cookies:
        req.cookies.set(cookie["name"], cookie["value"])
    return req


def cookies_expried():
    """
    判断cookies是否过期，若过期会自动登录获取cookies
    :return:
    """
    file = os.path.isfile("cookie.json")
    print(file)
    if not file:
        get_cookies()
    req = get_req()
    url = "https://maimai.cn/web/search_center?type=contact&query=cho&highlight=true"
    response = req.get(url)
    logger.info("验证cookies是否可用")
    login_state = True
    if "登录到脉脉" in response.text:
        login_state = False
    if login_state:
        logger.info("cookies可用")
        return req
    else:
        logger.info("cookies不可用，重新获取cookies")
        get_cookies()
        req = get_req()
        return req


def json_info(html):
    """
    处理获取的html，转换为json格式
    :param html:
    :return:
    """
    print(html.text)
    c = re.search('JSON\.parse\("(.*?)"\);</script><script\ssrc=', html.text, re.S).group(1)  # 正则匹配所需要的数据
    d = c.replace('\\u0022', '"').replace("\\u002D", "-").replace("\\u0026", '&').replace("\\u005C", "\\")  # 对数据进行处理
    data = json.loads(d)
    return data


def basic_info(data):
    """
    基本信息表--表1
    :param data:
    :return:
    """
    basic_info = {}
    basic_info['name'] = data["card"]["name"]  # 名字
    basic_info['mmid'] = int(data["card"]["mmid"])  # 脉脉id
    basic_info['rank'] = data["card"]["rank"]  # 影响力
    basic_info['company'] = data["card"]["company"]  # 目前公司简称
    basic_info['stdname'] = data["company"]["stdname"]  # 目前公司全称
    basic_info['position'] = data["card"]["position"]  # 目前职位
    basic_info['headline'] = data["uinfo"]["headline"]  # 自我介绍
    if basic_info["headline"]:
        basic_info['headline'] = basic_info['headline'].encode('gbk', errors='ignore').decode('gbk')
    try:
        basic_info['ht_province'] = data["uinfo"]["ht_province"]  # 家乡-省
    except:
        logger.info("家乡-省获取信息不存在")
        basic_info['ht_province'] = ""
    try:
        basic_info['ht_city'] = data["uinfo"]["ht_city"]  # 家乡-城市
    except:
        logger.info("家乡-城市获取信息不存在")
        basic_info['ht_city'] = ""
    basic_info['email'] = data["uinfo"]["email"]
    basic_info['mobile'] = data["uinfo"]["mobile"]  # 手机号
    basic_info['dist'] = data["card"]["dist"]  # 几度关系
    # logger.info('基本信息表:', basic_info)
    return basic_info


def work_exp(id_num, req, data):
    """
    工作经历--表2
    :param req:
    :param data:
    :param start_url:
    :return:
    """
    work_exps = []
    work_expzz = data["uinfo"]["work_exp"]
    for work_expz in work_expzz:
        work_exp = {}
        work_exp["start_year"] = 0000
        work_exp["start_mon"] = 0000
        work_exp["end_year"] = 0000
        work_exp["end_mon"] = 0000
        share_url = work_expz["company_info"]["share_url"]
        #  logger.info('start_url', share_url)
        random_steep()
        try:
            print(share_url)
            start_html = req.get(share_url)  # 用于获取的是公司的全称
            print(start_html)
            dataz = json_info(start_html)
            fullname = dataz["data"]["data"]["cinfo"]["fullname"]
            work_exp["stdname"] = fullname
        except:
            logger.info("获取公司全称失败")
            work_exp["stdname"] = ""
        start_date = work_expz["start_date"]
        end_date = work_expz["end_date"]
        work_exp["company"] = work_expz["company"]
        work_exp["et_url"] = share_url
        if "-" in str(start_date):
            work_exp["start_year"] = int(start_date.split("-")[0])
            work_exp["start_mon"] = int(start_date.split("-")[1])
        if "-" in str(end_date):
            work_exp["end_year"] = int(end_date.split("-")[0])
            work_exp["end_mon"] = int(end_date.split("-")[1])
        work_exp["position"] = work_expz["position"]
        work_exp["mmid"] = id_num
        work_exp["description"] = work_expz["description"]
        if work_exp["description"]:
            work_exp["description"] = work_exp["description"].encode('gbk', errors='ignore').decode('gbk')
        # logger.info("工作经历：", work_exp)
        work_exps.append(work_exp)
    return work_exps


def education_exp(mmid, data):
    """
    教育经历--表3
    :param data:
    :return:
    """
    education_exps = []
    educations = data["uinfo"]["education"]
    for education in educations:
        education_exp = {}
        education_exp['school_name'] = education["school"]
        education_exp['department'] = education["department"]
        try:
            education_exp["start_year"] = int(education["start"])
        except:
            education_exp["start_year"] = 0000
        try:
            education_exp["start_mon"] = int(education["start_month"])
        except:
            education_exp["start_mon"] = 0000
        try:
            education_exp["end_year"] = int(education["end"])
        except:
            education_exp["end_year"] = 0000
        try:
            education_exp["end_mon"] = int(education["end_month"])
        except:
            education_exp["end_mon"] = 0000
        education_exp["mmid"] = mmid

        education_exp["education"] = education["degree"]
        # logger.info('教育经历', education_exp)
        education_exps.append(education_exp)
    return education_exps


def tag_info(mmid, data):
    # 标签信息 --表4
    tag_infos = []
    tags = data["uinfo"]["weibo_tags"]
    tag_weights = data["uinfo"]["tag_weights"]
    for tag in tags:
        tag_info = {}
        tag_info["tag"] = tag
        if tag in tag_weights.keys():
            tag_info["rec_num"] = int(tag_weights[str(tag)]["weight"])
        else:
            tag_info["rec_num"] = 1
        tag_info["mmid"] = mmid
        tag_infos.append(tag_info)
        # logger.info("标签信息:", tag_info)
    return tag_infos


def review_info(mmid, data):
    """
    点评信息 --表5
    :param mmid:
    :param data:
    :return:
    """
    data = json.loads(data)
    review_infos = []
    evaluation_list = data["data"]["evaluation_list"]
    for evaluation in evaluation_list:
        review_info = {}
        review_info['reviewer'] = evaluation["src_user"]['name']
        review_info['relationship'] = evaluation["re"]
        review_info['position'] = evaluation["src_user"]["career"]
        review_info['eva_info'] = evaluation["text"].encode('gbk', errors='ignore').decode('gbk')
        review_info['mmid'] = mmid
        # logger.info('点评信息:', review_info)
        review_infos.append(review_info)
    # logger.info('review_infos:', review_infos)
    return review_infos


def main():
    cai_num = 1
    req = cookies_expried()
    a = 'https://maimai.cn/search/contacts?count=20&page='
    b = '&query=cho&dist=0&searchTokens=["cho"]&highlight=true&jsononly=1'
    for i in range(30):  # 列表页
        start_url = a + str(i) + b
        random_steep()
        response = req.get(url=start_url)
        res_json = response.json()  # 如果为空，则无数据
        infos = res_json["data"]["contacts"]  # 信息列表
        logger.info("本页信息条数：{}".format(len(infos)))
        if len(infos) == 0:
            break
        for info in infos:  # 详情页
            logger.info("正在获取第{}条数据".format(cai_num))
            cai_num += 1
            encode_mmid = info["contact"]["encode_mmid"]
            two_url = "https://maimai.cn/contact/detail/" + encode_mmid
            review_info_url = "https://maimai.cn/contact/comment_list/" + encode_mmid + "?jsononly=1"
            random_steep()
            html = req.get(two_url)  # 详细页面的信息
            basic_data = json_info(html)
            data = basic_data["data"]
            # plogger.info(data)
            id_num = int(data["card"]["mmid"])  # mmid
            logger.info("mmid:{}".format(id_num))
            time.sleep(1)
            # 基本信息--表1
            basic_infos = basic_info(data)
            conn = hu_utils3.open_local_db("caiji_maimai")
            try:
                hu_utils3.insert_update_one(conn, basic_infos, "basic_info", False)
                # 工作经历--表2
                work_exps = work_exp(id_num, req, data)
                hu_utils3.insert_update_many(conn, work_exps, 'work_exp', False)
                # 教育经历--表3
                education_exps = education_exp(id_num, data)
                hu_utils3.insert_update_many(conn, education_exps, 'education_exp', False)
                # 标签信息--表4
                tag_infos = tag_info(id_num, data)
                hu_utils3.insert_update_many(conn, tag_infos, 'tag_info', False)
                # 点评信息 --表5
                random_steep()
                review_data = req.get(review_info_url).text  # 点评页面
                review_infos = review_info(id_num, review_data)
                hu_utils3.insert_update_many(conn, review_infos, 'review_info', False)
            finally:
                logger.info("关闭数据库")
                conn.close()


if __name__ == "__main__":
    main()
