from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dingdian.spiders.dingdianxiaoshuo import DingdianxiaoshuoSpider

#获取settings.py模块的配置
setting = get_project_settings()
process = CrawlerProcess(settings=setting)

#可以添加多个spider
process.crawl(DingdianxiaoshuoSpider)

#启动爬虫，会阻塞，直到爬虫完成
process.start()