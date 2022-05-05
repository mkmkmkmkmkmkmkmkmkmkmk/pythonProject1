import scrapy


# class StorecrawlerItem(scrapy.Item):
#         img_url = scrapy.Field()
#         price = scrapy.Field()
#         title = scrapy.Field()
#         svolume = scrapy.Field()
#         evaluate = scrapy.Field()
#         integral = scrapy.Field()
#         detail_url = scrapy.Field()

class StoreCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义好name用来存储商品名
    name = scrapy.Field()
    # 定义好price用来存储商品价格
    price = scrapy.Field()
    # 定义好link用来存储商品链接
    link = scrapy.Field()
    # 定义好comnum用来存储商品评论数
    comnum = scrapy.Field()
    #商品详情链接（不完整)
