#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
from gevent.pool import Pool
from functools import partial
import requests
import opetating_db
import qiancheng
import dajie
import chinahr
import time
import liepin
import utils
import logging
import zhilian
from get_emails import get_email
import sys
reload(sys)
sys.setdefaultencoding('utf8')
monkey.patch_all()



et_cons = []
et_exts = []
et_statuss = []
def spider(company):
    """
    # 爬虫总框架
    :param conn:数据库
    :param cursor:游标
    :param company:公司信息（etid，公司名称）
    :return:
    """
    # print company[0]["etid"]
    if company != []:
        et_status = {}
        et_status['etid'] = company[0]["etid"]
        et_status['addtime'] = time.time()
        et_status['email_status'] = 2
        domains = ['51job', 'dajie', 'chinahr', 'liepin', 'zhilian',]
        for domain in domains:
            url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1' \
                  '&tn=93153557_hao_pg&wd=site%3A' + domain + '.com%20"' + company[0]['etname'] + '"'
            if domain == '51job':
                # print '前程无忧'
                text = qiancheng.anal_html(url)
            if domain == 'dajie':
                # print '大街'
                text = dajie.anal_html(url)
            if domain == 'chinahr':
                #print '中华英才网'
                text = chinahr.anal_html(url)
            if domain == 'zhilian':
                # print '智联招聘'
                text = zhilian.anal_html(url)
            if domain == 'liepin':
                # print '猎聘'
                text = liepin.anal_html(url)
            emails = get_email(text)
            if emails and et_status['email_status'] == 2:
                et_status['email_status'] = 3
            for email in emails:
                print '存在email:%s' % email
                email = email.lower()  # 大写转小写
                et_con = {}
                et_ext = {}
                et_con['etid'] = company[0]['etid']
                et_con['ecemail'] = email
                et_cons.append(et_con)
                et_ext['crawl_jobs_info'] = 1
                et_ext['email'] = email
                et_ext['addtime'] = time.time()
                et_exts.append(et_ext)
        et_statuss.append(et_status)

    # print '<--%s--爬取完成-->' % company[1]




def main():
    et_dingding = []
    num = 0
    etids = opetating_db.get_etid()
    et_dates = opetating_db.get_companys(etids)
    pool = Pool(15)
    pool.map(spider, et_dates)
    pool.join()
    print "et_cons:%s" % et_cons
    print "et_exts:%s" % et_exts
    lss = []
    for et_con in et_cons:  # 形成列表
        ls = tuple(et_con.values())
        lss.append(ls)
    chachongs = utils.query(lss)
    for chachong in chachongs:
        if chachong in lss:
            lss.remove(chachong)
    if lss:
        conn2 = utils.open_line_db()
        a = utils.insert_update_con(conn2, lss, 'et_contact')
    if et_exts:
        conn3 = utils.open_line_db()
        utils.insert_update_many(conn3, et_exts, 'et_email_extend')
    conn1 = utils.open_local_db()
    num = utils.insert_update_many(conn1, et_statuss, "et_info_status")

    logging.info("%s 添加钉钉数据" % utils.current_time())
    type = 2
    et_dingding.append(type)
    et_dingding.append(num)
    et_dingding.append(a)
    utils.insert_one(et_dingding)
    # text = "# 本次更新email情况统计\n\n----------\n\n- 本次总更新数：%s " \
    #        "\n\n- 更新成功数：%s" \
    #        "\n\n- 更新失败数：%s" % (num, a, num - a)
    # url = "http://47.95.214.108:6312/add/"
    # data = {
    #     'text': text,
    #     'access_token': '75c1562dfa4297dbb5e11452983db916d9685544679e99ab3ccc898f52c69285',
    # }
    # html = requests.post(url, data=data).text
    # print html


if __name__ == '__main__':
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logging.info("——————————开始更新email————————————")
    main()
    print "结束爬虫"
    logging.info("——————————结束更新email————————————")



