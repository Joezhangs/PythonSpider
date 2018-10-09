# -*- coding: utf-8 -*-
from gevent import monkey
from gevent.pool import Pool
import time
import MySQLdb
import requests
import random
from lxml import etree
import re
import mysql_spider
import sys
reload(sys)
sys.setdefaultencoding('utf8')
monkey.patch_all()

companys = dict()
jobs = dict()
z = 0
j = 0
d = 0
def storage(n):
    (cursor, conn) = link_db()
    dt_company = 'dt_company'
    dt_job2 = 'dt_jobs_2'
    start_url = 'https://www.shixiseng.com/interns?k=&t=zj&p=' + str(n)
    #print(start_url)
    url = analysis_start_html(start_url)
    for i in range(0, 10):
        global j
        j = j + 1
        print '目前共爬取数据%s条......'%j
        time.sleep(1)
        two_url = 'https://www.shixiseng.com' + url[i]
        jobs['url'] = two_url
        jobs['doid'] = re.findall(r'inn_(.*?)$', url[i])[0]
        three_url = analysis_two_html(two_url)
        doid = re.findall(r'com_(.*?)$', three_url)[0]
        companys['doid'] = doid
        companys['url'] = three_url
        analysis_three_html(three_url)
        # 将字典存到数据库中
        mysql_spider.replace_into_mysql(conn, companys, dt_company)
        mysql_spider.replace_into_mysql(conn, jobs, dt_job2)
        conn.commit()
    cursor.close()
    conn.close()

def get_url(url):
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    us = random.choice(user_agents)
    headers = {
        'User-Agent': us
    }
    try:
        html = requests.get(url, headers=headers).text
        response = etree.HTML(html)
        return response
    except:
        print '%s请求超出最大重试次数'%url
        time.sleep(1)
        print ('重新执行...')
        get_url(url)


def analysis_start_html(url):
    # 解析一级页面，获取二级页面的表
    response = get_url(url)
    href = response.xpath('//a[@class="name"]/@href')
    re_time = response.xpath('//span[@class ="release-time"]//text()')[0]
    print re_time
    # r_time = '小时前'
    # if r_time in re_time:
    #     if re_time[:-3] < 4:
    #         global z
    #         z = 1
    #     else:
    #         return href
    # else:
    return href


def analysis_two_html(url):
    # 解析二级页面，获取相关信息以及三级页面的链接

    response = get_url(url)
    company_address = response.xpath('//span[@class="com_position"]/text()')[0]
    jobs['job_name'] = response.xpath('//div[@class="new_job_name"]/text()')[0]
    jobs['job_updatetime'] = time.time()
    jobs['job_area'] = company_address
    jobs['job_degree'] = response.xpath('//span[@class="job_academic"]//text()')[0]
    job_welfare = response.xpath('//div[@class="job_good"]//text()')[0]
    jobs['job_welfare'] = job_welfare.split('：')[1]
    job_part = response.xpath('//div[@class="job_part"]//span//text()')
    a = '岗位职责'
    b = '任职资格'
    if a in job_part:
        jobs["job_detailed"] = job_part[0]
    else:
        jobs["job_detailed"] = ""
    if b in job_part:
        jobs['job_demand'] = job_part[1]
    else:
        jobs["job_demand"] = ""
    jobs['addtime'] = time.time()
    three_url = response.xpath('//div[@class="com-name"]/@data-sinfo')[0]
    three_url = re.findall(r'com_uuid\"\:\s\"(.*?)\"', three_url)
    three_url = 'https://www.shixiseng.com/com/' + three_url[0]
    companys["company_address"] = company_address
    return three_url


def analysis_three_html(url):
    # 解析三级页面，获取相关信息,将信息存成字典
    try:
        response = get_url(url)
        company_name = response.xpath('//div[@class="com_name"]/text()')[0]
        company_workers = response.xpath('//span[@class="com_num"]//text()')[0]  # 员工人数
        company_area = response.xpath('//span[@class="com_position"]//text()')[0]  # 所在地
        company_detail = response.xpath('//div[@class="content_left"]//div[@class="com_detail"]//text()')[0] # 公司描述
        companys['company_workers'] = company_workers
        companys['company_area'] = company_area
        company = response.xpath('//div[@class="content_right"]//div[@class="com_detail"]//text()')
        kind = '公司类型'
        uptime = '成立日期'
        capital = '注册资本'
        if kind in company:
                companys['company_kind'] = company[1].split('：')[1]  # 公司性质
        if uptime in company:
                companys['company_uptime'] = company[3].split('：')[1]  # 公司成立时间
        if capital in company:
                companys['company_capital'] = company[4].split('：')[1]  # 注册资金
        company_industry = response.xpath('//span[@class="com_class"]/text()')  # 所属行业
        if company_industry:
            companys['company_industry'] = company_industry[0]
        else:
            companys['company_industry'] = ""
        companys['site'] = 'shixiseng'
        jobs['site'] = 'shixiseng'
        companys['company_name'] = company_name
        jobs['company_name'] = company_name
        companys['company_detail'] = company_detail
    except:
        print '%s信息获取异常' % url



def link_db():
    # 连接数据库
    conn = MySQLdb.connect(host='192.168.1.4', user='root', passwd='666', db='wll_caiji', port=3306, charset='gbk')
    cursor = conn.cursor()
    return cursor, conn


def run(fn):
    # fn: 函数参数是数据列表的一个元素
    global d
    while d < 500:
        try:
            d += 1
            print d
            storage(d)
        except:
            print '存储异常'
    time.sleep(1)

if __name__ == "__main__":
    start_time = time.time()
    pool = Pool(15)
    pool.map(run, range(15))
    pool.join()
    eng_time = time.time()
    print (eng_time-start_time)
