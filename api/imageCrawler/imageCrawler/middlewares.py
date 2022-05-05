# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from logging import getLogger
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from api.imageCrawler.imageCrawler.settings import USER_AGENT, MY_USER_AGENT, IPOOLS
# import random
from random import choice
from scrapy.http import HtmlResponse
import time
# from fake_useragent import UserAgent  # 方式二随机选择一个user-agent
# import base64
# from urllib.parse import unquote, urlunparse
# from urllib.request import getproxies, proxy_bypass, _parse_proxy
#
# from scrapy.exceptions import NotConfigured
# from scrapy.utils.httpobj import urlparse_cached
# from scrapy.utils.python import to_bytes



class ImagecrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        # print(USER_AGENT) #配置文件原来的User_AGENT
        print(MY_USER_AGENT)  # 自定义的MY_USER_AGENT
        agent = choice(self.user_agent)  # 随机从MY_USER_AGENT中选择一个，choice选择一个,choices选择多个
        request.headers['User-Agent'] = agent
        # request.headers.setdefault(b'User-Agent',USER_AGENT().random)#方式二

class MyHttpProxyMiddleware(object):

    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        # request.meta["proxy"] ="http://ip:port"
        # request.meta["proxy"] ="http://uer:password@ip:port"
        pass
        # thisip = random.choice(IPOOLS)
        # print("this is ip:" + thisip["ipaddr"])
        # request.meta["proxy"] = "http://" + thisip["ipaddr"]

# class SeleniumSplashDownloadMiddleware(object):
#     def process_request(self, request, spider):
#         url = request.url
#         # self.chrome.get(url)
#         # html = self.chrome.page_source
#         # print(html)
#         spider.chrome.get(url)
#         load_index=0
#         if load_index%35==0:
#             js = 'document.documentElement.scrollTop=100000'
#             spider.chrome.execute_script(js)
#             time.sleep(10)  # 程序加载页面到执行js 不到1s
#         time.sleep(10)
#         load_index+=1
#         html=spider.chrome.page_source
#         return HtmlResponse(url, body=html, request=request, encoding="utf-8")  # request告诉是哪个响应回来的
