#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
import opetating_db
import time
import qiancheng
import dajie
import chinahr
import shixiseng
import zhilian
import re

i = 0
def get_website(et_date):
    # 处理信息
    global i
    i += 1
    print utils.current_time(), "正在更新第%s条数据" % i
    r = "(https\:\/\/www(?:\.+[\w-]+)+)|(http\:www(?:\.+[\w-]+)+)|" \
        "(http\:\/\/[\w-]+(?:\.+[\w-]+)+)|" \
        "(www(?:\.+[\w-]+)+)"
    res = et_date['etwebsite']
    # print res
    # print type(res)
    website = re.search(r, res)
    if website:
        website = website.group()
    else:
        # 站内搜索
        domains = ['51job', 'dajie', 'chinahr', 'liepin', 'zhilian']
        # print('公司:%s' % company[1])
        for domain in domains:
            url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1' \
                  '&tn=93153557_hao_pg&wd=site%3A' + domain + '.com%20"' + et_date['etname'] + '"'
            if domain == '51job':
                # print '前程无忧'
                website = qiancheng.anal_html(url)
                if website:
                    break
            if domain == 'dajie':
                # print '大街'
                website = dajie.anal_html(url)
                if website:
                    break
            if domain == 'chinahr':
                # print '中华英才网'
                website = chinahr.anal_html(url)
                if website:
                    break
            if domain == 'zhilian':
                # print '智联招聘'
                website = zhilian.anal_html(url)
                if website:
                    break
            if domain == 'shixiseng':
                # print '实习僧'
                website = shixiseng.anal_html(url)
                if website:
                    break
            # print website
    if website:
        doms = ['51job.com', 'dajie.com', 'chinahr.com', 'liepin.com', 'zhilian.com', 'lagou.com','liepin.com']
        for dom in doms:
            if dom in website:
                website = ""
                break
        et_date["etwebsite"] = website
    else:
        et_date["etwebsite"] = ""
    # print website
    return et_date

