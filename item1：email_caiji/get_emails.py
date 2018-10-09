#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_email(text):
    """
    正则匹配email
    :param text: 需要匹配的字符串
    :return: email
    """
    text = str(text)
    # print type(text)
    pattern = r'[\.\w-]+@[\w-]+(?:\.[\w-]+)+'
    emails = re.findall(pattern, text)
    # print emails
    # 用于筛选email,去重
    emails = list(set(emails))
    return emails
