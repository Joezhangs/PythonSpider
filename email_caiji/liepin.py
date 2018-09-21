#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opetating_db import get_companys
from get_emails import get_email
from get_url_html import get_url_html
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 猎聘网站解析
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
            con_txt = html.xpath('//div[@class="detail"]//text()')  #选取公司信息
            if con_txt:
                contxt = ','.join(con_txt)
                text.append(contxt)
                zhiwei_url = html.xpath('//a[@class="jobinfo"]/@href')[0]
                # print zhiwei_url
                response = get_url_html(zhiwei_url)
                zhiwei_html = etree.HTML(response)
                no_zhiwei = zhiwei_html.xpath('//p[@class="no-result-tips"]')
                if not no_zhiwei:
                    three_urls = zhiwei_html.xpath('//div[@class="joblist"]//div[@class="job-info"]/a/@href')
                    # print three_urls
                    for three_url in three_urls:
                        response = get_url_html(three_url)
                        # print ('三级页面：%s' % three_url)
                        html = etree.HTML(response)
                        job_msg = html.xpath('//div[contains(@class,"content-word")]//text()')  # 选取岗位信息
                        jobmsg = ','.join(job_msg)
                        text.append(jobmsg)
        # print text
        text = ','.join(text)
        return text
    except:
        pass
