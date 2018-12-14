#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:吉祥鸟
# datetime:2018/10/29 9:40
# software: PyCharm

from lxml import etree
import sys
import time
import hu_utils
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()
reload(sys)
sys.setdefaultencoding('utf8')

update_status = []
dt_url_twos = []
parse_start_url_num = 0
def get_etid():
    conn = hu_utils.open_local_db()
    et_names = hu_utils.select_one(conn)
    print "获取的企业数", len(et_names)
    return et_names




def start_requests(et_name):
    """
    拼接初始url，解析初始页面
    :param et_names: tuple元组类型，包含公司的etid和全名etname
    :return:一个字典，包含公司etid，etname，二级页面url
    """
    start_urls1 = []
    start_urlz = {}
    if et_name[1]:
        # print "update_status:", update_status
        start_url = "https://www.tianyancha.com/search?searchType=company&key=%s" % et_name[1]
        # start_url = "https://www.tianyancha.com/search?searchType=company&key=百度在线网络技术（北京）有限公司"
        # print "start_url:", start_url
        start_urlz["start_url"] = start_url
        start_urlz["etid"] = et_name[0]
        start_urlz["et_name"] = et_name[1]
        start_urls1.append(start_urlz)


def parse_start_url(start_urls):
    global parse_start_url_num
    parse_start_url_num += 1
    start_urls2 = []
    # print "start_urls:", start_urls
    for start_urlz in start_urls:
        start_url = start_urlz["start_url"]
        update_state = {}
        dt_url_two = {}
        html = hu_utils.get_url_html(start_url, True)
        if html:
            update_state["etid"] = start_urlz["etid"]
            update_state["et_name"] = start_urlz["et_name"]
            update_state["update_time"] = int(time.time())
            update_state["status"] = 1
            global update_status
            update_status.append(update_state)
            xp = etree.HTML(html)
            url_two = xp.xpath("//a[contains(@class,'select-none')]/@href")  # 获取二级页面url
            if url_two:  # 判断url是否存在，不存在表示查询没结果
                url_twoz = url_two[0]
                dt_url_two["etid"] = start_urlz["etid"]
                dt_url_two["etname"] = start_urlz["et_name"]
                dt_url_two["url_two"] = url_twoz
                dt_url_two["update_time"] = time.time()
                global dt_url_twos
                dt_url_twos.append(dt_url_two["url_two"])
        else:
            print "请求失败，将url放到start_urls2中"
            start_urls2.append(start_urlz)
    if len(start_urls2) > 3:
        print "一级url剩余数量：", len(start_urls2)
        if parse_start_url_num < 4:
            print "-------- 再次执行parse_start_url，第 %s 次 --------" % parse_start_url_num
            parse_start_url(start_urls2)
        else:
            print "循环请求达到最大次数，跳过"

