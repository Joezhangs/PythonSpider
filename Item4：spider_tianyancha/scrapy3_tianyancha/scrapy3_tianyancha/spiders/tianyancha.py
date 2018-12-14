# -*- coding: utf-8 -*-
import scrapy
import sys
import time

sys.path.append(".")
import logging
from scrapy import Request
from ..items import EtHostInfo, ParseEtBusiInfo, EtNameStatus, ParseEtShareholderInfo, ParseEtForeignInvestmentInfo, \
    ParseEtBranchOfficeInfo, ParseWechatListInfo, ParseEtContaInerCopyrightInfo, ParseEtContaInerIcpInfo, \
    ParseEtTrademarkInfo, ParseEtRongziInfo

logger = logging.getLogger(__name__)
from . import hu_utils

"""
使用yield是可以的，猜测是刚开始默认使用start_requests函数，之后的函数调用
scrapy中有一些默认使用的函数

"""


class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'

    def start_requests(self):
        """
        拼接初始url，解析初始页面
        :param et_names: tuple元组类型，包含公司的etid和全名etname
        :return:一个字典，包含公司etid，etname，二级页面url
        """
        conn = hu_utils.open_local_db()
        et_names = hu_utils.select_one(conn)
        logger.info("获取的企业数{}".format(len(et_names)))
        a = 0
        for et_name in et_names:
            a += 1
            logger.info("正在获取第{}条数据......".format(a))
            print("正在获取第{}条数据......".format(a))
            if et_name[1]:
                start_url = "https://www.tianyancha.com/search?searchType=company&key=%s" % et_name[1]
                request = Request(url=start_url, callback=self.parse_start_url,
                                  meta={"etid": et_name[0], "et_name": et_name[1]})
                yield request

    def parse_start_url(self, response):
        try:
            if "没有找到相关结果" not in response.text:
                url_two = response.xpath("//div[@class='header']/a/@href").extract_first()  # 获取二级页面url
                # logger.info("url_two{}".format(url_two))
            else:
                logger.info("没有搜索到结果")
                et_state = EtNameStatus()
                et_state["et_name"] = response.meta["et_name"]
                et_state['etid'] = response.meta["etid"]
                et_state["status"] = 1
                et_state["update_time"] = int(time.time())
                yield et_state
                return
            if url_two:  # 判断url是否存在，不存在表示查询没结果
                logger.info("存在二级url，正在获取数据......")
                yield Request(url=url_two, callback=self.parse,
                              meta={"etid": response.meta["etid"], "et_name": response.meta["et_name"]})
        except:
            logger.debug("出错")
            yield Request(url=response.url, callback=self.parse_start_url)

    def parse(self, response):
        et_state, item = self.parse_et_host_info(response)
        yield et_state
        yield item
        # logger.info("执行parse_et_busi_info---------")
        yield self.parse_et_busi_info(response)
        # logger.info("执行parse_et_shareholder_info---------")
        yield self.parse_et_shareholder_info(response)
        # logger.info("执行parse_et_foreign_investment_info---------")
        yield self.parse_et_foreign_investment_info(response)
        # logger.info("执行parse_et_branch_office_info---------")
        yield self.parse_et_branch_office_info(response)
        # logger.info("执行parse_wechat_list_info---------")
        yield self.parse_wechat_list_info(response)
        # logger.info("执行parse_et_container_copyright_info---------")
        yield self.parse_et_container_copyright_info(response)
        # logger.info("执行parse_et_container_icp_info---------")
        yield self.parse_et_container_icp_info(response)
        # logger.info("执行parse_et_trademark_info---------")
        yield self.parse_et_trademark_info(response)
        # logger.info("执行parse_et_rongzi_info---------")
        yield self.parse_et_rongzi_info(response)

    def parse_et_host_info(self, response):
        """
        --企业主要信息--
        :return:
        """
        item = EtHostInfo()
        et_state = EtNameStatus()
        et_website = response.xpath("//a[@class='company-link']/text()").extract()  # 官网
        et_address = response.xpath("//span[@class='address']/@title").extract()  # 地址
        et_detail = response.xpath("//script[@id='company_base_info_detail']/text()").extract()  # 简介
        et_legal_rp = response.xpath("//div[@class='humancompany']/div[@class='name']/a/text()").extract()  # 法定代表人
        et_states = response.xpath("//div[@class='num-opening']/text()").extract()  # 公司状态
        item["et_website"] = "".join(et_website)
        item["et_address"] = "".join(et_address)
        item["et_detail"] = "".join(et_detail)
        item["et_legal_rp"] = "".join(et_legal_rp)
        item["et_states"] = "".join(et_states)
        item["etid"] = response.meta["etid"]
        item["et_name"] = response.meta["et_name"]
        et_state["et_name"] = response.meta["et_name"]
        et_state['etid'] = response.meta["etid"]
        et_state["status"] = 1
        et_state["update_time"] = int(time.time())
        return et_state, item

    def parse_et_busi_info(self, response):
        """
        --工商信息解析部分--
        """
        busi_info = ParseEtBusiInfo()
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
        a = response.xpath("//table[contains(@class,'-striped-col')]/tbody/tr")
        for i in range(1, len(a)):
            if i == 8:
                for z in range(1, 2):
                    td = response.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z))
                    td = "".join(td.extract())
                    if td == "注册地址":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        reg_address = "".join(zhuce.extract())
            else:
                for z in range(1, 5, 2):
                    td = response.xpath("//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z))
                    td = "".join(td.extract())
                    if td == "工商注册号":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        busi_regi_num = "".join(zhuce.extract())
                    if td == "组织机构代码":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        orga_code = "".join(zhuce.extract())
                    if td == "统一社会信用代码":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        soci_cred_code = "".join(zhuce.extract())
                    if td == "公司类型":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        et_type = "".join(zhuce.extract())
                    if td == "纳税人识别号":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        taxp_lden_num = "".join(zhuce.extract())
                    if td == "行业":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        industry = "".join(zhuce.extract())
                    if td == "营业期限":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/span/text()" % (i, z + 1))
                        oper_period = "".join(zhuce.extract())
                    if td == "核准日期":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text/text()" % (i, z + 1))
                        approval_date = "".join(zhuce.extract())
                    if td == "纳税人资质":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        taxpayer_qual = "".join(zhuce.extract())
                    if td == "人员规模":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        staff_site = "".join(zhuce.extract())
                    if td == "实缴资本":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        paid_capital = "".join(zhuce.extract())
                    if td == "登记机关":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        regis_auth = "".join(zhuce.extract())
                    if td == "参保人数":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        part_num = "".join(zhuce.extract())
                    if td == "英文名称":
                        zhuce = response.xpath(
                            "//table[contains(@class,'-striped-col')]/tbody/tr[%s]/td[%s]/text()" % (i, z + 1))
                        english_name = "".join(zhuce.extract())
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
            busi_info["etid"] = response.meta["etid"]
            busi_info["et_name"] = response.meta["et_name"]
            return busi_info
        else:
            logger.info("信息不存在，不进行存储")

    def parse_et_shareholder_info(self, response):
        """
        --股东信息解析部分--
        """
        container_holder = response.xpath("//div[@id='_container_holder']/table/tbody/tr").extract()
        con_num = len(container_holder)
        for i in range(1, con_num + 1):
            et_shareholder_info = ParseEtShareholderInfo()
            et_shareholder_info["shareholder"] = ""
            et_shareholder_info["funded_ratio"] = ""
            et_shareholder_info["funded_num"] = ""
            et_shareholder_info["funded_time"] = ""
            tr = response.xpath("//div[@id='_container_holder']/table/tbody/tr[%s]/td" % i).extract()
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                if z == 2:
                    td = response.xpath(
                        "//div[@id='_container_holder']/table/tbody/tr[%s]/td[%s]//div[@class='dagudong']/a/text()" % (
                            i, z)).extract()
                    shareholder = "".join(td)  # 股东
                if z == 3 or z == 4 or z == 5:
                    td = response.xpath(
                        "//div[@id='_container_holder']/table/tbody/tr[%s]/td[%s]//span/text()" % (i, z)).extract()
                    td_format = "".join(td)
                    if z == 3:
                        funded_ratio = td_format  # 出资比例
                    if z == 4:
                        funded_num = td_format  # 认缴出资
                    if z == 5:
                        funded_time = td_format  # 出资时间
            if shareholder != "":
                et_shareholder_info["shareholder"] = shareholder
                et_shareholder_info["funded_ratio"] = funded_ratio
                et_shareholder_info["funded_num"] = funded_num
                et_shareholder_info["funded_time"] = funded_time
                et_shareholder_info["etid"] = response.meta["etid"]
                et_shareholder_info["et_name"] = response.meta["et_name"]
                return et_shareholder_info
            else:
                logger.info("信息不存在，不进行存储")

    def parse_et_foreign_investment_info(self, response):
        """
        --对外投资解析部分--
        """
        container_invest = response.xpath("//div[@id='_container_invest']/table/tbody/tr").extract()
        con_num = len(container_invest)
        for i in range(1, con_num + 1):
            et_foreign_investment_info = ParseEtForeignInvestmentInfo()
            tr = response.xpath("//div[@id='_container_invest']/table/tbody/tr[%s]/td" % i).extract()
            for z in range(2, len(tr) + 1):
                td = response.xpath(
                    "//div[@id='_container_invest']/table/tbody/tr[%s]/td[%s]//text()" % (i, z)).extract()
                td_format = "".join(td)
                if z == 2:
                    invested_et_name = td_format  # 被投资公司名称
                if z == 3:
                    td = response.xpath(
                        "//div[@id='_container_invest']/table/tbody/tr[%s]/td[%s]/span/a/text()" % (i, z)).extract()
                    invested_legal_rp = "".join(td)  # 被投资法定代表人
                if z == 4:
                    regi_capt = td_format  # 注册资本
                if z == 5:
                    invest_ratio = td_format  # 投资占比
                if z == 6:
                    regi_time = td_format  # 注册时间
                if z == 7:
                    states = td_format  # 状态
            if invested_et_name:
                et_foreign_investment_info["invested_et_name"] = invested_et_name
                et_foreign_investment_info["invested_legal_rp"] = invested_legal_rp
                et_foreign_investment_info["regi_capt"] = regi_capt
                et_foreign_investment_info["invest_ratio"] = invest_ratio
                et_foreign_investment_info["regi_time"] = regi_time
                et_foreign_investment_info["states"] = states
                et_foreign_investment_info["etid"] = response.meta["etid"]
                et_foreign_investment_info["et_name"] = response.meta["et_name"]
                return et_foreign_investment_info
            else:
                logger.info("信息不存在，不进行存储")

    def parse_et_branch_office_info(self, response):
        """
        --分支机构解析部分--
        """
        container_branch = response.xpath("//div[@id='_container_branch']/table/tbody/tr").extract()
        con_num = len(container_branch)
        for i in range(1, con_num + 1):
            et_branch_office = ParseEtBranchOfficeInfo()
            tr = response.xpath("//div[@id='_container_branch']/table/tbody/tr[%s]/td" % i).extract()
            for z in range(2, len(tr) + 1):
                td = response.xpath(
                    "//div[@id='_container_branch']/table/tbody/tr[%s]/td[%s]//text()" % (i, z)).extract()
                td_format = "".join(td)
                if z == 2:
                    fz_et_name = td_format  # 企业名称
                if z == 3:
                    td = response.xpath(
                        "//div[@id='_container_invest']/table/tbody/tr[%s]/td[%s]/span/a/text()" % (i, z)).extract()
                    fz_principal = "".join(td)  # 负责人
                if z == 4:
                    fz_regi_time = td_format  # 注册时间
                if z == 5:
                    fz_status = td_format  # 状态
            if fz_et_name:
                et_branch_office["fz_et_name"] = fz_et_name
                et_branch_office["fz_principal"] = fz_principal
                et_branch_office["fz_regi_time"] = fz_regi_time
                et_branch_office["fz_status"] = fz_status
                et_branch_office["et_name"] = response.meta["et_name"]
                et_branch_office["etid"] = response.meta["etid"]
                return et_branch_office
            else:
                logger.info("信息不存在，不进行存储")

    def parse_wechat_list_info(self, response):
        """
        --微信公众号解析部分--
        """
        wechat_list = response.xpath("//div[@class='wechat-list']/div[@class='wechat']").extract()
        for i in range(1, len(wechat_list) + 1):
            wechat_list_info = ParseWechatListInfo()
            wechat = response.xpath(
                "//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']/div" % i).extract()
            for z in range(1, len(wechat) + 1):
                zz = response.xpath(
                    "//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']/div[%s]//text()" % (
                        i, z)).extract()
                if z == 1:
                    wechat_name = "".join(zz)  # 微信名
                if z == 2:
                    wechat_code = response.xpath(
                        "//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']/div[%s]/span[2]/text()" % (
                            i, z)).extract_first()  # 微信号
                if z == 3:
                    weinfo = response.xpath("//div[@class='wechat-list']/div[@class='wechat'][%s]/div[@class='content']"
                                            "/div[%s]//script/text()" % (i, z)).extract()
                    weinfo = ''.join(weinfo)
                    weinfo = eval(weinfo)
                    wechat_info = weinfo["recommend"]  # 介绍
            if wechat_code:
                wechat_list_info["wechat_name"] = wechat_name
                wechat_list_info["wechat_code"] = wechat_code
                wechat_list_info["wechat_info"] = wechat_info
                wechat_list_info["etid"] = response.meta["etid"]
                wechat_list_info["et_name"] = response.meta["et_name"]
                return wechat_list_info
            else:
                logger.info("信息不存在，不进行存储")

    def parse_et_container_copyright_info(self, response):
        """
        --软件著作权解析部分-- _container_copyright
        """
        container_copyright = response.xpath("//div[@id='_container_copyright']/table/tbody/tr").extract()
        con_num = len(container_copyright)
        # print(con_num)
        for i in range(1, con_num + 1):
            container_copyright_info = ParseEtContaInerCopyrightInfo()
            tr = response.xpath("//div[@id='_container_copyright']/table/tbody/tr[%s]/td" % i).extract()
            for z in range(2, len(tr) + 1):
                td = response.xpath(
                    "//div[@id='_container_copyright']/table/tbody/tr[%s]/td[%s]//text()" % (i, z)).extract()
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
            if software_name:
                container_copyright_info["appro_date"] = appro_date
                container_copyright_info["software_name"] = software_name
                container_copyright_info["software_shortname"] = software_shortname
                container_copyright_info["rege_num"] = rege_num
                container_copyright_info["type_num"] = type_num
                container_copyright_info["version_num"] = version_num
                container_copyright_info["etid"] = response.meta["etid"]
                container_copyright_info["et_name"] = response.meta["et_name"]
                return container_copyright_info
            else:
                logger.info("信息不存在，不进行存储")

    def parse_et_container_icp_info(self, response):
        """
        --网站备案解析部分-- _container_icp
        """
        container_icp = response.xpath("//div[@id='_container_icp']/table/tbody/tr").extract()
        con_num = len(container_icp)
        # print(con_num)
        for i in range(1, con_num + 1):
            et_container_icp_info = ParseEtContaInerIcpInfo()
            tr = response.xpath("//div[@id='_container_icp']/table/tbody/tr[%s]/td" % i).extract()
            for z in range(2, len(tr) + 1):
                td = response.xpath("//div[@id='_container_icp']/table/tbody/tr[%s]/td[%s]//text()" % (i, z)).extract()
                td_form = ''.join(td)
                if z == 2:
                    review_time = td_form  # 审核时间
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
            if website_url:
                et_container_icp_info["review_time"] = review_time
                et_container_icp_info["website_name"] = website_name
                et_container_icp_info["website_url"] = website_url
                et_container_icp_info["domain_name"] = domain_name
                et_container_icp_info["case_num"] = case_num
                et_container_icp_info["status"] = status
                et_container_icp_info["unit_nature"] = unit_nature
                et_container_icp_info["et_name"] = response.meta["et_name"]
                et_container_icp_info["etid"] = response.meta["etid"]
                return et_container_icp_info
            else:
                logger.info("信息不存在，不进行存储")

    def parse_et_trademark_info(self, response):

        """
        --商标解析部分-- _container_icp
        """
        container_tmInfo = response.xpath("//div[@id='_container_tmInfo']//table/tbody/tr").extract()
        con_num = len(container_tmInfo)
        for i in range(1, con_num + 1):
            et_trademark_info = ParseEtTrademarkInfo()
            tr = response.xpath("//div[@id='_container_tmInfo']//table/tbody/tr[%s]/td" % i).extract()
            for z in range(2, len(tr) + 1):
                td = response.xpath(
                    "//div[@id='_container_tmInfo']//table/tbody/tr[%s]/td[%s]//text()" % (i, z)).extract()
                td_form = ''.join(td)
                if z == 2:
                    apply_time = td_form  # 申请时间
                if z == 3:
                    a = response.xpath(
                        "//div[@id='_container_tmInfo']//table/tbody/tr[%s]/td[%s]/div/div/img/@data-src" % (
                            i, z)).extract()  # 商标url
                    trademark_url = "".join(a)
                if z == 4:
                    trademark_name = td_form  # 商标名字
                if z == 5:
                    reg_num = td_form  # 注册号
                if z == 6:
                    apply_type = td_form  # 类别
                if z == 7:
                    process_status = td_form  # 流程状态
            if reg_num:
                et_trademark_info["apply_time"] = apply_time
                et_trademark_info["trademark_url"] = trademark_url
                et_trademark_info["trademark_name"] = trademark_name
                et_trademark_info["reg_num"] = reg_num
                et_trademark_info["apply_type"] = apply_type
                et_trademark_info["process_status"] = process_status
                et_trademark_info["etid"] = response.meta["etid"]
                et_trademark_info["et_name"] = response.meta["et_name"]
                return et_trademark_info
            else:
                logger.info("信息不存在，不进行存储")

    def parse_et_rongzi_info(self, response):
        """
        --融资信息解析部分-- _container_icp
        """
        container_rongzi = response.xpath("//div[@id='_container_rongzi']/table/tbody/tr").extract()
        con_num = len(container_rongzi)
        # print(con_num)
        for i in range(1, con_num + 1):
            et_rongzi_info = ParseEtRongziInfo()
            tr = response.xpath("//div[@id='_container_rongzi']//table/tbody/tr[%s]/td" % i).extract()
            # print "fd", len(tr)
            for z in range(2, len(tr) + 1):
                td = response.xpath(
                    "//div[@id='_container_rongzi']//table/tbody/tr[%s]/td[%s]//text()" % (i, z)).extract()
                td_form = ''.join(td)
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
            if investor:
                et_rongzi_info["rongzi_time"] = rongzi_time
                et_rongzi_info["rounds"] = rounds
                et_rongzi_info["valuation"] = valuation
                et_rongzi_info["amount"] = amount
                et_rongzi_info["proportion"] = proportion
                et_rongzi_info["investor"] = investor
                et_rongzi_info["news_source"] = news_source
                et_rongzi_info["et_name"] = response.meta["et_name"]
                et_rongzi_info["etid"] = response.meta["etid"]
                return et_rongzi_info
            else:
                logger.info("信息不存在，不进行存储")
