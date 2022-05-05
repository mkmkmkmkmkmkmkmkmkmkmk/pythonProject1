# -*- coding: utf-8 -*-
from time import sleep

import scrapy
import json

from selenium.webdriver.support.wait import WebDriverWait

import api.imageCrawler.imageCrawler.items
# from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
from selenium import webdriver
#浏览器不要有可视化界面
# from selenium.webdriver.chrome.options import Options
from scrapy import signals

# 加载api/imgeCrawler/imgeCrawler 下的settings.py
settings = get_project_settings()


class BingSpider(scrapy.Spider):
    name = 'bingspider'
    # 从配置文件加载关键词
    key_words = settings.getlist('KEY_WORDS')
    # url = 'https://www2.bing.com/images/search?q={}&go=Search&qs=ds&form=QBIR&first=1&tsc=ImageHoverTitle'.format(key_words)
    # start_urls = [url]
    start_urls=[]
    for key_word in key_words:
        for i in range(0, 100000, 35):
            # 特大半身像
            # url = 'https://cn.bing.com/images/async?q={1}&first={0}&count=35&relp=35&qft=+filterui%3aface-portrait+filterui%3aimagesize-wallpaper&lostate=r&mmasync=1&dgState=x*298_y*1195_h*191_c*1_i*176_r*33&IG=4BB493C8D7B44E2BAFB8F26EAF80D656&SFX=6&iid=images.5688'.format(i,key_word)
            # 电器url
            url = 'https://www2.bing.com/images/search?q={1}&go=Search&qs=ds&form=QBIR&first={0}&tsc=ImageHoverTitle'.format(
                i, key_word)
            start_urls.append(url)
            print("-----------------------nowi:{0}---------------------------".format(i))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BingSpider, cls).from_crawler(crawler, *args, **kwargs)  # 产生爬虫对象
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # 无界面浏览器
        spider.chrome= webdriver.Chrome(options=chrome_options)
        spider.wait=WebDriverWait(spider.chrome, timeout=4)
        crawler.signals.connect(spider.spider_closed,signal=signals.spider_closed)  # 第二个参数具体要捕捉哪个事件爬虫结束就甘比selenium
        return spider

    def spider_closed(self, spider):
        spider.chrome.quit()
        # spider.logger.info("Spider Closed:%s", spider.name)
        print("爬虫结束了。。。。。。。。。。。。。。。。。。。。。。")

    def parse(self, response, *args, **kwargs):
        # response.xpath('//*[@class="dgControl_list"]/li/div').extract()
        # imgs = response.xpath('//*[@class="dgControl_list"]/li/div/div[1]/a/@m').extract()
        # print(response.text)
        imgs = response.xpath('//*[@class="dgControl_list "]/li/div/div[1]/a/@m').extract()
        if not imgs:
            imgs = response.xpath('//*[@class="dgControl_list"]/li/div/div[1]/a/@m').extract()
        elif not imgs:
            imgs = response.xpath('//*[@class="iuscp isv"]/div[1]/a/@m').extract()
        elif not imgs:
            imgs = response.xpath('//*[@class="iuscp darkcb isv"]/div[1]/a/@m').extract()

        with open('./link_text/hotwater.txt', 'a') as f:  # 保存爬取过的链接到文件中
            for img in imgs:
                item = api.imageCrawler.imageCrawler.items.ImagecrawlerItem()  # 用于存储数据的类
                try:
                    imgurl = json.loads(img)
                    # item['image_urls'] = [json.loads(img)['murl'] for img in imgs]
                    item['image_urls'] = [imgurl['murl']]
                    # item['image_index']=li #吧索引传到pipeline中作为文件名
                    f.write(imgurl['murl'] + "\n")

                    yield item
                except Exception as e:
                    print(e)
