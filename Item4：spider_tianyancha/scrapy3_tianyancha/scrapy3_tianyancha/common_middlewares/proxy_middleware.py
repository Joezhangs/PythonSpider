# coding=utf-8
"""
为爬虫设置代理
"""
import abc


class ProxyMiddleware(abc.ABC):
    def process_request(self, request, spider):
        """
        处理请求数据，
        为请求添加静态代理
        :param request: 请求数据
        :param spider: 爬虫对象
        :return:
        """
        print("添加代理")
        request.meta['proxy'] = 'http://****'

    @abc.abstractmethod
    def process_response(self, request, response, spider):
        """
        处理响应数据，
        对错误的响应进行重试
        :param request: 请求数据
        :param response: 响应数据
        :param spider: 爬虫对象
        :return:
        """
        pass
