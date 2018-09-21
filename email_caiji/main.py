#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
from gevent.pool import Pool
from functools import partial
import opetating_db
import qiancheng
import dajie
import chinahr
import liepin
import zhilian
from get_emails import get_email
import sys
reload(sys)
sys.setdefaultencoding('utf8')
monkey.patch_all()


def spider(conn, cursor, company):
    """
    # 爬虫总框架
    :param conn:数据库
    :param cursor:游标
    :param company:公司信息（etid，公司名称）
    :return:
    """
    domains = ['51job', 'dajie', 'chinahr', 'liepin', 'zhilian',]
    # print('公司:%s' % company[1])
    for domain in domains:
        url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1' \
              '&tn=93153557_hao_pg&wd=site%3A' + domain + '.com%20"' + company[1] + '"'
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
        for email in emails:
            # print text
            comp_email = {}
            # print('公司:%s' % company[1])
            print email
            comp_email['etid'] = company[0]
            comp_email['email'] = email.lower()
            print comp_email
            opetating_db.replace_db(conn, comp_email, 'et_ema')
            opetating_db.down_db(conn, cursor)
    print '<--%s--爬取完成-->' % company[1]




def main():
    conn, cursor = opetating_db.open_db()  # 开启数据库
    companys = opetating_db.get_companys(cursor)  # 获取公司信息
    partial_work = partial(spider, conn, cursor)  # 作为partial函数的输入变量
    pool = Pool(15)
    pool.map(partial_work, companys)
    pool.join()
    print '全部爬取完成'




if __name__ == '__main__':
    main()