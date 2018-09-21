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
    :return: 获取的全部信息
    """
    text = []
    try:
        html = get_url_html(url)
        html = etree.HTML(html)
        two_url = html.xpath('//h3[@class = "t"]/a/@href')
        # print len(two_url)
        for i in two_url:
            response = get_url_html(i)
            html = etree.HTML(response)
            con_txt = html.xpath('//div[@class="con_txt"]/text()')  #选取公司信息
            if con_txt:
                # print 'xinxi:%s'%con_txt
                contxt = ','.join(con_txt)
                text.append(contxt)
            three_urls = html.xpath('//a[@class=" zw-name"]//@href')
            for three_url in three_urls:
                # print '三级%s' % three_urls
                response = get_url_html(three_url)
                # print (three_url)
                html = etree.HTML(response)
                job_msg = html.xpath('//div[contains(@class,"job_msg")]//text()')  # 选取岗位信息
                jobmsg = ','.join(job_msg)
                text.append(jobmsg)
        text = ','.join(text)
        return text
    except:
        pass
