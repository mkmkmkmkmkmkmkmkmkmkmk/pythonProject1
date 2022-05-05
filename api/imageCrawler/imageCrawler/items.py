# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class ImagecrawlerItem(scrapy.Item):
    # 图片url
    image_urls = scrapy.Field()
    #图片索引
    image_index = scrapy.Field()
    # 图片名称
    image_name = scrapy.Field()
    #图片分类
    image_classify= scrapy.Field()
