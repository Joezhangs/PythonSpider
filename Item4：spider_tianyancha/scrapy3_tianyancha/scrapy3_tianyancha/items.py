# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy import Field


class EtNameStatus(Item):
    table_name = "et_name_status"
    etid = scrapy.Field()
    status = scrapy.Field()
    update_time = scrapy.Field()
    et_name = Field()


class EtHostInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = "et_host_info"
    et_website = scrapy.Field()
    et_address = scrapy.Field()
    et_detail = scrapy.Field()
    et_legal_rp = scrapy.Field()
    et_states = scrapy.Field()
    etid = scrapy.Field()
    et_name = scrapy.Field()


class ParseEtBusiInfo(scrapy.Item):
    table_name = "et_busi_info"
    reg_address = scrapy.Field()
    busi_regi_num = scrapy.Field()
    orga_code = scrapy.Field()
    soci_cred_code = scrapy.Field()
    industry = scrapy.Field()
    oper_period = scrapy.Field()
    et_type = scrapy.Field()
    taxp_lden_num = scrapy.Field()
    approval_date = scrapy.Field()
    taxpayer_qual = scrapy.Field()
    staff_site = scrapy.Field()
    paid_capital = scrapy.Field()
    regis_auth = scrapy.Field()
    part_num = scrapy.Field()
    english_name = scrapy.Field()
    etid = scrapy.Field()
    et_name = scrapy.Field()


class ParseEtShareholderInfo(scrapy.Item):
    table_name = "et_shareholder_info"

    shareholder = Field()
    funded_ratio = Field()
    funded_num = Field()
    funded_time = Field()
    etid = Field()
    et_name = Field()


class ParseEtForeignInvestmentInfo(scrapy.Item):
    table_name = "et_foreign_investment_info"

    invested_et_name = Field()
    invested_legal_rp = Field()
    regi_capt = Field()
    invest_ratio = Field()
    regi_time = Field()
    states = Field()
    etid = Field()
    et_name = Field()


class ParseEtBranchOfficeInfo(scrapy.Item):
    table_name = "et_branch_office"

    fz_et_name = Field()
    fz_principal = Field()
    fz_regi_time = Field()
    fz_status = Field()
    et_name = Field()
    etid = Field()


class ParseWechatListInfo(scrapy.Item):
    table_name = "et_wechat_list_info"

    wechat_name = Field()
    wechat_code = Field()
    wechat_info = Field()
    etid = Field()
    et_name = Field()


class ParseEtContaInerCopyrightInfo(scrapy.Item):
    table_name = "et_container_copyright_info"

    appro_date = Field()
    software_name = Field()
    software_shortname = Field()
    rege_num = Field()
    type_num = Field()
    version_num = Field()
    etid = Field()
    et_name = Field()


class ParseEtContaInerIcpInfo(scrapy.Item):
    table_name = "et_container_icp_info"

    review_time = Field()
    website_name = Field()
    website_url = Field()
    domain_name = Field()
    case_num = Field()
    status = Field()
    unit_nature = Field()
    et_name = Field()
    etid = Field()


class ParseEtTrademarkInfo(scrapy.Item):
    table_name = "et_trademark_info"

    apply_time = Field()
    trademark_url = Field()
    trademark_name = Field()
    reg_num = Field()
    apply_type = Field()
    process_status = Field()
    etid = Field()
    et_name = Field()


class ParseEtRongziInfo(scrapy.Item):
    table_name = "et_rongzi_infos"

    rongzi_time = Field()
    rounds = Field()
    valuation = Field()
    amount = Field()
    proportion = Field()
    investor = Field()
    news_source = Field()
    et_name = Field()
    etid = Field()
