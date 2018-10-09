#!/usr/bin/env python
# # -*- coding: utf-8 -*-

from get_url_html import get_url_html
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 前程无忧网站解析
def anal_html(url):
    """
    解析数据
    :param url: 需要解析的本网站的url
    :return: 获取的官网url
    """

    try:
        html = get_url_html(url)
        html = etree.HTML(html)
        two_url = html.xpath('//h3[@class = "t"]/a/@href')
        # print len(two_url)
        for i in two_url:
            # print i
            response = get_url_html(i)
            html = etree.HTML(response)
            website = html.xpath('//p[contains(@class,"tmsg")]/a/text()')  # 选取公司官网url
            if website:
                # print website
                return website[0]
                break
    except:
        pass


