#!/usr/bin/env python
# -*- coding: utf-8 -*-
from get_url_html import get_url_html
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 大街网站解析
def anal_html(url):
    """
    解析数据
    :param url: 需要解析的本网站的url
    :return: 获取的全部信息
    """
    text = []
    try:
        html = get_url_html(url)
        html = etree.HTML(html)
        two_url = html.xpath('//h3[@class = "t"]/a/@href')
        # print len(two_url)
        for i in two_url:
            # print ('er级页面：%s'% i)
            response = get_url_html(i)
            html = etree.HTML(response)
            con_txt = html.xpath('//div[contains(@class,"centerContent")]//text()')  #选取公司信息
            # print type(con_txt)
            if con_txt:
                contxt = ','.join(con_txt)
                text.append(contxt)
        text = ','.join(text)
        # print type(text)
        return text
    except:
        pass

