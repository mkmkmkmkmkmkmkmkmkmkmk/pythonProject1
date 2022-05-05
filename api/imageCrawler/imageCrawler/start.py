from scrapy.cmdline import execute

# execute('scrapy crawl bingspider'.split())
execute(['scrapy', 'crawl', 'bingspider'])  # 注意一定不要加空格 爬虫起始文件