class Parse_url_two:
    """
    解析二级页面数据
    """
    def __init__(self, dt_url_twos):
        self.urls1 = []
        self.urls = dt_url_twos
        self.url = ""
        self.xp = ""
        self.et_name = ""
        self.et_host_infos = []
        self.et_busi_infos = []
        self.et_shareholder_infos = []
        self.et_foreign_investment_infos = []
        self.et_branch_offices = []
        self.wechat_list_infos = []
        self.et_container_copyright_infos =[]
        self.et_container_icp_infos = []
        self.et_trademark_infos = []
        self.et_rongzi_infos = []

    def parse_et_host_info(self):
        """
        --企业主要信息--
        :return:
        """
        et_host_info = {}
        et_website = self.xp.xpath("//a[@class='company-link']/text()")  # 官网
        # print "".join(et_website)
        et_address = self.xp.xpath("//span[@class='address']/@title")  # 地址
        # print "".join(et_address)
        et_detail = self.xp.xpath("//script[@id='company_base_info_detail']/text()")  # 简介
        # print "".join(et_detail)
        et_legal_rp = self.xp.xpath("//div[@class='humancompany']/div[@class='name']/a/text()")  # 法定代表人
        # print "".join(et_legal_rp)
        et_states = self.xp.xpath("//div[@class='num-opening']/text()")  # 公司状态
        # print "".join(et_states)
        et_host_info["et_website"] = "".join(et_website)
        et_host_info["et_address"] = "".join(et_address)
        et_host_info["et_detail"] = "".join(et_detail)
        et_host_info["et_legal_rp"] = "".join(et_legal_rp)
        et_host_info["et_states"] = "".join(et_states)
        et_host_info["etid"] = self.etid
        et_host_info["et_name"] = self.et_name
        # print "info", et_host_info
        self.et_host_infos.append(et_host_info)

    def parse_et_busi_info(self):
        """
        --工商信息解析部分--
        """
        busi_info = {}
        reg_address = ""
        busi_regi_num = ""
        orga_code = ""
        soci_cred_code = ""
        industry = ""
        oper_period = ""
        et_type = ""
        taxp_lden_num = ""
        approval_date = ""
        taxpayer_qual = ""
        staff_site = ""
        paid_capital = ""
        regis_auth = ""
        part_num = ""
        english_name = ""
        a = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr")
        for i in range(1, len(a)):
            # tr = xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td" % i)
            if i == 8:
                for z in range(1, 2):
                    td = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z))
                    td = "".join(td)
                    if td == "注册地址":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        reg_address = "".join(zhuce)
            else:
                for z in range(1, 5, 2):
                    td = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z))
                    td = "".join(td)
                    if td == "工商注册号":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        busi_regi_num = "".join(zhuce)
                    if td == "组织机构代码":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        orga_code = "".join(zhuce)
                    if td == "统一社会信用代码":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        soci_cred_code = "".join(zhuce)
                    if td == "公司类型":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        et_type = "".join(zhuce)
                    if td == "纳税人识别号":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        taxp_lden_num = "".join(zhuce)
                    if td == "行业":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        industry = "".join(zhuce)
                    if td == "营业期限":
                        zhuce = self.xp.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/span/text()" % (i, z + 1))
                        oper_period = "".join(zhuce)
                    if td == "核准日期":
                        zhuce = self.xp.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text/text()" % (i, z + 1))
                        approval_date = "".join(zhuce)
                    if td == "纳税人资质":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        taxpayer_qual = "".join(zhuce)
                    if td == "人员规模":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        staff_site = "".join(zhuce)
                    if td == "实缴资本":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        paid_capital = "".join(zhuce)
                    if td == "登记机关":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        regis_auth = "".join(zhuce)
                    if td == "参保人数":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        part_num = "".join(zhuce)
                    if td == "英文名称":
                        zhuce = self.xp.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        english_name = "".join(zhuce)
        if busi_regi_num:
            busi_info["reg_address"] = reg_address
            busi_info["busi_regi_num"] = busi_regi_num
            busi_info["orga_code"] = orga_code
            busi_info["soci_cred_code"] = soci_cred_code
            busi_info["industry"] = industry
            busi_info["oper_period"] = oper_period
            busi_info["et_type"] = et_type
            busi_info["taxp_lden_num"] = taxp_lden_num
            busi_info["approval_date"] = approval_date
            busi_info["taxpayer_qual"] = taxpayer_qual
            busi_info["staff_site"] = staff_site
            busi_info["paid_capital"] = paid_capital
            busi_info["regis_auth"] = regis_auth
            busi_info["part_num"] = part_num
            busi_info["english_name"] = english_name
            busi_info["etid"] = self.etid
            busi_info["et_name"] = self.et_name
            self.et_busi_infos.append(busi_info)

    def parse_et_shareholder_info(self):
        """
        --股东信息解析部分--
        """
        container_holder = self.xp.xpath("//div[@id='_container_holder']/table/tbody/tr")
        con_num = len(container_holder)
        for i in range(1, con_num + 1):
            et_shareholder_info = {}
            et_shareholder_info["shareholder"] = ""
            et_shareholder_info["funded_ratio"] = ""
            et_shareholder_info["funded_num"] = ""
            et_shareholder_info["funded_time"] = ""
            tr = self.xp.xpath("//div[@id='_container_holder']/table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                if z == 2:
                    td = self.xp.xpath(
                        "//div[@id='_container_holder']/table/tbody/tr[%s]/td[%s]//div[@class='dagudong']/a/text()" % (
                        i, z))
                    shareholder = "".join(td)  # 股东
                if z == 3 or z == 4 or z == 5:
                    td = self.xp.xpath("//div[@id='_container_holder']/table/tbody/tr[%s]/td[%s]//span/text()" % (i, z))
                    td_format = "".join(td)
                    if z == 3:
                        funded_ratio = td_format  # 出资比例
                    if z == 4:
                        funded_num = td_format  # 认缴出资
                    if z == 5:
                        funded_time = td_format  # 出资时间
            et_shareholder_info["shareholder"] = shareholder
            et_shareholder_info["funded_ratio"] = funded_ratio
            et_shareholder_info["funded_num"] = funded_num
            et_shareholder_info["funded_time"] = funded_time
            if shareholder:
                et_shareholder_info["etid"] = self.etid
                et_shareholder_info["et_name"] = self.et_name
                # print "et_shareholder_info:", et_shareholder_info
                self.et_shareholder_infos.append(et_shareholder_info)

    def parse_et_foreign_investment_info(self):
        """
        --对外投资解析部分--
        """
        container_invest = self.xp.xpath("//div[@id='_container_invest']/table/tbody/tr")
        con_num = len(container_invest)
        # print(con_num)
        for i in range(1, con_num + 1):
            et_foreign_investment_info = {}
            tr = self.xp.xpath("//div[@id='_container_invest']/table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = self.xp.xpath("//div[@id='_container_invest']/table/tbody/tr[%s]/td[%s]//text()" % (i, z))
                td_format = "".join(td)
                if z == 2:
                    invested_et_name = td_format  # 被投资公司名称
                if z == 3:
                    td = self.xp.xpath("//div[@id='_container_invest']/table/tbody/tr[%s]/td[%s]/span/a/text()" % (i, z))
                    invested_legal_rp = "".join(td)  # 被投资法定代表人
                if z == 4:
                    regi_capt = td_format  # 注册资本
                if z == 5:
                    invest_ratio = td_format  # 投资占比
                if z == 6:
                    regi_time = td_format  # 注册时间
                if z == 7:
                    states = td_format  # 状态
            et_foreign_investment_info["invested_et_name"] = invested_et_name
            et_foreign_investment_info["invested_legal_rp"] = invested_legal_rp
            et_foreign_investment_info["regi_capt"] = regi_capt
            et_foreign_investment_info["invest_ratio"] = invest_ratio
            et_foreign_investment_info["regi_time"] = regi_time
            et_foreign_investment_info["states"] = states
            if invested_et_name:
                et_foreign_investment_info["etid"] = self.etid
                et_foreign_investment_info["et_name"] = self.et_name
                self.et_foreign_investment_infos.append(et_foreign_investment_info)

    def parse_et_branch_office(self):
        """
        --分支机构解析部分--
        """
        container_branch = self.xp.xpath("//div[@id='_container_branch']/table/tbody/tr")
        con_num = len(container_branch)
        for i in range(1, con_num + 1):
            et_branch_office = {}
            tr = self.xp.xpath("//div[@id='_container_branch']/table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = self.xp.xpath("//div[@id='_container_branch']/table/tbody/tr[%s]/td[%s]//text()" % (i, z))
                td_format = "".join(td)
                if z == 2:
                    fz_et_name = td_format  # 企业名称
                if z == 3:
                    td = self.xp.xpath("//div[@id='_container_invest']/table/tbody/tr[%s]/td[%s]/span/a/text()" % (i, z))
                    fz_principal = "".join(td)  # 负责人
                    # print "".join(td)
                if z == 4:
                    fz_regi_time = td_format  # 注册时间
                if z == 5:
                    fz_status = td_format  # 状态
            et_branch_office["fz_et_name"] = fz_et_name
            et_branch_office["fz_principal"] = fz_principal
            et_branch_office["fz_regi_time"] = fz_regi_time
            et_branch_office["fz_status"] = fz_status
            if fz_et_name:
                et_branch_office["et_name"] = self.et_name
                et_branch_office["etid"] = self.etid
                self.et_branch_offices.append(et_branch_office)

    def parse_wechat_list_info(self):
        """
        --微信公众号解析部分--
        """
        wechat_list = self.xp.xpath("//div[@class='wechat-list']/div[@class='wechat']")
        for i in range(1, len(wechat_list) + 1):
            wechat_list_info = {}
            wechat = self.xp.xpath("//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']/div" % i)
            for z in range(1, len(wechat) + 1):
                zz = self.xp.xpath(
                    "//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']/div[%s]//text()" % (
                    i, z))
                if z == 1:
                    wechat_name = "".join(zz)  # 微信名
                if z == 2:
                    wechat_code = "".join(self.xp.xpath(
                    "//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']/div[%s]/span[2]/text()" % (
                    i, z)))  # 微信号
                if z == 3:
                    weinfo = self.xp.xpath("//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']"
                                      "/div[%s]//script/text()" % (i, z))
                    weinfo = ''.join(weinfo)
                    weinfo = eval(weinfo)
                    wechat_info = weinfo["recommend"].decode("utf-8").encode("gbk","replace")  # 介绍
            wechat_list_info["wechat_name"] = wechat_name
            wechat_list_info["wechat_code"] = wechat_code
            wechat_list_info["wechat_info"] = wechat_info
            if wechat_code:
                wechat_list_info["etid"] = self.etid
                wechat_list_info["et_name"] = self.et_name
                self.wechat_list_infos.append(wechat_list_info)

    def parse_et_container_copyright_info(self):
        """
        --软件著作权解析部分-- _container_copyright
        """
        container_copyright = self.xp.xpath("//div[@id='_container_copyright']/table/tbody/tr")
        con_num = len(container_copyright)
        # print(con_num)
        for i in range(1, con_num + 1):
            container_copyright_info = {}
            tr = self.xp.xpath("//div[@id='_container_copyright']/table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = self.xp.xpath("//div[@id='_container_copyright']/table/tbody/tr[%s]/td[%s]//text()" % (i, z))
                td_forma = ''.join(td)
                if z == 2:
                    appro_date = td_forma  # 批准日期
                if z == 3:
                    software_name = td_forma  # 软件全称
                if z == 4:
                    software_shortname = td_forma  # 软件简称
                if z == 5:
                    rege_num = td_forma  # 登记号
                if z == 6:
                    type_num = td_forma  # 类别号
                if z == 7:
                    version_num = td_forma  # 版本号
            container_copyright_info["appro_date"] = appro_date
            container_copyright_info["software_name"] = software_name
            container_copyright_info["software_shortname"] = software_shortname
            container_copyright_info["rege_num"] = rege_num
            container_copyright_info["type_num"] = type_num
            container_copyright_info["version_num"] = version_num
            if software_name:
                container_copyright_info["etid"] = self.etid
                container_copyright_info["et_name"] = self.et_name
                self.et_container_copyright_infos.append(container_copyright_info)

    def parse_et_container_icp_info(self):
        """
        --网站备案解析部分-- _container_icp
        """
        container_icp = self.xp.xpath("//div[@id='_container_icp']/table/tbody/tr")
        con_num = len(container_icp)
        # print(con_num)
        for i in range(1, con_num + 1):
            et_container_icp_info = {}
            tr = self.xp.xpath("//div[@id='_container_icp']/table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = self.xp.xpath("//div[@id='_container_icp']/table/tbody/tr[%s]/td[%s]//text()" % (i, z))
                td_form = ''.join(td)
                if z == 2:
                    review_time = td_form  # 审核时间
                    # print "review_time:", review_time
                if z == 3:
                    website_name = td_form  # 网站名称
                if z == 4:
                    website_url = td_form  # 网站首页
                if z == 5:
                    domain_name = td_form  # 域名
                if z == 6:
                    case_num = td_form  # 备案号
                if z == 7:
                    status = td_form  # 状态
                if z == 8:
                    unit_nature = td_form  # 单位性质
            et_container_icp_info["review_time"] = review_time
            et_container_icp_info["website_name"] = website_name
            et_container_icp_info["website_url"] = website_url
            et_container_icp_info["domain_name"] = domain_name
            et_container_icp_info["case_num"] = case_num
            et_container_icp_info["status"] = status
            et_container_icp_info["unit_nature"] = unit_nature
            if website_url:
                et_container_icp_info["et_name"] = self.et_name
                et_container_icp_info["etid"] = self.etid
                self.et_container_icp_infos.append(et_container_icp_info)

    def parse_et_trademark_info(self):

        """
        --商标解析部分-- _container_icp
        """
        container_tmInfo = self.xp.xpath("//div[@id='_container_tmInfo']//table/tbody/tr")
        con_num = len(container_tmInfo)
        # print(con_num)
        for i in range(1, con_num + 1):
            et_trademark_info = {}
            tr = self.xp.xpath("//div[@id='_container_tmInfo']//table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = self.xp.xpath("//div[@id='_container_tmInfo']//table/tbody/tr[%s]/td[%s]//text()" % (i, z))
                td_form = ''.join(td)
                if z == 2:
                    apply_time = td_form  # 申请时间
                if z == 3:
                    a = self.xp.xpath("//div[@id='_container_tmInfo']//table/tbody/tr[%s]/td[%s]/div/div/img/@data-src" % (
                    i, z))  # 商标url
                    trademark_url = "".join(a)
                if z == 4:
                    trademark_name = td_form  # 商标名字
                if z == 5:
                    reg_num = td_form  # 注册号
                if z == 6:
                    apply_type = td_form  # 类别
                if z == 7:
                    process_status = td_form  # 流程状态
            et_trademark_info["apply_time"] = apply_time
            et_trademark_info["trademark_url"] = trademark_url
            et_trademark_info["trademark_name"] = trademark_name
            et_trademark_info["reg_num"] = reg_num
            et_trademark_info["apply_type"] = apply_type
            et_trademark_info["process_status"] = process_status
            if reg_num:
                et_trademark_info["etid"] = self.etid
                et_trademark_info["et_name"] = self.et_name
                self.et_trademark_infos.append(et_trademark_info)

    def parse_et_rongzi_info(self):
        """
        --融资信息解析部分-- _container_icp
        """
        container_rongzi = self.xp.xpath("//div[@id='_container_rongzi']/table/tbody/tr")
        con_num = len(container_rongzi)
        # print(con_num)
        for i in range(1, con_num + 1):
            et_rongzi_info = {}
            tr = self.xp.xpath("//div[@id='_container_rongzi']//table/tbody/tr[%s]/td" % i)
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = self.xp.xpath("//div[@id='_container_rongzi']//table/tbody/tr[%s]/td[%s]//text()" % (i, z))
                td_form = ''.join(td)
                # print td_form
                if z == 2:
                    rongzi_time = td_form  # 融资时间
                if z == 3:
                    rounds = td_form  # 轮次
                if z == 4:
                    valuation = td_form  # 估值
                if z == 5:
                    amount = td_form  # 金额
                if z == 6:
                    proportion = td_form  # 比例
                if z == 7:
                    investor = td_form  # 投资方
                if z == 8:
                    news_source = td_form  # 新闻来源
            et_rongzi_info["rongzi_time"] = rongzi_time
            et_rongzi_info["rounds"] = rounds
            et_rongzi_info["valuation"] = valuation
            et_rongzi_info["amount"] = amount
            et_rongzi_info["proportion"] = proportion
            et_rongzi_info["investor"] = investor
            et_rongzi_info["news_source"] = news_source
            if investor:
                et_rongzi_info["et_name"] = self.et_name
                et_rongzi_info["etid"] = self.etid
                self.et_rongzi_infos.append(et_rongzi_info)

    def run(self):
        self.urls1 = self.urls
        self.urls = []
        for url in self.urls1:
            self.url = url
            self.etid = self.url.split("/")[-1]
            self.html = hu_utils.get_url_html(self.url, True)
            if self.html:
                self.xp = etree.HTML(self.html)
                self.et_name = "".join(self.xp.xpath("//h1[@class='name']/text()"))
                self.parse_et_busi_info()
                self.parse_et_host_info()
                self.parse_et_shareholder_info()
                self.parse_et_foreign_investment_info()
                self.parse_et_branch_office()
                self.parse_wechat_list_info()
                self.parse_et_container_copyright_info()
                self.parse_et_container_icp_info()
                self.parse_et_trademark_info()
                self.parse_et_rongzi_info()
            else:
                print "请求失败，将url放到self.urls中"
                self.urls.append(url)

    def main(self):
        for i in range(5):
            print "二级url剩余数量：", len(self.urls)
            if len(self.urls) > 7:
                print "--------再次执行请求,第 %s 次--------" % i
                self.run()
        return self.et_host_infos, self.et_busi_infos, self.et_shareholder_infos, self.et_foreign_investment_infos, \
               self.et_branch_offices, self.wechat_list_infos, self.et_container_copyright_infos, \
               self.et_container_icp_infos, self.et_trademark_infos, self.et_rongzi_infos


def main():
    """
    主框架
    :return:
    """
    start_urls1 = []
    et_names = get_etid()
    for et_name in et_names:
        start_urlz = {}
        if et_name[1]:
            start_url = "https://www.tianyancha.com/search?searchType=company&key=%s" % et_name[1]
            start_urlz["start_url"] = start_url
            start_urlz["etid"] = et_name[0]
            start_urlz["et_name"] = et_name[1]
            start_urls1.append(start_urlz)
    parse_start_url(start_urls1)
    parse = Parse_url_two(dt_url_twos)
    et_host_infos, et_busi_infos, et_shareholder_infos, et_foreign_investment_infos, et_branch_offices, wechat_list_infos, et_container_copyright_infos, et_container_icp_infos, et_trademark_infos, et_rongzi_infos = parse.main()
    # 分别存入数据库
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_busi_infos, "et_busi_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_host_infos, "et_host_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_shareholder_infos, "et_shareholder_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_foreign_investment_infos, "et_foreign_investment_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_branch_offices, "et_branch_office")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, wechat_list_infos, "et_wechat_list_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_container_copyright_infos, "et_container_copyright_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_container_icp_infos, "et_container_icp_info")
    conn = hu_utils.open_local_db()
    hu_utils.insert_ignore_many(conn, et_trademark_infos, "et_trademark_info")
    conn = hu_utils.open_local_db()
    # print("------et_rongzi_infos:", et_rongzi_infos)
    hu_utils.insert_ignore_many(conn, et_rongzi_infos, "et_rongzi_infos")
    conn = hu_utils.open_local_db()
    hu_utils.insert_update_many(conn, update_status, "et_name_status")

if __name__=="__main__":
    main()
