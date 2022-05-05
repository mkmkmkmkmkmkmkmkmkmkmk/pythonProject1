# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ImagecrawlerPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
            imagelink = item['image_urls'][0]
            print(imagelink)
            print('@' * 30)
            yield scrapy.Request(imagelink, meta={"item": item})

    # 修改下载的图片名称的函数
    # def file_path(self, request, response=None, info=None):
    #     '''图片保存的路径'''
    #     # 默认是settings.oy配置文件中/full文件夹下
    #     path="/full/xxx.jpg"
    #     return path

