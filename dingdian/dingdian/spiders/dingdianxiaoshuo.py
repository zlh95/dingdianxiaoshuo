# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from dingdian.items import DingdianItem,DcontentItem
import re
from dingdian.mysqlpipeline.sql import Sql
from bs4 import BeautifulSoup



class DingdianxiaoshuoSpider(scrapy.Spider):
    name = 'dingdianxiaoshuo'
    allowed_domains = ['www.x23us.com']
    base_url = 'https://www.x23us.com/class/'
    suffix = '.html'


    def start_requests(self):
        for i in range(1,11):
            url = self.base_url + str(i) + '_1' + self.suffix
            yield Request(url=url,callback=self.parse)
        #yield Request(url='https://www.x23us.com/quanben/1',callback=self.parse)

    def parse(self, response):
        #self.logger.debug(response.text)
        last = response.xpath('//*[@class="last"]/text()').extract_first()
        base_url = str(response.url[:-7])
        for i in range(1,int(last)+1):
            url = base_url + '_' + str(i) + self.suffix
            yield Request(url=url,callback=self.get_name)

    def get_name(self,response):
        #接受了每个页面的url并打开
        urls = response.xpath('//*[@bgcolor="#FFFFFF"]//td[1]//a[1]/@href|/@title').extract()
        novelnames = response.xpath('//*[@bgcolor="#FFFFFF"]//td[1]//a[2]/text()').extract()
        for i,url in enumerate(urls):
            #print(url)
            yield Request(url=url,callback=self.get_intro,meta={'name':novelnames[i]})

    def get_intro(self,response):
        #接受了每个简介的url并打开
        item = DingdianItem()
        item['category'] = response.xpath('//*[@id="at"]//tr[1]/td[1]/a/text()').extract_first()
        item['author'] = response.xpath('//*[@id="at"]//tr[1]/td[2]/text()').extract_first().replace('\xa0','')
        item['serialstatus'] = response.xpath('//*[@id="at"]//tr[1]/td[3]/text()').extract_first().replace('\xa0','')
        item['serialnumber'] = response.xpath('//*[@id="at"]//tr[2]/td[2]/text()').extract_first().replace('\xa0','')
        item['novelurl'] = response.xpath('//*[@class="read"]/@href').extract_first()
        item['name'] = str(response.meta['name'])
        name_id = item['novelurl'][-6:-1].replace('/','')
        item['name_id'] = name_id
        #print(item['novelurl'])
        yield item
        yield Request(url=item['novelurl'],callback=self.get_chapter,meta={'name_id':name_id})

    def get_chapter(self, response):
        urls = re.findall(r'<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)
        num = 0
        for url in urls:
            num = num + 1
            chapterurl = response.url + url[0]
            chaptername = url[1]
            rets = Sql.sclect_chapter(chapterurl)
            if rets[0] == 1:
                print('章节已经存在了')
                return False
            else:
                yield Request(chapterurl, callback=self.get_chaptercontent, meta={'num': num,
                                                                                  'name_id': response.meta['name_id'],
                                                                                  'chaptername': chaptername,
                                                                                  'chapterurl': chapterurl
                                                                                  })

    def get_chaptercontent(self, response):
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = str(response.meta['chaptername']).replace('\xa0', '')
        item['chapterurl'] = response.meta['chapterurl']
        content = BeautifulSoup(response.text, 'lxml').find('dd', id='contents').get_text()
        item['chaptercontent'] = str(content).replace('\xa0', '')
        yield item




