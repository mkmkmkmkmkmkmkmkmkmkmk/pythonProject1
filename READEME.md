## 一、项目说明：
> 爬取某网站电器图片链接保存在api/imageCrawler/imageCrawler/link_text不同分类文件
## 二、爬虫部分
### （1）。爬取图片启动步骤 bingspider.py
1.在pythonProject1下创建一个爬虫项目 `scrapy startproject imageCrawler`（scrapy startproject 【c创建的爬虫项目名称】）

2.`cd imageCrawler`

3. 初始化爬虫文件`scrapy genspider 【文件名】`生成的名称与`api/imageCrawler/imageCrawler/spiders/bingspider.py`类中name相同或者创建CrawlSpider`scrapy genspider -t crawl 文件名 (allowed_domain)`[-t 模板]

3.运行一个爬虫 `scrapy crawl bingspider`或者运行`imageCrawler/start.py`

4.修改`api/imageCrawler/imageCrawler/settings.py`中需要爬取的关键词kewords，如果你想爬取某一类物品图片到指定文件夹，建议您还是值写一个关键词，后续可能会麻烦一点

5.修改`spider/bingspider.py`中爬取图片的链接并且修改类似的refrigerator文件名

6.此时在`data/electricity/`创建了一个full文件，并且 但是保存的图片可能因为网速比较少，所以建议使用保存在`api/imageCrawler/imageCrawler/link_text`中的文件链接下载图片包存在本地，文件中有链接时，您可以运行`api/imageCrawler/imageCrawler/spiders/read_text.py`
文件
***
7.此时整理`/link_text/`下的图片数据

###（2）.爬取商城某图书部分 crawlspider.py


